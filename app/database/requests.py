from app.database.models import async_session, User, Category, Item, Rent, Favorite
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            

async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))
    

async def get_items_by_category(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))
    
    
async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))
    

async def get_rents():
    async with async_session() as session:
        return await session.scalars(select(Rent))
    
    
async def get_description_by_rents(rent_id: int):
    async with async_session() as session:
        result = await session.scalar(select(Rent.description).where(Rent.id == rent_id))
        return result or 'Описание не найдено'
    
    
async def get_user_favorites(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return []

        stmt = (
            select(Item)
            .join(Favorite, Favorite.item_id == Item.id)
            .where(Favorite.user_id == user.id)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
    
    
async def add_to_favorites(tg_id: int, item_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            user = await set_user(tg_id)

        fav = Favorite(user_id=user.id, item_id=item_id)
        session.add(fav)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            
            
async def remove_from_favorites(tg_id: int, item_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return

        stmt = delete(Favorite).where(
            Favorite.user_id == user.id,
            Favorite.item_id == item_id
        )
        await session.execute(stmt)
        await session.commit()