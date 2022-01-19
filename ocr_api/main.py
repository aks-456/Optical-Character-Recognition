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

#Use Pytesseract to return ocr text from image 
def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename) 
    return text


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
        if f and allowed_file(f.filename):
            filepath =  secure_filename(f.filename)
            f.save(filepath)
            return redirect(url_for('ocr', filepath = filepath))  #Directs POST request to ocr function           
        else: 
            #If file extension is not allowed or filename does not match, return an error message.
            return make_response('Either File Does Not Exist, Or The File Extension Is Incorrect. Make Sure To Use PNG Or JPG Files Only.') 
    else:
        #If the request is not a POST request, return an error message
        return make_response("Method not allowed")

@app.route('/ocr/<filepath>/<api_key>')
#reads file and returns text if api key exists
def ocr(filepath):

    return make_response(ocr_core(filepath)) #Return text in image to API request source

    
if __name__ == "__main__":
        app.run(host='127.0.0.1',port=5000,debug=False)
