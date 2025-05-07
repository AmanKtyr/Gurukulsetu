/**
 * Language Switcher Script
 * This script handles the language switching functionality for the application.
 */

// Language data with translations
const languageData = {
  'en': {
    name: 'English',
    flag: 'uk.svg',
    translations: {
      // Dashboard
      'dashboard': 'Dashboard',
      'welcome': 'Welcome to',
      'students': 'Students',
      'teachers': 'Teachers',
      'fees': 'Fees',
      'dues': 'Dues',
      'attendance': 'Attendance',
      'class_distribution': 'Class Distribution',
      'upcoming_events': 'Upcoming Events',
      'quick_actions': 'Quick Actions',
      'system_information': 'System Information',
      'new_admission': 'New Admission',
      'collect_fees': 'Collect Fees',
      'find_student': 'Find Student',
      'settings': 'Settings',
      'backup': 'Backup',
      'current_session': 'Current Session',
      'current_term': 'Current Term',
      'school_name': 'School Name',
      'principal': 'Principal',
      'manage_system_settings': 'Manage System Settings',
      
      // Navigation
      'home': 'Home',
      'students_nav': 'Students',
      'student_list': 'Student List',
      'admissions': 'Admissions',
      'udise_student_form': 'UDISE+ Student Form',
      'staff': 'Staff',
      'teaching_staff': 'Teaching Staff',
      'non_teaching_staff': 'Non-Teaching Staff',
      'attendance_nav': 'Attendance',
      'student_attendance': 'Student Attendance',
      'holiday_management': 'Holiday Management',
      'staff_attendance': 'Staff Attendance',
      'finance': 'Finance',
      'student_fee': 'Student Fee',
      'staff_salary': 'Staff Salary',
      'examinations': 'Examinations',
      'manage_exams': 'Manage Exams',
      'exam_schedule': 'Exam Schedule',
      'question_papers': 'Question Papers',
      'admit_cards': 'Admit Cards',
      'marks_entry': 'Marks Entry',
      'results_reports': 'Results & Reports',
      'exam_settings': 'Exam Settings',
      'documents': 'Documents',
      'all_documents': 'All Documents',
      'upload_document': 'Upload Document',
      'student_documents': 'Student Documents',
      'staff_documents': 'Staff Documents',
      'exam_documents': 'Exam Documents',
      'categories': 'Categories',
      'document_types': 'Document Types',
      'management': 'Management',
      'sessions': 'Sessions',
      'terms': 'Terms',
      'subjects': 'Subjects',
      'classes': 'Classes',
      'fee_settings': 'Fee Settings',
      'system_settings': 'System Settings',
      
      // Common actions
      'save': 'Save',
      'cancel': 'Cancel',
      'edit': 'Edit',
      'delete': 'Delete',
      'view': 'View',
      'search': 'Search',
      'filter': 'Filter',
      'print': 'Print',
      'export': 'Export',
      'import': 'Import',
      'submit': 'Submit',
      'back': 'Back',
      'next': 'Next',
      'finish': 'Finish',
      
      // Login page
      'login': 'Login',
      'username': 'Username',
      'password': 'Password',
      'remember_me': 'Remember Me',
      'forgot_password': 'Forgot Password?',
      'sign_in': 'Sign In',
      'modern_platform': 'Modern Platform for Education',
      
      // UDISE+ form
      'general_profile': 'General Profile',
      'enrolment_profile': 'Enrolment Profile',
      'facility_profile': 'Facility Profile',
      'document_upload': 'Document Upload',
      'profile_preview': 'Profile Preview'
    }
  },
  'hi': {
    name: 'हिंदी',
    flag: 'india.svg',
    translations: {
      // Dashboard
      'dashboard': 'डैशबोर्ड',
      'welcome': 'आपका स्वागत है',
      'students': 'छात्र',
      'teachers': 'शिक्षक',
      'fees': 'शुल्क',
      'dues': 'बकाया',
      'attendance': 'उपस्थिति',
      'class_distribution': 'कक्षा वितरण',
      'upcoming_events': 'आगामी कार्यक्रम',
      'quick_actions': 'त्वरित कार्य',
      'system_information': 'सिस्टम जानकारी',
      'new_admission': 'नया प्रवेश',
      'collect_fees': 'शुल्क संग्रह',
      'find_student': 'छात्र खोजें',
      'settings': 'सेटिंग्स',
      'backup': 'बैकअप',
      'current_session': 'वर्तमान सत्र',
      'current_term': 'वर्तमान अवधि',
      'school_name': 'विद्यालय का नाम',
      'principal': 'प्रधानाचार्य',
      'manage_system_settings': 'सिस्टम सेटिंग्स प्रबंधित करें',
      
      // Navigation
      'home': 'होम',
      'students_nav': 'छात्र',
      'student_list': 'छात्र सूची',
      'admissions': 'प्रवेश',
      'udise_student_form': 'यूडाइस+ छात्र फॉर्म',
      'staff': 'स्टाफ',
      'teaching_staff': 'शिक्षण स्टाफ',
      'non_teaching_staff': 'गैर-शिक्षण स्टाफ',
      'attendance_nav': 'उपस्थिति',
      'student_attendance': 'छात्र उपस्थिति',
      'holiday_management': 'अवकाश प्रबंधन',
      'staff_attendance': 'स्टाफ उपस्थिति',
      'finance': 'वित्त',
      'student_fee': 'छात्र शुल्क',
      'staff_salary': 'स्टाफ वेतन',
      'examinations': 'परीक्षाएं',
      'manage_exams': 'परीक्षा प्रबंधन',
      'exam_schedule': 'परीक्षा कार्यक्रम',
      'question_papers': 'प्रश्न पत्र',
      'admit_cards': 'प्रवेश पत्र',
      'marks_entry': 'अंक प्रविष्टि',
      'results_reports': 'परिणाम और रिपोर्ट',
      'exam_settings': 'परीक्षा सेटिंग्स',
      'documents': 'दस्तावेज़',
      'all_documents': 'सभी दस्तावेज़',
      'upload_document': 'दस्तावेज़ अपलोड करें',
      'student_documents': 'छात्र दस्तावेज़',
      'staff_documents': 'स्टाफ दस्तावेज़',
      'exam_documents': 'परीक्षा दस्तावेज़',
      'categories': 'श्रेणियां',
      'document_types': 'दस्तावेज़ प्रकार',
      'management': 'प्रबंधन',
      'sessions': 'सत्र',
      'terms': 'अवधि',
      'subjects': 'विषय',
      'classes': 'कक्षाएं',
      'fee_settings': 'शुल्क सेटिंग्स',
      'system_settings': 'सिस्टम सेटिंग्स',
      
      // Common actions
      'save': 'सहेजें',
      'cancel': 'रद्द करें',
      'edit': 'संपादित करें',
      'delete': 'हटाएं',
      'view': 'देखें',
      'search': 'खोजें',
      'filter': 'फ़िल्टर',
      'print': 'प्रिंट',
      'export': 'निर्यात',
      'import': 'आयात',
      'submit': 'जमा करें',
      'back': 'वापस',
      'next': 'अगला',
      'finish': 'समाप्त',
      
      // Login page
      'login': 'लॉगिन',
      'username': 'उपयोगकर्ता नाम',
      'password': 'पासवर्ड',
      'remember_me': 'मुझे याद रखें',
      'forgot_password': 'पासवर्ड भूल गए?',
      'sign_in': 'साइन इन',
      'modern_platform': 'शिक्षा के लिए आधुनिक मंच',
      
      // UDISE+ form
      'general_profile': 'सामान्य प्रोफाइल',
      'enrolment_profile': 'नामांकन प्रोफाइल',
      'facility_profile': 'सुविधा प्रोफाइल',
      'document_upload': 'दस्तावेज़ अपलोड',
      'profile_preview': 'प्रोफाइल पूर्वावलोकन'
    }
  }
};

