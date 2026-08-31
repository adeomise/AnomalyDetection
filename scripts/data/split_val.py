import os
import glob
import random
import shutil

# 기본 경로
BASE_DIR = r"D:\fire_yolo\datasets"

# Train 경로
train_image_dir = os.path.join(BASE_DIR, "images", "train")
train_label_dir = os.path.join(BASE_DIR, "labels", "train")

# Validation 경로
val_image_dir = os.path.join(BASE_DIR, "images", "val")
val_label_dir = os.path.join(BASE_DIR, "labels", "val")

# Validation 폴더가 없으면 생성
os.makedirs(val_image_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)

# Train 이미지 목록
images = glob.glob(os.path.join(train_image_dir, "*.*"))

print(f"현재 Train 이미지 수: {len(images)}개")

# 랜덤 시드 고정
random.seed(42)
random.shuffle(images)

# Train의 20%를 Validation으로 사용
val_size = int(len(images) * 0.2)

val_images = images[:val_size]

print(f"Validation으로 이동할 이미지 수: {len(val_images)}개")

# 이미지와 대응하는 라벨 이동
moved_count = 0

for img_path in val_images:

    file_name = os.path.basename(img_path)
    base_name = os.path.splitext(file_name)[0]

    # 이미지 이동
    new_image_path = os.path.join(
        val_image_dir,
        file_name
    )

    shutil.move(img_path, new_image_path)

    # 대응하는 라벨
    label_path = os.path.join(
        train_label_dir,
        base_name + ".txt"
    )

    if os.path.exists(label_path):

        new_label_path = os.path.join(
            val_label_dir,
            base_name + ".txt"
        )

        shutil.move(label_path, new_label_path)

    moved_count += 1

print()
print("=" * 50)
print("Validation 데이터 분할 완료!")
print("=" * 50)
print(f"이동한 이미지: {moved_count}개")

print()
print("최종 구조:")
print(f"Train: {len(glob.glob(os.path.join(train_image_dir, '*.*')))}개")
print(f"Val:   {len(glob.glob(os.path.join(val_image_dir, '*.*')))}개")
print(f"Test:  {len(glob.glob(os.path.join(BASE_DIR, 'images', 'test', '*.*')))}개")