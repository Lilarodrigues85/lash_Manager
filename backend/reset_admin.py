from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    admin = Usuario.query.filter_by(username='admin').first()
    
    if admin:
        print(f"Admin encontrado: {admin.username}")
        print(f"Email: {admin.email}")
        print(f"Tipo: {admin.tipo_usuario}")
        print(f"Ativo: {admin.ativo}")
        
        # Resetar senha
        admin.set_password('admin123')
        admin.tipo_usuario = 'admin'
        admin.ativo = True
        db.session.commit()
        
        print("\nSenha resetada para: admin123")
        print("Tipo atualizado para: admin")
        
        # Testar senha
        if admin.check_password('admin123'):
            print("\nTeste de senha: OK")
        else:
            print("\nTeste de senha: FALHOU")
    else:
        print("Admin nao encontrado. Criando...")
        admin = Usuario(
            username='admin',
            email='admin@lashmanager.com',
            nome='Administrador',
            tipo_usuario='admin',
            ativo=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin criado com sucesso!")
        print("Username: admin")
        print("Password: admin123")
