import requests

BASE_URL = 'http://127.0.0.1:8000'

def get_events():
    response = requests.get(f'{BASE_URL}/event/get_events')
    if response.status_code==200:
        return response.json()
    return []

def get_hour_summary():
    response = requests.get(f'{BASE_URL}/event/last_hour_summary')
    if response.status_code==200:
        return response.json()
    return []

def get_summary():
    response = requests.get(f'{BASE_URL}/summary/summarize')
    if response.status_code==200:
        return response.json()
    return []

