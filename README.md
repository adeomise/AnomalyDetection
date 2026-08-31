# AnomalyDetection

## 패럿 × 메카 AI · 드론 연합 프로젝트

### 산불 감지 및 소화 페이로드 투하 드론

카메라 영상을 통해 화재를 탐지하고, 탐지 결과를 드론 제어와 연결하여 최종적으로 화재 지점에 소화 페이로드를 투하하는 시스템을 구현하는 프로젝트입니다.

전체 흐름은 다음과 같습니다.

```text
카메라 영상
    ↓
화재 탐지 모델
    ↓
Bounding Box / Confidence
    ↓
탐지 판단
    ↓
드론 제어
    ↓
소화 페이로드 투하
```

프로젝트의 핵심은 **영상 기반 화재 탐지 AI**이며, 데이터 구성, 모델 선택, 성능 개선 방법, 실시간 추론 방식, AI와 드론 제어의 연결 방법은 조별로 자유롭게 설계할 수 있습니다.

---

# 1. 프로젝트 진행 흐름

참가자는 아래 순서를 기준으로 프로젝트를 진행하면 됩니다.

```text
1. FLAME 데이터셋 다운로드
        ↓
2. Object Detection용 데이터 전처리
        ↓
3. YOLO 형식 datasets/ + data.yaml 구성
        ↓
4. 데이터 검수
        ↓
5. Starter Baseline 또는 조별 모델 학습
        ↓
6. 학습된 모델 checkpoint 생성
        ↓
7. 스마트폰/영상 기반 실시간 추론
        ↓
8. 모델 개선 및 실험
        ↓
9. 탐지 결과 → 드론 제어 연결
        ↓
10. 실증 및 결과 발표
```

---

# 2. Repository Structure

주요 파일 및 폴더는 다음과 같습니다.

```text
AnomalyDetection/
├── README.md
├── README_firedetection.md
├── requirements.txt
├── stream_detect.py
│
├── colab/
│   └── participant-baseline.ipynb
│
├── scripts/
│   ├── data/
│   │   ├── prepare_yolo.py
│   │   ├── split_val.py
│   │   └── check_labels.py
│   └── ...
│
├── docs/
│   ├── architecture.md
│   ├── data_guide.md
│   ├── environment_setup.md
│   ├── training_guide.md
│   ├── realtime_guide.md
│   ├── validation_plan.md
│   └── open_source_references.md
│
├── data/
├── models/
├── experiments/
└── src/
```

참가자들이 주로 사용할 파일은 다음과 같습니다.

| 파일 | 용도 |
|---|---|
| `colab/participant-baseline.ipynb` | 참가자용 YOLOv8m Starter Baseline |
| `scripts/data/prepare_yolo.py` | YOLO 데이터셋 구축 참고 |
| `scripts/data/split_val.py` | Train / Validation / Test 분할 참고 |
| `scripts/data/check_labels.py` | 이미지·라벨 및 YOLO annotation 검수 |
| `stream_detect.py` | 실시간 영상 화재 탐지 |
| `README_firedetection.md` | 실시간 추론 실행 가이드 |

---

# 3. Quick Start

먼저 repository를 clone합니다.

```bash
git clone https://github.com/adeomise/AnomalyDetection.git
cd AnomalyDetection
```

프로젝트 전체 가이드를 먼저 확인한 뒤 데이터셋 구축부터 진행해주세요.

---

# 4. Dataset

## FLAME Dataset

본 프로젝트에서는 드론으로 통제소각 현장을 촬영한 **FLAME Dataset**을 기본 데이터로 사용합니다.

FLAME은 드론 항공 시점의 화재 데이터를 포함하고 있어 본 프로젝트의 목표인 드론 기반 화재 탐지와 비교적 유사한 환경을 제공합니다.

참가자는 FLAME 원본 데이터를 직접 다운로드하고 Object Detection 학습에 사용할 수 있도록 전처리합니다.

