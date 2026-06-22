from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Curriculo(db.Model):
    __tablename__ = 'curriculo'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    site_url = db.Column(db.String(255), nullable=True)
    experiencia_profissional = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'site_url': self.site_url,
            'experiencia_profissional': self.experiencia_profissional
        }
