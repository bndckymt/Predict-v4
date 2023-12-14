from ultralytics import YOLO
import cv2
import math

import time
import threading

from lib.sender import EmailSender
from datetime import datetime

today = datetime.now()

d2 = today.strftime("%B %d, %Y")

se = "predictsoftware2@gmail.com"  # system email
pw = "mlst jfmk xwbx hagq"
ser = "benedickyamat2@gmail.com"  # admin email to send notification ///change this
ser = "piamiguel00@gmail.com"

def send_notification():

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
    print("Message Sent!")



def notify_and_reset_timer(last_notification_time):
    current_time = time.time()
    if current_time - last_notification_time >= 5: 

        threading.Thread(target=send_notification).start()
        return current_time
    return last_notification_time

def video_detection(path_x):
    video_capture = path_x
    cap = cv2.VideoCapture(video_capture)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    model = YOLO("YOLO-Weights/best.pt")
    classNames = ['800', '820', '840', '860', '880', '900', '920', '940', '960', '980', 'Mistarair', 'loc 2']

    last_notification_time = time.time()

    def process_results(results):
        found_first_set = False
        found_second_set = False
        indicator = False

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                class_name = classNames[cls]
                label = f'{class_name}{conf}'

                if class_name in ['800', '820', '840', '860', '880', '900']:
                    found_first_set = True
                elif class_name in ['920', '940', '960', '980']:
                    found_second_set = True

                if class_name in ['800', '820', '840', '860', '880', '900', '920', '940', '960', '980', 'Mistarair', 'loc 2']:
                    indicator = True

                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3

                if found_first_set:
                    color = (0, 128, 0)  # Green for the first set of classes
                elif found_second_set:
                    color = (0, 0, 255)  # Red for the second set of classes
                else:
                    color = (85, 45, 255)  # Default color

                if conf > 0.5:
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                    cv2.rectangle(img, (x1, y1), c2, color, -1, cv2.LINE_AA)  # filled
                    cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        return found_first_set, found_second_set, indicator

    while True:
        success, img = cap.read()
        results = model(img, stream=True)

        found_first_set, found_second_set, indicator = process_results(results)

        if not indicator:
            cv2.putText(img, "No indicator found", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif indicator:
            if found_second_set and not found_first_set:
                cv2.putText(img, "Warning: Flood!!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                last_notification_time = notify_and_reset_timer(last_notification_time)
        else: 
            cv2.putText(img, "Syetem running", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        yield img

cv2.destroyAllWindows()
