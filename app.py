from flask import Flask
from flask_socketio import SocketIO
from models.database import db
from controllers import routes, chat
import os
app = Flask(__name__, template_folder='views')
# Configurações de Banco (exemplo com SQLite)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR,'models/rede_social.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave_secreta_rede_social'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
# Inicialização do SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
routes.init_app(app)
chat.init_app(socketio)
if __name__ == '__main__':
    # Cria a pasta de uploads caso não exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app=app)
with app.app_context():
db.create_all()
socketio.run(app, host='0.0.0.0', port=5000, debug=True)
