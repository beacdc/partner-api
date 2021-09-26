def partner_to_dict(partner: dict):
    return {
        "id": str(partner.get("_id")),
        "tradingName": partner.get("tradingName"),
        "ownerName": partner.get("ownerName"),
        "document": partner.get("document"),
        "coverageArea": geojson_to_dict(partner.get("coverageArea")),
        "address": geojson_to_dict(partner.get("address")),
    }


def geojson_to_dict(geo):
    return {
        "type": str(geo.get("type")).replace("GeoType.", ""),
        "coordinates": geo.get("coordinates"),
    }
