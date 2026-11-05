# SmartClinic – Clinic Management System

A Python-based desktop application for managing clinic operations using Object-Oriented Programming (OOP), Tkinter, and JSON.

## Project Overview

SmartClinic is a desktop application designed to manage essential clinic operations through a simple graphical user interface.

The system helps organize patient information, doctor details, appointments, medical records, and payments. It also provides a dashboard to monitor clinic statistics and recorded revenue.

## Key Features

- **Patient Management:** Add and manage patient information.
- **Doctor Management:** Store doctor details and specializations.
- **Appointment Management:** Book, cancel, and complete appointments.
- **Medical Records:** Record patient diagnoses, visit notes, and attach medical files (PDF, JPG, JPEG, PNG).
- **Payment Management:** Track patient payments and payment methods.
- **Dashboard:** Display clinic statistics and total recorded revenue.
- **Automatic ID Generation:** Generate unique IDs for patients, doctors, appointments, medical records, and payments.
- **Data Persistence:** Store and retrieve data using JSON files.
- **Input Validation:** Handle invalid inputs and prevent duplicate records.

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- Tkinter (GUI)
- JSON (Data Storage)
- Unittest (Testing)

## Project Structure

```text
SmartClinic/
├── main.py
├── models.py
├── clinic.py
├── file_manager.py
├── dashboard.py
├── gui.py
├── data/
│   └── medical_files/
├── tests/
│   └── test_clinic.py
├── ScreenShots/
├── .gitignore
└── README.md
```

## Screenshots

### Main Application

![SmartClinic Main Screen](ScreenShots/Screenshot%202026-11-05%20173141.png)

### Application Features

![SmartClinic Screenshot 2](ScreenShots/Screenshot%202026-11-05%20173203.png)

![SmartClinic Screenshot 3](ScreenShots/Screenshot%202026-11-05%20173221.png)

![SmartClinic Screenshot 4](ScreenShots/Screenshot%202026-11-05%20173235.png)

![SmartClinic Screenshot 5](ScreenShots/Screenshot%202026-11-05%20173257.png)

![SmartClinic Screenshot 6](ScreenShots/Screenshot%202026-11-05%20173311.png)

## OOP Concepts

The project applies core Object-Oriented Programming concepts, including:

- Classes and Objects
- Constructors
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction
- Composition
- Type Hints
- Exception Handling

## Installation & How to Run

1. Clone the repository:

```bash
git clone https://github.com/alielbadwy7/Smart-Clinic.git
```

2. Navigate to the project directory:

```bash
cd Smart-Clinic
```

3. Run the application:

```bash
python main.py
```

## Testing

The project includes unit tests using Python's built-in `unittest` framework.

**Test Results:** 10 tests passed successfully.

Run tests using:

```bash
python -m unittest discover -s tests -v
```

## Data Storage

The application uses JSON files for local data storage. Medical attachments are stored in the `data/medical_files/` directory.

Sensitive local data files are excluded from version control using `.gitignore`.

## Project Purpose

This project was developed as an Object-Oriented Programming course project to apply Python programming concepts in a practical healthcare management scenario.