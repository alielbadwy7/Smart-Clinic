
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
from pathlib import Path
import shutil
import webbrowser

from clinic import Clinic
from dashboard import DashboardService
from models import (
    Patient, Doctor, Appointment, MedicalRecord, Payment
)


class ClinicApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("SmartClinic Management System")
        self.root.geometry("1100x750")

        self.clinic = Clinic()
        self.dashboard_service = DashboardService(self.clinic)

        self.selected_attachment = ""

        title = ttk.Label(
            root,
            text="SmartClinic Management System",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)

        self.patient_tab = ttk.Frame(notebook)
        self.doctor_tab = ttk.Frame(notebook)
        self.appointment_tab = ttk.Frame(notebook)
        self.medical_record_tab = ttk.Frame(notebook)
        self.payment_tab = ttk.Frame(notebook)
        self.dashboard_tab = ttk.Frame(notebook)

        notebook.add(self.patient_tab, text="Patients")
        notebook.add(self.doctor_tab, text="Doctors")
        notebook.add(self.appointment_tab, text="Appointments")
        notebook.add(self.medical_record_tab, text="Medical Records")
        notebook.add(self.payment_tab, text="Payments")
        notebook.add(self.dashboard_tab, text="Dashboard")

        self.build_patient_tab()
        self.build_doctor_tab()
        self.build_appointment_tab()
        self.build_medical_record_tab()
        self.build_payment_tab()
        self.build_dashboard_tab()

        self.refresh_reference_lists()

    # ---------------- COMMON FUNCTIONS ----------------

    def refresh_reference_lists(self) -> None:
        patient_ids = list(self.clinic.patients.keys())
        doctor_ids = list(self.clinic.doctors.keys())

        if hasattr(self, "appointment_patient_box"):
            self.appointment_patient_box["values"] = patient_ids

        if hasattr(self, "record_patient_box"):
            self.record_patient_box["values"] = patient_ids

        if hasattr(self, "payment_patient_box"):
            self.payment_patient_box["values"] = patient_ids

        if hasattr(self, "appointment_doctor_box"):
            self.appointment_doctor_box["values"] = doctor_ids

        if hasattr(self, "record_doctor_box"):
            self.record_doctor_box["values"] = doctor_ids

    def generate_id(self, entity_type: str) -> str:
        return self.clinic.generate_id(entity_type)

    # ---------------- PATIENTS ----------------

    def build_patient_tab(self) -> None:
        form = ttk.LabelFrame(
            self.patient_tab, text="Add Patient", padding=10
        )
        form.pack(fill="x", padx=10, pady=10)

        self.patient_id = tk.StringVar(
            value=self.generate_id("patient")
        )
        self.patient_name = tk.StringVar()
        self.patient_age = tk.StringVar()
        self.patient_phone = tk.StringVar()

        fields = [
            ("Patient ID", self.patient_id),
            ("Name", self.patient_name),
            ("Age", self.patient_age),
            ("Phone", self.patient_phone),
        ]

        for row, (label, variable) in enumerate(fields):
            ttk.Label(form, text=label).grid(
                row=row, column=0, padx=5, pady=5, sticky="w"
            )

            state = "readonly" if label == "Patient ID" else "normal"

            ttk.Entry(
                form,
                textvariable=variable,
                width=30,
                state=state
            ).grid(row=row, column=1, padx=5, pady=5)

        ttk.Button(
            form,
            text="Add Patient",
            command=self.add_patient
        ).grid(row=4, column=1, padx=5, pady=10, sticky="e")

        self.patient_tree = ttk.Treeview(
            self.patient_tab,
            columns=("id", "name", "age", "phone"),
            show="headings"
        )

        for column, heading in [
            ("id", "Patient ID"),
            ("name", "Name"),
            ("age", "Age"),
            ("phone", "Phone"),
        ]:
            self.patient_tree.heading(column, text=heading)
            self.patient_tree.column(column, width=150)

        self.patient_tree.pack(
            fill="both", expand=True, padx=10, pady=10
        )

        self.refresh_patients()

    def add_patient(self) -> None:
        try:
            patient_id = self.generate_id("patient")

            patient = Patient(
                patient_id,
                self.patient_name.get().strip(),
                int(self.patient_age.get()),
                self.patient_phone.get().strip()
            )

            self.clinic.add_patient(patient)

            self.patient_id.set(self.generate_id("patient"))

            self.patient_name.set("")
            self.patient_age.set("")
            self.patient_phone.set("")

            self.refresh_patients()
            self.refresh_reference_lists()
            self.refresh_dashboard()

            messagebox.showinfo(
                "Success", f"Patient added successfully.\nID: {patient_id}"
            )

        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    def refresh_patients(self) -> None:
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)

        for patient in self.clinic.patients.values():
            self.patient_tree.insert(
                "",
                "end",
                values=(
                    patient.patient_id,
                    patient.name,
                    patient.age,
                    patient.phone,
                )
            )

    # ---------------- DOCTORS ----------------

    def build_doctor_tab(self) -> None:
        form = ttk.LabelFrame(
            self.doctor_tab, text="Add Doctor", padding=10
        )
        form.pack(fill="x", padx=10, pady=10)

        self.doctor_id = tk.StringVar(
            value=self.generate_id("doctor")
        )
        self.doctor_name = tk.StringVar()
        self.doctor_specialization = tk.StringVar()
        self.doctor_fee = tk.StringVar()

        fields = [
            ("Doctor ID", self.doctor_id),
            ("Name", self.doctor_name),
            ("Specialization", self.doctor_specialization),
            ("Consultation Fee", self.doctor_fee),
        ]

        for row, (label, variable) in enumerate(fields):
            ttk.Label(form, text=label).grid(
                row=row, column=0, padx=5, pady=5, sticky="w"
            )

            state = "readonly" if label == "Doctor ID" else "normal"

            ttk.Entry(
                form,
                textvariable=variable,
                width=30,
                state=state
            ).grid(row=row, column=1, padx=5, pady=5)

        ttk.Button(
            form,
            text="Add Doctor",
            command=self.add_doctor
        ).grid(row=4, column=1, padx=5, pady=10, sticky="e")

        self.doctor_tree = ttk.Treeview(
            self.doctor_tab,
            columns=("id", "name", "specialization", "fee"),
            show="headings"
        )

        for column, heading in [
            ("id", "Doctor ID"),
            ("name", "Name"),
            ("specialization", "Specialization"),
            ("fee", "Consultation Fee"),
        ]:
            self.doctor_tree.heading(column, text=heading)
            self.doctor_tree.column(column, width=180)

        self.doctor_tree.pack(
            fill="both", expand=True, padx=10, pady=10
        )

        self.refresh_doctors()

    def add_doctor(self) -> None:
        try:
            doctor_id = self.generate_id("doctor")

            doctor = Doctor(
                doctor_id,
                self.doctor_name.get().strip(),
                self.doctor_specialization.get().strip(),
                float(self.doctor_fee.get())
            )

            self.clinic.add_doctor(doctor)

            self.doctor_id.set(self.generate_id("doctor"))

            self.doctor_name.set("")
            self.doctor_specialization.set("")
            self.doctor_fee.set("")

            self.refresh_doctors()
            self.refresh_reference_lists()
            self.refresh_dashboard()

            messagebox.showinfo(
                "Success", f"Doctor added successfully.\nID: {doctor_id}"
            )

        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    def refresh_doctors(self) -> None:
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)

        for doctor in self.clinic.doctors.values():
            self.doctor_tree.insert(
                "",
                "end",
                values=(
                    doctor.doctor_id,
                    doctor.name,
                    doctor.specialization,
                    doctor.consultation_fee,
                )
            )

    # ---------------- APPOINTMENTS ----------------

    def build_appointment_tab(self) -> None:
        form = ttk.LabelFrame(
            self.appointment_tab,
            text="Book Appointment",
            padding=10
        )
        form.pack(fill="x", padx=10, pady=10)

        self.appointment_id = tk.StringVar(
            value=self.generate_id("appointment")
        )
        self.appointment_patient = tk.StringVar()
        self.appointment_doctor = tk.StringVar()

        ttk.Label(form, text="Appointment ID").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        ttk.Entry(
            form,
            textvariable=self.appointment_id,
            width=30,
            state="readonly"
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Patient").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )

        self.appointment_patient_box = ttk.Combobox(
            form,
            textvariable=self.appointment_patient,
            width=27,
            state="readonly"
        )
        self.appointment_patient_box.grid(
            row=1, column=1, padx=5, pady=5
        )

        ttk.Label(form, text="Doctor").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )

        self.appointment_doctor_box = ttk.Combobox(
            form,
            textvariable=self.appointment_doctor,
            width=27,
            state="readonly"
        )
        self.appointment_doctor_box.grid(
            row=2, column=1, padx=5, pady=5
        )

        ttk.Label(form, text="Appointment Date").grid(
            row=3, column=0, padx=5, pady=5, sticky="w"
        )

        dates = [
            (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(365)
        ]

        self.appointment_date = tk.StringVar(value=dates[0])

        self.appointment_date_box = ttk.Combobox(
            form,
            textvariable=self.appointment_date,
            values=dates,
            width=27,
            state="readonly"
        )
        self.appointment_date_box.grid(
            row=3, column=1, padx=5, pady=5
        )

        ttk.Label(form, text="Appointment Time").grid(
            row=4, column=0, padx=5, pady=5, sticky="w"
        )

        times = [
            f"{hour:02d}:{minute:02d}"
            for hour in range(24)
            for minute in (0, 30)
        ]

        self.appointment_time = tk.StringVar(value=times[18])

        ttk.Combobox(
            form,
            textvariable=self.appointment_time,
            values=times,
            width=27,
            state="readonly"
        ).grid(row=4, column=1, padx=5, pady=5)

        buttons = ttk.Frame(form)
        buttons.grid(row=5, column=1, sticky="w", pady=10)

        ttk.Button(
            buttons,
            text="Book Appointment",
            command=self.add_appointment
        ).pack(side="left", padx=3)

        ttk.Button(
            buttons,
            text="Cancel Selected",
            command=self.cancel_selected_appointment
        ).pack(side="left", padx=3)

        ttk.Button(
            buttons,
            text="Complete Selected",
            command=self.complete_selected_appointment
        ).pack(side="left", padx=3)

        self.appointment_tree = ttk.Treeview(
            self.appointment_tab,
            columns=("id", "patient", "doctor", "time", "status"),
            show="headings"
        )

        for column, heading in [
            ("id", "Appointment ID"),
            ("patient", "Patient ID"),
            ("doctor", "Doctor ID"),
            ("time", "Date and Time"),
            ("status", "Status"),
        ]:
            self.appointment_tree.heading(column, text=heading)
            self.appointment_tree.column(column, width=150)

        self.appointment_tree.pack(
            fill="both", expand=True, padx=10, pady=10
        )

        self.refresh_appointments()

    def add_appointment(self) -> None:
        try:
            appointment_id = self.generate_id("appointment")

            appointment_time = (
                f"{self.appointment_date.get()} "
                f"{self.appointment_time.get()}"
            )

            appointment = Appointment(
                appointment_id,
                self.appointment_patient.get(),
                self.appointment_doctor.get(),
                appointment_time
            )

            self.clinic.book_appointment(appointment)

            self.appointment_id.set(self.generate_id("appointment"))
            self.appointment_patient.set("")
            self.appointment_doctor.set("")

            self.refresh_appointments()
            self.refresh_dashboard()

            messagebox.showinfo(
                "Success",
                f"Appointment booked successfully.\nID: {appointment_id}"
            )

        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    def refresh_appointments(self) -> None:
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)

        for appointment in self.clinic.appointments.values():
            self.appointment_tree.insert(
                "",
                "end",
                values=(
                    appointment.appointment_id,
                    appointment.patient_id,
                    appointment.doctor_id,
                    appointment.appointment_time,
                    appointment.status,
                )
            )

    def cancel_selected_appointment(self) -> None:
        selected = self.appointment_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning", "Select an appointment first."
            )
            return

        appointment_id = self.appointment_tree.item(
            selected[0], "values"
        )[0]

        try:
            self.clinic.cancel_appointment(appointment_id)
            self.refresh_appointments()
            self.refresh_dashboard()

            messagebox.showinfo(
                "Success", "Appointment cancelled."
            )

        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    def complete_selected_appointment(self) -> None:
        selected = self.appointment_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning", "Select an appointment first."
            )
            return

        appointment_id = self.appointment_tree.item(
            selected[0], "values"
        )[0]

        try:
            self.clinic.complete_appointment(appointment_id)
            self.refresh_appointments()
            self.refresh_dashboard()

            messagebox.showinfo(
                "Success", "Appointment completed."
            )

        except (ValueError, OSError) as error:
            messagebox.showerror("Error", str(error))

    # ---------------- MEDICAL RECORDS ----------------

    def build_medical_record_tab(self) -> None:
        form = ttk.LabelFrame(
            self.medical_record_tab,
            text="Add Medical Record",
            padding=10
        )
        form.pack(fill="x", padx=10, pady=10)

        self.record_id = tk.StringVar(
            value=self.generate_id("medical_record")
        )
        self.record_patient_id = tk.StringVar()
        self.record_doctor_id = tk.StringVar()
        self.record_visit_date = tk.StringVar(
            value=datetime.now().strftime("%Y-%m-%d")
        )
        self.record_diagnosis = tk.StringVar()
        self.record_notes = tk.StringVar()
        self.record_attachment_label = tk.StringVar(
            value="No file selected"
        )

        ttk.Label(form, text="Record ID").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.record_id,
            width=35,
            state="readonly"
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Patient").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.record_patient_box = ttk.Combobox(
            form,
            textvariable=self.record_patient_id,
            width=32,
            state="readonly"
        )
        self.record_patient_box.grid(
            row=1, column=1, padx=5, pady=5, sticky="w"
        )

        ttk.Label(form, text="Doctor").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.record_doctor_box = ttk.Combobox(
            form,
            textvariable=self.record_doctor_id,
            width=32,
            state="readonly"
        )
        self.record_doctor_box.grid(
            row=2, column=1, padx=5, pady=5, sticky="w"
        )

        ttk.Label(form, text="Visit Date").grid(
            row=3, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.record_visit_date,
            width=35,
            state="readonly"
        ).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Diagnosis").grid(
            row=4, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.record_diagnosis,
            width=35
        ).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Notes").grid(
            row=5, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.record_notes,
            width=35
        ).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(
            form,
            text="Upload Medical File",
            command=self.upload_medical_file
        ).grid(row=6, column=0, padx=5, pady=5, sticky="w")

        ttk.Label(
            form,
            textvariable=self.record_attachment_label,
            width=45
        ).grid(row=6, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(
            form,
            text="Add Medical Record",
            command=self.add_medical_record
        ).grid(row=7, column=1, padx=5, pady=10, sticky="e")

        buttons = ttk.Frame(self.medical_record_tab)
        buttons.pack(fill="x", padx=10)

        ttk.Button(
            buttons,
            text="Open Selected File",
            command=self.open_selected_medical_file
        ).pack(side="left", padx=5)

        self.record_tree = ttk.Treeview(
            self.medical_record_tab,
            columns=(
                "id", "patient", "doctor", "date",
                "diagnosis", "notes", "file"
            ),
            show="headings"
        )

        headings = [
            ("id", "Record ID"),
            ("patient", "Patient ID"),
            ("doctor", "Doctor ID"),
            ("date", "Visit Date"),
            ("diagnosis", "Diagnosis"),
            ("notes", "Notes"),
            ("file", "Attachment")
        ]

        for column, heading in headings:
            self.record_tree.heading(column, text=heading)
            self.record_tree.column(column, width=135)

        self.record_tree.pack(
            fill="both", expand=True, padx=10, pady=10
        )

        self.refresh_medical_records()

    def upload_medical_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select Medical File",
            filetypes=[
                ("Medical Files", "*.pdf *.jpg *.jpeg *.png"),
                ("PDF Files", "*.pdf"),
                ("Image Files", "*.jpg *.jpeg *.png")
            ]
        )

        if file_path:
            self.selected_attachment = file_path
            self.record_attachment_label.set(
                Path(file_path).name
            )

    def add_medical_record(self) -> None:
        copied_file = None

        try:
            record_id = self.generate_id("medical_record")

            attachment_path = ""

            if self.selected_attachment:
                source = Path(self.selected_attachment)

                allowed_extensions = {
                    ".pdf", ".jpg", ".jpeg", ".png"
                }

                if source.suffix.lower() not in allowed_extensions:
                    raise ValueError("Unsupported medical file type.")

                folder = Path("data") / "medical_files"
                folder.mkdir(parents=True, exist_ok=True)

                destination = folder / f"{record_id}_{source.name}"

                shutil.copy2(source, destination)
                copied_file = destination

                attachment_path = str(destination)

            record = MedicalRecord(
                record_id,
                self.record_patient_id.get(),
                self.record_doctor_id.get(),
                self.record_visit_date.get(),
                self.record_diagnosis.get().strip(),
                self.record_notes.get().strip(),
                attachment_path
            )

            self.clinic.add_medical_record(record)

            self.record_id.set(self.generate_id("medical_record"))
            self.record_patient_id.set("")
            self.record_doctor_id.set("")
            self.record_visit_date.set(
                datetime.now().strftime("%Y-%m-%d")
            )
            self.record_diagnosis.set("")
            self.record_notes.set("")
            self.selected_attachment = ""
            self.record_attachment_label.set("No file selected")

            self.refresh_medical_records()
            self.refresh_dashboard()

            messagebox.showinfo(
                "Success",
                f"Medical record added successfully.\nID: {record_id}"
            )

        except (ValueError, OSError, TypeError) as error:
            if copied_file and copied_file.exists():
                copied_file.unlink()

            messagebox.showerror("Error", str(error))

    def refresh_medical_records(self) -> None:
        for item in self.record_tree.get_children():
            self.record_tree.delete(item)

        for record in self.clinic.medical_records.values():
            file_name = (
                Path(record.attachment_path).name
                if record.attachment_path else "No file"
            )

            self.record_tree.insert(
                "",
                "end",
                values=(
                    record.record_id,
                    record.patient_id,
                    record.doctor_id,
                    record.visit_date,
                    record.diagnosis,
                    record.notes,
                    file_name
                )
            )

    def open_selected_medical_file(self) -> None:
        selected = self.record_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning", "Select a medical record first."
            )
            return

        record_id = self.record_tree.item(
            selected[0], "values"
        )[0]

        record = self.clinic.medical_records.get(record_id)

        if not record or not record.attachment_path:
            messagebox.showwarning(
                "Warning", "No file is attached to this record."
            )
            return

        file_path = Path(record.attachment_path)

        if not file_path.exists():
            messagebox.showerror(
                "Error", "The attached file could not be found."
            )
            return

        webbrowser.open(file_path.resolve().as_uri())

    # ---------------- PAYMENTS ----------------

    def build_payment_tab(self) -> None:
        form = ttk.LabelFrame(
            self.payment_tab, text="Add Payment", padding=10
        )
        form.pack(fill="x", padx=10, pady=10)

        self.payment_id = tk.StringVar(
            value=self.generate_id("payment")
        )
        self.payment_patient_id = tk.StringVar()
        self.payment_amount = tk.StringVar()
        self.payment_date = tk.StringVar(
            value=datetime.now().strftime("%Y-%m-%d")
        )
        self.payment_method = tk.StringVar(value="Cash")

        ttk.Label(form, text="Payment ID").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.payment_id,
            width=35,
            state="readonly"
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Patient").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.payment_patient_box = ttk.Combobox(
            form,
            textvariable=self.payment_patient_id,
            width=32,
            state="readonly"
        )
        self.payment_patient_box.grid(
            row=1, column=1, padx=5, pady=5, sticky="w"
        )

        ttk.Label(form, text="Amount").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.payment_amount,
            width=35
        ).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Payment Date").grid(
            row=3, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.payment_date,
            width=35,
            state="readonly"
        ).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Payment Method").grid(
            row=4, column=0, padx=5, pady=5, sticky="w"
        )

        payment_methods = [
            "Cash",
            "Card",
            "Insurance",
            "Bank Transfer",
            "Other"
        ]

        ttk.Combobox(
            form,
            textvariable=self.payment_method,
            values=payment_methods,
            width=32,
            state="readonly"
        ).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(
            form,
            text="Add Payment",
            command=self.add_payment
        ).grid(row=5, column=1, padx=5, pady=10, sticky="e")

        self.payment_tree = ttk.Treeview(
            self.payment_tab,
            columns=("id", "patient", "amount", "date", "method"),
            show="headings"
        )

        for column, heading in [
            ("id", "Payment ID"),
            ("patient", "Patient ID"),
            ("amount", "Amount"),
            ("date", "Payment Date"),
            ("method", "Method")
        ]:
            self.payment_tree.heading(column, text=heading)
            self.payment_tree.column(column, width=170)

        self.payment_tree.pack(
            fill="both", expand=True, padx=10, pady=10
        )

        self.refresh_payments()

    def add_payment(self) -> None:
        try:
            payment_id = self.generate_id("payment")

            amount = float(self.payment_amount.get())

            payment = Payment(
                payment_id,
                self.payment_patient_id.get(),
                amount,
                self.payment_date.get(),
                self.payment_method.get()
            )

            self.clinic.add_payment(payment)

            self.payment_id.set(self.generate_id("payment"))
            self.payment_patient_id.set("")
            self.payment_amount.set("")
            self.payment_date.set(
                datetime.now().strftime("%Y-%m-%d")
            )
            self.payment_method.set("Cash")

            self.refresh_payments()
            self.refresh_dashboard()

            messagebox.showinfo(
                "Success",
                f"Payment added successfully.\nID: {payment_id}"
            )

        except (ValueError, OSError, TypeError) as error:
            messagebox.showerror("Error", str(error))

    def refresh_payments(self) -> None:
        for item in self.payment_tree.get_children():
            self.payment_tree.delete(item)

        for payment in self.clinic.payments.values():
            self.payment_tree.insert(
                "",
                "end",
                values=(
                    payment.payment_id,
                    payment.patient_id,
                    payment.amount,
                    payment.payment_date,
                    payment.method
                )
            )

    # ---------------- DASHBOARD ----------------

    def build_dashboard_tab(self) -> None:
        self.dashboard_labels = {}

        for key, title in [
            ("patients", "Total Patients"),
            ("doctors", "Total Doctors"),
            ("appointments", "Total Appointments"),
            ("scheduled", "Scheduled Appointments"),
            ("revenue", "Recorded Payments"),
        ]:
            frame = ttk.LabelFrame(
                self.dashboard_tab, text=title, padding=15
            )
            frame.pack(fill="x", padx=15, pady=8)

            label = ttk.Label(
                frame, text="0", font=("Arial", 16, "bold")
            )
            label.pack()

            self.dashboard_labels[key] = label

        ttk.Button(
            self.dashboard_tab,
            text="Refresh Dashboard",
            command=self.refresh_dashboard
        ).pack(pady=10)

        self.refresh_dashboard()

    def refresh_dashboard(self) -> None:
        metrics = self.dashboard_service.get_metrics()

        for key, label in self.dashboard_labels.items():
            value = metrics.get(key, 0)

            if key == "revenue":
                label.config(text=f"{value:,.2f}")
            else:
                label.config(text=str(value))


def run_app() -> None:
    root = tk.Tk()
    ClinicApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
