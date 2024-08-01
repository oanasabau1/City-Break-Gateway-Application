from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from marshmallow import Schema, fields, validate, ValidationError
import datetime
from config import db_url

app = Flask('Weather_Service')

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)

api = Api(app)


def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValidationError('Date must be in "YYYY-mm-dd" format.')


class WeatherSchema(Schema):
    city = fields.String(required=True, validate=validate.Length(min=1, max=128))
    date = fields.Date(required=True, format='%Y-%m-%d', validate=validate_date_format)
    temperature = fields.Integer(required=True, validate=validate.Range(min=-20, max=40,
                                                                        error="Temperature must be between -20 and 40 "
                                                                              "degrees Celsius"))
    humidity = fields.Integer(required=True, validate=validate.Range(min=0, max=100,
                                                                     error="Humidity must be between 0 and 100 percent"))
    description = fields.String(validate=validate.Length(max=128))


weather_schema = WeatherSchema()


class Weathers(Resource):
    def get(self):
        city = request.args.get('city')
        date = request.args.get('date')

        if city and date:
            weather = Weather.query.filter_by(city=city, date=date).all()
        elif city:
            weather = Weather.query.filter_by(city=city).all()
        elif date:
            weather = Weather.query.filter_by(date=date).all()
        else:
            return jsonify({'message': 'Please provide city and date'})

        fetched_weather = [w.to_dict() for w in weather]
        if fetched_weather:
            return jsonify({'weather': fetched_weather})
        else:
            return jsonify({'message': 'No weather found match the given criteria'})

    def post(self):
        data = request.json
        try:
            validated_data = weather_schema.load(data)
        except ValidationError as err:
            return err.messages, 400

        new_weather = Weather(
            city=validated_data['city'],
            date=validated_data['date'],
            temperature=validated_data['temperature'],
            humidity=validated_data['humidity'],
            description=validated_data['description'],
        )
        db.session.add(new_weather)
        db.session.commit()
        return 'Weather added successfully!', 200

    def put(self):
        weather_id = request.args.get('id')
        weather = Weather.query.get_or_404(weather_id)
        data = request.json
        try:
            validated_data = weather_schema.load(data)
        except ValidationError as err:
            return err.messages, 400

        weather.city = validated_data['city']
        weather.date = validated_data['date']
        weather.temperature = validated_data['temperature']
        weather.humidity = validated_data['humidity']
        weather.description = validated_data['description']
        db.session.commit()
        return 'Weather updated successfully!', 200

    def delete(self):
        weather_id = request.args.get('id')
        weather = Weather.query.get_or_404(weather_id)
        db.session.delete(weather)
        db.session.commit()
        return 'Weather deleted', 200


api.add_resource(Weathers, '/weather')


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    date = db.Column(db.Date)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    description = db.Column(db.String(128))

    def to_dict(self):
        return {
            'city': self.city,
            'date': self.date.strftime('%Y-%m-%d'),
            'temperature': self.temperature,
            'humidity': self.humidity,
            'description': self.description
        }


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
