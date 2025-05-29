# Multi-College System Testing Guide

## Quick Setup for Testing

### 1. Create Test Colleges via Super Admin

1. **Access Super Admin Panel**:
   - Go to `http://localhost:8000/super_admin/`
   - Login with super admin credentials

2. **Add Colleges**:
   ```
   College 1:
   - Name: ABC College
   - Code: ABC001
   - Email: admin@abc-college.edu
   - Phone: 9876543210
   - Address: 123 ABC Street, City
   
   College 2:
   - Name: XYZ Institute  
   - Code: XYZ001
   - Email: admin@xyz-institute.edu
   - Phone: 9876543211
   - Address: 456 XYZ Avenue, City
   ```

### 2. Create College Users

1. **Create Users via Super Admin**:
   ```
   User 1:
   - Username: abc_admin
   - Email: admin@abc-college.edu
   - Password: password123
   - College: ABC College
   
   User 2:
   - Username: xyz_admin
   - Email: admin@xyz-institute.edu
   - Password: password123
   - College: XYZ Institute
   ```

### 3. Test Data Isolation

#### Test 1: Login as ABC College Admin
1. Login as `abc_admin` / `password123`
2. Create some test data:
   - Add Academic Session: "2024-25"
   - Add Academic Term: "First Term"
   - Add Class: "Class 10"
   - Add Subject: "Mathematics"
   - Add Student: "John Doe"
   - Add Staff: "Prof. ABC Teacher"

#### Test 2: Login as XYZ Institute Admin
1. Logout and login as `xyz_admin` / `password123`
2. Create different test data:
   - Add Academic Session: "2024-25" (same name, different college)
   - Add Academic Term: "First Term" (same name, different college)
   - Add Class: "Class 10" (same name, different college)
   - Add Subject: "Mathematics" (same name, different college)
   - Add Student: "Jane Smith"
   - Add Staff: "Prof. XYZ Teacher"

#### Test 3: Verify Data Isolation
1. **As ABC College Admin**:
   - Should only see John Doe in students list
   - Should only see Prof. ABC Teacher in staff list
   - Should only see ABC College's academic data

2. **As XYZ Institute Admin**:
   - Should only see Jane Smith in students list
   - Should only see Prof. XYZ Teacher in staff list
   - Should only see XYZ Institute's academic data

### 4. Test Dashboard Features

#### College-Specific Dashboard
1. Each college should see their own statistics
2. Recent activities should be college-specific
3. College logo and information should be displayed
4. Subscription status should be shown

#### Navigation and Filtering
1. All dropdown menus should show only college-specific options
2. Academic sessions and terms should be filtered by college
3. Classes and subjects should be college-specific

### 5. Test Advanced Features

#### Attendance Management
1. Create attendance records for students
2. Verify each college only sees their students' attendance
3. Holiday management should be college-specific

#### Fee Management
1. Add fee payments for students
2. Verify fee reports are college-specific
3. Pending fees should be filtered by college

#### Exam and Results
1. Create exams for each college
2. Add results for students
3. Verify exam data is properly isolated

### 6. Test Super Admin Access

1. **Login as Super Admin**:
   - Should see data from all colleges
   - Can switch between college views
   - Has access to all management features

### 7. Test Error Scenarios

#### User Without College Assignment
1. Create a user without assigning a college
2. Try to login - should get appropriate error message
3. Assign college and verify access is granted

#### Expired Subscription
1. Set a college's subscription end date to past
2. Login as that college's user
3. Should see subscription expired warning

### 8. Performance Testing

#### Large Data Sets
1. Create multiple colleges with substantial data
2. Test response times for list views
3. Verify filtering performance

#### Concurrent Users
1. Have multiple users from different colleges login simultaneously
2. Verify no data leakage between sessions
3. Test system stability

## Expected Results

### ✅ Data Isolation
- Each college sees only their own data
- No cross-college data leakage
- Same-named items can exist in different colleges

### ✅ User Experience
- College-specific branding and information
- Intuitive navigation with filtered options
- Clear subscription status indicators

### ✅ Security
- Proper authentication and authorization
- Session management prevents data access across colleges
- Super admin has appropriate elevated access

### ✅ Functionality
- All CRUD operations work within college scope
- Reports and analytics are college-specific
- Academic workflow maintains data integrity

## Troubleshooting

### Common Issues

1. **User sees no data after login**:
   - Check if user has college assigned in profile
   - Verify college has academic sessions/terms set up

2. **Forms show no options in dropdowns**:
   - Ensure college has created academic sessions, terms, classes
   - Check if current session/term is set for the college

3. **Subscription warnings persist**:
   - Update college subscription end date
   - Clear browser session/cookies

4. **Data appears across colleges**:
   - Check middleware is properly configured
   - Verify college filtering in views
   - Review database migration completion

### Debug Commands

```bash
# Check college assignments
python manage.py shell
>>> from super_admin.models import UserProfile
>>> UserProfile.objects.all().values('user__username', 'college__name')

# Verify data isolation
>>> from apps.students.models import Student
>>> Student.objects.values('fullname', 'college__name')

# Check academic data
>>> from apps.corecode.models import AcademicSession
>>> AcademicSession.objects.values('name', 'college__name')
```

## Success Criteria

The multi-college system is working correctly when:

1. ✅ Each college user sees only their college's data
2. ✅ Super admin can see all data across colleges  
3. ✅ New data is automatically assigned to user's college
4. ✅ Forms show only college-relevant options
5. ✅ Dashboard displays college-specific statistics
6. ✅ No data leakage between colleges
7. ✅ System performance remains optimal
8. ✅ User experience is intuitive and clear
