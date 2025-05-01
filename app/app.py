
# Importing essential libraries and modules

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
import numpy as np
import pandas as pd
from utils.disease import disease_dic
from utils.fertilizer import fertilizer_dic
import requests
import config
import pickle
import io
import torch
from torchvision import transforms
from PIL import Image
from markupsafe import Markup

import re
import pdfplumber
import pytesseract
import os
from utils.model import ResNet9
import warnings
warnings.simplefilter("ignore", category=FutureWarning)

# email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import Celery



# ==============================================================================================

# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------

# Loading plant disease classification model

disease_classes = ['Apple___Apple_scab',
                   'Apple___Black_rot',
                   'Apple___Cedar_apple_rust',
                   'Apple___healthy',
                   'Blueberry___healthy',
                   'Cherry_(including_sour)___Powdery_mildew',
                   'Cherry_(including_sour)___healthy',
                   'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                   'Corn_(maize)___Common_rust_',
                   'Corn_(maize)___Northern_Leaf_Blight',
                   'Corn_(maize)___healthy',
                   'Grape___Black_rot',
                   'Grape___Esca_(Black_Measles)',
                   'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                   'Grape___healthy',
                   'Orange___Haunglongbing_(Citrus_greening)',
                   'Peach___Bacterial_spot',
                   'Peach___healthy',
                   'Pepper,_bell___Bacterial_spot',
                   'Pepper,_bell___healthy',
                   'Potato___Early_blight',
                   'Potato___Late_blight',
                   'Potato___healthy',
                   'Raspberry___healthy',
                   'Soybean___healthy',
                   'Squash___Powdery_mildew',
                   'Strawberry___Leaf_scorch',
                   'Strawberry___healthy',
                   'Tomato___Bacterial_spot',
                   'Tomato___Early_blight',
                   'Tomato___Late_blight',
                   'Tomato___Leaf_Mold',
                   'Tomato___Septoria_leaf_spot',
                   'Tomato___Spider_mites Two-spotted_spider_mite',
                   'Tomato___Target_Spot',
                   'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                   'Tomato___Tomato_mosaic_virus',
                   'Tomato___healthy']

disease_model_path = 'models/plant_disease_model.pth'
disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(
    disease_model_path, map_location=torch.device('cpu')))
disease_model.eval()


# Loading crop recommendation model

crop_recommendation_model_path = 'models/RandomForest.pkl'
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))


# =========================================================================================

# fetching temperature and humidity using city with the help of weather api

def weather_fetch(city_name):
    # Step 1: Get lat and lon using Geocoding API
    GEOCODING_API_URL = "http://api.openweathermap.org/geo/1.0/direct?"
    

    API_KEY1 = config.API_KEY1
    
    # Fetch coordinates
    geo_params = {
        "q": city_name,
        "limit": 1,
        "appid": API_KEY1
    }
    geo_response = requests.get(GEOCODING_API_URL, params=geo_params).json()
    
    print("geo_res: ", geo_response)
    if not geo_response:
        return None  # City not found
    
    lat = geo_response[0]["lat"]
    lon = geo_response[0]["lon"]

    print("Lat: ", lat)
    print("Lon: ", lon)
    
    # Step 2: Fetch weather using Current Weather API
    
    API_KEY2 = config.API_KEY2
    base_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY2}&units=metric"
    
    response = requests.get(base_url)
    weather_data = response.json()  # Parse JSON response
    
    print("Weather Data: ", weather_data)
    
    if weather_data.get("cod") == 200:  # Check if request was successful
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        return temperature, humidity
    else:
        return None



def predict_image(img, model=disease_model):
    """
    Transforms image to tensor and predicts disease label
    :params: image
    :return: prediction (string)
    """
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img))
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0)

    # Get predictions from model
    yb = model(img_u)
    # Pick index with highest probability
    _, preds = torch.max(yb, dim=1)
    prediction = disease_classes[preds[0].item()]
    # Retrieve the class label
    return prediction

# ===============================================================================================
# ------------------------------------ FLASK APP -------------------------------------------------


app = Flask(__name__)

# render home page


@ app.route('/')
def home():
    title = 'Crop Care - Home'
    return render_template('index.html', title=title)

# render crop recommendation form page


@ app.route('/crop-recommend')
def crop_recommend():
    title = 'Crop Care - Crop Recommendation'
    return render_template('crop.html', title=title)

# render fertilizer recommendation form page


@ app.route('/fertilizer')
def fertilizer_recommendation():
    title = 'Crop Care - Fertilizer Suggestion'

    return render_template('fertilizer.html', title=title)

# render disease prediction input page



# render weather broadcast from page
@ app.route('/weather')
def weather_broadcast():
    title = 'Weather Forecast'
    return render_template('weather_index.html', title=title)


#  explore more 
@ app.route('/explore')
def explore():
    title = 'Explore about crops'
    return render_template('explore.html', title=title)


# Smart farming guide

@ app.route('/guide')
def guide():
    title = 'Smart Farming Guide'
    return render_template('guide.html', title=title)




# ===============================================================================================

# RENDER PREDICTION PAGES

# render crop recommendation result page


@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'Crop Care - Crop Recommendation'

    if request.method == 'POST':
        try:
            N = int(request.form['nitrogen'])
            P = int(request.form['phosphorous'])
            K = int(request.form['pottasium'])
            ph = float(request.form['ph'])
            rainfall = float(request.form['rainfall'])
            city = request.form.get("city")
            # city="London"
            
            print("city : "+city)
           
            weather_data = weather_fetch(city)
            print("weather: data: ",weather_data)
            if weather_data is None:
                return render_template('try_again.html', retry_url=url_for('crop_recommend'), title=title)

            temperature, humidity = weather_data
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]

            return render_template('crop-result.html', prediction=final_prediction, title=title)

        except (ValueError, KeyError):
            return render_template('try_again.html', retry_url=url_for('crop_recommend'), title=title)

