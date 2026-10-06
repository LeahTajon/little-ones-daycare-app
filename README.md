# Little Ones — Daycare Management System

A full-stack daycare management application built with **Python, Flask, SQLAlchemy, SQLite, HTML, CSS, and Bootstrap**.

Little Ones is designed to help daycare staff manage children, daily care activities, parent information, authorized pickups, reports, events, and other common administrative tasks in one application.

## 🚀 Project Overview

Little Ones was created as a portfolio project to demonstrate full-stack web development skills, including:

* Building a Flask web application
* Designing relational database models
* Creating responsive user interfaces
* Implementing CRUD functionality
* Creating forms and validation
* Generating PDF reports
* Organizing application features into separate modules
* Working with Git and GitHub

## ✨ Features

### Child Management

* Add new children
* Edit child information
* View detailed child profiles
* Delete child records
* Child profile photos
* Parent information
* Authorized pickup information
* Program and enrollment information
* Medical information

### Daily Care Logs

Staff can record daily activities and care information, including:

* Meals
* Bottles
* Naps
* Diaper changes
* Potty activities
* Health checks
* Classroom activities

Daily logs can be viewed by child, date, and classroom.

### Calendar

The calendar allows daycare staff to manage:

* Upcoming events
* Event dates
* Event times
* Classroom-related events
* Upcoming birthdays

### Reports

The application includes several report types:

* Student Directory
* Students by Class
* Enrollment Summary
* Daily Log Reports
* Birthday Reports
* Parent Contact Reports
* Authorized Pickup information
* Child Profile reports

Reports can be previewed and generated as PDF documents.

### Parent Communication

The application includes tools for sharing daily log information with parents through:

* Email
* WhatsApp

## 📄 PDF Generation

Little Ones uses PDF generation to create printable reports and child records.

Examples include:

* Child profiles
* Daily logs
* Student directories
* Birthday reports
* Parent contact reports

## 🛠️ Technologies

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| Python           | Application programming   |
| Flask            | Web application framework |
| Flask-SQLAlchemy | Database integration      |
| SQLite           | Database                  |
| Jinja2           | HTML templating           |
| HTML5            | Page structure            |
| CSS3             | Styling                   |
| Bootstrap        | Responsive UI             |
| ReportLab        | PDF generation            |
| Git              | Version control           |
| GitHub           | Source code hosting       |

## 📁 Project Structure

```text
little-ones-daycare-app/
│
├── app.py
├── models.py
├── forms.py
├── extensions.py
├── reports.py
├── create_db.py
│
├── pdf/
│   └── daily_log_pdf.py
│
├── static/
│   └── css/
│
├── templates/
│   ├── children.html
│   ├── child_details.html
│   ├── daily_log.html
│   ├── calendar.html
│   ├── email_daily_log.html
│   ├── whatsapp_daily_log.html
│   └── reports/
│
└── .gitignore
```

## 💻 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/LeahTajon/little-ones-daycare-app.git
cd little-ones-daycare-app
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file for environment-specific settings such as:

```text
SECRET_KEY=your-secret-key
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-email-password
```

**Do not commit `.env` to GitHub.**

### 5. Create the database

```bash
python create_db.py
```

### 6. Start the application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## 🔐 Privacy

This repository does not contain real children's information, private contact information, passwords, email credentials, or production database files.

Sensitive configuration is stored using environment variables and excluded from version control.

## 🎯 Purpose

Little Ones was developed as a practical full-stack portfolio project based on a real-world daycare management workflow.

The goal was to create an application that goes beyond basic CRUD functionality and demonstrates how multiple features can work together in a single business application.

## 👩‍💻 Developer

**Leah Tajon**

Full-stack web development portfolio project.

Built with Python, Flask, SQLAlchemy, SQLite, HTML, CSS, and Bootstrap.
