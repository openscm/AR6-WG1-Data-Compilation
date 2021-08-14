from pathlib import Path

import pytest

ROOT_DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_DATA_DIR = ROOT_DATA_DIR / "processed"
RAW_DATA_DIR = ROOT_DATA_DIR / "raw"
TEST_DATA_DIR = Path(__file__).parent / "test-data"

@pytest.fixture
def processed_data_dir():
    return PROCESSED_DATA_DIR


@pytest.fixture
def raw_data_dir():
    return RAW_DATA_DIR


@pytest.fixture
def test_data_dir():
    return TEST_DATA_DIR
