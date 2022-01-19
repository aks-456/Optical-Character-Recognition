# Optical-Character-Recognition
An API for Optical Character Recognition (OCR)

## ocr_api
The ocr_api/main.py file is an API which accepts a POST request with an image parameter, then returns the text in that image as a response. The API can be hosted on heroku, but make sure the necessary python libraries are installed. 

## ocr_api_firebase
The ocr_api_firebase/main.py file is for optical character recognition through an API that uses Firebase as a backend. In the backend, certain details such as time, date and the user API key are recorded when a POST request is made. 

Note: It is necessary that along with the POST request, a string is passed as an 'api_key' parameter.

Make sure to add the filepath of your own Firebase Credentials Certificate (where indicated) since that is different for each developer. Then, the API can be hosted on a web server like heroku, but make sure the necessary python libraries are installed. 
