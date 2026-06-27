import urllib.parse
from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from config import Config
from models import db, Curriculo
from forms import CurriculoForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)

# Enable CSRF Protection globally
csrf = CSRFProtect(app)

# Initialize SQLAlchemy
db.init_app(app)

# Security Headers to prevent Cross-site History Manipulation (CSHM), Clickjacking, XSS, etc.
@app.after_request
def apply_security_headers(response):
    # CSHM prevention: Ensure browser doesn't cache dynamic pages, preventing back/forward cache manipulation of sensitive content
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    # XSS Protection & Clickjacking prevention
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Content Security Policy (CSP) to restrict scripts/styles and prevent XSS execution
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "script-src 'self' 'unsafe-inline';"
    )
    return response

# View 1: List Resumes (Apresenta o nome e o endereço de e-mail)
@app.route('/')
def list_curriculos():
    # Parameterized query handled safely by ORM
    curriculos = Curriculo.query.order_by(Curriculo.nome.asc()).all()
    return render_template('list.html', curriculos=curriculos)

# View 2: Create Resume (Cadastro de um novo registro)
@app.route('/cadastro', methods=['GET', 'POST'])
def create_curriculo():
    form = CurriculoForm()
    if form.validate_on_submit():
        # Sanitize data to prevent stored XSS (in addition to ORM preventing SQL Injection)
        form.sanitize_data()
        
        # Instantiate model with validated and sanitized data
        novo_curriculo = Curriculo(
            nome=form.nome.data,
            telefone=form.telefone.data,
            email=form.email.data,
            site_url=form.site_url.data,
            experiencia_profissional=form.experiencia_profissional.data.strip()
        )
        
        try:
            db.session.add(novo_curriculo)
            db.session.commit()
            flash('Currículo cadastrado com sucesso!', 'success')
            # POST-Redirect-GET Pattern: prevents history resubmission (part of CSHM protection)
            return redirect(url_for('list_curriculos'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao salvar no banco de dados. Tente novamente.', 'danger')
            app.logger.error(f"Erro ao salvar: {e}")
            
    return render_template('create.html', form=form)

# View 3: View Resume Details (Apresenta todas as informações da pessoa escolhida pela tela 1)
@app.route('/consulta/<int:id>')
def view_curriculo(id):
    # Parameterized select query (prevents SQL Injection)
    curriculo = Curriculo.query.get_or_404(id)
    return render_template('view.html', curriculo=curriculo)

if __name__ == '__main__':
    # Try to build database if not exists
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Banco de dados não disponível na inicialização automática: {e}")
    app.run(debug=True, port=5000)
