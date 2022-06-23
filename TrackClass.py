from packageImport import *


class TrackFace:
    def __init__(self, w=360, h=240):
        self.width = w
        self.height = h
        self.greenRange = [6400, 6800]
        self.pidPar = [0.4, 0.4, 0]
        self.preErrorX = 0
        self.preErrorY = 0
        self.face_cascade = cv2.CascadeClassifier(r"Resources/haarcascade_frontalface_default.xml")

    def findFace(self, img):
        img = cv2.resize(img, (self.width, self.height))
        # img = cv2.rotate(img, cv2.ROTATE_180)
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
            errorX = x - self.width // 2
            errorY = self.height // 2 - y

            yaw_speed = self.pidPar[0] * errorX + self.pidPar[1] * (errorX - self.preErrorX)
            ud_speed = self.pidPar[0] * errorY + self.pidPar[1] * (errorY - self.preErrorY)
            yaw_speed = int(np.clip(yaw_speed, -100, 100))
            ud_speed = int(np.clip(ud_speed, -100, 100))
            if self.greenRange[0] < area < self.greenRange[1]:
                fb = 0
            elif area > self.greenRange[1]:
                fb = -20
            elif area < self.greenRange[0]:
                fb = 20
            print(f"x: {x} y: {y} errorX: {errorX} errorY: {errorY} yaw_speed: {yaw_speed} ud_speed: {ud_speed} fb: {fb} area: {area}")
            return fb, yaw_speed, errorX, errorY
        else:
            fb = 0
            yaw_speed = 0
            errorX = 0
            errorY = 0
            return fb, yaw_speed, errorX, errorY


