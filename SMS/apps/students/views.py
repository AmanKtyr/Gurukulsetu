import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets, modelform_factory
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Finance app removed
from apps.corecode.filters import ClassSectionFilterForm
from apps.corecode.models import Section

from .models import Student, StudentBulkUpload, StudentDocument
from .filters import StudentFilter
from .forms import StudentForm

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_form = ClassSectionFilterForm(self.request.GET)

        if self.filter_form.is_valid():
            if self.filter_form.cleaned_data['class_name']:
                queryset = queryset.filter(current_class=self.filter_form.cleaned_data['class_name'])
            if self.filter_form.cleaned_data['section']:
                queryset = queryset.filter(section=self.filter_form.cleaned_data['section'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        return context

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        # Finance/Invoice references removed

        # Get student documents if they exist
        context['documents'] = StudentDocument.objects.filter(student=self.object).first()

        # Get pending fees
        from apps.fees.models import PendingFee, FeePayment
        from django.db.models import Sum

        # Get all pending fees that are not paid
        pending_fees = PendingFee.objects.filter(student=self.object, paid=False).order_by('due_date')
        context['pending_fees'] = pending_fees

        # Calculate total pending amount
        total_pending = sum(fee.get_discounted_amount() for fee in pending_fees)
        context['total_pending_amount'] = total_pending

        # Get payment history
        payment_history = FeePayment.objects.filter(student=self.object).order_by('-date')[:5]
        context['payment_history'] = payment_history

        # Calculate total paid amount
        total_paid = FeePayment.objects.filter(student=self.object, status='Paid').aggregate(total=Sum('amount'))['total'] or 0
        context['total_paid_amount'] = total_paid

        return context



class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    form_class = StudentForm
    success_message = "New student successfully added."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Add AJAX functionality to update sections when class changes
        form.fields['current_class'].widget.attrs.update({
            'class': 'form-select',
            'onchange': 'loadSections(this.value)'
        })

        return form

    def get_success_url(self):
        # Redirect to the student detail page after successful creation
        return reverse_lazy('student-detail', kwargs={'pk': self.object.pk})


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    form_class = StudentForm
    success_message = "Record successfully updated."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Add AJAX functionality to update sections when class changes
        form.fields['current_class'].widget.attrs.update({
            'class': 'form-select',
            'onchange': 'loadSections(this.value)'
        })

        return form


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy("student-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()

        # Import related models
        from apps.fees.models import FeePayment, PendingFee
        from apps.exams.models import AdmitCard, ExamAttendance, Mark
        from apps.attendance.models import Attendance

        # Count related records
        context['related_data'] = {
            'fee_payments': FeePayment.objects.filter(student=student).count(),
            'pending_fees': PendingFee.objects.filter(student=student).count(),
            'admit_cards': AdmitCard.objects.filter(student=student).count(),
            'exam_attendance': ExamAttendance.objects.filter(student=student).count(),
            'marks': Mark.objects.filter(student=student).count(),
            'attendance': Attendance.objects.filter(student=student).count(),
            'documents': StudentDocument.objects.filter(student=student).count(),
        }

        return context

    def post(self, request, *args, **kwargs):
        student = self.get_object()
        student_id = student.id
        student_name = student.fullname

        try:
            # Use direct database connection to force delete
            from django.db import connection
            cursor = connection.cursor()

            # Disable foreign key checks temporarily (for SQLite)
            cursor.execute("PRAGMA foreign_keys = OFF;")

            # Delete related records from all tables that reference students
            # 1. Delete fee-related records
            cursor.execute("DELETE FROM fees_feepayment WHERE student_id = ?", [student_id])
            cursor.execute("DELETE FROM fees_pendingfee WHERE student_id = ?", [student_id])

            # 2. Delete exam-related records
            cursor.execute("DELETE FROM exams_mark WHERE student_id = ?", [student_id])
            cursor.execute("DELETE FROM exams_examattendance WHERE student_id = ?", [student_id])
            cursor.execute("DELETE FROM exams_admitcard WHERE student_id = ?", [student_id])

            # 3. Delete attendance records
            cursor.execute("DELETE FROM attendance_attendance WHERE student_id = ?", [student_id])

            # 4. Delete student documents
            cursor.execute("DELETE FROM students_studentdocument WHERE student_id = ?", [student_id])

            # 5. Finally delete the student
            cursor.execute("DELETE FROM students_student WHERE id = ?", [student_id])

            # Re-enable foreign key checks
            cursor.execute("PRAGMA foreign_keys = ON;")

            messages.success(request, f"Student '{student_name}' and all related records have been successfully deleted.")
            return redirect(self.success_url)

        except Exception as e:
            messages.error(request, f"Error deleting student: {str(e)}")
            return redirect('student-detail', pk=student_id)


class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentBulkUpload
    template_name = "students/students_upload.html"
    fields = ["csv_file"]
    success_url = "/student/list"
    success_message = "Successfully uploaded students"


class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "registration_number",
                "fullname",
                "gender",
                "parent_number",
                "address",
                "current_class",
            ]
        )

        return response


@login_required
def upload_student_documents(request, pk):
    """Upload documents with their numbers"""
    student = get_object_or_404(Student, pk=pk)

    # Get or create student document record
    student_doc, created = StudentDocument.objects.get_or_create(student=student)

    if request.method == 'POST':
        # Handle document numbers and file uploads

        # Aadhar Card
        if 'aadhar_card' in request.FILES:
            student_doc.aadhar_card = request.FILES.get('aadhar_card')
            if 'aadhar_card_number' in request.POST:
                student_doc.aadhar_card_number = request.POST.get('aadhar_card_number')

        # Parent Photo
        if 'parent_photo' in request.FILES:
            student_doc.parent_photo = request.FILES.get('parent_photo')
            if 'parent_photo_number' in request.POST:
                student_doc.parent_photo_number = request.POST.get('parent_photo_number')

        # Parent ID Proof
        if 'parent_id_proof' in request.FILES:
            student_doc.parent_id_proof = request.FILES.get('parent_id_proof')
            if 'parent_id_proof_number' in request.POST:
                student_doc.parent_id_proof_number = request.POST.get('parent_id_proof_number')

        # Previous Marksheet
        if 'previous_marksheet' in request.FILES:
            student_doc.previous_marksheet = request.FILES.get('previous_marksheet')
            if 'previous_marksheet_number' in request.POST:
                student_doc.previous_marksheet_number = request.POST.get('previous_marksheet_number')

        # Transfer Certificate
        if 'transfer_certificate' in request.FILES:
            student_doc.transfer_certificate = request.FILES.get('transfer_certificate')
            if 'transfer_certificate_number' in request.POST:
                student_doc.transfer_certificate_number = request.POST.get('transfer_certificate_number')

        # Character Certificate
        if 'character_certificate' in request.FILES:
            student_doc.character_certificate = request.FILES.get('character_certificate')
            if 'character_certificate_number' in request.POST:
                student_doc.character_certificate_number = request.POST.get('character_certificate_number')

        # Caste Certificate
        if 'caste_certificate' in request.FILES:
            student_doc.caste_certificate = request.FILES.get('caste_certificate')
            if 'caste_certificate_number' in request.POST:
                student_doc.caste_certificate_number = request.POST.get('caste_certificate_number')

        # Medical Certificate
        if 'medical_certificate' in request.FILES:
            student_doc.medical_certificate = request.FILES.get('medical_certificate')
            if 'medical_certificate_number' in request.POST:
                student_doc.medical_certificate_number = request.POST.get('medical_certificate_number')

        # Other Document
        if 'other_document' in request.FILES:
            student_doc.other_document = request.FILES.get('other_document')
            if 'other_document_number' in request.POST:
                student_doc.other_document_number = request.POST.get('other_document_number')

        # Save the document record
        student_doc.save()

        messages.success(request, 'Documents uploaded successfully!')
        return redirect('student-detail', pk=student.pk)

    context = {
        'student': student,
        'documents': student_doc,
    }

    return render(request, 'students/upload_documents.html', context)


@login_required
def get_sections_for_class(request, class_id):
    """API endpoint to get sections for a class for the student form"""
    try:
        # Get sections from the Section model
        sections = Section.objects.filter(
            student_class_id=class_id,
            is_active=True
        ).values_list('name', flat=True)

        # Format sections for the response
        section_data = [{'id': section, 'name': section} for section in sections]

        return JsonResponse({'sections': section_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class StudentUDISECreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """UDISE+ style form for creating a new student"""
    model = Student
    form_class = StudentForm
    template_name = "students/udise_student_form.html"
    success_message = "New student successfully added using UDISE+ format."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Add AJAX functionality to update sections when class changes
        form.fields['current_class'].widget.attrs.update({
            'class': 'form-select',
            'onchange': 'loadSections(this.value)'
        })

        return form

    def form_valid(self, form):
        # Check if the form is being saved as a draft
        if 'save_as_draft' in self.request.POST:
            form.instance.current_status = 'inactive'  # Mark as draft by setting status to inactive
            self.success_message = "Student information saved as draft. You can complete it later."
        else:
            form.instance.current_status = 'active'

        # Save the form to get the student instance
        response = super().form_valid(form)

        # Handle document uploads
        self.handle_document_uploads(self.object)

        return response

    def handle_document_uploads(self, student):
        """Process document uploads and save them to StudentDocument model"""
        from .models import StudentDocument

        # Get or create StudentDocument instance for this student
        student_doc, created = StudentDocument.objects.get_or_create(student=student)

        # Handle student photo (passport)
        if 'student_photo' in self.request.FILES:
            student.passport = self.request.FILES['student_photo']
            student.save()

        # Handle birth certificate
        if 'birth_certificate' in self.request.FILES:
            student_doc.birth_certificate = self.request.FILES['birth_certificate']

        # Handle address proof
        if 'address_proof' in self.request.FILES:
            student_doc.address_proof = self.request.FILES['address_proof']

        # Handle transfer certificate
        if 'transfer_certificate' in self.request.FILES:
            student_doc.transfer_certificate = self.request.FILES['transfer_certificate']
            student_doc.transfer_certificate_number = self.request.POST.get('transfer_certificate_number', '')

        # Handle category certificate
        if 'category_certificate' in self.request.FILES:
            student_doc.caste_certificate = self.request.FILES['category_certificate']
            student_doc.caste_certificate_number = self.request.POST.get('category_certificate_number', '')

        # Handle disability certificate
        if 'disability_certificate' in self.request.FILES:
            student_doc.medical_certificate = self.request.FILES['disability_certificate']
            student_doc.medical_certificate_number = self.request.POST.get('disability_certificate_number', '')

        # Handle income certificate
        if 'income_certificate' in self.request.FILES:
            student_doc.other_document = self.request.FILES['income_certificate']
            student_doc.other_document_number = self.request.POST.get('income_certificate_number', '')

        # Save the document
        student_doc.save()

    def get_success_url(self):
        # Redirect to the student detail page after successful creation
        return reverse_lazy('student-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add current academic session to context
        from apps.corecode.models import AcademicSession
        current_session = AcademicSession.objects.filter(current=True).first()
        if current_session:
            context['current_session'] = current_session

        # Add school profile to context
        from apps.corecode.models import SiteConfig
        context['profile'] = {
            'college_name': SiteConfig.objects.filter(key='school_name').first().value if SiteConfig.objects.filter(key='school_name').exists() else 'VIDYA BHARTI',
            'college_code': SiteConfig.objects.filter(key='school_address').first().value if SiteConfig.objects.filter(key='school_address').exists() else '09161513902'
        }

        return context


class StudentUDISEUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """UDISE+ style form for updating an existing student"""
    model = Student
    form_class = StudentForm
    template_name = "students/udise_student_form.html"
    success_message = "Student record successfully updated using UDISE+ format."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Add AJAX functionality to update sections when class changes
        form.fields['current_class'].widget.attrs.update({
            'class': 'form-select',
            'onchange': 'loadSections(this.value)'
        })

        return form

    def form_valid(self, form):
        # Check if the form is being saved as a draft
        if 'save_as_draft' in self.request.POST:
            form.instance.current_status = 'inactive'  # Mark as draft by setting status to inactive
            self.success_message = "Student information saved as draft. You can complete it later."
        else:
            form.instance.current_status = 'active'

        # Save the form to get the student instance
        response = super().form_valid(form)

        # Handle document uploads
        self.handle_document_uploads(self.object)

        return response

    def handle_document_uploads(self, student):
        """Process document uploads and save them to StudentDocument model"""
        from .models import StudentDocument

        # Get or create StudentDocument instance for this student
        student_doc, created = StudentDocument.objects.get_or_create(student=student)

        # Handle student photo (passport)
        if 'student_photo' in self.request.FILES:
            student.passport = self.request.FILES['student_photo']
            student.save()

        # Handle birth certificate
        if 'birth_certificate' in self.request.FILES:
            student_doc.birth_certificate = self.request.FILES['birth_certificate']

        # Handle address proof
        if 'address_proof' in self.request.FILES:
            student_doc.address_proof = self.request.FILES['address_proof']

        # Handle transfer certificate
        if 'transfer_certificate' in self.request.FILES:
            student_doc.transfer_certificate = self.request.FILES['transfer_certificate']
            student_doc.transfer_certificate_number = self.request.POST.get('transfer_certificate_number', '')

        # Handle category certificate
        if 'category_certificate' in self.request.FILES:
            student_doc.caste_certificate = self.request.FILES['category_certificate']
            student_doc.caste_certificate_number = self.request.POST.get('category_certificate_number', '')

        # Handle disability certificate
        if 'disability_certificate' in self.request.FILES:
            student_doc.medical_certificate = self.request.FILES['disability_certificate']
            student_doc.medical_certificate_number = self.request.POST.get('disability_certificate_number', '')

        # Handle income certificate
        if 'income_certificate' in self.request.FILES:
            student_doc.other_document = self.request.FILES['income_certificate']
            student_doc.other_document_number = self.request.POST.get('income_certificate_number', '')

        # Save the document
        student_doc.save()

    def get_success_url(self):
        # Redirect to the student detail page after successful update
        return reverse_lazy('student-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add current academic session to context
        from apps.corecode.models import AcademicSession
        current_session = AcademicSession.objects.filter(current=True).first()
        if current_session:
            context['current_session'] = current_session

        # Add school profile to context
        from apps.corecode.models import SiteConfig
        context['profile'] = {
            'college_name': SiteConfig.objects.filter(key='school_name').first().value if SiteConfig.objects.filter(key='school_name').exists() else 'VIDYA BHARTI',
            'college_code': SiteConfig.objects.filter(key='school_address').first().value if SiteConfig.objects.filter(key='school_address').exists() else '09161513902'
        }

        return context

