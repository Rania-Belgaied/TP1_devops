from unittest.mock import patch
from app import app


def test_home_page():
    with patch("app.redis_client.incr", return_value=1):
        # Crée un petit client permettant de simuler un navigateur.
        client = app.test_client() 

        # Simule "GET http://localhost:5000/"
        response = client.get("/")

        # vérifie que Flask a répondu correctement.
        assert response.status_code == 200

        # vérifie que la réponse contient bien le compteur.
        assert b"1 fois" in response.data

