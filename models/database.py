# importando o flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Carregando o SQLAlchemy em uma variável
db = SQLAlchemy()

# Criando uma classe para representar a entidade Games no banco
# Nome de classe sempre no singular(boa pratica)
class Post(db.Model):
    # Definindo os atributos (colunas) da tabela
    # Schema (estrutura a baixo)
    id = db.Column(db.Integer, primary_key=True)
    filename=db.Column(db.String(255),unique=True,nullable=False)
    legenda = db.Column(db.String(150))
    data = db.Column(db.date)
    categoria = db.Column(db.String(150))
    
    # Incializando as variáveis a classe (metodo construtor)
    #self parametro que significa a si mesmo
    def __init__(self, filename, legenda, data, categoria):
        self.filename = filename
        self.legenda = legenda
        self.data = data
        self.categoria = categoria
       
