import os


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 8080 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "twitterAdmin123")
    user = os.environ.get("DB_USER",  "twitterAdmin")
    db_name = os.environ.get("DB_NAME", "twitter")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
