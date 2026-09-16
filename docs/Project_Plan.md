# 🚀 Project Plan – Najva School Management System

## 📌 Overview

Najva School Management System is a comprehensive web-based platform designed for
managing the academic, administrative, financial, communication, and public
activities of Najva School.

The system is designed as a Modular Monolith using Django and PostgreSQL.

The platform provides dedicated capabilities for:

- School Administration
- Teachers and Staff
- Students and Parents
- Academic Management
- Attendance
- Education and Evaluation
- Discipline and Educational Records
- Finance and Tuition
- Online Payments
- Communication
- Online Pre-registration
- Public School Website
- Management Dashboard

---

# 🎯 Project Vision

The primary goal is to create a centralized digital infrastructure for school
management, education, and communication between the school and families.

The system should:

- Centralize school information
- Reduce manual and paper-based processes
- Improve access to student information
- Provide a comprehensive student profile
- Improve communication with parents
- Simplify academic management
- Manage attendance and discipline
- Manage tuition and financial records
- Provide online payment capability
- Provide management dashboards
- Provide online pre-registration
- Provide a professional public website

---

# 🏗️ Architecture

The project follows a Modular Monolithic Architecture.

```text
                    ┌──────────────┐
                    │     core     │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   accounts   │
                    └──────┬───────┘
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
       ▼                   ▼                   ▼
   students            teachers           admissions
       │                   │                   │
       └─────────────┬─────┴───────────────────┘
                     │
                     ▼
                 academics
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
     attendance   education  discipline
          │          │          │
          └──────────┼──────────┘
                     │
                     ▼
                  dashboard

students / teachers
        │
        ▼
     finance
        │
        ▼
     payment

communication
     ▲
     │
All relevant apps

public
  │
  └── Public Website
```

---

# 🧭 Project Phases

| Phase | Title | Description |
|---------|---------|---------|
| 1️⃣ | Planning & Preparation | Requirements, proposal, architecture, technologies and applications |
| 2️⃣ | Initial Implementation | Project setup, GitHub, code quality, apps and database models |
| 3️⃣ | Apps & Raw Templates | Business logic, views, URLs and raw templates |
| 4️⃣ | Frontend & UI | TailwindCSS, responsive UI and user experience |
| 5️⃣ | Advanced Features, Testing & Optimization | Notifications, advanced workflows, testing and optimization |
| 6️⃣ | Development & Deployment | Production configuration, Docker, server deployment and release |

---

# 🧱 Phase 1 – Planning & Preparation

## Step 1 – Requirements Analysis

Review and extract all functional requirements from the project proposal.

## Step 2 – Project Proposal

Finalize the project proposal and scope.

## Step 3 – Technologies

Define:

- Python
- Django
- Django Templates
- Django ORM
- PostgreSQL
- REST API when required
- HTML
- CSS
- JavaScript
- TailwindCSS
- Git
- GitHub

## Step 4 – Applications

Define the project applications.

## Step 5 – Architecture

Define the modular monolithic architecture and application responsibilities.

## Step 6 – Project Workflow

Define the development workflow and project phases.

## Step 7 – Phase 2 Roadmap

Define the implementation sequence before starting development.

---

# ⚙️ Phase 2 – Initial Implementation

## Step 1 – Project Setup

- Create repository
- Create Django project
- Configure project structure
- Configure settings
- Configure environment variables
- Configure PostgreSQL
- Configure Git
- Configure `.gitignore`
- Configure `.editorconfig`
- Create initial README
- Create documentation structure

## Step 2 – Code Quality

Configure:

- Pre-commit
- Ruff
- Formatter
- Import sorting
- Basic static checks
- Test configuration

## Step 3 – Core

Implement shared project infrastructure.

## Step 4 – Accounts

Implement authentication, users, roles and permissions.

## Step 5 – Students

Implement student and parent/guardian data.

## Step 6 – Teachers

Implement teachers and staff.

## Step 7 – Academics

Implement academic structure.

## Step 8 – Attendance

Implement attendance and late records.

## Step 9 – Education

Implement academic activities, exams, grades and assignments.

## Step 10 – Discipline

Implement discipline and educational records.

## Step 11 – Finance

Implement tuition, installments, debts, expenses, income and staff salaries.

## Step 12 – Payment

Implement online payment infrastructure and gateway integration.

## Step 13 – Communication

Implement notifications, announcements and internal messaging.

## Step 14 – Admissions

Implement online pre-registration.

## Step 15 – Public

Implement public website data structures.

## Step 16 – Dashboard

Implement dashboard data structures and statistics.

## Step 17 – Database

- Create migrations
- Review relationships
- Add constraints
- Add indexes
- Prepare initial data

## Step 18 – Review

Review:

- Architecture
- Models
- Relationships
- Naming
- Code quality
- Database design

## Step 19 – Phase 3 Roadmap

Define detailed business logic and raw template implementation steps.

---

# 🗂️ Applications & Models