### 기본 데이터 구축 흐름

```text
FLAME 원본 데이터
        ↓
Image / Mask 확인
        ↓
Mask → Bounding Box 변환
        ↓
YOLO Annotation 생성
        ↓
Train / Validation / Test 분할
        ↓
Label / Bounding Box 검수
        ↓
data.yaml 작성
```

YOLO annotation 형식은 다음과 같습니다.

```text
class_id x_center y_center width height
```

좌표는 이미지의 가로·세로 크기를 기준으로 `0~1` 범위로 정규화합니다.

기본 화재 클래스는 다음과 같습니다.

```text
0 = fire
```

최종적으로 다음과 같은 구조를 구성합니다.

```text
datasets/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
│
└── labels/
    ├── train/
    ├── val/
    └── test/
```

그리고 YOLO가 데이터셋 위치와 클래스 정보를 인식할 수 있도록 `data.yaml`을 작성합니다.

예시:

```yaml
path: /your/dataset/path

train: images/train
val: images/val
test: images/test

names:
  0: fire
```

`path`는 각자의 실제 데이터셋 위치에 맞게 수정해야 합니다.

---

# 5. Data Preparation Scripts

데이터 구축 및 검수 과정에서는 repository의 다음 스크립트를 참고할 수 있습니다.

```text
scripts/data/prepare_yolo.py
scripts/data/split_val.py
scripts/data/check_labels.py
```

각 조는 반드시 제공된 스크립트만 사용할 필요는 없으며, 필요에 따라 직접 데이터 전처리 코드를 작성하거나 수정해도 됩니다.

데이터 구축 후에는 최소한 다음 항목을 확인해주세요.

- 이미지와 라벨 파일이 정상적으로 대응하는지
- YOLO annotation 형식이 올바른지
- Bounding Box가 실제 화재 영역에 위치하는지
- Bounding Box 좌표가 이미지 범위를 벗어나지 않는지
- Train / Validation / Test 사이에 데이터 중복이 없는지
- 연속 영상 프레임이 서로 다른 split에 섞여 data leakage가 발생하지 않는지
- `data.yaml`의 경로와 클래스 정보가 올바른지

---

# 6. Participant Starter Baseline

참가자가 직접 구축한 YOLO 데이터셋을 이용해 학습을 시작할 수 있도록 **YOLOv8m 기반 Starter Baseline**을 제공합니다.

```text
colab/participant-baseline.ipynb
```

이 notebook은 각 조가 준비한

```text
datasets/
data.yaml
```

을 직접 연결하여 학습할 수 있도록 구성되어 있습니다.

Colab에서 notebook을 열고 위에서부터 순서대로 실행하면 됩니다.

## 기본 Baseline

| 항목 | 설정 |
|---|---|
| Task | Object Detection |
| Model | YOLOv8m |
| Class | fire |
| Weight | Pretrained YOLOv8m |
| Training | Fine-tuning |

Notebook에서는 다음과 같은 설정을 직접 변경할 수 있습니다.

```python
MODEL_NAME = "yolov8m.pt"
EPOCHS = 50
IMG_SIZE = 640
BATCH_SIZE = 16
```

각 조의 환경과 실험 목적에 따라 자유롭게 변경해주세요.

### 중요

**YOLOv8m 사용은 필수가 아닙니다.**

Starter Baseline은 프로젝트 시작 과정에서 환경 설정이나 학습 파이프라인 구축에 막히지 않도록 제공되는 참고 예제입니다.

---

# 7. Model Training

각 조가 구축한 `data.yaml`을 이용하여 Object Detection 모델을 학습합니다.

YOLO를 사용하는 경우 예시는 다음과 같습니다.

```python
from ultralytics import YOLO

model = YOLO("yolov8m.pt")

model.train(
    data="data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
)
```

학습이 완료되면 YOLO 기준으로 일반적으로 다음 checkpoint가 생성됩니다.