@ app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    title = 'Crop Care - Fertilizer Suggestion'

    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorus'])
    K = int(request.form['potassium'])
    # ph = float(request.form['ph'])

    df = pd.read_csv('Data/fertilizer.csv')

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K
    temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
    max_value = temp[max(temp.keys())]
    if max_value == "N":
        if n < 0:
            key = 'NHigh'
        else:
            key = "Nlow"
    elif max_value == "P":
        if p < 0:
            key = 'PHigh'
        else:
            key = "Plow"
    else:
        if k < 0:
            key = 'KHigh'
        else:
            key = "Klow"

    response = Markup(str(fertilizer_dic[key]))

    return render_template('fertilizer-result.html', recommendation=response, title=title)

# render disease prediction result page


@ app.route('/disease-predict', methods=['GET', 'POST'])
def disease_prediction():
    title = 'Crop Care - Disease Detection'

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return render_template('disease.html', retry_url=url_for('disease_prediction'),title=title)
        try:
            img = file.read()

            prediction = predict_image(img)

            prediction = Markup(str(disease_dic[prediction]))
            return render_template('disease-result.html', prediction=prediction, title=title)
        except:
            pass
    return render_template('disease.html', title=title)



# upload file 


UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_text_from_pdf(pdf_path):
    report_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                report_text += page.extract_text()
    except Exception as e:
        print(f"Error while reading PDF: {e}")
    return report_text


def extract_npk(report):
    npk_values = {}
    try:
        # Extract phosphorus (P2O5)
        # Updated pattern to match the exact format from the image
        phosphorus_pattern = r"Available\s+Phosphorus\s+as\s+P2O5\s*\d*\s*Kg/acre\s*(?:Methods Manual - Soil Testing In India[\s\S]*?|IS\d+[\s\S]*?)\s*(\d+\.?\d*)"
        phosphorus_match = re.search(phosphorus_pattern, report, re.IGNORECASE)
        
        if not phosphorus_match:
            # Fallback pattern that's more lenient
            phosphorus_match = re.search(
                r"(?:4|Sr\. No\.\s*4).*?Available\s+Phosphorus\s+as\s+P2O5.*?(\d+\.?\d*)",
                report,
                re.IGNORECASE | re.DOTALL
            )
        npk_values['Phosphorus (P2O5)'] = float(phosphorus_match.group(1)) if phosphorus_match else None

        # Extract potassium (K2O)
        # Updated pattern to match the exact format from the image
        potassium_pattern = r"Available\s+Potassium\s+as\s+K2O\s*\d*\s*Kg/acre\s*(?:Methods Manual - Soil Testing In India[\s\S]*?|IS\d+[\s\S]*?)\s*(\d+\.?\d*)"
        potassium_match = re.search(potassium_pattern, report, re.IGNORECASE)
        
        if not potassium_match:
            # Fallback pattern that's more lenient
            potassium_match = re.search(
                r"(?:5|Sr\. No\.\s*5).*?Available\s+Potassium\s+as\s+K2O.*?(\d+\.?\d*)",
                report,
                re.IGNORECASE | re.DOTALL
            )
        npk_values['Potassium (K2O)'] = float(potassium_match.group(1)) if potassium_match else None

        # Extract Organic Carbon and calculate Nitrogen
        # Updated pattern to match the exact format from the image
        organic_carbon_pattern = r"Organic\s+Carbon\s*\(%\)\s*%\s*(?:Methods Manual - Soil Testing In India[\s\S]*?|IS\d+[\s\S]*?)\s*(\d+\.?\d*)"
        organic_carbon_match = re.search(organic_carbon_pattern, report, re.IGNORECASE)
        
        if not organic_carbon_match:
            # Fallback pattern that's more lenient
            organic_carbon_match = re.search(
                r"(?:3|Sr\. No\.\s*3).*?Organic\s+Carbon.*?(\d+\.?\d*)",
                report,
                re.IGNORECASE | re.DOTALL
            )
        
        if organic_carbon_match:
            organic_carbon = float(organic_carbon_match.group(1))
            # Using the standard conversion factor for nitrogen calculation
            npk_values['Nitrogen (N)'] = organic_carbon * 100
        else:
            npk_values['Nitrogen (N)'] = None

        # Add debug information
        npk_values['debug'] = {
            'extracted_text': report,
            'phosphorus_match': bool(phosphorus_match),
            'potassium_match': bool(potassium_match),
            'organic_carbon_match': bool(organic_carbon_match)
        }

    except Exception as e:
        print(f"Error while extracting NPK values: {e}")
        npk_values['error'] = str(e)

    return npk_values


@ app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading."})

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    if file.filename.lower().endswith('.pdf'):
        report_text = extract_text_from_pdf(file_path)
    else:
        return jsonify({"error": "Only PDF files are supported."})

    npk_values = extract_npk(report_text)
    
    # Clean up the uploaded file
    os.remove(file_path)
    
    return jsonify(npk_values)



# Contact Us Section

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'suprithry37@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'vyoo uukc bkin okyz')


@ app.route('/send_email', methods=['POST'])
def send_email():
    
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        if not name or not email or not phone or not message:
            return jsonify({'status': 'error', 'message': 'All fields are required!'})

        if '@' not in email:
            return jsonify({'status': 'error', 'message': 'Invalid email format!'})

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f"Contact Us Form: {name}"

        body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        print("Msg : "+body)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({'status': 'success', 'message': 'Your message has been sent successfully!'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to send the email. Please try again later.'})



# ===============================================================================================
if __name__ == '__main__':
    app.run(debug=True)