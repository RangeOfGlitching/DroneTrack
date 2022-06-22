from packageImport import *
import D435iClass as dc
import TrackClass as tc

# init camera
dc = dc.DepthCamera(3)
tr = tc.TrackFace()

try:
    while True:
        ret, bg_removed = dc.get_frame()
        frame, info, face = tr.findFace(bg_removed)
        print(f"face: {face} size{info[1]}")
        fbSpeed, yaw_speed, tr.preError = tr.track(info, face)
        # error = cv2.imshow("color frame", frame)
        #
        # if cv2.waitKey(1) == ord("q"):
        #     break
finally:
    dc.release()
