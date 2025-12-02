from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2 
import os
import io
from ultralytics import YOLO
from database import log_event, get_all_detections, get_detection_stats
from datetime import datetime
import logging
from typing import Optional

app = FastAPI()

#allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Human-Count"] 
)

#load YOLOv8 model once at startup
model = YOLO("yolov8n.pt")

@app.post("/detect/")
async def detect_image(file: UploadFile = File(...)):
    image_bytes = await file.read()

    #convert bytes to NumPy array and decode
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    #run detection with lower confidence threshold
    results = model(img, conf=0.25)

    #extract class IDs
    class_ids = results[0].boxes.cls.tolist() if results[0].boxes else []
    print("All class IDs:", class_ids)

    max_conf=0.0

    #count 'person' class (class 0)
    person_count = sum(1 for cls in class_ids if int(cls) == 0)
    print("Person count:", person_count)

    #DEBUG: Draw boxes for all detected classes
    for box, cls in zip(results[0].boxes.xyxy, class_ids):
        x1, y1, x2, y2 = map(int, box.tolist())
        label = f"Class {int(cls)}"
        color = (0, 255, 0) if int(cls) == 0 else (255, 0, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    #if no person detected, return JSON
    if person_count == 0:
        return JSONResponse(content={"message": "No human detected", "count": 0})
    
    timestamp=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("captures",exist_ok=True)
    file_path=f"captures/{timestamp}.jpg"
    cv2.imwrite(file_path,img)
    log_event(timestamp, file_path, person_count, max_conf)

    #encode image with bounding boxes
    _, encoded_img = cv2.imencode(".jpg", img)

    #stream back image with person count in headers
    response = StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")
    response.headers["X-Human-Count"] = str(person_count)
    response.headers["X-Confidence"] = str(max_conf)

    return response