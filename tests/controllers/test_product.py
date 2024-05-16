from typing import List

import pytest
from fastapi import status

from tests.factories import product_data


async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())
    content = response.json()

    # print("Response content:", content)

    assert response.status_code == status.HTTP_201_CREATED
    assert content["name"] == "Iphone 14 Pro Max"
    assert content["quantity"] == 10
    assert content["price"] == "8500.00"
    assert content["status"] is True
    assert "id" in content
    assert "created_at" in content
    assert "updated_at" in content


async def test_controller_get_should_return_success(
    client, products_url, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")
    content = response.json()

    # print("Response content:", content)

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == str(product_inserted.id)
    assert content["name"] == "Iphone 14 Pro Max"
    assert content["quantity"] == 10
    assert content["price"] == "8500.00"
    assert content["status"] is True
    assert "created_at" in content
    assert "updated_at" in content


async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_patch_should_return_success(
    client, products_url, product_inserted
):
    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "7500.00"}
    )

    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == str(product_inserted.id)
    assert content["name"] == "Iphone 14 Pro Max"
    assert content["quantity"] == 10
    assert content["price"] == "7500.00"
    assert content["status"] is True
    assert "created_at" in content
    assert "updated_at" in content


async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(
        f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }
