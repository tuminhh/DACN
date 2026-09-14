from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import cv2
import easyocr
from ultralytics import YOLO
import os

app = FastAPI()

print("Đang tải mô hình EasyOCR...")
reader = easyocr.Reader(['en'], gpu=True) 

print("Đang tải mô hình YOLO...")
model = YOLO('yolov8n.pt') 

class ImageRequest(BaseModel):
    image_path: str

@app.post("/detect-plate")
async def detect_plate(request: ImageRequest):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_image_path = os.path.join(base_dir, 'backend', request.image_path)
    
    if not os.path.exists(full_image_path):
        raise HTTPException(status_code=404, detail=f"Không tìm thấy file ảnh tại: {full_image_path}")

    img = cv2.imread(full_image_path)
    if img is None:
        raise HTTPException(status_code=400, detail="Lỗi khi đọc file ảnh")
    results = reader.readtext(img)

    plate_text = ""
    for (bbox, text, prob) in results:
        clean_text = ''.join(e for e in text if e.isalnum()).upper()
        if clean_text:
            plate_text += clean_text + "-"

    plate_text = plate_text.strip("-")

    if not plate_text:
        plate_text = "UNKNOWN"

    print(f"Nhận diện thành công: {plate_text}")
    return {"plate_number": plate_text}