"""Integration between Google Trends data and the Medallion pipeline."""

from pandas import DataFrame

from app.ingestion.google_trends import GoogleTrendsClient


def find_first_significant_year(df: DataFrame, threshold: int = 10) -> int | None:
    """Find the first year with significant search interest.

    Args:
        df: DataFrame with Google Trends data indexed by date.
        threshold: Minimum interest value to consider significant.

    Returns:
        Year of first significant interest, or None if not found.
    """
    if df.empty:
        return None

    significant = df[df.iloc[:, 0] >= threshold]
    if significant.empty:
        return None

    return significant.index[0].year


def build_propagation_data(genre: str, country_codes: list[str]) -> list[dict]:
    """Build propagation data for a genre across multiple countries.

    Args:
        genre: Genre name to search for.
        country_codes: List of ISO country codes to check.

    Returns:
        List of dicts with genre, country_code, and first_year.
    """
    client = GoogleTrendsClient()
    results = []

    for country_code in country_codes:
        try:
            df = client.get_interest_over_time([genre], geo=country_code)
            first_year = find_first_significant_year(df)

            if first_year:
                results.append(
                    {
                        "genre": genre,
                        "country_code": country_code,
                        "first_year": first_year,
                    }
                )
        except Exception:
            continue

    return results
