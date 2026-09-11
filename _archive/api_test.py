from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY=os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")