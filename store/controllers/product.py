from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from pydantic import UUID4

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecase

router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    return await usecase.create(body=body)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(usecase: ProductUsecase = Depends()) -> List[ProductOut]:
    return await usecase.query()


@router.get("/filter", response_model=List[ProductOut])
async def filter_by_price(
    min_price: float = Query(..., alias="minPrice"),
    max_price: float = Query(..., alias="maxPrice"),
    usecase: ProductUsecase = Depends(),
) -> List[ProductOut]:
    return await usecase.filter_by_price(min_price=min_price, max_price=max_price)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(..., alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(..., alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
    try:
        return await usecase.update(id=id, body=body)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(..., alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
