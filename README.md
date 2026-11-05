# SmartClinic – Clinic Management System

## Project Overview
SmartClinic is a Python-based desktop application designed to manage essential clinic operations through a simple graphical user interface.

The system helps organize patient information, doctor details, appointments, medical records, and payments. It also provides a dashboard to monitor basic clinic statistics and revenue.

## Key Features
- **Patient Management:** Add and manage patient information.
- **Doctor Management:** Store doctor details and specializations.
- **Appointment Management:** Book, cancel, and complete appointments.
- **Medical Records:** Record patient diagnoses and visit notes.
- **Payment Management:** Track patient payments and payment methods.
- **Dashboard:** Display clinic statistics and total recorded revenue.
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
├── tests/
├── screenshots/
└── README.md
```

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
git clone https://github.com/YOUR_USERNAME/SmartClinic.git
```

2. Navigate to the project directory:
```bash
cd SmartClinic
```

3. Run the application:
```bash
python main.py
```

## Testing
The project includes unit tests using Python's built-in `unittest` framework.

Current test results: **10 tests passed successfully.**

Run tests using:
```bash
python -m unittest discover -s tests -v
```

## Project Purpose
This project was developed as an Object-Oriented Programming course project to apply Python programming concepts in a practical healthcare management scenario.