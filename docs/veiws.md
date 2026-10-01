# 4. Academic

## SubjectModel

### Views

* `SubjectListView`
* `SubjectDetailView`
* `SubjectCreateView`
* `SubjectUpdateView`
* `SubjectDeleteView`

## StudentEnrollmentModel

### Views

* `StudentEnrollmentListView`
* `StudentEnrollmentDetailView`
* `StudentEnrollmentCreateView`
* `StudentEnrollmentUpdateView`
* `StudentEnrollmentDeleteView`

## ScheduleSessionModel

### Views

* `ScheduleSessionListView`
* `ScheduleSessionDetailView`
* `ScheduleSessionCreateView`
* `ScheduleSessionUpdateView`
* `ScheduleSessionDeleteView`

---

# 5. Attendance

## AttendanceSessionModel

### Views

* `AttendanceSessionListView`
* `AttendanceSessionDetailView`
* `AttendanceSessionCreateView`
* `AttendanceSessionUpdateView`
* `AttendanceSessionDeleteView`

## StudentAttendanceModel

### Views

* `StudentAttendanceListView`
* `StudentAttendanceDetailView`
* `StudentAttendanceCreateView`
* `StudentAttendanceUpdateView`
* `StudentAttendanceDeleteView`

## StaffAttendanceModel

### Views

* `StaffAttendanceListView`
* `StaffAttendanceDetailView`
* `StaffAttendanceCreateView`
* `StaffAttendanceUpdateView`
* `StaffAttendanceDeleteView`

---

## TeacherNoteModel

### Views

* `TeacherNoteListView`
* `TeacherNoteDetailView`
* `TeacherNoteCreateView`
* `TeacherNoteUpdateView`
* `TeacherNoteDeleteView`

# 6. Education

## ExamModel

### Views

* `ExamListView`
* `ExamDetailView`
* `ExamCreateView`
* `ExamUpdateView`
* `ExamDeleteView`

## ExamResultModel

### Views

* `ExamResultListView`
* `ExamResultDetailView`
* `ExamResultCreateView`
* `ExamResultUpdateView`
* `ExamResultDeleteView`

## DailyGradeModel

### Views

* `DailyGradeListView`
* `DailyGradeDetailView`
* `DailyGradeCreateView`
* `DailyGradeUpdateView`
* `DailyGradeDeleteView`

## AssignmentModel

### Views

* `AssignmentListView`
* `AssignmentDetailView`
* `AssignmentCreateView`
* `AssignmentUpdateView`
* `AssignmentDeleteView`

## EducationalActivityModel

### Views

* `EducationalActivityListView`
* `EducationalActivityDetailView`
* `EducationalActivityCreateView`
* `EducationalActivityUpdateView`
* `EducationalActivityDeleteView`

---

# 7. Discipline

## DisciplineTypeModel

### Views

* `DisciplineTypeListView`
* `DisciplineTypeDetailView`
* `DisciplineTypeCreateView`
* `DisciplineTypeUpdateView`
* `DisciplineTypeDeleteView`

## DisciplineRecordModel

### Views

* `DisciplineRecordListView`
* `DisciplineRecordDetailView`
* `DisciplineRecordCreateView`
* `DisciplineRecordUpdateView`
* `DisciplineRecordDeleteView`

## BehavioralEvaluationModel

### Views

* `BehavioralEvaluationListView`
* `BehavioralEvaluationDetailView`
* `BehavioralEvaluationCreateView`
* `BehavioralEvaluationUpdateView`
* `BehavioralEvaluationDeleteView`

## EducationalRecordModel

### Views

* `EducationalRecordListView`
* `EducationalRecordDetailView`
* `EducationalRecordCreateView`
* `EducationalRecordUpdateView`
* `EducationalRecordDeleteView`

---

# 8. Finance

## TuitionModel

### Views

* `TuitionListView`
* `TuitionDetailView`
* `TuitionCreateView`
* `TuitionUpdateView`
* `TuitionDeleteView`

## TuitionInstallmentModel

### Views

* `TuitionInstallmentListView`
* `TuitionInstallmentDetailView`
* `TuitionInstallmentCreateView`
* `TuitionInstallmentUpdateView`
* `TuitionInstallmentDeleteView`

## PaymentRecordModel

### Views

* `PaymentRecordListView`
* `PaymentRecordDetailView`
* `PaymentRecordCreateView`
* `PaymentRecordUpdateView`
* `PaymentRecordDeleteView`

## StaffSalaryModel

### Views

* `StaffSalaryListView`
* `StaffSalaryDetailView`
* `StaffSalaryCreateView`
* `StaffSalaryUpdateView`
* `StaffSalaryDeleteView`

## SalaryPaymentModel

### Views

