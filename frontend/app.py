import requests
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from config import Config
from forms import CurriculoForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)

BACKEND_URL = app.config['BACKEND_URL']

@app.after_request
def apply_security_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "script-src 'self' 'unsafe-inline';"
    )
    return response

@app.route('/')
def list_curriculos():
    resp = requests.get(f"{BACKEND_URL}/curriculos")
    resp.raise_for_status()
    curriculos = resp.json()
    return render_template('list.html', curriculos=curriculos)

@app.route('/cadastro', methods=['GET', 'POST'])
def create_curriculo():
    form = CurriculoForm()
    if form.validate_on_submit():
        form.sanitize_data()
        payload = {
            'nome': form.nome.data,
            'email': form.email.data,
            'experiencia_profissional': form.experiencia_profissional.data.strip(),
        }
        if form.telefone.data:
            payload['telefone'] = form.telefone.data
        if form.site_url.data:
            payload['site_url'] = form.site_url.data

        try:
            resp = requests.post(f"{BACKEND_URL}/curriculos", json=payload)
            resp.raise_for_status()
            flash('Currículo cadastrado com sucesso!', 'success')
            return redirect(url_for('list_curriculos'))
        except requests.HTTPError:
            flash('Erro ao salvar no banco de dados. Tente novamente.', 'danger')
            app.logger.error(f"Backend error: {resp.status_code} {resp.text}")

    return render_template('create.html', form=form)

@app.route('/consulta/<int:id>')
def view_curriculo(id):
    resp = requests.get(f"{BACKEND_URL}/curriculos/{id}")
    if resp.status_code == 404:
        abort(404)
    resp.raise_for_status()
    curriculo = resp.json()
    return render_template('view.html', curriculo=curriculo)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
