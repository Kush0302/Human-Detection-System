from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from ultralytics import YOLO
import io

app = FastAPI()

# Allow frontend access (React on localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Human-Count"] 
)

# Load YOLOv8 model once at startup
model = YOLO("yolov8n.pt")

@app.post("/detect/")
async def detect_image(file: UploadFile = File(...)):
    image_bytes = await file.read()

    # Convert bytes to NumPy array and decode
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Run detection with lower confidence threshold
    results = model(img, conf=0.25)

    # Extract class IDs
    class_ids = results[0].boxes.cls.tolist() if results[0].boxes else []
    print("All class IDs:", class_ids)

    # Count 'person' class (class 0)
    person_count = sum(1 for cls in class_ids if int(cls) == 0)
    print("Person count:", person_count)

    # DEBUG: Draw boxes for all detected classes
    for box, cls in zip(results[0].boxes.xyxy, class_ids):
        x1, y1, x2, y2 = map(int, box.tolist())
        label = f"Class {int(cls)}"
        color = (0, 255, 0) if int(cls) == 0 else (255, 0, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # If no person detected, return JSON
    if person_count == 0:
        return JSONResponse(content={"message": "No human detected", "count": 0})

    # Encode image with bounding boxes
    _, encoded_img = cv2.imencode(".jpg", img)

    # Stream back image with person count in headers
    response = StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")
    response.headers["X-Human-Count"] = str(person_count)

    return response