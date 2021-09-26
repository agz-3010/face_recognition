import os
import cv2
import face_recognition
import mysql.connector
import pymysql

path = './images'


def takePicture(name):
    video = cv2.VideoCapture(0)
    while True:
        check, frame = video.read()
        cv2.imshow('Taking Picture', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
        elif key == ord('c'):
            cv2.imwrite(os.path.join(path, name + '.jpg'), frame)
            cv2.destroyAllWindows()
            video.release()
            return frame


def getNamesAndImages(way):
    faces = []  # List which will store faces
    faceName = []  # List which will store different id
    for root, directory, filenames in os.walk(way):
        for filename in filenames:  # file will store all the name of each image
            separe = filename.split(".")  # spliting filename by '.'
            nom = str(separe[0])  # save just the id given to the image wich is in position [1]
            img_path = os.path.join(root, filename)  # this directly assigns folder name 0,1,...
            img = cv2.imread(img_path)  # reading the path containing image
            faces.append(img)  # Add faces to my list
            faceName.append(nom)  # Add the id in our list
    return faceName, faces


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def prisonerInformation():
    conn = pymysql.connect(host="localhost", database="facerecog", user="root", password="")  # Connection to DB
    mycursor = conn.cursor()
    cmd = "SELECT accuse.noms, accuse.age, accuse.nationalite, infraction.designationI, infraction.dateI, " \
          "peine.designationP, peine.dateCondamnation, peine.statusP, peine.dateSortie, adresse.phone FROM " \
          "accuse INNER JOIN accuse_infraction ON accuse_infraction.idAccuse = accuse.idAccuse INNER JOIN infraction " \
          "ON infraction.idInfraction = accuse_infraction.idInfraction INNER JOIN peine ON peine.idPeine = " \
          "infraction.idPeine INNER JOIN adresse ON accuse.idAccuse = adresse.idAccuse "
    mycursor.execute(cmd)
    prisonniers = mycursor.fetchall()
    return prisonniers


def enroler(noms, nationalite, age, genre, photo, phone, email, dateNaissance, ville, commune, quartier, avenue,
            cellule, numParcelle, longitude, latitude, designationI, dateI, designationP, dateCondamnation, statusP,
            dateSortie):
    con = pymysql.connect(host="localhost", database="facerecog", user="root", password="")
    cursor = con.cursor()

    if noms != "" and age != "" and nationalite != "" and genre != "" and photo != "" and phone != "" and email != "" and email != "" and ville != "" and commune != "" and quartier != "" and avenue != "" and cellule != "" and numParcelle != "" and designationI != "" and dateI != "" and designationP != "" and dateCondamnation != "" and statusP != "" and dateSortie != "":
        insertAc = "INSERT INTO accuse (noms,age,genre,nationalite,dateNaissance,photo ) VALUES (%s,%s,%s,%s,%s,%s)"
        valeursAc = (noms, age, genre, nationalite, dateNaissance, photo)
        cursor.execute(insertAc, valeursAc)

        cursor.execute("SELECT idAccuse FROM accuse ORDER BY idAccuse DESC LIMIT 1")
        idAccuse = cursor.fetchone()

        insertP = "INSERT INTO peine (designationP,dateCondamnation,statusP,dateSortie) VALUES (%s,%s,%s,%s)"
        valeursP = (designationP, dateCondamnation, statusP, dateSortie)
        cursor.execute(insertP, valeursP)

        cursor.execute("SELECT idPeine FROM peine ORDER BY idPeine DESC LIMIT 1")
        idPeine = cursor.fetchone()

        insertI = "INSERT INTO infraction (idPeine, designationI, dateI) VALUES (%s,%s,%s)"
        valeursI = (idPeine[0], designationI, dateI)
        cursor.execute(insertI, valeursI)

        insertAd = "INSERT INTO adresse (idAccuse,phone,email,ville,commune,quartier,avenue,cellule,numParcelle," \
                   "longitude,latitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        valeursAd = (
            idAccuse[0], phone, email, ville, commune, quartier, avenue, cellule, numParcelle, longitude, latitude)
        cursor.execute(insertAd, valeursAd)

        cursor.execute("SELECT idInfraction FROM infraction ORDER BY idInfraction DESC LIMIT 1")
        idInfraction = cursor.fetchone()

        insertAcIn = "INSERT INTO accuse_infraction (idAccuse,idInfraction) VALUES (%s,%s)"
        valeursAcIn = (idAccuse[0], idInfraction[0])
        cursor.execute(insertAcIn, valeursAcIn)

        con.commit()
        con.close()

        print("data saved successfully")