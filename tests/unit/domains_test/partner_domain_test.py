from api.domains.partner_domain import validate_and_format_document


def test_validate_and_format_cnpj():
    document, is_valid = validate_and_format_document("53.770.799/0001-61")
    assert document == "53770799000161"
    assert is_valid is True


def test_validate_and_format_cnpj_all_equal():
    document, is_valid = validate_and_format_document("11.111.111/1111-11")
    assert document == "11111111111111"
    assert is_valid is False


def test_validate_and_format_cnpj_invalid():
    document, is_valid = validate_and_format_document("53.770.545/0001-61")
    assert document == "53770545000161"
    assert is_valid is False


def test_validate_and_format_cpf():
    document, is_valid = validate_and_format_document("934.604.280-07")
    assert document == "93460428007"
    assert is_valid is True


def test_validate_and_format_cpf_invalid():
    document, is_valid = validate_and_format_document("123.604.280-07")
    assert document == "12360428007"
    assert is_valid is False


def test_validate_and_format_cpf_all_equal():
    document, is_valid = validate_and_format_document("111.111.111-11")
    assert document == "11111111111"
    assert is_valid is False


def test_validate_and_format_invalid():
    document, is_valid = validate_and_format_document("abcde1234")
    assert document == "1234"
    assert is_valid is False
