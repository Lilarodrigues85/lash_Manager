from app import create_app, db
from app.models.usuario import Usuario
from app.models.funcionario import Funcionario
from app.models.procedimento import Procedimento

app = create_app()

with app.app_context():
    # Criar tabelas
    db.create_all()
    
    # Criar usuário admin
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(
            username='admin',
            email='admin@lashmanager.com',
            nome='Administrador'
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Criar funcionários padrão
    funcionarios_data = [
        {'nome': 'Ana Silva', 'especialidade': 'Volume Brasileiro', 'porcentagem': 25.00},
        {'nome': 'Maria Santos', 'especialidade': 'Volume Russo', 'porcentagem': 25.00},
        {'nome': 'Julia Costa', 'especialidade': 'Fio a Fio', 'porcentagem': 25.00}
    ]
    
    for func_data in funcionarios_data:
        if not Funcionario.query.filter_by(nome=func_data['nome']).first():
            funcionario = Funcionario(**func_data)
            db.session.add(funcionario)
    
    db.session.commit()
    
    # Criar procedimentos padrão
    procedimentos_data = [
        {'nome': 'Volume Brasileiro', 'preco': 80.00, 'duracao_minutos': 120, 'funcionario_id': 1},
        {'nome': 'Volume Russo', 'preco': 120.00, 'duracao_minutos': 180, 'funcionario_id': 2},
        {'nome': 'Fio a Fio', 'preco': 60.00, 'duracao_minutos': 90, 'funcionario_id': 3},
        {'nome': 'Manutenção Volume', 'preco': 50.00, 'duracao_minutos': 60, 'funcionario_id': 1},
        {'nome': 'Remoção', 'preco': 30.00, 'duracao_minutos': 30, 'funcionario_id': 1}
    ]
    
    for proc_data in procedimentos_data:
        if not Procedimento.query.filter_by(nome=proc_data['nome']).first():
            procedimento = Procedimento(**proc_data)
            db.session.add(procedimento)
    
    db.session.commit()
    print("Banco de dados inicializado com sucesso!")