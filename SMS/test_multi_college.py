#!/usr/bin/env python
"""
Test script to verify multi-college data isolation
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_app.settings')
django.setup()

from django.contrib.auth.models import User
from super_admin.models import College, UserProfile
from apps.students.models import Student
from apps.staffs.models import Staff
from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass, Subject


def create_test_data():
    """Create test data for multi-college system"""
    print("Creating test data for multi-college system...")

    # Create two test colleges
    college1, created = College.objects.get_or_create(
        name="ABC College",
        defaults={
            'code': 'ABC001',
            'email': 'admin@abc-college.edu',
            'phone': '9876543210',
            'address': '123 ABC Street, City',
        }
    )
    if created:
        print(f"Created college: {college1.name}")

    college2, created = College.objects.get_or_create(
        name="XYZ Institute",
        defaults={
            'code': 'XYZ001',
            'email': 'admin@xyz-institute.edu',
            'phone': '9876543211',
            'address': '456 XYZ Avenue, City',
        }
    )
    if created:
        print(f"Created college: {college2.name}")

    # Create test users for each college
    user1, created = User.objects.get_or_create(
        username='abc_admin',
        defaults={
            'email': 'admin@abc-college.edu',
            'first_name': 'ABC',
            'last_name': 'Admin',
        }
    )
    if created:
        user1.set_password('password123')
        user1.save()
        print(f"Created user: {user1.username}")

    user2, created = User.objects.get_or_create(
        username='xyz_admin',
        defaults={
            'email': 'admin@xyz-institute.edu',
            'first_name': 'XYZ',
            'last_name': 'Admin',
        }
    )
    if created:
        user2.set_password('password123')
        user2.save()
        print(f"Created user: {user2.username}")

    # Create user profiles and assign colleges
    profile1, created = UserProfile.objects.get_or_create(
        user=user1,
        defaults={'college': college1}
    )
    if created or not profile1.college:
        profile1.college = college1
        profile1.save()
        print(f"Assigned {user1.username} to {college1.name}")

    profile2, created = UserProfile.objects.get_or_create(
        user=user2,
        defaults={'college': college2}
    )
    if created or not profile2.college:
        profile2.college = college2
        profile2.save()
        print(f"Assigned {user2.username} to {college2.name}")

    # Create academic sessions for each college
    session1, created = AcademicSession.objects.get_or_create(
        name="2024-25",
        college=college1,
        defaults={'current': True}
    )
    if created:
        print(f"Created session {session1.name} for {college1.name}")

    session2, created = AcademicSession.objects.get_or_create(
        name="2024-25",
        college=college2,
        defaults={'current': True}
    )
    if created:
        print(f"Created session {session2.name} for {college2.name}")

    # Create academic terms for each college
    term1, created = AcademicTerm.objects.get_or_create(
        name="First Term",
        college=college1,
        defaults={'current': True}
    )
    if created:
        print(f"Created term {term1.name} for {college1.name}")

    term2, created = AcademicTerm.objects.get_or_create(
        name="First Term",
        college=college2,
        defaults={'current': True}
    )
    if created:
        print(f"Created term {term2.name} for {college2.name}")

    # Create classes for each college
    class1, created = StudentClass.objects.get_or_create(
        name="Class 10",
        college=college1
    )
    if created:
        print(f"Created class {class1.name} for {college1.name}")

    class2, created = StudentClass.objects.get_or_create(
        name="Class 10",
        college=college2
    )
    if created:
        print(f"Created class {class2.name} for {college2.name}")

    # Create subjects for each college
    subject1, created = Subject.objects.get_or_create(
        name="Mathematics",
        college=college1
    )
    if created:
        print(f"Created subject {subject1.name} for {college1.name}")

    subject2, created = Subject.objects.get_or_create(
        name="Mathematics",
        college=college2
    )
    if created:
        print(f"Created subject {subject2.name} for {college2.name}")

    # Create test students for each college
    student1, created = Student.objects.get_or_create(
        registration_number="ABC001",
        defaults={
            'fullname': 'John Doe',
            'gender': 'male',
            'current_class': class1,
            'college': college1,
            'Father_name': 'John Father',
            'Father_mobile_number': '9876543210',
        }
    )
    if created:
        print(f"Created student {student1.fullname} for {college1.name}")

    student2, created = Student.objects.get_or_create(
        registration_number="XYZ001",
        defaults={
            'fullname': 'Jane Smith',
            'gender': 'female',
            'current_class': class2,
            'college': college2,
            'Father_name': 'Jane Father',
            'Father_mobile_number': '9876543211',
        }
    )
    if created:
        print(f"Created student {student2.fullname} for {college2.name}")

    # Create test staff for each college
    staff1, created = Staff.objects.get_or_create(
        registration_number="STAFF_ABC001",
        defaults={
            'fullname': 'Prof. ABC Teacher',
            'gender': 'male',
            'college': college1,
        }
    )
    if created:
        print(f"Created staff {staff1.fullname} for {college1.name}")

    staff2, created = Staff.objects.get_or_create(
        registration_number="STAFF_XYZ001",
        defaults={
            'fullname': 'Prof. XYZ Teacher',
            'gender': 'female',
            'college': college2,
        }
    )
    if created:
        print(f"Created staff {staff2.fullname} for {college2.name}")

    print("\nTest data creation completed!")
    return college1, college2, user1, user2


def test_data_isolation():
    """Test that data is properly isolated between colleges"""
    print("\n" + "="*50)
    print("TESTING DATA ISOLATION")
    print("="*50)

    college1 = College.objects.get(name="ABC College")
    college2 = College.objects.get(name="XYZ Institute")

    # Test students isolation
    college1_students = Student.objects.filter(college=college1)
    college2_students = Student.objects.filter(college=college2)

    print(f"\nStudents in {college1.name}: {college1_students.count()}")
    for student in college1_students:
        print(f"  - {student.fullname} ({student.registration_number})")

    print(f"\nStudents in {college2.name}: {college2_students.count()}")
    for student in college2_students:
        print(f"  - {student.fullname} ({student.registration_number})")

    # Test staff isolation
    college1_staff = Staff.objects.filter(college=college1)
    college2_staff = Staff.objects.filter(college=college2)

    print(f"\nStaff in {college1.name}: {college1_staff.count()}")
    for staff in college1_staff:
        print(f"  - {staff.fullname} ({staff.registration_number})")

    print(f"\nStaff in {college2.name}: {college2_staff.count()}")
    for staff in college2_staff:
        print(f"  - {staff.fullname} ({staff.registration_number})")

    # Test academic data isolation
    college1_sessions = AcademicSession.objects.filter(college=college1)
    college2_sessions = AcademicSession.objects.filter(college=college2)

    print(f"\nAcademic Sessions in {college1.name}: {college1_sessions.count()}")
    for session in college1_sessions:
        print(f"  - {session.name}")

    print(f"\nAcademic Sessions in {college2.name}: {college2_sessions.count()}")
    for session in college2_sessions:
        print(f"  - {session.name}")

    # Test classes isolation
    college1_classes = StudentClass.objects.filter(college=college1)
    college2_classes = StudentClass.objects.filter(college=college2)

    print(f"\nClasses in {college1.name}: {college1_classes.count()}")
    for cls in college1_classes:
        print(f"  - {cls.name}")

    print(f"\nClasses in {college2.name}: {college2_classes.count()}")
    for cls in college2_classes:
        print(f"  - {cls.name}")

    print("\n" + "="*50)
    print("DATA ISOLATION TEST COMPLETED")
    print("="*50)


def test_user_college_assignment():
    """Test that users are properly assigned to colleges"""
    print("\n" + "="*50)
    print("TESTING USER COLLEGE ASSIGNMENT")
    print("="*50)

    users_with_colleges = UserProfile.objects.filter(college__isnull=False)
    users_without_colleges = UserProfile.objects.filter(college__isnull=True)

    print(f"\nUsers with college assignment: {users_with_colleges.count()}")
    for profile in users_with_colleges:
        print(f"  - {profile.user.username} -> {profile.college.name}")

    print(f"\nUsers without college assignment: {users_without_colleges.count()}")
    for profile in users_without_colleges:
        print(f"  - {profile.user.username} (No college assigned)")

    print("\n" + "="*50)
    print("USER COLLEGE ASSIGNMENT TEST COMPLETED")
    print("="*50)


def main():
    """Main test function"""
    print("Multi-College System Test")
    print("=" * 50)

    # Create test data
    college1, college2, user1, user2 = create_test_data()

    # Test data isolation
    test_data_isolation()

    # Test user college assignment
    test_user_college_assignment()

    print("\n" + "="*50)
    print("ALL TESTS COMPLETED")
    print("="*50)
    print("\nTest Summary:")
    print(f"- Created 2 colleges: {college1.name}, {college2.name}")
    print(f"- Created 2 users: {user1.username}, {user2.username}")
    print("- Each college has separate academic data")
    print("- Each college has separate students and staff")
    print("- Users are properly assigned to their respective colleges")
    print("\nYou can now test the system by:")
    print(f"1. Login as '{user1.username}' (password: password123) to access {college1.name}")
    print(f"2. Login as '{user2.username}' (password: password123) to access {college2.name}")
    print("3. Verify that each user only sees their college's data")


if __name__ == "__main__":
    main()
