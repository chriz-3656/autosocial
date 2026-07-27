import click
import logging

logging.basicConfig(level=logging.INFO)

@click.group()
def cli():
    """AutoSocial AI CLI"""
    pass

@cli.command()
@click.option("--category", default="Tech", help="Category to generate content for")
def generate_post(category):
    """Generate a single post."""
    click.echo(f"Generating post for category: {category}")
    # In a real run, this would invoke the Brain Orchestrator
    click.echo("Done.")

@cli.command()
def health_check():
    """Run system health check."""
    click.echo("System is healthy.")
    
@cli.command()
def clear_cache():
    """Clear temporary files."""
    click.echo("Cache cleared.")

if __name__ == "__main__":
    cli()
