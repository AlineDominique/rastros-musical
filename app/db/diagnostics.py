"""Database diagnostic commands (read-only)."""

import sys

from app.db.database import db_manager


def show_stats():
    """Show database overview."""
    with db_manager.get_connection() as conn:
        artists = conn.execute("SELECT COUNT(*) FROM bronze.artist_raw").fetchone()[0]
        genres = conn.execute("SELECT COUNT(*) FROM bronze.genre_raw").fetchone()[0]
        relations = conn.execute(
            "SELECT COUNT(*) FROM bronze.artist_genre_raw"
        ).fetchone()[0]
        locations = conn.execute("SELECT COUNT(*) FROM silver.location").fetchone()[0]
        import os

        size = os.path.getsize(db_manager.db_path)
        print(f"Bronze artists:   {artists}")
        print(f"Bronze genres:    {genres}")
        print(f"Bronze relations: {relations}")
        print(f"Silver locations:  {locations}")
        print(f"Database size:    {size / 1024:.1f} KB")


def show_top_countries():
    """Show top 10 countries by artist count."""
    with db_manager.get_connection() as conn:
        for row in conn.execute(
            "SELECT country_code, COUNT(*) as c FROM bronze.artist_raw "
            "WHERE country_code != '' GROUP BY country_code ORDER BY c DESC LIMIT 10"
        ).fetchall():
            print(f"{row[0]}: {row[1]}")


def show_top_genres():
    """Show genres by artist count."""
    with db_manager.get_connection() as conn:
        for row in conn.execute(
            "SELECT g.name, COUNT(agr.artist_id) as c "
            "FROM bronze.genre_raw g "
            "JOIN bronze.artist_genre_raw agr ON g.genre_id = agr.genre_id "
            "GROUP BY g.name ORDER BY c DESC"
        ).fetchall():
            print(f"{row[0]}: {row[1]}")


def show_sample():
    """Show 10 sample artists."""
    with db_manager.get_connection() as conn:
        for row in conn.execute(
            "SELECT name, country_code FROM bronze.artist_raw "
            "WHERE country_code != '' LIMIT 10"
        ).fetchall():
            print(f"{row[0]} ({row[1]})")


if __name__ == "__main__":
    commands = {
        "stats": show_stats,
        "countries": show_top_countries,
        "genres": show_top_genres,
        "sample": show_sample,
    }
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    commands.get(cmd, show_stats)()
