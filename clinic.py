
from models import (
    Patient,
    Doctor,
    Appointment,
    MedicalRecord,
    Payment
)
from file_manager import FileManager


class Clinic:
    def __init__(self, folder: str = "data") -> None:
        self.file_manager = FileManager(folder)

        self.patients: dict[str, Patient] = {}
        self.doctors: dict[str, Doctor] = {}
        self.appointments: dict[str, Appointment] = {}
        self.medical_records: dict[str, MedicalRecord] = {}
        self.payments: dict[str, Payment] = {}

        self.load_data()

    # ---------------- GENERATE IDs ----------------

    def generate_id(self, entity_type: str) -> str:
        configurations = {
            "patient": (self.patients, "P"),
            "doctor": (self.doctors, "D"),
            "appointment": (self.appointments, "A"),
            "medical_record": (self.medical_records, "R"),
            "payment": (self.payments, "PAY")
        }

        if entity_type not in configurations:
            raise ValueError("Invalid entity type.")

        collection, prefix = configurations[entity_type]

        highest_number = 0

        for current_id in collection:
            if current_id.startswith(prefix):
                number = current_id[len(prefix):]

                if number.isdigit():
                    highest_number = max(
                        highest_number,
                        int(number)
                    )

        return f"{prefix}{highest_number + 1:03d}"

    # ---------------- LOAD DATA ----------------

    def load_data(self) -> None:

        # Load patients
        for item in self.file_manager.load("patients.json"):
            patient = Patient(**item)

            if patient.patient_id in self.patients:
                raise ValueError("Duplicate patient ID in saved data.")

            self.patients[patient.patient_id] = patient

        # Load doctors
        for item in self.file_manager.load("doctors.json"):
            doctor = Doctor(**item)

            if doctor.doctor_id in self.doctors:
                raise ValueError("Duplicate doctor ID in saved data.")

            self.doctors[doctor.doctor_id] = doctor

        # Load appointments
        for item in self.file_manager.load("appointments.json"):
            appointment = Appointment(**item)

            if appointment.appointment_id in self.appointments:
                raise ValueError("Duplicate appointment ID in saved data.")

            self.appointments[appointment.appointment_id] = appointment

        self.validate_appointments()

        # Load medical records
        for item in self.file_manager.load("medical_records.json"):
            record = MedicalRecord(**item)

            if record.record_id in self.medical_records:
                raise ValueError("Duplicate medical record ID.")

            self.medical_records[record.record_id] = record

        # Load payments
        for item in self.file_manager.load("payments.json"):
            payment = Payment(**item)

            if payment.payment_id in self.payments:
                raise ValueError("Duplicate payment ID.")

            self.payments[payment.payment_id] = payment

        # Validate medical record references
        for record in self.medical_records.values():

            if record.patient_id not in self.patients:
                raise ValueError(
                    "Medical record has an unknown patient."
                )

            if record.doctor_id not in self.doctors:
                raise ValueError(
                    "Medical record has an unknown doctor."
                )

        # Validate payment references
        for payment in self.payments.values():

            if payment.patient_id not in self.patients:
                raise ValueError("Payment has an unknown patient.")

    # ---------------- VALIDATE APPOINTMENTS ----------------

    def validate_appointments(self) -> None:

        for appointment in self.appointments.values():

            if appointment.patient_id not in self.patients:
                raise ValueError("Appointment has an unknown patient.")

            if appointment.doctor_id not in self.doctors:
                raise ValueError("Appointment has an unknown doctor.")

            if appointment.status != "Scheduled":
                continue

            for other in self.appointments.values():

                if other.appointment_id == appointment.appointment_id:
                    continue

                if (
                    other.status == "Scheduled"
                    and other.doctor_id == appointment.doctor_id
                    and other.appointment_time == appointment.appointment_time
                ):
                    raise ValueError("Conflicting saved appointments.")

    # ---------------- SAVE PATIENTS ----------------

    def save_patients(self) -> None:

        data = [
            {
                "patient_id": p.patient_id,
                "name": p.name,
                "age": p.age,
                "phone": p.phone
            }
            for p in self.patients.values()
        ]

        self.file_manager.save("patients.json", data)

    # ---------------- SAVE DOCTORS ----------------

    def save_doctors(self) -> None:

        data = [
            {
                "doctor_id": d.doctor_id,
                "name": d.name,
                "specialization": d.specialization,
                "consultation_fee": d.consultation_fee
            }
            for d in self.doctors.values()
        ]

        self.file_manager.save("doctors.json", data)

    # ---------------- SAVE APPOINTMENTS ----------------

    def save_appointments(self) -> None:

        data = [
            {
                "appointment_id": a.appointment_id,
                "patient_id": a.patient_id,
                "doctor_id": a.doctor_id,
                "appointment_time": a.appointment_time,
                "status": a.status
            }
            for a in self.appointments.values()
        ]

        self.file_manager.save("appointments.json", data)

    # ---------------- SAVE MEDICAL RECORDS ----------------

    def save_medical_records(self) -> None:

        data = [
            {
                "record_id": r.record_id,
                "patient_id": r.patient_id,
                "doctor_id": r.doctor_id,
                "visit_date": r.visit_date,
                "diagnosis": r.diagnosis,
                "notes": r.notes,
                "attachment_path": r.attachment_path
            }
            for r in self.medical_records.values()
        ]

        self.file_manager.save("medical_records.json", data)

    # ---------------- SAVE PAYMENTS ----------------

    def save_payments(self) -> None:

        data = [
            {
                "payment_id": p.payment_id,
                "patient_id": p.patient_id,
                "amount": p.amount,
                "payment_date": p.payment_date,
                "method": p.method
            }
            for p in self.payments.values()
        ]

        self.file_manager.save("payments.json", data)

    # ---------------- ADD PATIENT ----------------

    def add_patient(self, patient: Patient) -> None:

        if patient.patient_id in self.patients:
            raise ValueError("Patient ID already exists.")

        self.patients[patient.patient_id] = patient

        try:
            self.save_patients()

        except OSError:
            del self.patients[patient.patient_id]
            raise

    # ---------------- ADD DOCTOR ----------------

    def add_doctor(self, doctor: Doctor) -> None:

        if doctor.doctor_id in self.doctors:
            raise ValueError("Doctor ID already exists.")

        self.doctors[doctor.doctor_id] = doctor

        try:
            self.save_doctors()

        except OSError:
            del self.doctors[doctor.doctor_id]
            raise

    # ---------------- BOOK APPOINTMENT ----------------

    def book_appointment(self, appointment: Appointment) -> None:

        if appointment.appointment_id in self.appointments:
            raise ValueError("Appointment ID already exists.")

        if appointment.patient_id not in self.patients:
            raise ValueError("Patient does not exist.")

        if appointment.doctor_id not in self.doctors:
            raise ValueError("Doctor does not exist.")

        if appointment.status != "Scheduled":
            raise ValueError("New appointments must be scheduled.")

        for existing in self.appointments.values():

            if (
                existing.status == "Scheduled"
                and existing.doctor_id == appointment.doctor_id
                and existing.appointment_time == appointment.appointment_time
            ):
                raise ValueError(
                    "Doctor already has an appointment at this time."
                )

        self.appointments[appointment.appointment_id] = appointment

        try:
            self.save_appointments()

        except OSError:
            del self.appointments[appointment.appointment_id]
            raise

    # ---------------- CANCEL APPOINTMENT ----------------

    def cancel_appointment(self, appointment_id: str) -> None:

        if appointment_id not in self.appointments:
            raise ValueError("Appointment does not exist.")

        appointment = self.appointments[appointment_id]

        if appointment.status != "Scheduled":
            raise ValueError(
                "Only scheduled appointments can be cancelled."
            )

        old_status = appointment.status
        appointment.cancel()

        try:
            self.save_appointments()

        except OSError:
            appointment.status = old_status
            raise

    # ---------------- COMPLETE APPOINTMENT ----------------

    def complete_appointment(self, appointment_id: str) -> None:

        if appointment_id not in self.appointments:
            raise ValueError("Appointment does not exist.")

        appointment = self.appointments[appointment_id]

        if appointment.status != "Scheduled":
            raise ValueError(
                "Only scheduled appointments can be completed."
            )

        old_status = appointment.status
        appointment.status = "Completed"

        try:
            self.save_appointments()

        except OSError:
            appointment.status = old_status
            raise

    # ---------------- ADD MEDICAL RECORD ----------------

    def add_medical_record(self, record: MedicalRecord) -> None:

        if record.record_id in self.medical_records:
            raise ValueError("Record ID already exists.")

        if record.patient_id not in self.patients:
            raise ValueError("Patient does not exist.")

        if record.doctor_id not in self.doctors:
            raise ValueError("Doctor does not exist.")

        self.medical_records[record.record_id] = record

        try:
            self.save_medical_records()

        except OSError:
            del self.medical_records[record.record_id]
            raise

    # ---------------- ADD PAYMENT ----------------

    def add_payment(self, payment: Payment) -> None:

        if payment.payment_id in self.payments:
            raise ValueError("Payment ID already exists.")

        if payment.patient_id not in self.patients:
            raise ValueError("Patient does not exist.")

        self.payments[payment.payment_id] = payment

        try:
            self.save_payments()

        except OSError:
            del self.payments[payment.payment_id]
            raise
