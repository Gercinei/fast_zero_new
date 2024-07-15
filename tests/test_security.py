from http import HTTPStatus

from jwt import decode

from fast_zero_new.security import create_access_token, settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert decoded['exp']  # Testa se o valor de exp foi adicionado ao token


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_not(client):
    data = {'password': 'testeteste'}
    token_sem_sub = create_access_token(data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token_sem_sub}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_decoderro(client):
    data = {'username': '@@@@'}
    token = create_access_token(data)
    token_invalid = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token_invalid}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_is_none(client, user):
    data = {'sub': 'alguem@email.com', 'password': 'segredo'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
