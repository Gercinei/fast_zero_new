from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero_new.app import app

client = TestClient(app)


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # Arrange (organização)

    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # assert (afirmar)
    assert response.json() == {'message': 'Olá Mundo!!'}
