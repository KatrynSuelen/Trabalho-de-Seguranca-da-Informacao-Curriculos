import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-csrf-protection-987654321'
    
    # Connection details for MySQL as requested:
    # Port: 3306
    # Senha: katryn
    # NomeDB: sistema_curriculos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:katryn@localhost:3306/sistema_curriculos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

