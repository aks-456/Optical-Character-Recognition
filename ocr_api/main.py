try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import numpy as np
import os
from flask import Flask, request, redirect, url_for, make_response
from werkzeug import secure_filename
import cv2
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore



def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename) 
    return text

cred = credentials.Certificate("_______") #Enter Firebase Credentials Certificate
firebase_admin.initialize_app(cred)

db = firestore.client()  # this connects to our Firestore database

collection = db.collection('api_keys')  # opens 'places' collection

ALLOWED_EXTENSIONS = {'png', 'jpg'} #Specifies file types allowed

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        f = request.files['filename']
        api_key = request.form['api_key']
        if f and allowed_file(f.filename):
            filepath =  secure_filename(f.filename)
            f.save(filepath)
            return redirect(url_for('ocr', filepath = filepath, api_key = api_key))            
        else:
            return make_response('Either File Does Not Exist, Or The File Extension Is Incorrect. Make Sure To Use PNG Or JPG Files Only.')
    else:
        return make_response("Something went wrong. Please Try Again")

# get the data for the requested query
@app.route('/ocr/<filepath>/<api_key>')
#Flask route function
def ocr(filepath, api_key):
    img = cv2.imread(filepath)
    api_key = api_key
    detector = cv2.QRCodeDetector()

    doc = collection.document(api_key)
    try:
        res = doc.get()
    except:
        pass

    # Check if API Key Exists
    if(res.exists):
        #Log use of API
        user_collection = db.collection('uses_ocr')
        dateTimeObj = datetime.now()
        use_case = user_collection.document(api_key + " " + str(dateTimeObj)).set({
            "api_key": api_key,
            "time_key": str(dateTimeObj),
            "date": str(dateTimeObj.year) + '/' + str(dateTimeObj.month) + '/' + str(dateTimeObj.day),
            "api": "OCR"
        })
        return make_response(ocr_core(filepath))

    else:
        make_response("API Key does not exist.")
    
#Only when testing the production server
if __name__ == "__main__":
        app.run(host='127.0.0.1',port=5000,debug=False)
