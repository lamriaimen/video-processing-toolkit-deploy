"""Console script for video_processing_toolkit."""
import video_processing_toolkit

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for video_processing_toolkit."""
    console.print("Replace this message by putting your code into "
               "video_processing_toolkit.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
