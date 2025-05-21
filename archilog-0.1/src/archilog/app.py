import sys
from archilog import create_app
from archilog.views.cli import cli

if __name__ == '__main__':
    # Si on est dans un contexte CLI, on lance les commandes
    if len(sys.argv) > 1:
        cli()
    else:
        # Sinon, on lance l'application Flask
        app = create_app()
        app.run(debug=True)