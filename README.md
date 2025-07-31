# Human Detection System 🧠🚶‍♂️

A full-stack Human Detection System using **YOLOv8**, **FastAPI**, and **React.js**.

This project allows you to upload an image, detects all humans using the YOLOv8 object detection model, and returns:
- A processed image with bounding boxes.
- A count of detected humans.

---

## 🚀 Features

- YOLOv8-powered human detection
- FastAPI backend with image upload and inference
- React frontend to display detection result and human count
- CORS-enabled and production-ready architecture
- Accurate bounding boxes and count display

---

## 🧠 Tech Stack

- **Frontend**: React.js
- **Backend**: FastAPI (Python)
- **Model**: YOLOv8 (`ultralytics`)
- **Libraries**: OpenCV, NumPy, Axios

---

## 📸 How It Works

1. Upload an image with humans.
2. Backend processes the image using YOLOv8.
3. Draws bounding boxes around detected humans.
4. Returns the updated image and human count.
5. Frontend displays results live.

---

## 🛠️ Installation

### 🔙 Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

🔜 Frontend (React)
```bash
cd frontend
npm install
npm start
```
⚠️ Make sure the backend is running at http://localhost:8000

🖼️ Sample Result


## 📌 TODOs

- [ ] Add webcam support  
- [ ] Deploy to cloud (Render/Vercel)  
- [ ] Add logging or CSV export of results  


🤝 Contributing

Pull requests are welcome! Feel free to fork and submit improvements.




