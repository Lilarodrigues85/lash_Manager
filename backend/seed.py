from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    # Criar usuário admin
    admin = Usuario.query.filter_by(username='admin').first()
    if not admin:
        admin = Usuario(
            username='admin',
            email='admin@lashmanager.com',
            nome='Administrador',
            tipo_usuario='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Usuario admin criado!')
    else:
        if admin.tipo_usuario != 'admin':
            admin.tipo_usuario = 'admin'
            db.session.commit()
            print('Usuario admin atualizado!')
        else:
            print('Usuario admin ja existe')
