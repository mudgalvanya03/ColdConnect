import re

# Common career-page boilerplate to remove
STOPWORDS = [
    "apply now",
    "apply online",
    "about us",
    "privacy policy",
    "cookie policy",
    "terms of use",
    "careers",
    "job openings",
    "current openings",
    "view more jobs",
    "subscribe",
    "sign up",
    "log in",
    "back to careers",
    "contact us"
]

def clean_text(text: str) -> str:
    """
    Clean raw scraped text from a web page.
    Steps:
    - Remove HTML tags
    - Remove URLs
    - Remove special characters (keep letters, numbers, spaces)
    - Lowercase and filter out common stopwords/boilerplate
    - Collapse multiple spaces into one
    - Trim whitespace
    """
    if not text:
        return ""

    # Remove HTML tags
    text = re.sub(r"<[^>]*?>", "", text)

    # Remove URLs
    text = re.sub(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|"
        r"(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        "",
        text,
    )

    # Remove special characters (keep alphanumeric + spaces)
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)

    # Normalize case
    text = text.lower()

    # Remove stopwords (career page junk)
    for sw in STOPWORDS:
        text = re.sub(rf"\b{re.escape(sw)}\b", " ", text)

    # Replace multiple spaces with a single space
    text = re.sub(r"\s{2,}", " ", text)

    # Trim whitespace
    text = text.strip()

    return text
