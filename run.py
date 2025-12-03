from app import create_app, db
from flask_migrate import Migrate
from app.models import User

# Creamos la instancia de la aplicación
app = create_app()

# Creamos la instancia de Migrate
migrate = Migrate(app, db)

# Contexto de shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

# --- ESTO ES LO QUE FALTABA ---
if __name__ == '__main__':
    app.run(debug=True)