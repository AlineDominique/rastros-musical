"""Script to run the ingestion pipeline."""

from app.db.database import db_manager
from app.db.setup import setup_database
from app.ingestion.ingestion_runner import run_ingestion


def main():
    """Setup database and run ingestion."""
    print("Setting up database...")
    with db_manager.get_connection() as conn:
        setup_database(conn)

    print("Starting ingestion...")
    run_ingestion()

    print("Done!")


if __name__ == "__main__":
    main()
