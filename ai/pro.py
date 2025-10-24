"""
advanced_national_id_ocr.py

Features:
- Deskew images
- EAST Text Detection for accurate text region detection
- OCR with EasyOCR on detected regions (Persian + English)
- Convert numbers to English for printing
- Copy image for each valid national ID
- Original images remain unchanged
- All print/debug messages are in English
"""

import os
import re
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

try:
    import easyocr
except Exception:
    raise RuntimeError("EasyOCR is not installed. Please install: pip install easyocr")

# ===== Settings =====
INPUT_DIR = "input_images"
OUTPUT_DIR = "renamed_images"
EAST_MODEL_PATH = "frozen_east_text_detection.pb"  # Download from OpenCV repo if needed
MIN_CONFIDENCE = 0.5
PADDING = 5
# ====================

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Utility: validate Iranian national code
def is_valid_iranian_national_code(code: str) -> bool:
    code = code.strip()
    if not re.fullmatch(r"\d{10}", code):
        return False
    digits = [int(ch) for ch in code]
    s = sum(digits[i] * (10 - i) for i in range(9))
    r = s % 11
    check = digits[9]
    if r < 2:
        return check == r
    else:
        return check == (11 - r)

# Convert Persian/Arabic numbers to English
def to_english_numbers(text):
    translation_table = str.maketrans(
        '۰۱۲۳۴۵۶۷۸۹', '0123456789'
    )
    return text.translate(translation_table)

# Deskew image
def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    if coords.size == 0:
        return image
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w,h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# Preprocess for OCR
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    _, th = cv2.threshold(enhanced,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th

# Decode EAST output
def decode_predictions(scores, geometry, min_confidence):
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    for y in range(numRows):
        scoresData = scores[0,0,y]
        xData0 = geometry[0,0,y]
        xData1 = geometry[0,1,y]
        xData2 = geometry[0,2,y]
        xData3 = geometry[0,3,y]
        anglesData = geometry[0,4,y]

        for x in range(numCols):
            score = scoresData[x]
            if score < min_confidence:
                continue
            offsetX = x * 4.0
            offsetY = y * 4.0

            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            rects.append((startX, startY, endX, endY))
            confidences.append(float(score))
    return (rects, confidences)

# Get text boxes with EAST
def get_text_boxes(image, net, min_confidence=MIN_CONFIDENCE):
    (H, W) = image.shape[:2]
    newW, newH = (320, 320)
    rW = W / float(newW)
    rH = H / float(newH)

    blob = cv2.dnn.blobFromImage(image, 1.0, (newW,newH),(123.68,116.78,103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(net.getUnconnectedOutLayersNames())
    (rects, confidences) = decode_predictions(scores, geometry, min_confidence)
    boxes = cv2.dnn.NMSBoxes(rects, confidences, min_confidence, 0.4)
    final_boxes = []
    if len(boxes) > 0:
        for i in boxes.flatten():
            (startX, startY, endX, endY) = rects[i]
            startX = max(0, int(startX * rW))
            startY = max(0, int(startY * rH))
            endX = min(W, int(endX * rW))
            endY = min(H, int(endY * rH))
            final_boxes.append((startX, startY, endX, endY))
    return final_boxes

# Extract national codes from text
def extract_national_codes(text):
    text_en = to_english_numbers(text)
    candidates = re.findall(r"\d{10}", text_en)
    seen = set()
    uniq = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            uniq.append(c)
    valid = [c for c in uniq if is_valid_iranian_national_code(c)]
    return valid

# Process images folder
def process_images(input_dir=INPUT_DIR, output_dir=OUTPUT_DIR):
    files = list(Path(input_dir).glob("*"))
    if not files:
        print("No files found in input directory:", input_dir)
        return

    reader = easyocr.Reader(['fa','en'])
    net = cv2.dnn.readNet(EAST_MODEL_PATH)

    for f in files:
        if f.is_dir():
            continue
        ext = f.suffix.lower()
        if ext not in [".jpg",".jpeg",".png",".bmp",".tif",".tiff",".webp"]:
            print(f"Skipping unsupported file format: {f.name}")
            continue
        print(f"Processing: {f.name}")
        try:
            img = cv2.imdecode(np.fromfile(str(f), dtype=np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                print("Failed to read image:", f.name)
                continue
        except Exception as e:
            print("Error loading image:", e)
            continue

        img = deskew(img)
        boxes = get_text_boxes(img, net)

        all_texts = []
        for (startX, startY, endX, endY) in boxes:
            pad = PADDING
            roi = img[max(0,startY-pad):min(img.shape[0],endY+pad), max(0,startX-pad):min(img.shape[1],endX+pad)]
            text = "\n".join(reader.readtext(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB), detail=0))
            if text.strip():
                all_texts.append(text)

        combined_text = "\n".join(all_texts)
        valid_codes = extract_national_codes(combined_text)

        if valid_codes:
            for idx, code in enumerate(valid_codes):
                new_name = f"{code}{ext}" if idx==0 else f"{code}_{idx}{ext}"
                dst = Path(output_dir) / new_name
                counter = 1
                while dst.exists():
                    dst = Path(output_dir) / f"{code}_{idx}_{counter}{ext}"
                    counter += 1
                shutil.copy2(str(f), str(dst))
                print(f"Copied {f.name} → {dst.name} (National ID: {code})")
        else:
            rejected_dir = Path(output_dir) / "no_valid_national_id"
            rejected_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(f), str(rejected_dir / f.name))
            print(f"No valid national ID found for {f.name} — moved to {rejected_dir.name}")

if __name__ == "__main__":
    print("Starting processing of images folder...")
    process_images()
    print("Processing completed.")
