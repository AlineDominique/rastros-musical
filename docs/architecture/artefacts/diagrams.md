# Architecture Diagrams — Rastros Musical

## Database Schema (Medallion Architecture)

```mermaid
erDiagram
    bronze_artist_raw {
        VARCHAR artist_id PK
        VARCHAR name
        VARCHAR country_code
        DOUBLE latitude
        DOUBLE longitude
        TIMESTAMP ingested_at
    }

    bronze_genre_raw {
        VARCHAR genre_id PK
        VARCHAR name
        INTEGER parent_genre_id
        TIMESTAMP ingested_at
    }

    bronze_artist_genre_raw {
        VARCHAR artist_id PK
        VARCHAR genre_id PK
        VARCHAR start_date
        VARCHAR end_date
        TIMESTAMP ingested_at
    }

    silver_artist {
        VARCHAR artist_id PK
        VARCHAR name
        VARCHAR country_code
        DOUBLE latitude
        DOUBLE longitude
        VARCHAR region
        TIMESTAMP created_at
    }

    silver_genre {
        VARCHAR genre_id PK
        VARCHAR name
        INTEGER parent_genre_id
        TIMESTAMP created_at
    }

    silver_artist_genre {
        VARCHAR artist_id PK
        VARCHAR genre_id PK
        DATE start_date
        DATE end_date
    }

    silver_location {
        VARCHAR country_code PK
        VARCHAR country_name
        VARCHAR region
        DOUBLE latitude
        DOUBLE longitude
    }

    silver_genre_propagation {
        VARCHAR genre PK
        VARCHAR country_code PK
        INTEGER first_year
    }

    gold_genre_first_appearance {
        VARCHAR genre PK
        VARCHAR target_country PK
        DOUBLE target_lat
        DOUBLE target_lon
        INTEGER first_year
        VARCHAR source
    }

    bronze_artist_raw ||--o{ bronze_artist_genre_raw : ""
    bronze_genre_raw ||--o{ bronze_artist_genre_raw : ""
    silver_location ||--o{ silver_artist : ""
    silver_location ||--o{ gold_genre_first_appearance : ""
    silver_genre_propagation ||--o{ gold_genre_first_appearance : ""