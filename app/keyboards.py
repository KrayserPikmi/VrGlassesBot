from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_items_by_category, get_rents, get_user_favorites


menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
    [InlineKeyboardButton(text='Избранное', callback_data='favourites'),
     InlineKeyboardButton(text='Наш адрес', callback_data='geolocation')],
    [InlineKeyboardButton(text='Сотрудничество', callback_data='cooperation'),
     InlineKeyboardButton(text='Тест драйвы', callback_data='testdrives')],
    [InlineKeyboardButton(text='Соцсети', callback_data='socialnetwork'),
     InlineKeyboardButton(text='Аренда', callback_data='rent')]
])


btm = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='<< Назад', callback_data='back_to_menu')]
])


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.row(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    keyboard.row(InlineKeyboardButton(text='<< Назад', callback_data='start'))
    return keyboard.as_markup()


async def get_items(category_id):
    all_items = await get_items_by_category(category_id)
    keyboard = InlineKeyboardBuilder()
    for items in all_items:
        keyboard.row(InlineKeyboardButton(text=items.name, callback_data=f'item_{items.id}'))
    keyboard.row(InlineKeyboardButton(text='<< Назад к категориям', callback_data='catalog'))
    return keyboard.as_markup()


async def rents():
    all_rents = await get_rents()
    keyboard = InlineKeyboardBuilder()
    for rent in all_rents:
        keyboard.row(InlineKeyboardButton(text=rent.name, callback_data=f"rent_{rent.id}"))
    keyboard.row(InlineKeyboardButton(text="<< Назад", callback_data="start"))
    return keyboard.as_markup()



async def back_to_rents():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="<< Назад к аренде", callback_data="btrents"))
    return keyboard.as_markup()
    

async def back_to_category(category_id):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='<< Назад', callback_data=f'category_{category_id}')]])


async def item_keyboard(tg_id, item_id, category_id):
    favorites = await get_user_favorites(tg_id)
    is_fav = any(item.id == item_id for item in favorites)
    keyboard = InlineKeyboardBuilder()
    if is_fav:
        keyboard.row(InlineKeyboardButton(text='💔', callback_data=f'fav_rm_{item_id}'))
    else:
        keyboard.row(InlineKeyboardButton(text='❤️', callback_data=f'fav_add_{item_id}'))
    keyboard.row(InlineKeyboardButton(text='<< Назад', callback_data=f'category_{category_id}'))
    return keyboard.as_markup()


async def favourites_keyboard(tg_id):
    favorites = await get_user_favorites(tg_id)
    keyboard = InlineKeyboardBuilder()
    if favorites:
        for item in favorites:
            item_name = item.name[:30] + '...' if len(item.name) > 30 else item.name
            keyboard.row(InlineKeyboardButton(text=f'{item_name}',
                    callback_data=f'item_{item.id}'))
    else:
        keyboard.row(InlineKeyboardButton(text='У вас нет избранных товаров', callback_data='ignore'))
    keyboard.row(InlineKeyboardButton(text='<< Назад', callback_data='start'))
    return keyboard.as_markup()