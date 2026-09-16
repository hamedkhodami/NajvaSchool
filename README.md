# 🎓 Najva School Management System

A comprehensive web-based management platform developed for Najva School
to centralize school administration, education, communication, finance,
student management, and public services.

The system is designed as a Modular Monolithic application using Django
and PostgreSQL.

---

## 🎯 Project Vision

The goal of this project is to create a unified digital infrastructure
for school management, education, and communication between the school
and families.

The platform is designed to:

- Centralize school management processes
- Reduce manual and paper-based workflows
- Provide a comprehensive student profile
- Improve academic monitoring
- Manage attendance and discipline
- Manage tuition and financial operations
- Provide online payment capabilities
- Improve communication with families
- Provide management dashboards
- Support online pre-registration
- Provide a professional public school website

---

## 🏗️ Architecture

The project follows a **Modular Monolithic Architecture**.

The application is organized into independent Django apps with clear
domain responsibilities while running as a single application.

```text
                         ┌──────────────┐
                         │     core     │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │   accounts   │
                         └──────┬───────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
          students          teachers         admissions
              │                 │                 │
              └──────────┬──────┴─────────────────┘
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
          School Communication

                public
                   │
                   ▼
            Public Website
```

---

## ✨ Core Features

### 🏫 School Administration

- Student management
- Teacher and staff management
- Academic year management
- Grade management
- Classroom management
- Subject management
- Teacher assignment
- Student enrollment
- User and permission management
- Management dashboard

---

### 👨‍🏫 Teacher Features

- View assigned classrooms
- View assigned students
- Weekly schedule
- Daily class schedule
- Student attendance
- Late registration
- Grade registration
- Daily evaluation
- Assignment creation
- Assignment tracking
- Discipline records
- Student notes
- Upcoming meetings and events
- Personal salary information

---

### 👨‍👩‍👧 Parent Features

Parents can access information related to their children:

- Academic profile
- Grades
- Average
- Report cards
- Attendance
- Absence history
- Late records
- Discipline records
- Assignments
- Exams
- Weekly schedule
- School events
- Parent-teacher meetings
- Tuition
- Payments
- Outstanding balance
- Payment history
- Notifications
- School communication

---

### 🎓 Student Features

Students can access their own educational information:

- Academic information
- Grades
- Average
- Assignments
- Exams
- Attendance
- Discipline records
- Weekly schedule
- School notifications

---

### 📊 Management Dashboard

The management dashboard provides summarized information about:

#### Students

- Total students
- Present students
- Absent students
- Late students
- Recent discipline records

#### Education

- Average grades
- Classroom status
- Upcoming exams
- Students requiring attention

#### Finance

- Collected tuition
- Outstanding tuition
- Recent payments
- School expenses

#### Staff

- Present teachers
- Absent staff
- Leave status
- Salary payment status

---

### 💰 Finance & Tuition

The financial module includes:

- Student tuition
- Tuition installments
- Payment records
- Student debts
- School expenses
- School income
- Staff salaries
- Salary payments
- Financial reports

---

### 💳 Online Payment

The payment application provides infrastructure for:

- Creating payment requests
- Connecting to payment gateways
- Payment callbacks
- Transaction verification
- Successful payments
- Failed payments
- Transaction history
- Linking verified payments to financial records

---

### 📢 Communication

The communication system provides:

- Notifications
- Announcements
- Internal messages
- Message threads
- Read/unread status
- Notification history

Communication may include:

- Manager ↔ Teacher
- Manager ↔ Parent
- Teacher ↔ Parent
- School ↔ Family

---

### 📝 Online Pre-registration

The public website provides online pre-registration capabilities.

The admission system manages:

- Applicant information
- Guardian information
- Pre-registration requests
- Application status
- Administrative review
- Approval/rejection workflow

---

### 🌐 Public Website

The public application contains:

- Homepage
- About school
- School achievements
- News
- Public events
- Contact information
- Public announcements
- Online pre-registration

The public website acts as the online presence of the school.


---

## 🛠️ Technology Stack

| Layer            | Technology                          |
|------------------|-------------------------------------|
| Language         | Python                              |
| Backend          | Django                              |
| Templates        | Django Templates                    |
| Frontend         | HTML, CSS, JavaScript               |
| UI               | TailwindCSS                         |
| Database         | PostgreSQL                          |
| ORM              | Django ORM                          |
| API              | Django REST Framework when required |
| Background Tasks | Django Q2                           |
| Code Quality     | Pre-commit, Ruff                    |
| Version Control  | Git                                 |
| Repository       | GitHub                              |
| Deployment       | Docker, Gunicorn, Nginx             |

---

## 📁 Project Documentation

```text
docs/
├── TODO.md
└── Project_Plan.md
```

### TODO.md

Project task tracker including:

- Project phases
- Development steps
- Application tasks
- Progress
- Timeline
- Testing
- Documentation

### Project_Plan.md

Main project roadmap including:

- Architecture
- Applications
- Models
- Responsibilities
- Relationships
- Access control
- Development phases

---

## 🔐 Security

Because the system handles sensitive student, family, academic,
disciplinary, and financial information, access control is a core
requirement.

The system should provide:

- Authentication
- Role-based authorization
- Permission management
- Restricted student access
- Parent-child data isolation
- Teacher-class access isolation
- Financial data protection
- Activity/audit logging
- Secure payment processing

---

## 🚀 Development Phases

```text
Phase 1
Planning & Preparation
        │
        ▼
Phase 2
Initial Implementation
        │
        ▼
Phase 3
Apps & Raw Templates
        │
        ▼
Phase 4
Frontend & UI
        │
        ▼
Phase 5
Advanced Features
Testing & Optimization
        │
        ▼
Phase 6
Development & Deployment
```

Each phase is completed and reviewed before the roadmap of the next phase
is finalized.

---

## 📌 Current Status

**Current Phase:** Initial Implementation

**Current Focus:**

- Project setup
- GitHub repository
- Project architecture
- Code quality tools
- Pre-commit
- Django applications
- Database models

---

## 📄 License

Private Project

Developed as a custom School Management Platform for Najva School.

