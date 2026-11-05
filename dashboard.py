"""Simple dashboard metrics for the SmartClinic application."""

from typing import Any


class DashboardService:
    """Calculates summary indicators from the Clinic data."""

    def __init__(self, clinic: Any) -> None:
        self.clinic = clinic

    def get_metrics(self) -> dict[str, int | float]:
        appointments = self.clinic.appointments.values()
        payments = self.clinic.payments.values()

        return {
            "patients": len(self.clinic.patients),
            "doctors": len(self.clinic.doctors),
            "appointments": len(self.clinic.appointments),
            "scheduled": sum(
                1 for appointment in appointments
                if appointment.status == "Scheduled"
            ),
            # Revenue means the total value of payments recorded in the system.
            "revenue": sum(float(payment.amount) for payment in payments),
        }
