"""
Script to associate existing students with the college of their admin user.
This script should be run after adding the college field to the Student model.
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_app.settings')
django.setup()

from django.contrib.auth.models import User
from super_admin.models import UserProfile, College
from apps.students.models import Student

def associate_students_with_college():
    """Associate existing students with the college of their admin user."""
    # Get all colleges
    colleges = College.objects.all()
    
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
                        
                    # Associate all students with this college
                    students_updated = Student.objects.filter(college__isnull=True).update(college=college)
                    
                    print(f"Associated {students_updated} students with college '{college.name}'")
                    
                except UserProfile.DoesNotExist:
                    print(f"No profile found for admin user '{admin_user.username}' of college '{college.name}'")
                    
            except User.DoesNotExist:
                print(f"Admin user '{college.admin_username}' not found for college '{college.name}'")
        else:
            print(f"No admin username set for college '{college.name}'")
    
    # Count students without a college
    students_without_college = Student.objects.filter(college__isnull=True).count()
    print(f"{students_without_college} students still don't have a college assigned")

if __name__ == '__main__':
    associate_students_with_college()
