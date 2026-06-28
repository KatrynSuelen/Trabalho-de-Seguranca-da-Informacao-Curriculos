from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, Regexp
import html

class CurriculoForm(FlaskForm):
    nome = StringField('Nome Completo', validators=[
        DataRequired(message="O nome é obrigatório."),
        Length(min=2, max=255, message="O nome deve ter entre 2 e 255 caracteres.")
    ])
    
    telefone = StringField('Telefone', validators=[
        Optional(),
        Length(max=15, message="O telefone deve ter no máximo 15 caracteres."),
        Regexp(r'^\+?[\d\s\-()]{8,15}$', message="Telefone inválido. Ex: (11) 99999-9999")
    ])
    
    email = StringField('Endereço de E-mail', validators=[
        DataRequired(message="O e-mail é obrigatório."),
        Email(message="Endereço de e-mail inválido."),
        Length(max=255, message="O e-mail deve ter no máximo 255 caracteres.")
    ])
    
    site_url = StringField('Endereço WEB (Website)', validators=[
        Optional(),
        URL(require_tld=True, message="URL inválida. Deve iniciar com http:// ou https://"),
        Length(max=255, message="O endereço web deve ter no máximo 255 caracteres.")
    ])
    
    experiencia_profissional = TextAreaField('Experiência Profissional', validators=[
        DataRequired(message="A experiência profissional é obrigatória."),
        Length(min=10, message="Por favor, detalhe mais a sua experiência (mínimo 10 caracteres).")
    ])

    def sanitize_data(self):
        """
        Sanitizes all form data to prevent XSS attacks.
        Escapes HTML characters in text fields before database insertion.
        """
        self.nome.data = html.escape(self.nome.data.strip())
        if self.telefone.data:
            self.telefone.data = html.escape(self.telefone.data.strip())
        self.email.data = html.escape(self.email.data.strip().lower())
        if self.site_url.data:
            self.site_url.data = html.escape(self.site_url.data.strip())
        self.experiencia_profissional.data = html.escape(self.experiencia_profissional.data.strip())
