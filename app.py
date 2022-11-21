from flask import Flask,request
from flask_cors import CORS,cross_origin
from MailSend import Send
from AgeDetection_with_Image import FinalPrediction
from werkzeug.utils import secure_filename
import os
import base64

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/mail",methods = ['POST', 'GET'])
@cross_origin()
def mailing():
    res=""
    message=""
    if request.method == 'POST':
        try:
            subject = request.form['subject']
            body = request.form['body']
            to = request.form['to']
            res,message=Send(body=body,subject=subject,email_receiver=to)
        except:
            res=True
            message="missing data"


    else:
        res=True
        message="invalid request"
        
    response={ "message":message,"response":res}
    return response,200


@app.route("/age",methods = ['POST', 'GET'])
def age_detection():

    if request.method == 'POST':
        try:
            image = request.form['image']
            # image = request.files['image']
            fileName="some.jpg"
            image=base64.b64decode(str(image))
            handler = open(fileName, "wb+")
            handler.write(image)
            handler.close()
            # fileName=secure_filename(image.filename)
            # image.save(fileName)app.py
            res=FinalPrediction(image=fileName)
            os.remove(fileName)
            if res[2]==-1:
                response={ "response":res[0],"message":res[1]}
            else:
                response={ "response":res[0],"message":res[1],"age":res[2]}
        except:
            res=True
            message="missing data"
            response={ "response":res,"message":message}
        return response,200

    else:
        res=True
        message="invalid request"
        response={ "message":message,"response":res}
        return response,200



if __name__ == "__main__":
    app.run(debug=True)


