"""
Finds all licences where the client is TELSTRA and at least one device operates on 882.5 MHz.
Run with:
    uv run examples/join_query_telstra_frequency.py
"""

from acma_orm import enable_debug_logging
from acma_orm.models import Licence, Client, DeviceDetail
from acma_orm.database import close_db
from playhouse.shortcuts import model_to_dict


def main():
    enable_debug_logging()
    print("Executing join query for TELSTRA licences operating on 882.5 MHz...\n")

    query = (
        Licence.select(Licence)
        .join(Client)
        .switch(Licence)
        .join(DeviceDetail)
        .where(
            (
                Client.licencee.contains("TELSTRA")  # Match 'TELSTRA' in licencee name
                & (DeviceDetail.frequency == 882500000)  # Match frequency exactly
            )
        )
        .distinct()
    )

    for licence in query:
        data = model_to_dict(licence, recurse=True)
        print(data["licence_no"])

    close_db()
    print("\nQuery completed.")


if __name__ == "__main__":
    main()
