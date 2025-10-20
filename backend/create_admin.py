from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    # Verificar se admin existe
    admin = Usuario.query.filter_by(username='admin').first()
    
    if admin:
        print(f"Admin já existe: {admin.username}")
        print(f"Email: {admin.email}")
        print(f"Ativo: {admin.ativo}")
        print(f"Tipo: {admin.tipo_usuario}")
    else:
        # Criar admin
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
        
        print("✅ Admin criado com sucesso!")
        print("Username: admin")
        print("Password: admin123")
