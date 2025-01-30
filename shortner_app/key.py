
from sqlalchemy.orm import Session
import secrets, string
from . import table, structure

def create_random_key(length: int = 5) -> str:
    chars = string.hexdigits + string.ascii_lowercase
    return "".join(secrets.choice(chars) for _ in range(length))

def create_unique_random_key(db: Session) -> str:
    key = create_random_key()
    while get_db_url_by_key(db, key):
        key = create_random_key()
    return key

def create_db_url(db: Session, url: structure.URLBase):
    key = create_random_key()
    db_url = table.URL(
        target_url=url.target_url, key=key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_db_url_by_key(db: Session, url_key: str) -> table.URL:
    return (
        db.query(table.URL)
        .filter(table.URL.key == url_key, table.URL.is_active)
        .first()
    )