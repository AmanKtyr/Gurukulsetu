# Gurukulsetu School Management Software - Industry-Ready Overhaul Plan

This document outlines the detailed workflow to transform the Gurukulsetu SMS project into a professional, industry-ready, fully functional school management ERP tailored to the needs of modern Indian schools.

---

## 📋 Phase 1: Authentication & Layout Styling Fixes (Immediate Priority)
- [ ] **Fix Login Page Checkbox Alignment:** Adjust the custom CSS in `login-page.css` and the HTML structure in `login.html` to align the "Remember Me" checkbox next to its label instead of rendering it as full-width and pushing the text to a new line.
- [ ] **Sidebar Sub-menu Indentation:** Fix `sidebar-fix.css` to add proper indentation (e.g., 15-20px left margin/padding) for sub-menu items (under treeview lists) to establish a clear visual hierarchy.
- [ ] **Dashboard Chart Data Fallback:** Ensure that if no database entries exist for attendance or fee collections, the chart logic in `IndexView` provides dummy but realistic-looking data, or renders a "No Data Available" placeholder message to prevent empty grids from appearing.

---

## 🗂️ Phase 2: Navigation & Sidebar Completeness
- [ ] **Review Navigation Links:** Add links for any missing pages like Fee Settings, Class-wise Subjects, Exam Dashboard, and Database Backup/Restore to the sidebar.
- [ ] **Indian School ERP Specifics:** Ensure all standard modules for Indian schools are present:
  - **Academics:** Session, Class, Section, Subject, Class Teacher assignment
  - **Students:** Admission, Student List, Details view, Document Upload
  - **Attendance:** Student Daily Attendance, Staff Attendance, Holidays
  - **Finance:** Fee Structures, Collect Fee, Paid Receipts, Dues Report
  - **Exams:** Exam Schedule, Marks Entry, Grade management, printable Report Cards
  - **Settings:** School Profile (Branding, Logo, Affiliation No.), Backup/Restore, Permissions

---

## 🎓 Phase 3: Core Academic & Setup Verification
- [ ] **Sessions, Terms, Classes, and Subjects:** Verify that CRUD operations and list pages are fully functional and professional.
- [ ] **Class Section Management:** Ensure that sections can be added, updated, and deleted dynamically.
- [ ] **Class Teacher Assignment:** Verify the UI/API for assigning teachers to classes.

---

## 🧑‍🎓 Phase 4: Student & HR/Staff Management
- [ ] **Admission Form Overhaul:** Ensure the admission flow contains fields relevant to Indian schools (e.g., Aadhaar Number, Category (General/OBC/SC/ST), Religion, Mother Tongue, Blood Group, Father's Name, Mother's Name).
- [ ] **Staff Profiles & Salary:** Verify teaching and non-teaching staff onboarding and salary calculation/disbursement.
- [ ] **Student Profiles:** Ensure comprehensive tabs (Overview, Fees History, Attendance, Exam Results) are working correctly inside student detail views.

---

## 📈 Phase 5: Attendance & Holiday Management
- [ ] **Student Attendance UI:** Check that teachers can select a Class, Section, and Date, then toggle attendance (Present/Absent/Late) in a bulk grid and save it with one click.
- [ ] **Staff Attendance UI:** Verify daily check-ins for teaching and non-teaching staff.
- [ ] **Holiday Management:** Ensure list and addition of school holidays works.

---

## 💰 Phase 6: Finance & Fees Management
- [ ] **Fee Structure Customization:** Ensure fee settings allows defining term-wise or monthly structures.
- [ ] **Fee Collection:** Verify student fee search, payment processing (cash, card, online, UPI), and receipt generation.
- [ ] **Fee Dues Reports:** Ensure administrators can view pending dues class-wise or individually.

---

## 📝 Phase 7: Examination & Report Cards
- [ ] **Exam Management:** Create exams, link to academic sessions/terms, and schedule exams per subject.
- [ ] **Marks Entry Grid:** Verify that the marks entry screen is clean and works smoothly for teachers to enter marks by class/section.
- [ ] **Report Card Generation:** Ensure report cards can be generated as clean, printable HTML or PDF sheets with the school's logo, grades, percentages, and teacher remarks.

---

## ⚙️ Phase 8: System Settings & Database Backup
- [ ] **School Profile settings:** Verify that uploaded logos display correctly in headers and dashboards.
- [ ] **Backup and Restore:** Ensure DB backups can be created, downloaded, and restored successfully.
- [ ] **Security Logs:** Ensure logs page renders correctly and displays login attempts.

---

*Note: We will complete these tasks one by one, verifying each layout change in the browser to ensure the user gets a polished, premium experience.*
