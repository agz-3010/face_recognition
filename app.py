import face_recognition
import cv2
import numpy as np
from flask import Flask
from flask import render_template, redirect
from flask import Response
from numpy.lib.function_base import insert
from flask import request, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
from requetes import takePicture, enroler
from camera import VideoCamera
from io import BytesIO
from PIL import Image

# from imutils.video import VideoStream
# import imutils
# import time
app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

path = './images'

app.secret_key = "Cairocoders-Ednalan"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'facerecog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/users/', methods=["GET", "POST"])
def register():
    return render_template("users.html")


@app.route("/index/")
def index():
    return render_template("index.html")


@app.route("/enrollment/")
def enrollment():
    return render_template("enrollment.html")


@app.route("/insertAcc", methods=['POST', 'GET'])
def enregistrer():
    if request.method == "POST":
        noms = request.form['noms']
        nationalite = request.form['nationalite']
        dateNaissance = request.form['dateNaissance']
        age = request.form['age']
        genre = request.form['genre']
        email = request.form['email']
        phone = request.form['phone']
        ville = request.form['ville']
        commune = request.form['commune']
        quartier = request.form['quartier']
        avenue = request.form['avenue']
        cellule = request.form['cellule']
        numParcelle = request.form['numParcelle']
        longitude = request.form['longitude']
        latitude = request.form['latitude']
        designationI = request.form['designationI']
        dateI = request.form['dateI']
        designationP = request.form['designationP']
        dateCondamnation = request.form['dateCondamnation']
        dateSortie = request.form['dateSortie']
        statusP = request.form['statusP']

        print(noms)
        if request.form['submit'] == 'save':
            photo = takePicture(noms)
            enroler(noms, nationalite, age, genre, photo, phone, email, dateNaissance, ville, commune, quartier, avenue,
                    cellule, numParcelle, longitude, latitude, designationI, dateI, designationP, dateCondamnation,
                    statusP, dateSortie)

            return redirect(url_for('enrollment'))


@app.route("/tables/")
def tables():
    return render_template("tables.html")


@app.route("/recognation/")
def recognation():
    return render_template("recognation.html")


# @app.route("/video")
# def video():
#     return Response(generateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(camer):
    while True:
        frame = camer.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/recognizing')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
