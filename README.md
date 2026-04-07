# Lens-Distortion-Rectifier

**Lens-Distortion-Rectifier**는 [OpenCV](https://opencv.org/)를 활용해 카메라 캘리브레이션을 수행하고, 렌즈로 인한 이미지 왜곡을 정밀하게 보정하는 도구입니다.

---

## 1. 프로젝트 개요 (Description)

### 목표

체스보드 패턴을 활용해 카메라의 내부 파라미터(카메라 행렬, 왜곡 계수)를 추출하고, 이를 기반으로 왜곡된 영상을 보정합니다.

### 주요 기능

| 스크립트 | 설명 |
|----------|------|
| **`camera_calibration.py`** | 영상에서 체스보드 코너를 검출하고, **Camera Matrix**, **Distortion Coefficients**, RMSE(재투영 오차)를 계산한 뒤 `calibration_result.pkl`에 저장합니다. |
| **`distortion_correction.py`** | 저장된 파라미터를 적용해 왜곡을 보정하고, **전·후 비교**를 위한 데모 이미지와 보정 영상을 생성합니다. |

---

## 2. 파일 구조 (File Structure)

```
Lens-Distortion-Rectifier/
├── data/
│   └── chessboard.mp4           # 캘리브레이션용 원본 영상
├── results/
│   ├── corrected.avi            # 왜곡 보정 완료 영상
│   └── demo_comparison.jpg      # README용 전·후 비교 이미지
├── camera_calibration.py        # 캘리브레이션 실행 스크립트
├── distortion_correction.py     # 왜곡 보정 실행 스크립트
├── calibration_result.pkl       # 계산된 파라미터 저장 파일
└── README.md                    # 프로젝트 설명서
```

---

## 3. 카메라 캘리브레이션 결과 (Calibration Results)

아래는 **20개의 유효 프레임**을 사용하여 계산된 카메라 파라미터입니다.

| 항목 | 값 |
|------|-----|
| **RMSE** (재투영 오차) | **0.696018** |

### Camera Matrix (K)

| | |
|--|--|
| **fx** | 2358.2874 |
| **fy** | 2277.9619 |
| **cx** | 849.7998 |
| **cy** | 657.5251 |

### Distortion Coefficients

계산된 5개 계수 **\[k1, k2, p1, p2, k3\]**:

```
[0.3986, 0.2271, -0.0521, 0.0561, -4.6176]
```

> **참고:** 보정 단계(`distortion_correction.py`)에서는 안정적인 결과를 위해 **k3(5번째 계수)를 0으로 고정**하여 적용합니다. 고차 왜곡 항이 과도하게 반영될 때 발생할 수 있는 뒤틀림을 줄이기 위한 설정입니다.

---

## 4. 왜곡 보정 데모 (Demonstration)

보정 전(왼쪽)과 후(오른쪽)를 나란히 비교한 이미지와, 보정이 적용된 **결과 동영상**을 아래에서 확인할 수 있습니다.

> 본 실험에 사용된 스마트폰 렌즈는 광학 설계상 육안으로는 왜곡이 크게 느껴지지 않을 수 있습니다. 그럼에도 추출된 파라미터를 통해 **수학적으로 정밀한 보정**이 적용되었음을 비교 이미지·영상으로 확인할 수 있습니다.

### 비교 이미지

![demo_comparison](https://github.com/user-attachments/assets/bbb8b0c3-2bdd-4f9d-91ed-ec39fada7534)


### 결과 동영상

https://github.com/user-attachments/assets/31c687d7-f08d-4d12-83f1-1b02554b9103

## 5. 사용 방법

1. `data/chessboard.mp4`에 체스보드가 충분히 보이는 원본 영상을 둡니다.  
2. 캘리브레이션 실행:

   ```bash
   python camera_calibration.py
   ```

3. 왜곡 보정 및 데모 이미지·영상 생성:

   ```bash
   python distortion_correction.py
   ```

**필요 패키지:** Python 3, OpenCV (`opencv-python`), NumPy

---

## 라이선스

이 저장소의 사용 조건은 필요 시 별도로 명시할 수 있습니다.
