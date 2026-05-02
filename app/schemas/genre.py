from pydantic import BaseModel, Field


class GenreSchema(BaseModel):
    """Data contract for the musical Genre entity.

    Ensures structural integrity for genre classification and hierarchy
    within the Medallion architecture.

    Attributes:
        name: The unique name of the musical genre.
        region_origin: Geographic region where the genre emerged.
        subgenres: A list of related sub-classifications.
        is_active: Flag indicating if the genre is currently in use in the system.
    """

    name: str = Field(..., min_length=1)
    region_origin: str | None = None
    subgenres: list[str] = Field(default_factory=list)
    is_active: bool = True
