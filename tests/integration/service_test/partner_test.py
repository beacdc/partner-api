import pytest

from api.exceptions.errors import InvalidDocumentNumber, DuplicateDocumentNumber
from api.services.partner_service import PartnerService


@pytest.mark.asyncio
async def test_create_partner(fake_db, fake_partner_1):
    service = PartnerService(db=fake_db)
    response = await service.create_partner(fake_partner_1)
    query = fake_db["Partner"].find_one({"tradingName": response.get("tradingName")})
    assert fake_partner_1 == response
    assert response.get("document") == query.get("document")
    assert response.get("id") == str(query.get("_id"))


@pytest.mark.asyncio
async def test_create_partner_wrong_document(fake_db, fake_partner_1):
    with pytest.raises(InvalidDocumentNumber) as ex:
        service = PartnerService(db=fake_db)
        fake_partner_1.document = "12345645412435"
        await service.create_partner(fake_partner_1)
    assert ex.value.status_code == 400
    assert (
        ex.value.detail.get("description")
        == f"Received partner document number is not valid. Document: {fake_partner_1.document}"
    )


@pytest.mark.asyncio
async def test_create_partner_duplicate_document(fake_db, fake_partner_1):
    fake_db["Partner"].insert_one(fake_partner_1.dict(exclude_none=True))
    with pytest.raises(DuplicateDocumentNumber) as ex:
        service = PartnerService(db=fake_db)
        await service.create_partner(fake_partner_1)
    assert ex.value.status_code == 400
    assert (
        ex.value.detail.get("description")
        == f"Duplicate entry found for document number: {fake_partner_1.document}"
    )


@pytest.mark.asyncio
async def test_search_partner(fake_db, fake_partner_1):
    insert = fake_db["Partner"].insert_one(fake_partner_1.dict(exclude_none=True))
    service = PartnerService(db=fake_db)
    response = await service.search_partner(str(insert.inserted_id))
    assert fake_partner_1.document == response.get("document")
    assert str(insert.inserted_id) == response.get("id")


# @pytest.mark.asyncio
# async def test_search_nearest(fake_db, fake_partner_1, fake_partner_2, fake_partner_3):
#     insert_1 = fake_db.db["Partner"].insert_one(fake_partner_1.dict(exclude_none=True))
#     insert_2 = fake_db.db["Partner"].insert_one(fake_partner_2.dict(exclude_none=True))
#     insert_3 = fake_db.db["Partner"].insert_one(fake_partner_3.dict(exclude_none=True))
#     service = PartnerService(client=fake_db)
#     response = await service.find_nearest_partner(lat=-23.5635955, long=-46.6469084)
#     for partner in response:
#         print(partner)
