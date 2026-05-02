from typing import Annotated

from pydantic import BaseModel, Field


class ArtistSchema(BaseModel):
    """Data contract for the Artist entity.

    Acts as the primary integrity barrier for the Medallion architecture,
    ensuring only strongly typed and geographically valid data is persisted.

    Attributes:
        name: Full name of the artist or band.
        origin_country: Country of origin for migration mapping.
        latitude: GPS coordinate (-90 to 90) for Deck.gl visualization.
        longitude: GPS coordinate (-180 to 180) for Deck.gl visualization.
        genre: Primary musical genre (optional).
    """

    name: str = Field(..., min_length=1)
    origin_country: str
    latitude: Annotated[float, Field(ge=-90, le=90)]
    longitude: Annotated[float, Field(ge=-180, le=180)]
    genre: str | None = None
