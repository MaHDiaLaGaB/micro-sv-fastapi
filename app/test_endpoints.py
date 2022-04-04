from fastapi.testclient import TestClient
from app.main import app, BASE_DIR, PHOTO_DIR
from PIL import Image
import shutil
import time
import io


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
    for path in img_path.glob("*.jpg"):
        try:
            image = Image.open(path)
        except:
            image = None
        response = client.post('/img-echo/', files={"file": open(path, 'rb')})
        if image is not None:
            assert response.status_code == 200

        else:
            assert response.status_code == 400

    time.sleep(3)
    shutil.rmtree(PHOTO_DIR)
