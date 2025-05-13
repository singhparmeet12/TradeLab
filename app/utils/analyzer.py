import torch
from pathlib import Path

# Load YOLO model once
YOLOV5_PATH = r'E:\Parmeet\TradeLab\yolov5'
model = torch.hub.load(YOLOV5_PATH, 'custom', path=Path(__file__).parent / 'best.pt', source='local')

def detect_chart(image_path, output_path):
    results = model(image_path)
    results.save(save_dir=output_path)
