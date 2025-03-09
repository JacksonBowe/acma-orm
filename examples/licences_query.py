from acma_orm.models import Licence, Client, DeviceDetail
from playhouse.shortcuts import model_to_dict

# Query: Get unique licence numbers (from Licence) for which there is at least one
# DeviceDetail with frequency between 2,550,000,000 and 2,650,000,000 Hz,
# along with the associated client number and client name.
query = (
    Licence.select(Licence.licence_no, Client.client_no, Client.licencee)
    .join(DeviceDetail, on=(Licence.licence_no == DeviceDetail.licence))
    .join(Client, on=(Licence.client == Client.client_no))
    .where(DeviceDetail.frequency.between(2550000000, 2650000000))
    .distinct()
)

for row in query.dicts():
    print(row)
