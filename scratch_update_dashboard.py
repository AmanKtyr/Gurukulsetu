import os

target_path = r"d:\Work-Space\Industrial Prijects\Gurukulsetu\templates\students\dashboard.html"

with open(target_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    "57 new orders": "57 new admissions",
    "Awating processing": "Pending approval",
    "5 orders": "15 inquiries",
    "On hold": "Needs follow up",
    "15 products": "12 staff members",
    "Out of stock": "Absent today",
    "Total sells": "Fees Collected",
    "Total orders": "Total Students",
    "New customers": "Recent Admissions",
    "Top coupons": "Student Attendance",
    "Paying vs non paying": "Fees Paid vs Pending",
    "Percentage discount": "Present",
    "Fixed card discount": "Absent",
    "Fixed product discount": "Late",
    "Paying customer": "Paid full fees",
    "Non-paying customer": "Pending fees",
    "Latest reviews": "Notice Board",
    "Top regions by revenue": "Student Demographics",
    "Project status": "Upcoming Events",
    "fa-solid fa-star": "fa-solid fa-user-plus",
    "fa-solid fa-pause": "fa-solid fa-phone",
    "fa-solid fa-xmark": "fa-solid fa-user-clock",
    "Ecommerce Dashboard": "College Dashboard",
    "Payment received across all channels": "Fees collected across all payment methods"
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully updated dashboard metrics in {target_path}")
