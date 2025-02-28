from typing import List

from acma_orm.database import initialize, close_db
from acma_orm.models import Site, Client, Licence
from acma_orm.importer import import_all_data
from acma_orm import enable_debug_logging


def main():
    enable_debug_logging()

    # Run a simple query.
    site_count = Site.select().count()
    print(f"Total number of Site records: {site_count}")

    query: List[Licence] = (
        Licence.select().join(Client).where(Client.client_no == 20053843)
    )

    for licence in query:
        print(licence)

    # Close the database connection.
    close_db()
    print("Database closed.")


if __name__ == "__main__":
    main()