// Initialize language system
document.addEventListener('DOMContentLoaded', function() {
  // Set default language from localStorage or use English
  const currentLang = localStorage.getItem('preferredLanguage') || 'en';
  setLanguage(currentLang);
  
  // Initialize language selector
  initLanguageSelector();
  
  // Add event listeners to language options
  document.querySelectorAll('.language-option').forEach(option => {
    option.addEventListener('click', function() {
      const lang = this.getAttribute('data-lang');
      setLanguage(lang);
      toggleLanguageDropdown();
    });
  });
});

// Initialize language selector
function initLanguageSelector() {
  const currentLang = localStorage.getItem('preferredLanguage') || 'en';
  const langData = languageData[currentLang];
  
  // Update language selector display
  const langToggle = document.querySelector('.language-selector-toggle');
  if (langToggle) {
    const langFlag = langToggle.querySelector('.language-flag');
    const langName = langToggle.querySelector('.language-name');
    
    if (langFlag) langFlag.src = `/static/dist/img/flags/${langData.flag}`;
    if (langName) langName.textContent = langData.name;
  }
  
  // Mark active language in dropdown
  document.querySelectorAll('.language-option').forEach(option => {
    if (option.getAttribute('data-lang') === currentLang) {
      option.classList.add('active');
    } else {
      option.classList.remove('active');
    }
  });
  
  // Add click event to toggle
  const toggle = document.querySelector('.language-selector-toggle');
  if (toggle) {
    toggle.addEventListener('click', toggleLanguageDropdown);
  }
  
  // Close dropdown when clicking outside
  document.addEventListener('click', function(event) {
    const selector = document.querySelector('.language-selector');
    const dropdown = document.querySelector('.language-selector-dropdown');
    
    if (selector && dropdown && !selector.contains(event.target)) {
      dropdown.classList.remove('show');
    }
  });
}

// Toggle language dropdown
function toggleLanguageDropdown() {
  const dropdown = document.querySelector('.language-selector-dropdown');
  if (dropdown) {
    dropdown.classList.toggle('show');
  }
}

// Set language and update UI
function setLanguage(lang) {
  if (!languageData[lang]) return;
  
  // Save preference
  localStorage.setItem('preferredLanguage', lang);
  
  // Update all translatable elements
  document.querySelectorAll('[data-i18n]').forEach(element => {
    const key = element.getAttribute('data-i18n');
    if (languageData[lang].translations[key]) {
      element.textContent = languageData[lang].translations[key];
    }
  });
  
  // Update placeholders
  document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
    const key = element.getAttribute('data-i18n-placeholder');
    if (languageData[lang].translations[key]) {
      element.placeholder = languageData[lang].translations[key];
    }
  });
  
  // Update language selector
  initLanguageSelector();
  
  // Dispatch event for custom components
  document.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
}
