from sender import EmailSender
from datetime import datetime

today = datetime.now()

d2 = today.strftime("%B %d, %Y")

se = "predictsoftware2@gmail.com"  # system email
pw = "mlst jfmk xwbx hagq"
ser = "piamiguel00@gmail.com"  # admin email to send notification ///change this
ser = "benedickyamat2@gmail.com"
ser = "benedick.v.yamat@isu.edu.ph"
my_message = f"""
        Urgent Alert: Potential Flooding at Annafunan Bridge


            Hello {ser},

        I hope this message finds you well. Our monitoring system has detected a 
        significant rise in water levels near Annafunan Bridge, indicating an imminent flood threat.
         Please take immediate action to assess the situation and implement necessary measures to mitigate potential risks.

        Key steps:

        1. Alert Local Authorities: Notify relevant local authorities about the potential flood situation at Inafunan Bridge.
        2. Evaluate Systems: Assess the functionality of flood prevention systems and infrastructure in the vicinity.
        3. Notify Residents: If applicable, alert residents in the area about the potential risk and advise necessary precautions.
        4. Your swift response is crucial to ensure the safety of both the infrastructure and the community.
        If you require additional information or assistance, please don't hesitate to reach out.
        Thank you for your prompt attention to this matter.

        Best regards,
            {se} 
            {d2}
"""

send_this = EmailSender(email_sender=se, password_sender=pw, email_receiver=ser)
send_this.send_email("Subject", my_message)
