from flask import Flask, render_template,request, redirect , session
from cloudant.client import Cloudant
import re
import numpy as np
from tensorflow.keras import models
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.python.ops.gen_array_ops import concat
from tensorflow.keras.applications.inception_v3 import preprocess_input
import requests


import os 
import tensorflow
app=Flask(__name__)

client = Cloudant.iam('e28a1b5f-8c16-40ef-8146-a08d8943bd3d-bluemix','rYoHZX9IgFIuhC8bpt3zxn6zPihT8U4WyHREiPW3BL0Y',connect=True)
myDatabase = client.create_database('myproject')
print(client)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('Register.html')


@app.route('/afterreg', methods=['POST'])
def afterreg():
    x=[x for x in request.form.values()]
    print(x)
    data={'_id':x[1],'name':x[0],'psw':x[2]}
    print(data)
    query={'_id':{'$eq':data['_id']}}
    docs = myDatabase.get_query_result(query)
    print(docs)
    print(len(docs.all()))
    #return "<p> Sucessful Register</p>"
    if len(docs.all())==0:
        url = myDatabase.create_document(data)
        return render_template('Register.html',pred="Register Suecess , Need to login")
    else:
        return render_template('Register.html',pred="You are already member, Need to login")

@app.route('/afterlogin',methods=['POST'])
def afterlogin():
    user = request.form['_id']
    passw = request.form['psw']
    print(user,passw)

    query ={'_id':{'$eq':user}}
    docs=myDatabase.get_query_result(query)
    print(docs)
    print(len(docs.all()))
    print(docs[0])
    print(docs.all())
    print("Query ",query)

    if(len(docs.all())==0):
        return render_template('login.html',pred="User Name is Not Found.")
    else:
        if((user==docs[0][0]['_id'] and passw==docs[0][0]['psw'])):
            return render_template('prediction.html')
        else:
            print("invalid user")

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/result', methods=["GET","POST"])
def res():
    if request.method=="POST":
        f=request.files['image']
        basepath=os.path.dirname(__file__)
        filepath=os.path.join(basepath,'uploads',f.filename)
        f.save(filepath)

@app.route("/prediction", methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':


        file = request.files['fileupload']
        file.save('static/Out/Test.jpg')

        import warnings
        warnings.filterwarnings('ignore')

        import tensorflow as tf
        classifierLoad = tf.keras.models.load_model('body.h5')

        import numpy as np
        from keras.preprocessing import image

        test_image = image.load_img('static/Out/Test.jpg', target_size=(200, 200))
        img1 = cv2.imread('static/Out/Test.jpg')
        # test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = classifierLoad.predict(test_image)

        result1 = ''

        if result[0][0] == 1:

            result1 = "front"


        elif result[0][1] == 1:

            result1 = "rear"

        elif result[0][2] == 1:
            result1 = "side"



        file = request.files['fileupload1']
        file.save('static/Out/Test1.jpg')

        import warnings
        warnings.filterwarnings('ignore')

        import tensorflow as tf
        classifierLoad = tf.keras.models.load_model('level.h5')

        import numpy as np
        from keras.preprocessing import image

        test_image = image.load_img('static/Out/Test1.jpg', target_size=(200, 200))
        img1 = cv2.imread('static/Out/Test1.jpg')
        # test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = classifierLoad.predict(test_image)

        result2 = ''

        if result[0][0] == 1:

            result2 = "minor"


        elif result[0][1] == 1:

            result2 = "moderate"

        elif result[0][2] == 1:
            result2 = "severe"



        if (result1 == "front" and result2 == "minor"):
            value = "3000 - 5000 INR"
        elif (result1 == "front" and result2 == "moderate"):
            value = "6000 8000 INR"
        elif (result1 == "front" and result2 == "severe"):
            value = "9000 11000 INR"

        elif (result1 == "rear" and result2 == "minor"):
            value = "4000 - 6000 INR"

        elif (result1 == "rear" and result2 == "moderate"):
            value = "7000 9000 INR"

        elif (result1 == "rear" and result2 == "severe"):
            value = "11000 - 13000 INR"

        elif (result1 == "side" and result2 == "minor"):
            value = "6000 - 8000 INR"

        elif (result1 == "side" and result2 == "moderate"):
            value = "9000 - 11000 INR"

        elif (result1 == "side" and result2 == "severe"):
            value = "12000 - 15000 INR"

        else:
            value = "16000 - 50000 INR"


        return render_template('userhome.html', prediction=value)



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)