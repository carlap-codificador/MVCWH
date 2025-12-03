from flask import Flask, request, render_template, redirect, url_for, session, flash
from controllers import user_controller, client_controller, commodity_controller, whr_controller, cr_controller

from database import db
from models.user_model import User
from models.client_model import Client
from models.commodity_model import Commodity
from models.whr_model import WHR
from models.cr_model import CargoRelease, CargoReleaseItem


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///whr.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.secret_key = "12345"

db.init_app(app)

# Crear tablas automáticamente (en local y en Render)
with app.app_context():
    db.create_all()
    if User.query.count() == 0:
        admin = User(
            name="Administrator",
            username="admin",
            password="admin123",
            rol="admin"
        )
        admin.save()
        print("✔ Usuario administrador creado: admin / admin123")

# Registrar Blueprints
app.register_blueprint(user_controller.user_bp)
app.register_blueprint(client_controller.client_bp)
app.register_blueprint(commodity_controller.commodity_bp)
app.register_blueprint(whr_controller.whr_bp)
app.register_blueprint(cr_controller.cr_bp)

print("== URL MAP ==")
print(app.url_map)


@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return dict(
        is_active=is_active,
        logged_in=('user_id' in session),   
        current_user=session.get('username')
    )
    

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Buscar usuario en la BD
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash("User not found", "danger")
            return render_template("login.html")

        # Verificar contraseña (usa verify_password del modelo)
        if not user.verify_password(password):
            flash("Invalid password", "danger")
            return render_template("login.html")

        # Autenticación correcta
        session["user_id"] = user.id
        session["username"] = user.username
        session["rol"] = user.rol

        # Redirigir a lista de WHR (asegúrate de tener ese blueprint)
        return redirect(url_for("whr.index"))  # 👈 endpoint del blueprint WHR

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
    


if __name__ == "__main__":
    app.run(debug=True)