# 1️⃣ core

## Responsibility

Shared infrastructure and reusable components.

## Models

### BaseModel

Common base for project models.

Potential fields:

- id
- created_at
- updated_at

### SchoolSetting

General school-level configuration.

Potential fields:

- school_name
- phone
- email
- address
- academic_year
- configuration data

## Other Components

- Common Mixins
- Constants
- Validators
- Utilities
- Shared Exceptions
- Common Choices
- Model Helpers

---

# 2️⃣ accounts

## Responsibility

Authentication, users, roles and permissions.

## Models

### User

Main authentication model.

Possible responsibilities:

- Authentication
- User status
- Phone/email
- Last login
- Active status

### Role

Defines system roles.

Examples:

- Administrator
- Manager
- Teacher
- Parent
- Student
- Staff

### UserProfile

Additional user information.

### Permission

Permission structure when custom permissions are required.

## Access Rules

- Manager → School management
- Teacher → Assigned classes and students
- Parent → Own children
- Student → Personal academic information

---

# 3️⃣ students

## Responsibility

Student information and comprehensive student profile.

## Models

### Student

Main student entity.

Potential information:

- Personal information
- Student code
- Birth information
- Contact information
- Status
- Academic references

### Guardian

Parent/guardian information.

### StudentGuardian

Relationship between student and guardian.

Potential information:

- relation type
- is_primary
- contact priority

### StudentProfile

Extended student information when separation is useful.

### StudentActivity

Student educational/activity records.

### StudentNote

General student notes.

## Student Comprehensive Profile

The student profile should provide access to:

- Personal information
- Guardian information
- Academic status
- Grades
- Average
- Attendance
- Late records
- Discipline
- Educational records
- Assignments
- Exams
- Financial status
- Payment history
- Notes

---

# 4️⃣ teachers

## Responsibility

Teacher and school staff management.

## Models

### Teacher

Teacher information.

### Staff

Non-teaching school staff.

### EmploymentRecord

Employment and work history.

### WorkSchedule

Working hours and work schedule.

### LeaveRequest

Leave records.

### SalaryRecord

Salary and benefits information.

### SalaryPayment

Salary payments.

> Financial salary records may be linked to the finance app
> depending on the final database architecture.

---

# 5️⃣ academics

## Responsibility

Academic structure of the school.

## Models

### AcademicYear

School academic year.

### Grade

Educational grade.

Examples:

- Seventh
- Eighth
- Ninth

### Classroom

School class.

Examples:

- 7A
- 8A
- 9B

### Subject

Educational subject.

### ClassSubject

Subject assigned to a classroom.

### TeacherAssignment

Teacher assigned to a subject/class.

### StudentEnrollment

Student enrollment in an academic year/class.

### WeeklySchedule

Weekly class schedule.

### ScheduleSession

Individual scheduled session.

Potential information:

- day
- start_time
- end_time
- classroom
- subject
- teacher

---

# 6️⃣ attendance

## Responsibility

Student and staff attendance.

## Models

### StudentAttendance

Student attendance record.

Possible statuses:

- Present
- Absent
- Late
- Excused

### StaffAttendance

Teacher/staff attendance.

### AttendanceSession

Attendance session related to a class.

### LateRecord

Detailed late-arrival record.

## Requirements

- Daily attendance
- Attendance history
- Late tracking
- Attendance reports
- Parent visibility
- Teacher registration

---

# 7️⃣ education

## Responsibility

Educational activities and academic evaluation.

## Models

### Exam

Exam information.

### ExamResult

Student exam result.

### Grade

Academic grade record.

### DailyGrade

Daily evaluation.

### Assignment

Homework/assignment.

### AssignmentStatus

Student assignment completion status.

### EducationalActivity

Educational activity record.

### TeacherNote

Teacher notes about students.

## Requirements

- Grade registration
- Daily grades
- Exams
- Assignments
- Assignment status
- Educational activities
- Teacher notes
- Academic reports

---

# 8️⃣ discipline

## Responsibility

Discipline and educational/behavioral records.

## Models

### DisciplineType

Type/category of discipline record.

### DisciplineRecord

Student discipline event.

Potential information:

- student
- teacher/staff
- date
- type
- description
- status

### BehavioralEvaluation

Behavioral evaluation.

### EducationalRecord

Educational/ تربیتی record.

## Requirements

- Discipline records
- Behavioral history
- Educational records
- Parent visibility
- Management review

---

# 9️⃣ finance

## Responsibility

School financial management.

## Models

### Tuition

Student tuition record.

### TuitionInstallment

Tuition installment.

### PaymentRecord

Financial payment record.

### StudentDebt

Student financial debt.

### SchoolExpense

School expense.

### SchoolIncome

School income.

### StaffSalary

Staff salary information.

### SalaryPayment

Salary payment record.

### FinancialReport

Financial reporting data when required.

## Requirements

