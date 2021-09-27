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


def validate_and_format_document(document: str):
    document = "".join(char for char in document if char.isdigit())
    validate_document_processor = {
        11: validate_cpf(document),
        14: validate_cnpj(document),
    }
    is_valid = validate_document_processor.get(len(document), False)
    return document, is_valid


def validate_cpf(document):
    #  verify length
    if len(document) != 11:
        return False

    #  verify if document is not for ex: 111.111.111-11
    if document == document[::-1]:
        return False

    #  validate digits
    for i in range(9, 11):
        value = sum((int(document[num]) * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != int(document[i]):
            return False
    return True


def validate_cnpj(document):
    # defining some variables
    validation_list = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    validation_list_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    # finding out the digits
    verification_digits = document[-2:]

    # verifying the length of the cnpj
    if len(document) != 14:
        return False

    # calculating the first digit
    sum_ = 0
    id_ = 0
    for number in document:

        try:
            validation_list[id_]
        except Exception:
            break

        sum_ += int(number) * int(validation_list[id_])
        id_ += 1

    sum_ = sum_ % 11
    if sum_ < 2:
        first_digit = 0
    else:
        first_digit = 11 - sum_

    first_digit = str(first_digit)  # converting to string, for later comparison

    # calculating the second digit
    # suming the two lists
    sum_ = 0
    id_ = 0

    # suming the two lists
    for number in document:
        try:
            validation_list_2[id_]
        except Exception:
            break

        sum_ += int(number) * int(validation_list_2[id_])
        id_ += 1

    # defining the digit
    sum_ = sum_ % 11
    if sum_ < 2:
        second_digit = 0
    else:
        second_digit = 11 - sum_

    second_digit = str(second_digit)

    return (
        False if not bool(verification_digits == (first_digit + second_digit)) else True
    )
