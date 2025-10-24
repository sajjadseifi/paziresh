"""
advanced_national_id_ocr.py

Advanced OCR with pytesseract + Pillow
- Multi-pass OCR
- Split image into regions
- Rotate images
- Step-by-step progress bars
- Overall progress bar
- Completely without OpenCV
"""

import os
import re
import shutil
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import pytesseract
from tqdm import tqdm

# ===== Settings =====
INPUT_DIR = "input_images"
OUTPUT_DIR = "renamed_images"
REGION_ROWS = 2  # Split image vertically
REGION_COLS = 3  # Split image horizontally
ROTATE_ANGLES = [0, -5, 5, -10, 10]
# Tesseract path if not in PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# ====================

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Validate Iranian national code
def is_valid_iranian_national_code(code: str) -> bool:
    code = code.strip()
    if not re.fullmatch(r"\d{10}", code):
        return False
    digits = [int(ch) for ch in code]
    s = sum(digits[i] * (10 - i) for i in range(9))
    r = s % 11
    check = digits[9]
    return check == r if r < 2 else check == (11 - r)

# Convert Persian/Arabic numbers to English
def to_english_numbers(text):
    return text.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹','0123456789'))

# Preprocess image
def preprocess(img: Image.Image) -> Image.Image:
    img = img.convert("L")
    img = ImageOps.autocontrast(img, cutoff=2)
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img = ImageEnhance.Brightness(img).enhance(1.2)
    return img

# Split image into regions
def split_image(img: Image.Image, rows: int, cols: int):
    width, height = img.size
    regions = []
    row_height = height // rows
    col_width = width // cols
    for r in range(rows):
        for c in range(cols):
            left = c * col_width
            upper = r * row_height
            right = (c + 1) * col_width if c < cols - 1 else width
            lower = (r + 1) * row_height if r < rows - 1 else height
            regions.append(img.crop((left, upper, right, lower)))
    return regions

# Extract valid national codes from text
def extract_codes_from_text(text):
    text_en = to_english_numbers(text)
    candidates = re.findall(r'\d{10}', text_en)
    return [c for c in candidates if is_valid_iranian_national_code(c)]

# Process single image
def process_single_image(f: Path):
    try:
        img = Image.open(f)
    except Exception as e:
        print(f"Cannot open {f.name}: {e}")
        return []

    codes_found = set()
    regions = split_image(img, REGION_ROWS, REGION_COLS)

    steps = ["preprocess+OCR on region"] * len(regions) * len(ROTATE_ANGLES)
    with tqdm(total=len(steps), desc=f"Processing {f.name}", ncols=100, leave=False) as pbar:
        for region in regions:
            for angle in ROTATE_ANGLES:
                tmp = region.rotate(angle, expand=True)
                tmp = preprocess(tmp)
                text = pytesseract.image_to_string(tmp, lang='fas+eng')
                codes_found.update(extract_codes_from_text(text))
                pbar.update(1)
    return list(codes_found)

# Process all images
def process_folder(input_dir=INPUT_DIR, output_dir=OUTPUT_DIR):
    files = [f for f in Path(input_dir).glob("*") if f.is_file()]
    if not files:
        print("No files found in input directory.")
        return

    with tqdm(total=len(files), desc="Overall Progress", ncols=100) as overall_bar:
        for f in files:
            ext = f.suffix.lower()
            if ext not in [".jpg",".jpeg",".png",".bmp",".tif",".tiff",".webp"]:
                print(f"Skipping unsupported file format: {f.name}")
                overall_bar.update(1)
                continue

            codes = process_single_image(f)
            if codes:
                for idx, code in enumerate(codes):
                    new_name = f"{code}{ext}" if idx==0 else f"{code}_{idx}{ext}"
                    dst = Path(output_dir) / new_name
                    counter = 1
                    while dst.exists():
                        dst = Path(output_dir) / f"{code}_{idx}_{counter}{ext}"
                        counter += 1
                    shutil.copy2(f, dst)
                    print(f"Copied {f.name} → {dst.name} (National ID: {code})")
            else:
                rejected_dir = Path(output_dir) / "no_valid_national_id"
                rejected_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, rejected_dir / f.name)
                print(f"No valid national ID for {f.name} — moved to {rejected_dir.name}")

            overall_bar.update(1)

if __name__ == "__main__":
    print("Starting processing of images folder...")
    process_folder()
    print("Processing completed.")
