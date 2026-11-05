
from datetime import datetime


class Patient:
    def __init__(
        self,
        patient_id: str,
        name: str,
        age: int,
        phone: str
    ) -> None:
        if not patient_id.strip():
            raise ValueError("Patient ID is required.")

        if not name.strip():
            raise ValueError("Patient name is required.")

        if not 0 <= age <= 120:
            raise ValueError("Age must be between 0 and 120.")

        if not phone.strip():
            raise ValueError("Phone number is required.")

        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.phone = phone

    def display_info(self) -> str:
        return (
            f"{self.patient_id} | {self.name} | "
            f"{self.age} | {self.phone}"
        )


class Doctor:
    def __init__(
        self,
        doctor_id: str,
        name: str,
        specialization: str,
        consultation_fee: float
    ) -> None:
        if not doctor_id.strip():
            raise ValueError("Doctor ID is required.")

        if not name.strip():
            raise ValueError("Doctor name is required.")

        if not specialization.strip():
            raise ValueError("Specialization is required.")

        if consultation_fee < 0:
            raise ValueError("Consultation fee cannot be negative.")

        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.consultation_fee = consultation_fee


class Appointment:
    VALID_STATUSES = ("Scheduled", "Completed", "Cancelled")

    def __init__(
        self,
        appointment_id: str,
        patient_id: str,
        doctor_id: str,
        appointment_time: str,
        status: str = "Scheduled"
    ) -> None:
        if not all([
            appointment_id.strip(),
            patient_id.strip(),
            doctor_id.strip()
        ]):
            raise ValueError("Appointment IDs are required.")

        try:
            datetime.strptime(
                appointment_time, "%Y-%m-%d %H:%M"
            )
        except ValueError:
            raise ValueError(
                "Use date format YYYY-MM-DD HH:MM."
            )

        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid appointment status.")

        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_time = appointment_time
        self.status = status

    def cancel(self) -> None:
        if self.status == "Completed":
            raise ValueError(
                "A completed appointment cannot be cancelled."
            )

        self.status = "Cancelled"

    def complete(self) -> None:
        if self.status != "Scheduled":
            raise ValueError(
                "Only scheduled appointments can be completed."
            )

        self.status = "Completed"


class MedicalRecord:
    def __init__(
        self,
        record_id: str,
        patient_id: str,
        doctor_id: str,
        visit_date: str,
        diagnosis: str,
        notes: str = "",
        attachment_path: str = ""
    ) -> None:
        if not all([
            record_id.strip(),
            patient_id.strip(),
            doctor_id.strip(),
            diagnosis.strip()
        ]):
            raise ValueError("Required medical record data is missing.")

        try:
            datetime.strptime(visit_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Use visit date format YYYY-MM-DD.")

        self.record_id = record_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.visit_date = visit_date
        self.diagnosis = diagnosis
        self.notes = notes
        self.attachment_path = attachment_path


class Payment:
    VALID_METHODS = (
        "Cash",
        "Card",
        "Insurance",
        "Bank Transfer",
        "Other"
    )

    def __init__(
        self,
        payment_id: str,
        patient_id: str,
        amount: float,
        payment_date: str,
        method: str = "Cash"
    ) -> None:
        if not payment_id.strip() or not patient_id.strip():
            raise ValueError("Payment and patient IDs are required.")

        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        try:
            datetime.strptime(payment_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Use payment date format YYYY-MM-DD.")

        if method not in self.VALID_METHODS:
            raise ValueError("Invalid payment method.")

        self.payment_id = payment_id
        self.patient_id = patient_id
        self.amount = amount
        self.payment_date = payment_date
        self.method = method
