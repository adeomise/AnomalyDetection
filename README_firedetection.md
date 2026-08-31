# 실시간 화재 탐지 (Realtime Fire Detection)

스마트폰 카메라 영상을 노트북으로 실시간 수신하여, YOLO로 프레임마다 화재를 탐지하고
화면에 표시하는 데모입니다. 실시간 운용 가능 여부 판단을 위해 **FPS·추론 지연(latency)**을 함께 측정합니다.

> 패럿 X 메카 · 산불 감지 및 소화 페이로드 투하 드론 프로젝트 — 실시간 추론 파트

---

## 1. 설치

```bash
pip install -r requirements.txt
```

## 2. 스마트폰 스트리밍 설정

1. 스마트폰에 **IP Webcam**(Android) 앱 설치 후 실행 → **Start server**
2. 화면에 뜨는 주소 확인 (예: `http://192.168.0.12:8080`)
3. 실제 스트림 주소는 뒤에 **`/video`** 를 붙인 것 → `http://192.168.0.12:8080/video`

> ⚠️ 폰과 노트북이 **같은 Wi-Fi**에 연결되어 있어야 합니다. 안 되면 폰 핫스팟을 켜고 노트북을 붙이면 대부분 해결됩니다.
> iPhone은 **DroidCam** 또는 **Larix Broadcaster(RTSP)** 앱을 사용하세요.

## 3. 실행

```bash
# 스마트폰 스트림으로 (best.pt = 학습된 화재 가중치)
python stream_detect.py --source "http://192.168.0.12:8080/video" --weights best.pt

# 노트북 내장 웹캠으로 빠르게 테스트
python stream_detect.py --source 0 --weights best.pt

# 저장된 영상 파일로 테스트
python stream_detect.py --source fire.mp4 --weights best.pt
```

**주요 옵션**

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--source` | (필수) | 스트림 URL / `0`(내장 웹캠) / 영상파일 경로 |
| `--weights` | `best.pt` | YOLO 가중치 경로 |
| `--conf` | `0.25` | 탐지 임계값 (화재가 안 잡히면 `0.15`로 낮추기) |
| `--imgsz` | `640` | 입력 크기 (FPS 부족하면 `416`/`320`으로 낮추기) |
| `--log` | `metrics.csv` | FPS·지연 기록 파일 |

## 4. 출력

- 실시간 화면: 화재 위치에 **빨간 bounding box** + 좌상단에 **FPS / 추론 지연** 표시 (`q` 키로 종료)
- **`metrics.csv`**: 프레임별 `infer_ms`(추론 지연) · `fps` · `num_det`(탐지 개수)
- 종료 시 콘솔에 **평균 FPS / 평균 추론 지연** 요약 출력

## 5. 실시간 운용 판단 지표

| 지표 | 의미 | 기준(예시) |
|---|---|---|
| 추론 지연 (infer ms) | 한 프레임 추론 시간 | 낮을수록 좋음 |
| FPS | 초당 처리 프레임 수 | 15↑ 실용 · 30↑ 부드러움 |

> FPS가 낮으면 `--imgsz`를 낮추거나(640→416→320), 더 가벼운 모델(nano), GPU를 사용하세요.
> 낮게 나오더라도 **그 수치를 기록하는 것** 자체가 실시간 운용 가능 여부의 판단 근거가 됩니다.
