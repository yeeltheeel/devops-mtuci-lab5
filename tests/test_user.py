from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

'''Существующие пользователи'''
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'none@mail.com'})
    assert response.status_code == 404

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'name': 'Mark Markovich',
        'email': 'm.m.markovich@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    new_user = {
        'name': 'Fakevan Fakevanov',
        'email': 'i.i.ivanov@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 409

def test_delete_user():
    '''Удаление пользователя'''
    new_user = {
        'name': 'test user',
        'email': 'test@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    response = client.get("/api/v1/user", params={'email': 'test@mail.com'})
    assert response.status_code == 204