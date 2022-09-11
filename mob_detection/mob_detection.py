import cv2
import datetime
import requests
from collections import deque

#Enter your own token.
line_notify_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
line_notify_api = 'https://notify-api.line.me/api/notify'
#Capture video from webcam
vid_capture = cv2.VideoCapture(0)
vid_cod = cv2.VideoWriter_fourcc('m','p','4','v')
circle = deque(maxlen=200)
post_recording = 0
#Adjust so as to fit to your environment.
#The duration that recording lasts after a mob is detected.
DEF_POST_RECORDING=125
#A frame to be stored as a JPEG image file.
DEF_CAPTURE_FRAME=2
DEF_FRAME_DIFF_THRESHOLD=350

while True:
    # Capture each frame of webcam video
    ret,tmp = vid_capture.read()
    circle.append(tmp)

    if 0 < post_recording:
        post_recording -= 1
        if 0 >= post_recording:
            post_recording = 0
            now = datetime.datetime.now()
            filename = 'camvideo_' + now.strftime('%Y%m%d_%H%M%S') + '.mp4'
            output = cv2.VideoWriter(filename, vid_cod, 20.0, (640,480))
            for frame in circle:
                output.write(frame)
            output.release()
            circle.clear()
            cv2.imwrite(fname, det_frame)
            headers = {'Authorization': f'Bearer {line_notify_token}'}
            payload = {'message': 'from camera'}
            files = {'imageFile': open(fname, 'rb')}
            data = {'message': f' Detected!!'}
            requests.post(line_notify_api, headers = headers, data = data, params = payload, files = files)
        elif DEF_CAPTURE_FRAME == DEF_POST_RECORDING-post_recording:
            det_frame = circle[-1]
        else:
            continue
    
    if len(circle)>=3:
        #Convert to grayscale.
        gray1 = cv2.cvtColor(circle[-3], cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(circle[-2], cv2.COLOR_BGR2GRAY)
        gray3 = cv2.cvtColor(circle[-1], cv2.COLOR_BGR2GRAY)

        diff1 = cv2.absdiff(gray2,gray1)
        diff2 = cv2.absdiff(gray3,gray2)
        diff_and = cv2.bitwise_and(diff1, diff2)
        th = cv2.threshold(diff_and, 50, 255, cv2.THRESH_BINARY)[1]
        wh_pixels = cv2.countNonZero(th)
  
        #Start recording if diff is beyond the threshold.
        if wh_pixels > DEF_FRAME_DIFF_THRESHOLD:
            print('detected!!')
            post_recording = DEF_POST_RECORDING
            dt = datetime.datetime.now()
            fname = dt.strftime('%Y%m%d_%H%M%S') + '.jpg'

# close the already opened camera
vid_capture.release()
# close the window and de-allocate any associated memory usage
cv2.destroyAllWindows()