```text
best.pt
last.pt
```

- `best.pt` : Validation 성능이 가장 좋았던 checkpoint
- `last.pt` : 마지막 epoch의 checkpoint

최종 모델은 이후 실시간 추론 단계에서 사용합니다.

---

# 8. Model & Experiment Freedom

각 조의 모델 및 실험 방향은 자유롭게 설정할 수 있습니다.

예를 들어 다음과 같은 실험이 가능합니다.

- YOLOv8n / YOLOv8s / YOLOv8m 등 모델 크기 변경
- 다른 YOLO 계열 모델 사용
- Faster R-CNN
- DETR 계열 Object Detection 모델
- Epoch 변경
- Image Size 변경
- Batch Size 변경
- Data Augmentation
- 추가 데이터셋 사용
- Hard Negative 추가
- Confidence Threshold 조정
- NMS 관련 설정 변경
- 화재와 연기를 구분하는 Multi-Class 모델

다른 Object Detection 모델을 선택하는 경우 해당 모델에 맞는 학습 및 실시간 추론 코드는 조별로 직접 구성합니다.

---

# 9. Additional Dataset

FLAME만으로 데이터 다양성이 부족하다고 판단되는 경우 추가 데이터셋을 사용할 수 있습니다.

예를 들어 **D-Fire Dataset** 등을 활용해 화염·연기·다양한 배경 이미지를 추가할 수 있습니다.

추가 데이터셋을 병합할 경우 반드시 다음을 확인해주세요.

- 클래스 정의 통일
- Annotation format 통일
- 중복 데이터 확인
- Train / Validation / Test leakage 확인

특히 노을, 붉은 조명, 붉은 물체, 구름 등 화재와 비슷하게 보일 수 있는 이미지를 활용하면 False Positive 분석 및 개선에 도움이 될 수 있습니다.

---

# 10. Real-time Fire Detection

학습된 모델은 스마트폰, 웹캠 또는 저장된 영상에 연결하여 실시간 화재 탐지를 수행할 수 있습니다.

실시간 추론 관련 파일:

```text
stream_detect.py
README_firedetection.md
```

자세한 실행 방법은 다음 문서를 참고해주세요.

```text
README_firedetection.md
```

기본 흐름은 다음과 같습니다.

```text
스마트폰 / 웹캠 / 영상
        ↓
OpenCV 영상 수신
        ↓
학습된 Object Detection 모델
        ↓
Bounding Box + Confidence
        ↓
FPS / Latency 확인
```

각 조가 학습한 YOLO checkpoint를 사용하는 경우 자신의 `best.pt` 경로를 연결하여 사용하면 됩니다.

---

# 11. Real-time Performance

실시간 추론에서는 모델의 정확도뿐만 아니라 처리 속도도 함께 확인해주세요.

주요 지표:

- FPS
- Frame inference latency
- Confidence
- Detection stability
- False Positive
- False Negative

모델 성능과 실시간 처리 속도 사이에는 trade-off가 있을 수 있으므로 각 조의 실험 목적에 맞게 모델 크기와 입력 해상도를 조정할 수 있습니다.

---

# 12. Validation

학습 결과는 정량 평가와 실제 영상 테스트를 함께 사용하는 것을 권장합니다.

대표적인 Object Detection 지표:

- Precision
- Recall
- mAP@0.5
- mAP@0.5:0.95

또한 실제 환경과 유사한 영상에 모델을 적용하여 오탐과 미탐을 확인해주세요.

가능한 검증 예시:

```text
Test Dataset
        ↓
정량 성능 평가
        ↓
스마트폰 / 영상 실시간 추론
        ↓
통제된 소형 화원 실증
        ↓
오류 사례 분석
        ↓
모델 개선
```

실제 화원 테스트는 반드시 안전한 통제 환경에서 진행해주세요.

---

# 13. AI → Drone Integration

