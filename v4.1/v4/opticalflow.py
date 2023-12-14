import cv2
import numpy as np

def calculate_average_speed(flow, roi):
    u, v = flow[roi[1]:roi[3], roi[0]:roi[2]].T
    magnitude = np.sqrt(u**2 + v**2)
    average_speed = np.mean(magnitude)
    return average_speed

cv2.namedWindow("Optical Flow")
roi = (100, 100, 300, 300)

cap = cv2.VideoCapture(0)

ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    step = 16
    h, w = gray.shape
    y, x = np.mgrid[step // 2:h:step, step // 2:w:step].reshape(2, -1).astype(int)
    fx, fy = flow[y, x].T

    lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.2)

    flow_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    cv2.polylines(flow_img, lines, 0, (0, 255, 0), 1)

    average_speed = calculate_average_speed(flow, roi)

    cv2.putText(flow_img, f"Average Speed: {average_speed:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    prev_gray = gray

    cv2.imshow("Optical Flow", flow_img)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
