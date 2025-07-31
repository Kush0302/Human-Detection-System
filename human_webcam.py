import cv2
from ultralytics import YOLO

#initialize YOLOv8 model
model = YOLO("yolov8n.pt")  #use yolov8s.pt or yolov8m.pt for better accuracy if needed

#initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access webcam.")
    exit()

print("Press 'q' to quit")

while True:
#ret: Boolean indicating if frame reading was successful.
#frame: The actual image captured from the webcam.
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    #resize (optional for speed)
    frame = cv2.resize(frame, (640, 480))

    #run YOLO detection
    results = model(frame)

    people_count = sum(1 for cls in results[0].boxes.cls if int(cls) == 0)
    print(f"People detected: {people_count}")


    #draw bounding boxes for 'person' class (class 0)
    for box, cls in zip(results[0].boxes.xyxy, results[0].boxes.cls):
        if int(cls) == 0:
            x1, y1, x2, y2 = map(int, box.tolist())
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    #display the frame
    cv2.imshow('YOLOv8 Human Detection - Webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
