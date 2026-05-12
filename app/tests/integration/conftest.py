"""Fixtures for integration tests."""

import os
from unittest.mock import patch

import pytest

from app.db.database import db_manager
from app.db.setup import load_all, setup_all
from app.ingestion.ingestion_runner import run_ingestion


@pytest.fixture(autouse=True)
def prepare_database():
    """Prepare the database with schemas, seed, and essential data.

    Before integration tests.
    """
    if os.path.exists(db_manager.db_path):
        os.remove(db_manager.db_path)

    setup_all()
    run_ingestion()

    with patch("app.ingestion.trends_integration.GoogleTrendsClient"):
        with patch(
            "app.ingestion.silver_loader.build_propagation_data", return_value=[]
        ):
            load_all()  # Silver + Gold sem Google Trends

    yield
