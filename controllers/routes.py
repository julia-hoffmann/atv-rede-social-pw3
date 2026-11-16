from flask import  render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
@app.route('/cadastro', methods=['GET', 'POST'])
def init_app(app):
    # CRIANDO FUNÇÃO DE MIDDLEWARE (ROTAS QUE PRECISAM DE LOGIN OU NÃO)
    @app.before_request
    def check_auth():
        # ROTAS QUE NÃO PRECISAM DE AUTENTICAÇÃO
        rotasPermitidas = ['home', 'login', 'cadastro', 'static']
        # Se a rota da requisição não requer autenticação, permitir o acesso
        if request.endpoint in rotasPermitidas:
            # Prosssiga
            return
        # Se o usuário não estiver logado e tentar acessar uma rota protegida
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        
def cadastro():
    if request.method == 'POST':
        # COLETA OS DADOS DO FORMULÁRIO
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        # GERANDO O HASH DE SENHA (CRIPTOGRAFIA)
        senha_com_hash = generate_password_hash(senha, method='scrypt')
         # ENVIANDO OS DADOS PARA O MODEL
        novo_usuario = Usuario(nome=nome,email=email, senha=senha_com_hash)
        # GRAVANDO NO BANCO
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login')
def login():
        
        if request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            senha = request.form['senha']
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario:
                if check_password_hash(usuario.senha, senha):
                    
                 session['usuario_id'] = usuario.id
                 session['usuario_email'] = usuario.email
                 msgLogin = "voce foi autenticado com sucesso!"
                 flash(msgLogin, 'sucess')
                 return redirect(url_for('home'))
        return render_template('login.html')
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
        # Destruindo a sessão do usuário
        session.clear()
        return redirect(url_for('home'))
@app.route('/feed', methods=['GET', 'POST'])
def feed():
        # Selecionando todos os nomes de imagens do banco
        imagens = Imagem.query.all()
        # LISTA DE EXTENSÕES PERMITIDAS
        FILE_TYPES = set(['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'])
        # FUNÇÃO PARA VALIDAR O TIPO DE ARQUIVO ENVIADO
        def arquivos_permitidos(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES 
        # RECEBENDO O ARQUIVO DO FORMULÁRIO
        if request.method == 'POST':
            # GUARDO O ARQUIVO EM UMA VARIÁVEL
            file = request.files['file']
            # Verificar se a extensão é válida
            if not arquivos_permitidos(file.filename):
                flash("Arquivo não permitido! Envie somente arquivos de imagem.", 'danger')
                return redirect(request.url)
            # SE A EXTENSÃO FOR VÁLIDA
            # Gere um nome aleatório para o arquivo
            filename = str(uuid.uuid4())
            # Grava o nome do arquivo na tabela de Imagem
            imagem = Imagem(filename)
            # Salva no banco
            db.session.add(imagem)
            # Confirma a alteração
            db.session.commit()
            # Salva o arquivo no servidor (na pasta uploads)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
            flash("Imagem recebida com sucesso!", 'success')
            return redirect(url_for('feed'))      
        return render_template('feed.html', imagens=imagens)
    
     @app.route('/chat')
     def chat():
             return render_template('chat.html', nickname=session.get('usuario_email'))