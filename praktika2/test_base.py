import pytest
import requests
import logging
from faker import Faker

logging.basicConfig(filename='loger.log', encoding='utf-8', level=logging.DEBUG)


class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url
        # set headers, authorisation etc

    def _request(self, url, request_type, data=None, expected_error=False):
        stop_flag = False
        while not stop_flag:
            if request_type == 'GET':
                response = requests.get(url)
            elif request_type == 'POST':
                response = requests.post(url, json=data)
            elif request_type == 'PUT':
                response = requests.put(url, json=data)
            else:
                response = requests.delete(url)

            if not expected_error and response.status_code == 200:
                stop_flag = True
            elif expected_error:
                stop_flag = True
        return response

    def get(self, endpoint, endpoint_id, expected_error=True):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'GET', expected_error=expected_error)
        logging.info(f'GET request to {url}')
        logging.info(f'STATUS - {response.status_code}')
        logging.info(f'TEXT - {response.text}')
        logging.info(f'JSON - {response.json()}')
        return response.json()

    def post(self, endpoint, endpoint_id='', body=None):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'POST', data=body, expected_error=True)
        logging.info(f'POST request to {url}')
        logging.info(f'STATUS - {response.status_code}')
        logging.info(f'TEXT - {response.text}')
        logging.info(f'JSON - {response.json()}')
        return response.json()

    def delete(self, endpoint, endpoint_id=''):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        logging.info(f'DELETE request to {url}')
        logging.info(f'STATUS - {response.status_code}')
        logging.info(f'TEXT - {response.text}')
        logging.info(f'JSON - {response.json()}')
        return response.json()

    def put(self, endpoint, endpoint_id, body):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'PUT', data=body)
        logging.info(f'PUT request to {url}')
        logging.info(f'STATUS - {response.status_code}')
        logging.info(f'TEXT - {response.text}')
        logging.info(f'JSON - {response.json()}')
        return response.json()


req = BaseRequest('http://localhost:3000')

a = req.get('posts', '1')


fake = Faker()
#
# for i in range(10):
#     req.post('users', '', {
#         "name": fake.name(),
#         "text": fake.text()
#     })

users_list = req.get('users', '')
print(users_list)


@pytest.mark.parametrize('users', [key for key in users_list])
def test_type(users):
    assert type(users_list) == list


@pytest.mark.parametrize('users', [key for key in users_list])
def test_type2(users):
    print(users)
    assert type(users["name"]) == str


def test_put():
    name = fake.name()
    text = fake.text()
    b = req.put('users', '1', {
        "name": name,
        "text": text,
    })
    assert b["name"] == name
    assert b["text"] == text
