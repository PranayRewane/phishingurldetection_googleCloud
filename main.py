import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
import pickle
import detect_features


app = Flask(__name__)
model = pickle.load(open('decisiontree_pickle_model','rb'))


@app.route('/')
def home():
    #return 'Hello World'
    return render_template('home.html')
    #return render_template('index.html')

@app.route('/predict',methods = ['POST'])
def predict():
    url = request.form['url']
    res=detect_features.generate_data_set(url)
    res = np.array(res).reshape(1,-1)
    pred= model.predict(res)
    
    isphishing=pred[0]
    if isphishing==1:
        prediction="not a phishing site"
    else:
        prediction="a phishing site"
    
    print("/\/\/\/\/\/my prediction ------>",prediction)

    #output = round(prediction[0], 2)
    return render_template('home.html', prediction_text=prediction)

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)



if __name__ == '__main__':
    app.run(debug=True)
# © 2021 GitHub, Inc.