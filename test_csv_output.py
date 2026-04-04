import pytest
import pandas as pd


def test_csv_empty():
    df = pd.read_csv("CLEANED_DATA/rightmove/rm_properties_belfast.csv")

    assert not df.empty, "DataFrame should not be empty"


def test_csv_title_column():
    df = pd.read_csv("CLEANED_DATA/rightmove/rm_properties_belfast.csv")
    assert "title" in df.columns, "DataFrame should contain 'title' column"


def test_csv_location_column():
    df = pd.read_csv("CLEANED_DATA/rightmove/rm_properties_belfast.csv")
    assert "location" in df.columns, "DataFrame should contain 'location' column"


def test_csv_price_column():
    df = pd.read_csv("CLEANED_DATA/rightmove/rm_properties_belfast.csv")

    assert "price" in df.columns, "DataFrame should contain 'price' column"


def test_csv_property_type_column():
    df = pd.read_csv("CLEANED_DATA/rightmove/rm_properties_belfast.csv")
    assert "property_type" in df.columns, "DataFrame should contain 'property_type' column"


def test_csv_bedrooms_column():
    df = pd.read_csv("CLEANED_DATA/rightmove/rm_properties_belfast.csv")
    assert "bedrooms" in df.columns, "DataFrame should contain 'bedrooms' column"


def test_csv_bathrooms_column():
    df = pd.read_csv("CLEANED_DATA/rightmove/rm_properties_belfast.csv")
    assert "bathrooms" in df.columns, "DataFrame should contain 'bathrooms' column"


def test_csv_area_column():
    df = pd.read_csv("CLEANED_DATA/rightmove/rm_properties_belfast.csv")
    assert "area" in df.columns, "DataFrame should contain 'area' column"


def test_csv_link_column():
    df = pd.read_csv("CLEANED_DATA/rightmove/rm_properties_belfast.csv")

    assert "link" in df.columns, "DataFrame should contain 'link' column"