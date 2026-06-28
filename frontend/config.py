import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-csrf-protection-987654321'
    BACKEND_URL = os.environ.get('BACKEND_URL') or 'http://localhost:3000'

