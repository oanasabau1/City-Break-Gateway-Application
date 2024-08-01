from flask import Flask, request, jsonify
import requests

app = Flask('Gateway_Service')

EVENTS_SERVICE_URL = 'http://localhost:5001/events'
WEATHER_SERVICE_URL = 'http://localhost:5002/weather'


@app.route('/', methods=['GET'])
def get_data():
    city = request.args.get('city')
    date = request.args.get('date')

    if not city or not date:
        return jsonify({'message': 'Please provide city and date'}), 400

    events_response = requests.get(EVENTS_SERVICE_URL, params={'city': city, 'date': date})
    weather_response = requests.get(WEATHER_SERVICE_URL, params={'city': city, 'date': date})

    aggregated_data = {}

    if events_response.status_code == 200:
        events_data = events_response.json()
        aggregated_data['events'] = events_data
    else:
        aggregated_data['events'] = {'message': 'No events found matching the given criteria'}

    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        aggregated_data['weather'] = weather_data
    else:
        aggregated_data['weather'] = {'message': 'No weather found matching the given criteria'}

    if not aggregated_data.get('events').get('events') and not aggregated_data.get('weather').get('weather'):
        return jsonify({'message': 'No data found for the given city and date'}), 404

    return jsonify(aggregated_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
