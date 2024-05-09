from flask import Flask, request, jsonify
import requests
import weather

from flask_cors import CORS
app = Flask(__name__)
CORS(app)
def calculate_energy(weather_data):
    # Dane z zewnętrznego API
    solar_exposure = weather_data['sunshine_duration']

    # Stałe i parametry
    installation_power = 2.5  # kW
    panel_efficiency = 0.2

    # Obliczenie wygenerowanej energii
    energy_generated = [installation_power * hours_of_sunlight * panel_efficiency for hours_of_sunlight in solar_exposure]
    return energy_generated

@app.route('/weather-forecast', methods=['GET'])
def weather_forecast():
        # Pobranie parametrów od klienta
        lat = request.args.get('latitude')
        lon = request.args.get('longitude')

        # Walidacja danych
        if not lat or not lon:
            return jsonify({'error': 'Brak wymaganych parametrów: szerokość i długość geograficzna.'}), 400

        # Pobranie danych pogodowych z zewnętrznego API
        response = weather.get_weather_data(latitude=lat, longitude=lon)
        weather_data = response

        # Obliczenie energii wyprodukowanej przez instalację fotowoltaiczną
        energy_generated = calculate_energy(weather_data)
        # date_j = [str(s) for s in weather_data['date']]
        # Przygotowanie danych do zwrócenia
        forecast_data = {
            'date': weather_data['date'].tolist(),
            'weather_code': weather_data['weather_code'].tolist(),
            'min_temperature': weather_data['temperature_2m_min'].tolist(),
            'max_temperature': weather_data['temperature_2m_max'].tolist(),
            'energy_generated_kwh': energy_generated
        }

        return jsonify(forecast_data)


if __name__ == '__main__':
    app.run(port=8080)
