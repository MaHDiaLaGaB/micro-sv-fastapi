from fastapi.testclient import TestClient
from app.main import app, BASE_DIR
import shutil
import time


client = TestClient(app)


def test_get_root():
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']


def test_post_root():
    response = client.post('/')
    assert response.status_code == 200
    assert 'application/json' in response.headers['content-type']


def test_image_echo():
    img_path = BASE_DIR / "images"
    for path in img_path.glob("*"):
        response = client.post('/img-echo/', files={"file": open(path, 'rb')})
        assert response.status_code == 200
        print(path.suffix)
        print(response.headers['content-type'])
        file_type = str(path.suffix).replace('.', '')
        assert file_type in response.headers['content-type']