최종적으로 화재 탐지 모델의 출력을 드론 제어 단계와 연결합니다.

예를 들어 Object Detection 모델에서는 다음 정보를 활용할 수 있습니다.

```text
Bounding Box
Confidence
Class
Bounding Box Center
```

전체 연결 구조는 다음과 같습니다.

```text
화재 탐지
    ↓
탐지 결과
    ↓
판단 로직
    ↓
드론 제어 명령
    ↓
화재 위치 접근
    ↓
소화 페이로드 투하
```

AI와 드론 제어를 연결하는 구체적인 방식은 **조별로 자유롭게 설계**합니다.

각 조의 드론 시스템, 통신 방식, 제어 방식에 맞춰 인터페이스를 구성해주세요.

---

# 14. Final Goal

프로젝트의 최종 목표는 다음과 같습니다.

### 1차 목표

```text
스마트폰 / 카메라 영상
→ 실시간 화재 탐지
```

### 최종 목표

```text
화재 탐지
→ 탐지 판단
→ 드론 제어
→ 화재 위치 접근
→ 소화 페이로드 투하
```

프로젝트 진행 상황과 장비 환경에 따라 실증 범위는 조별로 조정할 수 있습니다.

---

# 15. 발표 권장 항목

최종 발표에서는 다음 내용을 포함하는 것을 권장합니다.

- 사용 데이터 및 전처리 방법
- 선택한 Object Detection 모델
- 학습 설정
- 모델 선택 또는 개선 이유
- Precision / Recall / mAP 등 정량 성능
- False Positive / False Negative 분석
- 실시간 탐지 데모
- FPS / Latency
- 모델 개선 과정
- 실제 화원 또는 영상 실증 결과
- AI와 드론 제어 연결 방법
- 페이로드 투하 결과
- 한계점 및 향후 개선 방향

---

# 16. GitHub 사용 시 유의사항

대용량 데이터셋과 모델 weight는 repository에 직접 commit하지 않습니다.

```text
datasets/
*.pt
*.pth
*.onnx
```

등의 대용량 파일은 별도로 관리해주세요.

또한 다음 정보는 절대 GitHub에 올리지 않습니다.

```text
API Key
Token
Password
.env
Credential
```

개인 PC의 절대경로나 개인 API Key를 코드에 hard-coding하지 않도록 주의해주세요.

---

# 17. 참고 문서

세부 내용은 `docs/`의 문서를 참고할 수 있습니다.

```text
docs/data_guide.md
docs/training_guide.md
docs/realtime_guide.md
docs/environment_setup.md
docs/validation_plan.md
docs/open_source_references.md
docs/architecture.md
```

---

# 18. Current Status

프로젝트 배포 전 사전 검증에서는 다음 항목을 확인했습니다.

| Area | Status |
|---|---|
| YOLO baseline 학습 환경 | Verified |
| 데이터 전처리 및 검수 스크립트 | Available |
| Dataset → YOLOv8m 학습 연결 | Verified |
| YOLOv8m smoke test | Verified |
| Checkpoint 생성 | Verified |
| OpenCV real-time inference | Available |
| Smartphone streaming | Available |
| Drone control integration | Team implementation |

참가자용 데이터와 모델은 각 조가 직접 구축하고 개선합니다.

---

# Safety

실제 드론 비행 및 페이로드 투하 실험은 관련 안전 규정과 비행·촬영 규정을 준수해야 합니다.

초기에는 저장 영상, 스마트폰 영상, 시뮬레이션 또는 통제된 소형 화원 환경에서 충분히 검증한 뒤 실제 비행으로 확장하는 것을 권장합니다.

---

본 repository의 baseline 및 코드는 **참고용 Starter**입니다.

각 조는 프로젝트 목표에 맞게 데이터, 모델, 실시간 추론 방식 및 드론 연결 구조를 자유롭게 개선·확장할 수 있습니다.