from flask import Flask
import requests
import json
from dotenv import load_dotenv
import os
from pathlib import Path

dotenv_path = Path(__file__).resolve().parent.parent / 'config.env'
load_dotenv(dotenv_path=dotenv_path)

print(dotenv_path)

API_URL = os.getenv("API_URL")
TOKEN = os.getenv("TOKEN")

print(f"API_URL: {API_URL}")

app = Flask(__name__)

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)
    

def get_platforms():
    url = f"{API_URL}/platforms"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    return response.json()['platforms']

def get_accounts(platform):
    url = f"{API_URL}/accounts?platform={platform}"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    return response.json()['accounts']

def get_fields(platform):
    url = f"{API_URL}/fields?platform={platform}"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    return response.json()['fields']

def get_insights(platform, account, fields):
    url = f"{API_URL}/insights?platform={platform}&account={account['id']}&token={account['token']}&fields={','.join(fields)}"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    return response.json()['insights']