# City Break Website

This is a Flask-based application designed to serve as a city break planning tool. It allows users to discover city events and check weather information seamlessly. 

Some of the technologies used are Flask, Flask-SQLAlchemy (for database interactions and ORM), Marshmallow (for data serialization and validation),
Requests (for making HTTP requests to the events and weather services from the gateway service), pytest (for unit testing to ensure the reliability and correctness of the services). It only features the backend part, the endpoints were tested via Postman and by using cURL commands.

To ensure the reliability and correctness of the web application, unit testing is implemented using pytest, that is a powerful testing framework for Python that makes it easy to write simple and scalable test cases.

The application is comprised of three main components:

### Events Service
Allows users to search and manage city events. Supports:

- **GET /events?city=CityName&date=YYYY-MM-DD**: List events by city and date. If you want, you can list events by only one of these parameters. 
- **POST /events**: Add a new event.
- **PUT /events?id=EventID**: Modify an existing event.
- **DELETE /events?id=EventID**: Delete an event.

### Weather Service
Provides weather information for cities. Supports:

- **GET /weather?city=CityName&date=YYYY-MM-DD**: Get weather for a city and date. If you want, you can list weather by only one of these parameters.
- **POST /weather**: Add new weather data.
- **PUT /weather?id=WeatherID**: Modify existing weather data.
- **DELETE /weather?id=WeatherID**: Delete weather data.

### Gateway Service
A centralized gateway that aggregates data from the Events and Weather services. It simplifies the interaction for users by exposing:

- **GET /city_info?city=CityName&date=YYYY-MM-DD**: Fetches both events and weather for the specified city and date. Returns available data even if one service has no matching entries.

### Getting started

In order to run the city break web application, you need to ensure that you have Docker and then create a docker container by running the following command that will create our database:

- docker run --name CitybreakDB -e MYSQL_ROOT_PASSWORD=myrootpw -e MYSQL_USER=myuser -e MYSQL_PASSWORD=mypassword -e MYSQL_DATABASE=citybreak -p 3306:3306 -d mysql

Because the app uses different packages written in requirements.txt file, you have to run the following command to install them:

- pip install -r requirements.txt

This architecture ensures that each service operates independently. Therefore, those services can be runned as such. The Gateway Service plays a crucial role in the application by acting as a centralized access point for users to retrieve integrated information about city events and weather. It simplifies interactions for users by aggregating data from the standalone Events and Weather services. The endpoint is:
   - GET /city_info?city=CityName&date=YYYY-MM-DD, that fetches both events and weather for the specified city and date and returns available data even if one service has no matching entries.

