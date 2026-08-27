import os
import cv2
import zipfile
import random
import shutil

# ============================================================
# 1. 경로 설정
# ============================================================

BASE_DIR = os.getcwd()

IMAGES_ZIP = os.path.join(BASE_DIR, "Images.zip")
MASKS_ZIP = os.path.join(BASE_DIR, "Masks.zip")

DATASET_DIR = os.path.join(BASE_DIR, "datasets")

TRAIN_IMAGE_DIR = os.path.join(DATASET_DIR, "images", "train")
TEST_IMAGE_DIR = os.path.join(DATASET_DIR, "images", "test")

TRAIN_LABEL_DIR = os.path.join(DATASET_DIR, "labels", "train")
TEST_LABEL_DIR = os.path.join(DATASET_DIR, "labels", "test")


# ============================================================
# 2. 설정
# ============================================================

TRAIN_RATIO = 0.8
RANDOM_SEED = 42

# 너무 작은 영역 제거
MIN_WIDTH = 3
MIN_HEIGHT = 3


# ============================================================
# 3. 폴더 생성
# ============================================================

for directory in [
    TRAIN_IMAGE_DIR,
    TEST_IMAGE_DIR,
    TRAIN_LABEL_DIR,
    TEST_LABEL_DIR
]:
    os.makedirs(directory, exist_ok=True)


# ============================================================
# 4. 기존 데이터 삭제 여부
# ============================================================

print("=" * 60)
print("YOLO 데이터셋 생성 시작")
print("=" * 60)

print(f"\nImages ZIP : {IMAGES_ZIP}")
print(f"Masks ZIP  : {MASKS_ZIP}")

if not os.path.exists(IMAGES_ZIP):
    print("\n❌ Images.zip을 찾을 수 없습니다.")
    exit()

if not os.path.exists(MASKS_ZIP):
    print("\n❌ Masks.zip을 찾을 수 없습니다.")
    exit()


# ============================================================
# 5. ZIP 파일 열기
# ============================================================

print("\n📦 ZIP 파일 확인 중...")

