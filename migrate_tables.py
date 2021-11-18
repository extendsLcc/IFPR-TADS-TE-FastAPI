import sqlalchemy

from config import DATABASE_URL, metadata
from models.product import Product


def migrate_refresh_database(database_url=DATABASE_URL):
    engine = sqlalchemy.create_engine(database_url)
    metadata.drop_all(engine)
    metadata.create_all(engine)


if __name__ == "__main__":
    migrate_refresh_database()
