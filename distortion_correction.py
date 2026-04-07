import cv2
import numpy as np
import pickle
import os

# ── 설정 ────────────────────────────────────────────────────
CALIB_FILE   = 'calibration_result.pkl'
INPUT_VIDEO  = 'data/chessboard.mp4'   
OUTPUT_VIDEO = 'results/corrected.avi'
DEMO_FRAME   = 'results/demo_comparison.jpg'
# ────────────────────────────────────────────────────────────

if __name__ == '__main__':
    os.makedirs('results', exist_ok=True)
    
    with open(CALIB_FILE, 'rb') as f:
        data = pickle.load(f)
    K, dist, img_size = data['K'], data['dist'], data['img_size']

    # [수정] k3 값을 0으로 고정하여 과도한 뒤틀림 방지
    dist[0, 4] = 0 

    # [수정] alpha=0으로 설정하여 검은 여백 없이 꽉 차게 보정
    new_K, roi = cv2.getOptimalNewCameraMatrix(K, dist, img_size, alpha=0, newImgSize=img_size)
    map1, map2 = cv2.initUndistortRectifyMap(K, dist, None, new_K, img_size, cv2.CV_32FC1)

    cap = cv2.VideoCapture(INPUT_VIDEO)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, cap.get(cv2.CAP_PROP_FPS), img_size)

    saved_demo = False
    print("[INFO] 보정 영상 생성 중...")

    while True:
        ret, frame = cap.read()
        if not ret: break

        undistorted = cv2.remap(frame, map1, map2, cv2.INTER_LINEAR)
        
        # 유효 영역 자르기 및 리사이즈
        x, y, w, h = roi
        if w > 0 and h > 0:
            undistorted = undistorted[y:y+h, x:x+w]
            undistorted = cv2.resize(undistorted, img_size)

        out.write(undistorted)

        if not saved_demo:
            side_by_side = np.hstack([frame, undistorted])
            cv2.imwrite(DEMO_FRAME, side_by_side) # README용 이미지
            saved_demo = True

        cv2.imshow('Final Result', undistorted)
        if cv2.waitKey(1) == 27: break

    cap.release()
    out.release()
    cv2.destroyAllWindows()