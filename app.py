import os
from flask import Flask, render_template, request, send_from_directory
from predict import *

app = Flask(__name__) 
app.secret_key = 'mysecretkey'

@app.route('/')    # route to display the welcome page
def index():
    return render_template('home.html')
    

@app.route('/upload', methods=['GET', 'POST'])    # route to accept the image and run the classifier model on it
def upload_image():
    if request.method == 'GET':
        return render_template('upload.html')

    else:
        try:
            img = request.files['image']
            fullname = os.path.join('./static/uploads', img.filename)
            img.save(fullname)

            accuracy, label = predict_result(fullname)

            return render_template('prediction.html', image_file_name = img.filename, label = label, accuracy = accuracy)
        except FileNotFoundError:
            return render_template('upload.html', message='Please upload image first')


@app.route('/upload/<filename>')    # displays the name of the image file uploaded
def send_file(filename):
    return send_from_directory('./static/uploads', filename)


if __name__ == '__main__':
    app.run(debug=True)