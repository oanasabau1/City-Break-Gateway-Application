from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from marshmallow import Schema, fields, validate, ValidationError
import datetime
from config import db_url

app = Flask('Events_Service')

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)

api = Api(app)


def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, '%YYYY-%mm-%dd')
    except ValueError:
        raise ValidationError('Date must be in "YYYY-mm-dd" format.')


class EventSchema(Schema):
    city = fields.String(required=True, validate=validate.Length(min=1, max=128))
    date = fields.Date(required=True, format='%Y-%m-%d', validate=validate_date_format)
    title = fields.String(required=True, validate=validate.Length(min=1, max=128))
    description = fields.String(required=True, validate=validate.Length(min=1, max=128))
    address = fields.String(validate=validate.Length(max=128))
    category = fields.String(validate=validate.Length(max=128))
    price = fields.Float()


event_schema = EventSchema()


class Events(Resource):
    def get(self):
        city = request.args.get('city')
        date = request.args.get('date')

        if city and date:
            event = Event.query.filter_by(city=city, date=date).all()
        elif city:
            event = Event.query.filter_by(city=city).all()
        elif date:
            event = Event.query.filter_by(date=date).all()
        else:
            return jsonify({'message': 'Please provide city and date'})

        fetched_events = [e.to_dict() for e in event]
        if fetched_events:
            return jsonify({'events': fetched_events})
        else:
            return jsonify({'message': 'No events found match the given criteria'})

    def post(self):
        data = request.json
        try:
            validated_data = event_schema.load(data)
        except ValidationError as err:
            return err.messages, 400

        new_event = Event(
            city=validated_data['city'],
            date=validated_data['date'],
            title=validated_data['title'],
            description=validated_data['description'],
            address=validated_data.get('address'),
            category=validated_data.get('category'),
            price=validated_data.get('price')
        )
        db.session.add(new_event)
        db.session.commit()
        return 'Event added', 200

    def put(self):
        event_id = request.args.get('id')
        event = Event.query.get_or_404(event_id)
        data = request.json
        try:
            validated_data = event_schema.load(data)
        except ValidationError as err:
            return err.messages, 400

        event.city = validated_data['city']
        event.date = validated_data['date']
        event.title = validated_data['title']
        event.description = validated_data['description']
        event.address = validated_data.get('address')
        event.category = validated_data.get('category')
        event.price = validated_data.get('price')
        db.session.commit()
        return 'Event updated successfully!', 200

    def delete(self):
        event_id = request.args.get('id')
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return 'Event deleted successfully!', 200


api.add_resource(Events, '/events')


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    date = db.Column(db.Date)
    title = db.Column(db.String(128))
    description = db.Column(db.String(128))
    address = db.Column(db.String(128))
    category = db.Column(db.String(128))
    price = db.Column(db.Float)

    def to_dict(self):
        return {
            'city': self.city,
            'date': self.date.strftime('%Y-%m-%d'),
            'title': self.title,
            'description': self.description,
            'address': self.address,
            'category': self.category,
            'price': self.price
        }


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
