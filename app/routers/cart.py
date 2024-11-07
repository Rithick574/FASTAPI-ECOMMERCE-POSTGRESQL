from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemResponse, CartItemDetailResponse
from app.database import get_db
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=list[CartItemDetailResponse])
async def view_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(CartItem).where(CartItem.user_id == current_user.id)
    result = await db.execute(query)
    cart_items = result.scalars().all()

    detailed_cart_items = []
    for item in cart_items:
        product = await db.execute(select(Product).where(Product.id == item.product_id))
        product = product.scalar_one_or_none()
        if product:
            detailed_cart_items.append(CartItemDetailResponse(
                id=item.id,
                user_id=item.user_id,
                product_id=item.product_id,
                quantity=item.quantity,
                product_name=product.name,
                product_description=product.description,
                product_price=product.price
            ))

    return detailed_cart_items


@router.post("/", response_model=CartItemResponse)
async def add_to_cart(
    cart_item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
   
    product = await db.execute(select(Product).where(Product.id == cart_item.product_id))
    product = product.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_cart_item = CartItem(
        user_id=current_user.id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity
    )
    db.add(new_cart_item)
    await db.commit()
    await db.refresh(new_cart_item)
    return new_cart_item


@router.put("/{cart_item_id}", response_model=CartItemResponse)
async def update_cart_item(
    cart_item_id: int,
    cart_item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(CartItem).where(CartItem.id == cart_item_id, CartItem.user_id == current_user.id)
    result = await db.execute(query)
    existing_cart_item = result.scalar_one_or_none()

    if not existing_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    existing_cart_item.quantity = cart_item.quantity
    await db.commit()
    await db.refresh(existing_cart_item)
    return existing_cart_item


@router.delete("/{cart_item_id}", response_model=dict)
async def remove_cart_item(
    cart_item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(CartItem).where(CartItem.id == cart_item_id, CartItem.user_id == current_user.id)
    result = await db.execute(query)
    existing_cart_item = result.scalar_one_or_none()

    if not existing_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    await db.delete(existing_cart_item)
    await db.commit()
    return {"detail": "Cart item removed successfully"}