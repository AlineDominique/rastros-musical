Extract:  Wikipedia (genre_origins.py) + Google Trends (pytrends)
    ↓
Load:     BronzeLoader → bronze.* (raw data)
    ↓
Transform: SilverLoader → silver.* (clean, validated, integrated)
    ↓
Analyze:  GoldLoader → gold.genre_first_appearance (analytics-ready)
    ↓
Serve:    FastAPI → /api/genres, /api/propagation
    ↓
Display:  React + Deck.gl → interactive map