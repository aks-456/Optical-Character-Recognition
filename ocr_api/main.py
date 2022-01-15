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

#Use Pytesseract to return ocr text from image 
def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename) 
    return text


#Firebase info
cred = credentials.Certificate("_______") #Enter Firebase Credentials Certificate
firebase_admin.initialize_app(cred)
db = firestore.client()  # this connects to our Firestore database
collection = db.collection('api_keys')  # opens 'api_keys' collection
ALLOWED_EXTENSIONS = {'png', 'jpg'} #Specifies file types allowed



#Checks if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS #split filename  by period and check if file extension exists in ALLOWED_EXTENSIONS

app = Flask(__name__)
@app.route('/', methods=['POST'])
#Directs POST request
def home():
    if request.method == 'POST': #Check for POST requests
        f = request.files['filename'] #get file from POST request
        api_key = request.form['api_key'] #get api_key from POST request
        if f and allowed_file(f.filename):
            filepath =  secure_filename(f.filename)
            f.save(filepath)
            return redirect(url_for('ocr', filepath = filepath, api_key = api_key))  #Directs POST request to ocr function           
        else: 
            #If file extension is not allowed or filename does not match, return an error message.
            return make_response('Either File Does Not Exist, Or The File Extension Is Incorrect. Make Sure To Use PNG Or JPG Files Only.') 
    else:
        #If the request is not a POST request, return an error message
        return make_response("Method not allowed")

@app.route('/ocr/<filepath>/<api_key>')
#reads file and returns text if api key exists
def ocr(filepath, api_key):
    doc = collection.document(api_key) #Store firebase collection which contains api_key
    try:
        res = doc.get() #Get firebase collection
    except:
        pass

    # Check if API Key Exists
    if(res.exists):
        #Log use of API
        user_collection = db.collection('uses_ocr') #Store firebase 'uses_ocr' collection
        dateTimeObj = datetime.now() #Get current date and time
        use_case = user_collection.document(api_key + " " + str(dateTimeObj)).set({ #Create new row in 'uses_ocr' collection
            "api_key": api_key, #Store API key which used the API
            "time_key": str(dateTimeObj), #
            "date": str(dateTimeObj.year) + '/' + str(dateTimeObj.month) + '/' + str(dateTimeObj.day), #Store date that API was used
            "api": "OCR" #Store which API was being used (if you have multiple)
        })
        return make_response(ocr_core(filepath)) #Return text in image to API request

    else: #If API key does not exist, return an error
        make_response("API Key does not exist.") 
    
if __name__ == "__main__":
        app.run(host='127.0.0.1',port=5000,debug=False)
