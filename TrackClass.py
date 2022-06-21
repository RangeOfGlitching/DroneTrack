from packageImport import *


class TrackFace:
    def __init__(self, w=360, h=240):
        self.width = w
        self.height = h
        self.greenRange = [6400, 6800]
        self.pidPar = [0.4, 0.4, 0]
        self.preError = 0
        self.face_cascade = cv2.CascadeClassifier(r"Resources\haarcascade_frontalface_default.xml")

    def findFace(self, img):
        img = cv2.resize(img, (self.width, self.height))
        # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = self.face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=8)
        myFaceListCenter = []
        myFaceListArea = []

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            centerX = x + w // 2
            centerY = y + h // 2
            area = w * h
            print(area)
            cv2.circle(img, (centerX, centerY), 5, (0, 255, 0), cv2.FILLED)
            myFaceListCenter.append([centerX, centerY])
            myFaceListArea.append(area)

        if len(myFaceListArea) != 0:
            i = myFaceListArea.index(max(myFaceListArea))
            info = [myFaceListCenter[i], myFaceListArea[i]]
            return img, info, True
        else:
            return img, [[0, 0], 0], False

    def track(self, info, face):
        if face:
            fb = 0
            area = info[1]
            x, y = info[0]
            error = x - self.width // 2

            yaw_speed = self.pidPar[0] * error + self.pidPar[1] * (error - self.preError)
            yaw_speed = int(np.clip(yaw_speed, -100, 100))
            if self.greenRange[0] < area < self.greenRange[1]:
                fb = 0
            elif area > self.greenRange[1]:
                fb = -20
            elif area < self.greenRange[0]:
                fb = 20
            print(area)
            return fb, yaw_speed, error
        else:
            fb = 0
            yaw_speed = 0
            error = 0
            return fb, yaw_speed, error