* `SalaryPaymentListView`
* `SalaryPaymentDetailView`
* `SalaryPaymentCreateView`
* `SalaryPaymentUpdateView`
* `SalaryPaymentDeleteView`

## SchoolExpenseModel

### Views

* `SchoolExpenseListView`
* `SchoolExpenseDetailView`
* `SchoolExpenseCreateView`
* `SchoolExpenseUpdateView`
* `SchoolExpenseDeleteView`

---

# 9. Payment

این بخش مربوط به فرآیند پرداخت آنلاین و اتصال به درگاه است.

### Views

* `PaymentCreateView`
* `PaymentStartView`
* `PaymentCallbackView`
* `PaymentVerifyView`
* `PaymentSuccessView`
* `PaymentFailedView`
* `PaymentDetailView`
* `PaymentListView`

---

# 10. Notifications

برای سیستم اعلان‌ها:

### Views

* `NotificationListView`
* `NotificationDetailView`
* `NotificationCreateView`
* `NotificationDeleteView`
* `NotificationMarkAsReadView`
* `NotificationMarkAllAsReadView`

---

# 11. Dashboard

داشبوردها بر اساس نقش کاربر جدا می‌شوند.

## عمومی

* `DashboardView`

## Student Dashboard

* `StudentDashboardView`

## Teacher Dashboard

* `TeacherDashboardView`

## Admin Dashboard

* `AdminDashboardView`

---

# 12. Public

بخش عمومی سایت:

* `HomeView`
* `AboutView`
* `ContactView`
* `PublicAnnouncementListView`
* `PublicAnnouncementDetailView`

---

# ترتیب پیشنهادی پیاده‌سازی

برای اینکه وابستگی مدل‌ها باعث دوباره‌کاری نشود، View ها را به این ترتیب پیاده می‌کنیم:

## مرحله 1 — Account

* Login
* Logout
* User List
* User Detail
* Password Reset

## مرحله 2 — Student

* Student List
* Student Detail
* Student Profile
* Student Note List
* Student Note Create
* Student Note Detail

## مرحله 3 — Teacher

* Teacher List
* Teacher Detail
* Teacher Profile
* Teacher Note
* Employment Record

## مرحله 4 — Academic

* Academic Year
* Grade
* Classroom
* Subject
* Student Enrollment
* Schedule

## مرحله 5 — Attendance

* Attendance Session
* Student Attendance
* Staff Attendance

## مرحله 6 — Education

* Exam
* Exam Result
* Daily Grade
* Assignment
* Educational Activity

## مرحله 7 — Discipline

* Discipline Type
* Discipline Record
* Behavioral Evaluation
* Educational Record

## مرحله 8 — Finance

* Tuition
* Installment
* Payment Record
* Staff Salary
* Salary Payment
* School Expense

## مرحله 9 — Payment

* شروع پرداخت
* Callback
* Verify
* Success / Failed
* Payment History

## مرحله 10 — Notifications

* لیست اعلان‌ها
* جزئیات
* خوانده‌شدن
* مدیریت اعلان‌ها

## مرحله 11 — Dashboard

* Student Dashboard
* Teacher Dashboard
* Admin Dashboard

## مرحله 12 — Public

* Home
* About
* Contact
* Public Announcements

---

# الگوی کلی View ها

برای اکثر مدل‌های CRUD از این الگو استفاده می‌کنیم:

```text
ListView
    ↓
DetailView
    ↓
CreateView
    ↓
UpdateView
    ↓
DeleteView
```

اما برای View های عملیاتی، مثل:

```text
Login
Logout
Password Reset
Payment
Callback
Verify
Mark As Read
Dashboard
Profile
```

از View اختصاصی استفاده می‌کنیم.

---

# نکته مهم معماری

همه مدل‌ها الزاماً نباید CRUD کامل داشته باشند.

مثلاً:

* `StudentProfileView` برای خود دانش‌آموز است.
* `StudentListView` برای مدیریت دانش‌آموزان است.
* `PaymentCallbackView` یک View عملیاتی است و CRUD نیست.
* `StudentAttendanceCreateView` بهتر است منطق دسترسی و کلاس دانش‌آموز را بررسی کند.
* `ExamResultCreateView` باید بررسی کند دانش‌آموز متعلق به کلاس امتحان باشد.
* `TeacherNoteCreateView` باید مشخص کند چه کسی اجازه ثبت یادداشت دارد.
* View های مالی باید دسترسی محدودتری نسبت به View های عمومی داشته باشند.

بنابراین بعد از ساخت لیست View ها، مرحله بعدی فقط «ساختن کلاس‌های CRUD پشت سر هم» نیست؛ برای هر View باید **Role، Permission، Queryset و ارتباط مدل‌ها** را هم مشخص کنیم.
