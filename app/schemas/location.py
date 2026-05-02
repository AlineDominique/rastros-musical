from typing import Literal

from pydantic import BaseModel, Field, model_validator

LATAM_CODES = {
    "AR",
    "BO",
    "BR",
    "CL",
    "CO",
    "CR",
    "CU",
    "DO",
    "EC",
    "SV",
    "GT",
    "HT",
    "HN",
    "MX",
    "NI",
    "PA",
    "PY",
    "PE",
    "PR",
    "UY",
    "VE",
}

ASIA_CODES = {
    "AF",
    "AM",
    "AZ",
    "BH",
    "BD",
    "BT",
    "BN",
    "KH",
    "CN",
    "CY",
    "GE",
    "IN",
    "ID",
    "IR",
    "IQ",
    "IL",
    "JP",
    "JO",
    "KZ",
    "KW",
    "KG",
    "LA",
    "LB",
    "MY",
    "MV",
    "MN",
    "MM",
    "NP",
    "KP",
    "OM",
    "PK",
    "PS",
    "PH",
    "QA",
    "RU",
    "SA",
    "SG",
    "KR",
    "LK",
    "SY",
    "TW",
    "TJ",
    "TH",
    "TL",
    "TR",
    "TM",
    "AE",
    "UZ",
    "VN",
    "YE",
}


class LocationSchema(BaseModel):
    """Data contract for geographical localization.

    Assigns region (LatAm/Asia) based on ISO-3166 country codes.
    """

    country: str = Field(..., min_length=2)
    country_code: str = Field(..., min_length=2, max_length=2)
    region: Literal["Latam", "Asia"] | None = Field(None)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @model_validator(mode="after")
    def set_region_from_code(self) -> "LocationSchema":
        """Assign the region based on the comprehensive ISO code list."""
        code = self.country_code.upper()

        if code in LATAM_CODES:
            self.region = "Latam"
        elif code in ASIA_CODES:
            self.region = "Asia"
        else:
            raise ValueError(f"Country code {code} is outside LatAm or Asia scope.")

        return self
