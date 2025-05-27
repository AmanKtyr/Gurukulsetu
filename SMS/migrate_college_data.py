#!/usr/bin/env python
"""
Script to migrate existing data to associate with colleges.
This script should be run after adding college fields to models.
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_app.settings')
django.setup()

from super_admin.models import College
from apps.students.models import Student
from apps.staffs.models import Staff
from apps.NonTeachingStaffs.models import NonTeachingStaff
from apps.corecode.models import (
    AcademicSession, AcademicTerm, StudentClass, Subject,
    ClassSubject, FeeSettings, FeeStructure, Section, ClassTeacher
)
from apps.attendance.models import Holiday, Attendance
from apps.fees.models import PendingFee, FeePayment
from apps.exams.models import ExamType, Exam
from apps.result.models import Result

def migrate_data():
    """
    Migrate existing data to associate with colleges.
    """
    print("Starting data migration...")
    
    # Get all colleges
    colleges = College.objects.all()
    
    if not colleges.exists():
        print("No colleges found. Please create colleges first through super admin.")
        return
    
    # For this migration, we'll associate all existing data with the first college
    # In a real scenario, you might want to ask the user which college to associate data with
    default_college = colleges.first()
    print(f"Associating all existing data with college: {default_college.name}")
    
    # Migrate Students
    students_updated = Student.objects.filter(college__isnull=True).update(college=default_college)
    print(f"Updated {students_updated} students")
    
    # Migrate Staff
    staff_updated = Staff.objects.filter(college__isnull=True).update(college=default_college)
    print(f"Updated {staff_updated} staff members")
    
    # Migrate Non-Teaching Staff
    non_teaching_updated = NonTeachingStaff.objects.filter(college__isnull=True).update(college=default_college)
    print(f"Updated {non_teaching_updated} non-teaching staff members")
    
    # Migrate Core Code models
    sessions_updated = AcademicSession.objects.filter(college__isnull=True).update(college=default_college)
    print(f"Updated {sessions_updated} academic sessions")
    
    terms_updated = AcademicTerm.objects.filter(college__isnull=True).update(college=default_college)
    print(f"Updated {terms_updated} academic terms")
    
    classes_updated = StudentClass.objects.filter(college__isnull=True).update(college=default_college)
    print(f"Updated {classes_updated} student classes")
    
    subjects_updated = Subject.objects.filter(college__isnull=True).update(college=default_college)
    print(f"Updated {subjects_updated} subjects")
    
    # Migrate other models
    try:
        class_subjects_updated = ClassSubject.objects.filter(college__isnull=True).update(college=default_college)
        print(f"Updated {class_subjects_updated} class subjects")
    except:
        print("ClassSubject model doesn't have college field yet")
    
    try:
        fee_settings_updated = FeeSettings.objects.filter(college__isnull=True).update(college=default_college)
        print(f"Updated {fee_settings_updated} fee settings")
    except:
        print("FeeSettings model doesn't have college field yet")
    
    try:
        fee_structures_updated = FeeStructure.objects.filter(college__isnull=True).update(college=default_college)
        print(f"Updated {fee_structures_updated} fee structures")
    except:
        print("FeeStructure model doesn't have college field yet")
    
    try:
        sections_updated = Section.objects.filter(college__isnull=True).update(college=default_college)
        print(f"Updated {sections_updated} sections")
    except:
        print("Section model doesn't have college field yet")
    
    try:
        class_teachers_updated = ClassTeacher.objects.filter(college__isnull=True).update(college=default_college)
        print(f"Updated {class_teachers_updated} class teachers")
    except:
        print("ClassTeacher model doesn't have college field yet")
    
    # Migrate Attendance models
    try:
        holidays_updated = Holiday.objects.filter(college__isnull=True).update(college=default_college)
        print(f"Updated {holidays_updated} holidays")
    except:
        print("Holiday model doesn't have college field yet")
    
    try:
        attendance_updated = Attendance.objects.filter(college__isnull=True).update(college=default_college)
        print(f"Updated {attendance_updated} attendance records")
    except:
        print("Attendance model doesn't have college field yet")
    
    # Migrate Fees models
    try:
        pending_fees_updated = PendingFee.objects.filter(college__isnull=True).update(college=default_college)
        print(f"Updated {pending_fees_updated} pending fees")
    except:
        print("PendingFee model doesn't have college field yet")
    
    try:
        fee_payments_updated = FeePayment.objects.filter(college__isnull=True).update(college=default_college)
        print(f"Updated {fee_payments_updated} fee payments")
    except:
        print("FeePayment model doesn't have college field yet")
    
    # Migrate Exams models
    try:
        exam_types_updated = ExamType.objects.filter(college__isnull=True).update(college=default_college)
        print(f"Updated {exam_types_updated} exam types")
    except:
        print("ExamType model doesn't have college field yet")
    
    try:
        exams_updated = Exam.objects.filter(college__isnull=True).update(college=default_college)
        print(f"Updated {exams_updated} exams")
    except:
        print("Exam model doesn't have college field yet")
    
    # Migrate Results
    try:
        results_updated = Result.objects.filter(college__isnull=True).update(college=default_college)
        print(f"Updated {results_updated} results")
    except:
        print("Result model doesn't have college field yet")
    
    print("Data migration completed!")

if __name__ == "__main__":
    migrate_data()
