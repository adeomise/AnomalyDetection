"""
실시간 화재 탐지 데모 (스마트폰 영상 -> 노트북)
------------------------------------------------
- IP Webcam 등으로 송출된 폰 영상을 OpenCV로 받아 YOLO로 프레임마다 추론
- 화면에 화재 bounding box 표시 + FPS / 추론 지연(latency) 측정
- 측정 결과는 metrics.csv 로 저장

사용법:
    python stream_detect.py --source "http://<폰IP>:8080/video" --weights best.pt
    python stream_detect.py --source 0            # 노트북 내장 웹캠으로 테스트
    python stream_detect.py --source fire.mp4      # 저장된 영상으로 테스트
"""
import argparse
import time
import csv
from collections import deque

import cv2
from ultralytics import YOLO


def parse_args():
    ap = argparse.ArgumentParser(description="실시간 화재 탐지 데모")
    ap.add_argument("--source", required=True,
                    help="스트림 URL / 0(내장웹캠) / 영상파일 경로")
    ap.add_argument("--weights", default="best.pt", help="YOLO 가중치 경로")
    ap.add_argument("--conf", type=float, default=0.25, help="탐지 임계값")
    ap.add_argument("--imgsz", type=int, default=640, help="입력 크기(작을수록 빠름)")
    ap.add_argument("--log", default="metrics.csv", help="FPS·지연 기록 CSV 경로")
    return ap.parse_args()


def main():
    args = parse_args()
    source = int(args.source) if args.source.isdigit() else args.source

    model = YOLO(args.weights)                    # 학습된 화재 탐지 가중치
    cap = cv2.VideoCapture(source)                # 폰 영상 실시간 수신
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)           # 버퍼 최소화 -> 지연 감소
    if not cap.isOpened():
        raise SystemExit(f"[!] 스트림 열기 실패: {args.source} (URL/Wi-Fi 확인)")

    f = open(args.log, "w", newline="", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow(["frame", "infer_ms", "fps", "num_det"])

    ts = deque(maxlen=30)                         # 최근 30프레임 -> FPS 평활화
    infer_times = []
    idx = 0
    t_start = time.perf_counter()

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("[!] 프레임 수신 실패 - 종료")
                break

            t_a = time.perf_counter()
            results = model(frame, conf=args.conf, imgsz=args.imgsz, verbose=False)[0]
            infer_ms = (time.perf_counter() - t_a) * 1000    # 추론 지연(ms)

            annotated = results.plot()            # 화재 bbox 자동 표시

            idx += 1
            ts.append(time.perf_counter())
            fps = (len(ts) - 1) / (ts[-1] - ts[0]) if len(ts) > 1 else 0.0
            infer_times.append(infer_ms)
            writer.writerow([idx, round(infer_ms, 1), round(fps, 1), len(results.boxes)])

            # 화면 좌상단에 FPS / 지연 표시
            cv2.putText(annotated, f"FPS: {fps:.1f}   infer: {infer_ms:.0f} ms",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("Fire Detection (press q to quit)", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        f.close()
        elapsed = time.perf_counter() - t_start
        if idx:
            avg_infer = sum(infer_times) / len(infer_times)
            print("\n===== 측정 요약 =====")
            print(f"총 프레임      : {idx}")
            print(f"평균 FPS       : {idx / elapsed:.1f}")
            print(f"평균 추론 지연 : {avg_infer:.1f} ms")
            print(f"로그 저장      : {args.log}")


if __name__ == "__main__":
    main()
