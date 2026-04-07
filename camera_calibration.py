import cv2
import numpy as np
import os
import pickle

# ── 설정 (성공 확률을 높이기 위해 최적화) ───────────────────────
VIDEO_FILE   = 'data/chessboard.mp4'   
BOARD_SIZE   = (7, 7)                  
SQUARE_SIZE  = 0.025                   
FRAME_SKIP   = 1                       # 모든 프레임을 검사하여 10개 이상 무조건 확보
MAX_FRAMES   = 30                      # 연산 속도를 위해 30개만 찾으면 바로 계산 시작
SAVE_PATH    = 'calibration_result.pkl' 
# ─────────────────────────────────────────────────────────────

def find_chessboard_corners(video_path, board_size, frame_skip):
    objp = np.zeros((board_size[0] * board_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)
    objp *= SQUARE_SIZE

    obj_points, img_points = [], []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened(): return None, None, None

    frame_idx, found_cnt, img_size = 0, 0, None
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    print("[INFO] 코너 추출 중... 30개까지만 찾고 바로 계산합니다.")

    while found_cnt < MAX_FRAMES:
        ret, frame = cap.read()
        if not ret: break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if img_size is None: img_size = gray.shape[::-1]

        found, corners = cv2.findChessboardCorners(gray, board_size, 
            cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE + cv2.CALIB_CB_FAST_CHECK)

        if found:
            corners_sub = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            obj_points.append(objp)
            img_points.append(corners_sub)
            found_cnt += 1
            print(f"[SUCCESS] {found_cnt}/{MAX_FRAMES} 확보 완료")
            
        frame_idx += 1

    cap.release()
    cv2.destroyAllWindows()
    return obj_points, img_points, img_size

if __name__ == '__main__':
    os.makedirs('results', exist_ok=True)
    obj_pts, img_pts, img_sz = find_chessboard_corners(VIDEO_FILE, BOARD_SIZE, FRAME_SKIP)

    if not obj_pts or len(obj_pts) < 10:
        print(f"[ERROR] {len(obj_pts)}개만 찾았습니다. 10개 이상이 필요합니다.")
    else:
        print("[INFO] 캘리브레이션 계산 시작...")
        # [중요] CALIB_FIX_K3를 추가하여 결과가 찌그러지는 현상을 방지합니다.
        rmse, K, dist, rvecs, tvecs = cv2.calibrateCamera(
            obj_pts, img_pts, img_sz, None, None, flags=cv2.CALIB_FIX_K3
        )
        
        print("\n" + "="*45)
        print("   [ README.md 작성용 결과 데이터 ]")
        print("="*45)
        print(f"RMSE : {rmse:.6f}")
        print(f"fx : {K[0,0]:.4f}, fy : {K[1,1]:.4f}")
        print(f"cx : {K[0,2]:.4f}, cy : {K[1,2]:.4f}")
        print(f"Distortion: {dist.flatten()}")
        print("="*45 + "\n")

        with open(SAVE_PATH, 'wb') as f:
            pickle.dump({'K': K, 'dist': dist, 'img_size': img_sz, 'rmse': rmse}, f)
        print(f"[INFO] 결과 저장 완료: {SAVE_PATH}")