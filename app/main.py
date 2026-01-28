"""
FastAPI entrypoint.
"""

import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.video import VideoProcessor
# from app.core import CAMERA_INDEX
from app.core.config import RtSP_URL

app = FastAPI()
processor = VideoProcessor()

@app.get("/stream")
def stream():
    cap = cv2.VideoCapture(f"{RtSP_URL}?rtsp_transport=udp", cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    # cap = cv2.VideoCapture(RtSP_URL)

    def generate():
        while True:
            # Flush buffered frames
            for _ in range(3):
                cap.grab()
            #  Retrieve the latest frame
            ret, frame = cap.retrieve()
            if not ret:
                break
            
            # 3️ Process only the latest frame
            frame = processor.process(frame)
            _, buffer = cv2.imencode(".jpg", frame)

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + buffer.tobytes()
                + b"\r\n"
            )

    return StreamingResponse(
        generate(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )











###################################POPUP Window Streaming - IGNORE #########################################
# """
# FastAPI entrypoint.
# """

# import cv2
# from fastapi import FastAPI

# from app.video import VideoProcessor
# from app.core.config import RtSP_URL

# app = FastAPI()
# processor = VideoProcessor()

# SHOW_LOCAL = True  # ✅ enable local window

# @app.get("/stream")
# def stream():
#     cap = cv2.VideoCapture(f"{RtSP_URL}?rtsp_transport=udp", cv2.CAP_FFMPEG)
#     cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

#     def generate():
#         while True:
#             # Flush buffered frames
#             for _ in range(5):
#                 cap.grab()

#             # Retrieve the latest frame
#             ret, frame = cap.retrieve()
#             if not ret:
#                 break

#             # Process frame
#             frame = processor.process(frame)

#             # ✅ Show local OpenCV window
#             if SHOW_LOCAL:
#                 cv2.imshow("RTSP Inference (Local)", frame)
#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     break

            

#         cap.release()
#         cv2.destroyAllWindows()

#     # Just run the generator so the window opens
#     generate()

#     return {"status": "Local RTSP window running (browser streaming disabled)"}










