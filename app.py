from flask import Flask, request, render_template
import requests

app = Flask(__name__)
key = '938f3cb89e3aaf8567775472b7140cd3'

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    weather = None
    temp = None
    city = None
    background_image = None

    if request.method == 'POST':
        city = request.form['city']
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={key}")

        if weather_data.status_code == 404 or weather_data.json()['cod'] == '404':
            error = "No City Found"
        else:
            weather_json = weather_data.json()
            weather = weather_json['weather'][0]['main']
            temp = round(weather_json['main']['temp'])
            
            # Map weather condition to a background image
            if weather.lower() in ['clear', 'sunny']:
                background_image = 'sunny.jpg'
            elif weather.lower() in ['clouds', 'cloudy']:
                background_image = 'cloudy.jpg'
            elif weather.lower() in ['rain', 'drizzle']:
                background_image = 'rainy.jpg'
            elif weather.lower() in ['snow']:
                background_image = 'snowy.jpg'
            elif weather.lower() in ['thunderstorm']:
                background_image = 'thunderstorm.jpg'
            else:
                background_image = 'default.jpg'  # Fallback image for other conditions

    return render_template('index.html', weather=weather, temp=temp, city=city, error=error, background_image=background_image)

if __name__ == '__main__':
    app.run(debug=True)
