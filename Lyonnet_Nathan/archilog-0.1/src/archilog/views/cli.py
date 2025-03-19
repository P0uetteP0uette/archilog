import click
import archilog.models as models
import archilog.services as services


# CLI Commands
@click.group()
def cli():
    """Gérer les commandes CLI pour l'application"""
    pass

@cli.command()
def init_db():
    """Initialiser la base de données"""
    models.init_db()
    click.echo("Base de données initialisée avec succès !")

@cli.command()
@click.option("-n", "--name", prompt="Name")
@click.option("-a", "--amount", type=float, prompt="Amount")
@click.option("-c", "--category", prompt="Category")
def create(name: str, amount: float, category: str | None):
    """Créer une nouvelle entrée"""
    models.create_entry(name, amount, category)
    click.echo(f"Entry for {name} created successfully!")

@cli.command()
@click.option("--id", required=True, type=int)
def get(id: int):
    """Obtenir une entrée par son ID"""
    entry = models.get_entry(id)
    click.echo(entry)

@cli.command()
@click.option("--id", required=True, type=int)
def delete(id: int):
    """Supprimer une entrée"""
    models.delete_entry(id)
    click.echo(f"Entry {id} deleted.")

@cli.command()
@click.option("--as-csv", is_flag=True, help="Export entries to CSV")
def get_entries(as_csv: bool):
    """Récupérer toutes les entrées"""
    entries = models.get_all_entries()

    if as_csv:
        click.echo(services.export_to_csv())
    else:
        click.echo(entries)


@cli.command()
@click.argument('csv_file', type=click.File('rb'))  # 'rb' pour lire un fichier binaire
def import_csv(csv_file):
    """Importer des entrées depuis un fichier CSV"""
    services.import_from_csv(csv_file)
    click.echo("Les entrées ont été importées avec succès depuis le fichier CSV!")
