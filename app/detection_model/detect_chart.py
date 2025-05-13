import torch
from pathlib import Path
import os

# # Define the YOLOv5 path and load model
# YOLOV5_PATH = r'E:\Parmeet\TradeLab\yolov5'
# model = torch.hub.load(YOLOV5_PATH, 'custom', path=Path(__file__).parent / 'best.pt', source='local')

# def detect_chart(image_path, output_path):
#     if not os.path.exists(output_path):
#         os.makedirs(output_path)

#     results = model(image_path)

#     # Use results.save with proper folder
#     results.save(save_dir=output_path)

#     print(f"Saved detection results to {output_path}")


import sys
import os
from pathlib import Path
import torch
import cv2
import numpy as np

sys.path.append(r"D:\Parmeet\TradeLab\yolov5")
from models.common import DetectMultiBackend

# Load model
model = DetectMultiBackend(weights=str(Path(__file__).parent / 'best.pt'), device='cpu')
stride, names, pt = model.stride, model.names, model.pt

def detect_chart(image_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Load image
    img0 = cv2.imread(image_path)  # BGR
    assert img0 is not None, f"Image Not Found {image_path}"

    # Padded resize
    img = letterbox(img0, 640, stride=stride, auto=True)[0]

    # Convert
    img = img.transpose((2, 0, 1))[::-1]  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)

    # Normalize
    img = torch.from_numpy(img).to(model.device)
    img = img.float()
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    pred = model(img)

    # Apply NMS (Non-Maximum Suppression)
    pred = non_max_suppression(pred)

    # Save result image
    save_path = os.path.join(output_path, os.path.basename(image_path))
    for det in pred:  # detections per image
        if len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

            for *xyxy, conf, cls in reversed(det):
                label = f'{names[int(cls)]} {conf:.2f}'
                plot_one_box(xyxy, img0, label=label, color=[255, 0, 0], line_thickness=2)

    # Save final output
    cv2.imwrite(save_path, img0)

    print(f"Detection done. Output saved to {save_path}")

# Helper functions
def letterbox(im, new_shape=640, color=(114, 114, 114), stride=32, auto=True):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    ratio = r, r
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad
