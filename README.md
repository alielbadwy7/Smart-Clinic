# SmartClinic – Clinic Management System

A Python-based desktop application for managing clinic operations using Object-Oriented Programming (OOP), Tkinter, and JSON.

## Project Overview

SmartClinic helps organize essential clinic operations through a simple graphical user interface. It supports patient and doctor management, appointment scheduling, medical records, payment tracking, and a dashboard for monitoring clinic statistics.

## Features

- **Patient Management:** Add and manage patient information.
- **Doctor Management:** Store doctor details and specializations.
- **Appointment Management:** Book, cancel, and complete appointments.
- **Medical Records:** Store diagnoses, visit notes, and medical attachments (PDF, JPG, JPEG, PNG).
- **Payment Management:** Track payments and payment methods.
- **Dashboard:** Display clinic statistics and total recorded revenue.
- **Automatic ID Generation:** Generate unique IDs for patients, doctors, appointments, records, and payments.
- **Data Persistence:** Store and retrieve information using JSON files.
- **Input Validation:** Handle invalid inputs and prevent duplicate records.

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- Tkinter (GUI)
- JSON (Data Storage)
- Unittest (Testing)

## Screenshots

### Main Application
![SmartClinic Screenshot 1](ScreenShots/Screenshot%202026-11-05%20173141.png)

### Application Features
![SmartClinic Screenshot 2](ScreenShots/Screenshot%202026-11-05%20173203.png)

![SmartClinic Screenshot 3](ScreenShots/Screenshot%202026-11-05%20173221.png)

![SmartClinic Screenshot 4](ScreenShots/Screenshot%202026-11-05%20173235.png)

![SmartClinic Screenshot 5](ScreenShots/Screenshot%202026-11-05%20173257.png)

![SmartClinic Screenshot 6](ScreenShots/Screenshot%202026-11-05%20173311.png)

## Project Structure

```text
SmartClinic/
│
├── main.py
├── models.py
├── clinic.py
├── file_manager.py
├── dashboard.py
├── gui.py
├── tests/
│   └── test_clinic.py
├── ScreenShots/
├── data/
├── .gitignore
└── README.md
```

## OOP Concepts Applied

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

2. Navigate to the project folder:

```bash
cd Smart-Clinic
```

3. Run the application:

```bash
python main.py
```

## Testing

The project includes unit tests using Python's built-in `unittest` framework.

**Latest test result:** 10 tests passed successfully.

Run the tests using:

```bash
python -m unittest discover -s tests -v
```

## Data Storage

The application uses JSON files for local data storage. Medical attachments are stored locally in `data/medical_files/`.

## Project Purpose

This project was developed as an Object-Oriented Programming course project to apply Python programming concepts in a practical healthcare management scenario.