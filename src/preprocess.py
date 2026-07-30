import re
from typing import List
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download required resources if not present
try:
    NLTK_STOPWORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", quiet=True)
    NLTK_STOPWORDS = set(stopwords.words("english"))

stemmer = PorterStemmer()

# Define special placeholders that should NEVER be stemmed
SPECIAL_TOKENS = {"xurl", "xemail", "xmoney", "xnum"}


def clean_text(raw_text: str) -> str:
    """
    Cleans raw SMS text for NLP modeling.
    
    Steps:
    1. Handle empty inputs
    2. Lowercase
    3. Normalize URLs, emails, currency, and numbers into special placeholders
    4. Strip non-alphanumeric punctuation
    5. Tokenize, remove stopwords, and apply Stemming (skipping special tokens)
    """
    if not isinstance(raw_text, str) or not raw_text.strip():
        return ""

    # 1. Lowercase
    text = raw_text.lower()

    # 2. Normalize URLs & Emails
    text = re.sub(r"https?://\S+|www\.\S+", " xurl ", text)
    text = re.sub(r"\S+@\S+\.\S+", " xemail ", text)

    # 3. Normalize Currency (e.g., $1000, £50 -> xmoney)
    text = re.sub(r"[\$\£\€]\d+|\d+[\$\£\€]", " xmoney ", text)

    # 4. Normalize standalone numbers / phone numbers -> xnum
    text = re.sub(r"\b\d+\b", " xnum ", text)

    # 5. Remove remaining punctuation (keep spaces and alphanumeric characters)
    text = re.sub(r"[^\w\s]", "", text)

    # 6. Tokenize & Clean
    tokens = text.split()
    cleaned_tokens: List[str] = []
    
    for word in tokens:
        if word in NLTK_STOPWORDS:
            continue
        
        # Don't stem special placeholder tokens!
        if word in SPECIAL_TOKENS:
            cleaned_tokens.append(word)
        else:
            cleaned_tokens.append(stemmer.stem(word))

    return " ".join(cleaned_tokens)