with zipfile.ZipFile(IMAGES_ZIP, "r") as images_zip, \
     zipfile.ZipFile(MASKS_ZIP, "r") as masks_zip:

    # --------------------------------------------------------
    # 이미지 파일 목록
    # --------------------------------------------------------

    image_files = [
        f for f in images_zip.namelist()
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    # --------------------------------------------------------
    # 마스크 파일 목록
    # --------------------------------------------------------

    mask_files = [
        f for f in masks_zip.namelist()
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    print(f"이미지 파일 수 : {len(image_files):,}")
    print(f"마스크 파일 수 : {len(mask_files):,}")

    # --------------------------------------------------------
    # 마스크를 파일명 기준으로 dictionary 생성
    #
    # image_1.png
    # image_10.png
    # image_100.png
    # ...
    # --------------------------------------------------------

    mask_dict = {}

    for mask_path in mask_files:
        filename = os.path.basename(mask_path)
        stem = os.path.splitext(filename)[0]

        mask_dict[stem] = mask_path


    # ========================================================
    # 6. 이미지-마스크 매칭
    # ========================================================

    matched_pairs = []

    for image_path in image_files:

        filename = os.path.basename(image_path)
        stem = os.path.splitext(filename)[0]

        if stem in mask_dict:
            matched_pairs.append(
                (image_path, mask_dict[stem])
            )

    print(f"\n🔗 매칭된 이미지-마스크 : {len(matched_pairs):,}")

    if len(matched_pairs) == 0:
        print("\n❌ 매칭되는 이미지와 마스크가 없습니다.")
        print("이미지와 마스크의 파일명이 같은지 확인해주세요.")
        exit()


    # ========================================================
    # 7. Train / Test 분할
    # ========================================================

    random.seed(RANDOM_SEED)

    random.shuffle(matched_pairs)

    train_count = int(len(matched_pairs) * TRAIN_RATIO)

    train_pairs = matched_pairs[:train_count]
    test_pairs = matched_pairs[train_count:]

    print(f"\n📊 데이터 분할")
    print(f"Train : {len(train_pairs):,}")
    print(f"Test  : {len(test_pairs):,}")


    # ========================================================
    # 8. YOLO 라벨 생성 함수
    # ========================================================

    def process_pair(image_zip_path, mask_zip_path, image_output_dir, label_output_dir):

        image_filename = os.path.basename(image_zip_path)

        # ----------------------------------------------------
        # 이미지 읽기
        # ----------------------------------------------------

        image_data = images_zip.read(image_zip_path)

        image_array = cv2.imdecode(
            __import__("numpy").frombuffer(
                image_data,
                dtype=__import__("numpy").uint8
            ),
            cv2.IMREAD_COLOR
        )

        if image_array is None:
            return False

        H, W = image_array.shape[:2]


        # ----------------------------------------------------
        # 마스크 읽기
        # ----------------------------------------------------

        mask_data = masks_zip.read(mask_zip_path)

        mask_array = cv2.imdecode(
            __import__("numpy").frombuffer(
                mask_data,
                dtype=__import__("numpy").uint8
            ),
            cv2.IMREAD_GRAYSCALE
        )

        if mask_array is None:
            return False


        # ----------------------------------------------------
        # 이미지와 마스크 크기가 다르면 마스크 크기 조정
        # ----------------------------------------------------

        if mask_array.shape[:2] != (H, W):

            mask_array = cv2.resize(
                mask_array,
                (W, H),
                interpolation=cv2.INTER_NEAREST
            )


        # ----------------------------------------------------
        # 마스크에서 객체 영역 추출
        # ----------------------------------------------------

        contours, _ = cv2.findContours(
            mask_array,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )


        # ----------------------------------------------------
        # YOLO label 파일 생성
        # ----------------------------------------------------

        txt_filename = (
            os.path.splitext(image_filename)[0] + ".txt"
        )

        txt_path = os.path.join(
            label_output_dir,
            txt_filename
        )

        valid_objects = 0

        with open(txt_path, "w", encoding="utf-8") as f:

            for contour in contours:

                x, y, w, h = cv2.boundingRect(contour)

                # 너무 작은 노이즈 제거
                if w < MIN_WIDTH or h < MIN_HEIGHT:
                    continue

                # YOLO 정규화 좌표
                x_center = (x + w / 2) / W
                y_center = (y + h / 2) / H

                norm_w = w / W
                norm_h = h / H

                # Class 0 = Fire/Smoke
                f.write(
                    f"0 "
                    f"{x_center:.6f} "
                    f"{y_center:.6f} "
                    f"{norm_w:.6f} "
                    f"{norm_h:.6f}\n"
                )

                valid_objects += 1


        # ----------------------------------------------------
        # 이미지 저장
        # ----------------------------------------------------

        image_output_path = os.path.join(
            image_output_dir,
            image_filename
        )

        shutil.copyfile(
            os.path.join(BASE_DIR, image_filename),
            image_output_path
        ) if False else None


        # ZIP에서 이미지 원본 저장
        with open(image_output_path, "wb") as f:
            f.write(image_data)


        return True


    # ========================================================
    # 9. Train 데이터 생성
    # ========================================================

    print("\n🚀 Train 데이터 변환 중...")

    train_success = 0
    train_empty = 0

    for i, (image_path, mask_path) in enumerate(train_pairs, 1):

        result = process_pair(
            image_path,
            mask_path,
            TRAIN_IMAGE_DIR,
            TRAIN_LABEL_DIR
        )

        if result:
            train_success += 1

        if i % 500 == 0 or i == len(train_pairs):
            print(
                f"Train 진행률: "
                f"{i:,}/{len(train_pairs):,}"
            )


    # ========================================================
    # 10. Test 데이터 생성
    # ========================================================

    print("\n🚀 Test 데이터 변환 중...")

    test_success = 0

    for i, (image_path, mask_path) in enumerate(test_pairs, 1):

        result = process_pair(
            image_path,
            mask_path,
            TEST_IMAGE_DIR,
            TEST_LABEL_DIR
        )

        if result:
            test_success += 1

        if i % 500 == 0 or i == len(test_pairs):
            print(
                f"Test 진행률: "
                f"{i:,}/{len(test_pairs):,}"
            )


# ============================================================
# 11. data.yaml 생성
# ============================================================

yaml_path = os.path.join(
    DATASET_DIR,
    "data.yaml"
)

with open(yaml_path, "w", encoding="utf-8") as f:

    f.write(
        "path: " + DATASET_DIR.replace("\\", "/") + "\n"
    )

    f.write(
        "train: images/train\n"
    )

    f.write(
        "val: images/test\n"
    )

    f.write(
        "test: images/test\n"
    )

    f.write("\n")

    f.write("names:\n")
    f.write("  0: FireSmoke\n")


# ============================================================
# 12. 최종 결과
# ============================================================

print("\n" + "=" * 60)
print("🎉 YOLO 데이터셋 생성 완료!")
print("=" * 60)

print(f"\nTrain 이미지 : {train_success:,}")
print(f"Test 이미지  : {test_success:,}")

print(f"\n데이터셋 위치:")
print(DATASET_DIR)

print(f"\ndata.yaml:")
print(yaml_path)

print("\n폴더 구조:")
print("datasets/")
print("├── images/")
print("│   ├── train/")
print("│   └── test/")
print("├── labels/")
print("│   ├── train/")
print("│   └── test/")
print("└── data.yaml")

print("\n다음 단계:")
print("YOLO 모델 학습을 진행하면 됩니다.")