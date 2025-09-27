class AppointmentExecutorAgent:
    def __init__(self, calendar_api_client, email_client):
        self.calendar = calendar_api_client
        self.email = email_client

    def book_appointment(self, patient_name, patient_email, plan_result):
        doctor = plan_result["doctor"]
        time_slot = plan_result["time_slot"]

        # Create Google Calendar event
        self.calendar.create_event(doctor, patient_name, time_slot)

        # Send email confirmation
        self.email.send_email(
            to=patient_email,
            subject="Appointment Confirmation",
            body=f"Your appointment with {doctor} is scheduled for {time_slot}."
        )

        return f"Appointment booked for {patient_name} with {doctor} at {time_slot}"