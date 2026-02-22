import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope='session')
def base_url():
    return os.getenv('BASE_URL', 'https://petstore.swagger.io/v2')

@pytest.fixture(scope='session')
def session():
    s = requests.Session()
    s.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    })
    return s

@pytest.fixture
def sample_pet():
    return {
        'id': 988877,
        'name': 'TestPetAI',
        'status': 'available',
        'photoUrls': ['https://example.com/photo.jpg'],
        'tags': [{'id': 1, 'name': 'automated-test'}],
        'category': {'id': 1, 'name': 'dogs'},
    }