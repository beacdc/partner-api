import pytest

from api.services.partner_service import PartnerService


@pytest.mark.asyncio
async def test_create_partner(fake_client, fake_partner):
    service = PartnerService(client=fake_client)
    response = await service.create_partner(fake_partner)
    query = fake_client.db["Partner"].find_one({"tradingName": "Teste do Ze"})
    assert fake_partner == response
    assert response.get("document") == query.get("document")
    assert response.get("id") == query.get("_id")


@pytest.mark.asyncio
async def test_search_partner(fake_client, fake_partner):
    insert = fake_client.db["Partner"].insert_one(fake_partner.dict(exclude_none=True))
    service = PartnerService(client=fake_client)
    response = await service.search_partner(insert.inserted_id)
    assert fake_partner.document == response.get("document")
    assert str(insert.inserted_id) == response.get("id")
