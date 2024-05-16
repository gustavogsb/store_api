import pytest
from pydantic import ValidationError

from store.schemas.product import ProductIn
from tests.factories import product_data


def test_schemas_return_success():
    data = product_data()
    product = ProductIn.model_validate(data)

    assert product.name == "Iphone 14 Pro Max"


def test_schemas_return_raise():
    # Omitindo o campo 'name', que é obrigatório
    data = {
        "quantity": 10,
        "price": "8500.00",
        "status": True,
    }

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("name",),
        "msg": "Field required",
        "input": {
            "quantity": 10,
            "price": "8500.00",
            "status": True,
        },
        "url": "https://errors.pydantic.dev/2.5/v/missing",
    }