- Tuition management
- Installments
- Debts
- Payments
- Expenses
- Income
- Salary
- Financial reports

---

# 🔟 payment

## Responsibility

Online payment and payment gateway integration.

## Models

### PaymentTransaction

Main online payment transaction.

Potential fields:

- user
- amount
- authority
- reference_id
- gateway
- status
- created_at
- paid_at

### PaymentRequest

Payment request information.

### PaymentCallback

Gateway callback information.

### PaymentVerification

Payment verification result.

## Requirements

- Create payment request
- Redirect to gateway
- Receive callback
- Verify transaction
- Handle success/failure
- Prevent duplicate payment processing
- Connect verified payments to finance

---

# 1️⃣1️⃣ communication

## Responsibility

School communication and notification system.

## Models

### Notification

System notification.

Examples:

- Attendance notification
- New grade notification
- Schedule change
- School announcement

### NotificationRecipient

Notification recipient and read status.

### NotificationTemplate

Reusable notification templates.

### Announcement

School announcements.

### MessageThread

Conversation/thread.

### InternalMessage

Internal message.

## Communication Channels

- Manager ↔ Teacher
- Manager ↔ Parent
- Teacher ↔ Parent
- School ↔ Family

---

# 1️⃣2️⃣ admissions

## Responsibility

Online pre-registration and applicant management.

## Models

### PreRegistration

Main pre-registration request.

### Applicant

Applicant information.

### ApplicantGuardian

Applicant guardian information.

### AdmissionStatus

Pre-registration status.

Examples:

- Pending
- Reviewing
- Approved
- Rejected
- Completed

### AdmissionReview

Administrative review of an application.

## Workflow

```text
Public Website
      │
      ▼
Pre-registration
      │
      ▼
Applicant
      │
      ▼
Review
      │
 ┌────┴────┐
 ▼         ▼
Approve   Reject
 │
 ▼
Student
```

---

# 1️⃣3️⃣ public

## Responsibility

Public-facing school website.

## Public Sections

### Home

- School introduction
- Important information
- Latest news
- Important announcements

### About

- School introduction
- Mission
- Achievements
- General information

### News

Public school news and announcements.

### Events

Publicly visible school events.

### Contact

- Phone
- Address
- Contact information

### Pre-registration

Public access to online pre-registration.

## Notes

The public app should not contain private student,
teacher, financial, or internal school information.

---

# 1️⃣4️⃣ dashboard

## Responsibility

Management dashboards and summarized statistics.

## Dashboard Sections

### Student Statistics

- Total students
- Present students
- Absent students
- Late students
- New discipline records

### Academic Statistics

- Average grades
- Classroom status
- Upcoming exams
- Students requiring attention

### Financial Statistics

- Collected tuition
- Outstanding tuition
- Recent payments
- School expenses

### Staff Statistics

- Present teachers
- Absent staff
- Leave status
- Salary payment status

## Architecture Note

Dashboard should primarily aggregate data from domain apps
rather than becoming the owner of business data.

---

# 🔗 Application Relationships

```text
accounts
   │
   ├── students
   ├── teachers
   └── admissions
           │
           └── students

students ───────── academics
teachers ───────── academics

academics ──────── attendance
academics ──────── education
students ───────── education
students ───────── discipline

students ───────── finance
teachers ───────── finance

finance ────────── payment

All relevant apps ── communication

admissions ──────── public

All domain apps ─── dashboard
```

---

# 🔐 Authorization Model

The system should follow role-based access control.

## Manager

- Full school management
- Student management
- Teacher/staff management
- Academic management
- Financial management
- Reports
- Dashboard
- Communication

## Teacher

- Assigned classes
- Assigned students
- Attendance
- Grades
- Daily evaluation
- Assignments
- Discipline records
- Student notes
- Schedule
- Personal salary information

## Parent

- Own children
- Academic information
- Attendance
- Discipline
- Schedule
- Exams
- Assignments
- Financial information
- Notifications
- Communication

## Student

- Personal academic information
- Attendance
- Grades
- Assignments
- Exams
- Schedule
- Relevant notifications

---

# 🧪 Testing Strategy

Testing should cover:

- Models
- Relationships
- Constraints
- Authentication
- Permissions
- Attendance
- Education
- Discipline
- Finance
- Payment
- Admissions
- Communication

Target:

- Reliable business logic
- Safe financial transactions
- Correct access control
- Stable database relationships

---

# 🚀 Future Extensibility

The architecture should allow future implementation of:

- SMS integration
- Email notifications
- Online education
- Assignment submission
- Mobile application
- Advanced analytics
- Additional payment gateways
- External service integrations

These features are considered future extensions unless explicitly included
in the current implementation scope.

---

# 📌 Phase Completion Rule

Each phase must be completed and reviewed before the next phase roadmap
is finalized.

```text
Phase N
   │
   ▼
Implementation
   │
   ▼
Review
   │
   ▼
Completion
   │
   ▼
Define next phase
```

