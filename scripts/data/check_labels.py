import os
import random
import cv2

BASE_DIR = r"D:\fire_yolo\datasets"

IMAGE_DIR = os.path.join(BASE_DIR, "images", "train")
LABEL_DIR = os.path.join(BASE_DIR, "labels", "train")

OUTPUT_DIR = r"D:\fire_yolo\label_check"

os.makedirs(OUTPUT_DIR, exist_ok=True)

image_files = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

random.seed(42)
random.shuffle(image_files)

selected_images = image_files[:10]

print("=" * 60)
print("YOLO Label Check")
print("=" * 60)
print(f"Images to check: {len(selected_images)}")
print(f"Output folder: {OUTPUT_DIR}")
print()

for image_file in selected_images:

    image_path = os.path.join(IMAGE_DIR, image_file)

    base_name = os.path.splitext(image_file)[0]
    label_path = os.path.join(LABEL_DIR, base_name + ".txt")

    image = cv2.imread(image_path)

    if image is None:
        print(f"ERROR: Cannot read image: {image_file}")
        continue

    H, W = image.shape[:2]

    if not os.path.exists(label_path):
        print(f"WARNING: Label missing: {image_file}")
        continue

    with open(label_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    box_count = 0

    for line in lines:

        values = line.strip().split()

        if len(values) != 5:
            continue

        class_id, x_center, y_center, width, height = map(float, values)

        x_center *= W
        y_center *= H
        width *= W
        height *= H

        x1 = int(x_center - width / 2)
        y1 = int(y_center - height / 2)
        x2 = int(x_center + width / 2)
        y2 = int(y_center + height / 2)

        x1 = max(0, min(W - 1, x1))
        y1 = max(0, min(H - 1, y1))
        x2 = max(0, min(W - 1, x2))
        y2 = max(0, min(H - 1, y2))

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            image,
            f"class {int(class_id)}",
            (x1, max(y1 - 5, 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1
        )

        box_count += 1

    output_path = os.path.join(
        OUTPUT_DIR,
        image_file
    )

    cv2.imwrite(output_path, image)

    print(f"{image_file} -> {box_count} boxes")

print()
print("=" * 60)
print("Label visualization complete!")
print("=" * 60)