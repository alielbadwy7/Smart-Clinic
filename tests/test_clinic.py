
import tempfile
import unittest

from clinic import Clinic
from models import Patient, Doctor, Appointment, Payment


class TestClinic(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.clinic = Clinic(self.temp_dir.name)

        self.patient = Patient(
            "P001", "Test Patient", 30, "01000000000"
        )

        self.doctor = Doctor(
            "D001", "Test Doctor", "Dentist", 300
        )

        self.clinic.add_patient(self.patient)
        self.clinic.add_doctor(self.doctor)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_patient(self):
        self.assertIn("P001", self.clinic.patients)

    def test_duplicate_patient(self):
        with self.assertRaises(ValueError):
            self.clinic.add_patient(self.patient)

    def test_invalid_patient_age(self):
        with self.assertRaises(ValueError):
            Patient("P002", "Test", -1, "01000000000")

    def test_invalid_doctor_fee(self):
        with self.assertRaises(ValueError):
            Doctor("D002", "Doctor", "ENT", -10)

    def test_book_appointment(self):
        appointment = Appointment(
            "A001", "P001", "D001", "2026-10-27 10:30"
        )
        self.clinic.book_appointment(appointment)
        self.assertIn("A001", self.clinic.appointments)

    def test_unknown_patient(self):
        appointment = Appointment(
            "A002", "P999", "D001", "2026-10-27 11:30"
        )
        with self.assertRaises(ValueError):
            self.clinic.book_appointment(appointment)

    def test_double_booking(self):
        first = Appointment(
            "A001", "P001", "D001", "2026-10-27 10:30"
        )
        second = Appointment(
            "A002", "P001", "D001", "2026-10-27 10:30"
        )

        self.clinic.book_appointment(first)

        with self.assertRaises(ValueError):
            self.clinic.book_appointment(second)

    def test_unknown_doctor(self):
        appointment = Appointment(
            "A003", "P001", "D999", "2026-10-27 12:30"
        )
        with self.assertRaises(ValueError):
            self.clinic.book_appointment(appointment)
    
    def test_add_payment(self):
        payment = Payment(
        "PAY001", "P001", 300, "2026-10-26" )
        self.clinic.add_payment(payment)
        self.assertIn("PAY001", self.clinic.payments)

    def test_duplicate_doctor(self):
        with self.assertRaises(ValueError):
            self.clinic.add_doctor(self.doctor)


if __name__ == "__main__":
    unittest.main()
