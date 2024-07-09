from http import HTTPStatus

from jwt import decode

from fast_zero_new.security import SECRET_KEY, create_access_token


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']  # Testa se o valor de exp foi adicionado ao token


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_not(client, user):
    data = {'username': 'teste@invalido.com'}
    token = create_access_token(data)
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_none(client, user):
    data = {'sub': 'teste@invalido.com'}
    token = create_access_token(data)
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_logon_for_access_token_email_invalid(client, user):
    response = client.post(
        '/token',
        data={'username': 'alguem@teste.com', 'password': 'testeteste'},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token == {'detail': 'Incorrect email or password'}


def test_logon_access_token_password_invalid(client, user):
    response = client.post(
        '/token',
        data={'username': 'teste@teste.com', 'password': 'senhadiferente'},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token == {'detail': 'Incorrect email or password'}
