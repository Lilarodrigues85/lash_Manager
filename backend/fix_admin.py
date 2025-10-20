from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    admin = Usuario.query.filter_by(username='admin').first()
    
    if admin:
        admin.tipo_usuario = 'admin'
        admin.set_password('admin123')
        db.session.commit()
        print("Admin atualizado!")
        print("Username: admin")
        print("Password: admin123")
        print(f"Tipo: {admin.tipo_usuario}")
