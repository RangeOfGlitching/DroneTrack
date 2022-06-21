from packageImport import *
import D435iClass as dc
import TrackClass as tc

# init camera
dc = dc.DepthCamera(3)
tr = tc.TrackFace()

try:
    while True:
        ret, bg_removed = dc.get_frame()
        # distance = depth_frame[point[1], point[0]] / 1000
        frame, info, face = tr.findFace(bg_removed)
        fbSpeed, yaw_speed, tr.preError = tr.track(info, face)
        error = cv2.imshow("color frame", frame)

        if cv2.waitKey(1) == ord("q"):
            break
finally:
    dc.release()
