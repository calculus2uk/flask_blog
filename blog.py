from app import db, create_app
from app.models import User, Post

app = create_app()

# with app.app_context():
#     db.drop_all()
#     db.create_all()
    
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}