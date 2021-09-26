import cv2
import numpy as np
import face_recognition
from requetes import getNamesAndImages, findEncodings, prisonerInformation


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    path = './images'
    namesDB = []  # List which will store all id from DB
    nameList, images = getNamesAndImages(path)  # Returns ID and Images
    encodeImgKnown = findEncodings(images)  # takes images encodes
    prisoniers = prisonerInformation()  # Stores all the information from DB

    def process_frame(self, img):
        imgReduced = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgReduced = cv2.cvtColor(imgReduced, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgReduced)  # Find and extract face position in the image
        encodesCurFrame = face_recognition.face_encodings(imgReduced, facesCurFrame)  # encodeCurFrame contains a unic encoding facial features that can be compared to any other picture of a face!
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            faceDis = face_recognition.face_distance(self.encodeImgKnown, encodeFace)  # Compare distance between known face and face from camera. It returns distance in %
            distance = list(faceDis)  # Converts an array to a list
            print('Equart de ressemblance ', distance)
            minDistance = min(distance)  # Get the min value in the list
            print('distance', minDistance)
            if minDistance <= 0.40:
                minIndex = np.argmin(faceDis)  # Get the index of the min element in the array.
                print('minIndex', minIndex)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

                for rows in self.prisoniers:
                    self.namesDB.append(rows[0])  # Add id from DB to the list idDB
                    newIdDB = set(self.namesDB)  # Filter the stand-in element in the list
                    print('id from DB ', newIdDB)
                    identifiant = self.nameList[minIndex]  # Takes one ID corresponding to the index
                    print('indentifiant similaire ', identifiant)
                    if identifiant not in newIdDB:
                        cv2.putText(img, "Unknown face ..!", (40, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                    else:
                        for val in self.prisoniers:
                            if val[0] == identifiant:  # check if id from dataset are in DB
                                names = val[0]
                                peine = val[5]
                                statut = val[7]
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                        # cv2.rectangle(img, (x1 - 25, y2 + 60), (x2 + 25, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, f"Nom: {names}", (x1 - 20, y2 + 15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (0, 255, 0), 1)
                        cv2.putText(img, f'Peine: {peine}', (x1 - 20, y2 + 35), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (0, 255, 0), 1)
                        cv2.putText(img, f'Statut: {statut}', (x1 - 20, y2 + 55), cv2.FONT_HERSHEY_COMPLEX_SMALL, .75, (0, 255, 0), 1)
            else:
                cv2.putText(img, "Unknown face need Registering ..!", (40, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(img, " ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        return img

    def get_frame(self):
        success, data = self.video.read()
        frame = self.process_frame(data)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
