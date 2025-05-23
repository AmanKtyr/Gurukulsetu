from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from super_admin.models import UserProfile, College
from apps.students.models import Student


class Command(BaseCommand):
    help = 'Associate existing students with the college of their admin user'

    def handle(self, *args, **options):
        # Get all colleges
        colleges = College.objects.all()
        total_students_updated = 0
        
        # For each college, find the admin user and associate all students with that college
        for college in colleges:
            if college.admin_username:
                try:
                    # Find the admin user for this college
                    admin_user = User.objects.get(username=college.admin_username)
                    
                    # Get the admin user's profile
                    try:
                        profile = UserProfile.objects.get(user=admin_user)
                        
                        # Make sure the profile has the college set
                        if not profile.college:
                            profile.college = college
                            profile.save()
                            self.stdout.write(f"Updated profile for admin user '{admin_user.username}' with college '{college.name}'")
                        
                        # Associate all students with this college
                        students_updated = Student.objects.filter(college__isnull=True).update(college=college)
                        total_students_updated += students_updated
                        
                        self.stdout.write(f"Associated {students_updated} students with college '{college.name}'")
                        
                    except UserProfile.DoesNotExist:
                        self.stdout.write(self.style.WARNING(
                            f"No profile found for admin user '{admin_user.username}' of college '{college.name}'"
                        ))
                        
                except User.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Admin user '{college.admin_username}' not found for college '{college.name}'"
                    ))
            else:
                self.stdout.write(self.style.WARNING(f"No admin username set for college '{college.name}'"))
        
        # Count students without a college
        students_without_college = Student.objects.filter(college__isnull=True).count()
        
        self.stdout.write(self.style.SUCCESS(f"Total students updated: {total_students_updated}"))
        self.stdout.write(f"{students_without_college} students still don't have a college assigned")
