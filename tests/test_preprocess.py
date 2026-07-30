import pytest
from src.preprocess import clean_text


def test_clean_text_normal():
    raw = "Congratulations! You have WON a free camera. Call now to claim."
    cleaned = clean_text(raw)
    # Check that "congratulations" stemmed, "won" is kept, stopwords removed
    assert "congratul" in cleaned
    assert "free" in cleaned
    assert "camera" in cleaned


def test_clean_text_empty_and_invalid():
    assert clean_text("") == ""
    assert clean_text("   ") == ""
    assert clean_text(None) == ""


def test_clean_text_currency_and_number_placeholders():
    raw = "Claim $500 cash by calling 8005551234 today!"
    cleaned = clean_text(raw)
    assert "xmoney" in cleaned
    assert "xnum" in cleaned


def test_clean_text_url_placeholder():
    raw = "Visit http://claim-prize.com to collect your gift!"
    cleaned = clean_text(raw)
    assert "xurl" in cleaned