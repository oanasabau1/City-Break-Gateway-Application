from gateway_service import app


def test_get_1():
    response = app.test_client().get('/')
    assert response.status_code == 400
    assert b'{"message":"Please provide city and date"}\n' in response.data


def test_get_2():
    response = app.test_client().get('/?city=Brasov&date=2024-07-19')
    assert response.status_code == 200
    assert (b'{"events":{"events":[{"address":"Central Park","category":"Festival","city":"Brasov",'
            b'"date":"2024-07-19","description":"A fun summer festival with music, food, and games.","price":25.0,'
            b'"title":"Summer Festival"}]},"weather":{"weather":[{"city":"Brasov","date":"2024-07-19",'
            b'"description":"The sun shines very bright.","humidity":10,"temperature":38}]}}\n') in response.data


def test_get_3():
    response = app.test_client().get('/?city=Cluj-Napoca&date=2024-07-19')
    assert response.status_code == 404  # not found
    assert b'{"message":"No data found for the given city and date"}\n' in response.data



def test_get_4():
    response = app.test_client().get('/?city=Cluj-Napoca&date=a')
    assert response.status_code == 404
    assert b'{"message":"No data found for the given city and date"}\n' in response.data
