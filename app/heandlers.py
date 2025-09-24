from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.keyboards as kb
from app.database.requests import set_user, get_item, get_description_by_rents, add_to_favorites, remove_from_favorites, get_user_favorites
from app.info import DESCRIPTION, GEO_INFO, SOCIALNETWORK_INFO, COOPERATION_INFO, RENT_INFO, TESTGRIVES_INFO

router = Router()


@router.message(CommandStart())
async def cmd_start(message:Message):
    await set_user(message.from_user.id)
    await message.answer(text=DESCRIPTION,
                        reply_markup=kb.menu)
    

@router.callback_query(F.data == 'start')
async def callback_start(callback: CallbackQuery):
    await callback.answer('Вы вернулись на главное меню')
    await callback.message.edit_text(text=DESCRIPTION,
                                     reply_markup=kb.menu)


@router.callback_query(F.data == 'socialnetwork')
async def callback_socialnetwork(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(text=SOCIALNETWORK_INFO,
                                     reply_markup=kb.btm)
    
    
@router.callback_query(F.data == 'geolocation')
async def callback_geolocation(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(text=GEO_INFO,
                                     reply_markup=kb.btm)
    
    
@router.callback_query(F.data == 'testdrives')
async def callback_geolocation(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(text=TESTGRIVES_INFO,
                                     reply_markup=kb.btm)   
                                     

@router.callback_query(F.data == 'cooperation')
async def callback_socialnetwork(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(text=COOPERATION_INFO,
                                     reply_markup=kb.btm)
    
  
@router.callback_query(F.data == 'back_to_menu')
async def callback_start(callback: CallbackQuery):
    await callback.answer('Вы вернулись на главное меню')
    await callback.message.edit_text(text=DESCRIPTION,
                                     reply_markup=kb.menu)

  
@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите категорию товара',
                                     reply_markup=await kb.categories())
    
    
@router.callback_query(F.data == 'rent')
async def rents(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(RENT_INFO,
                                     reply_markup=await kb.rents())
    
    
@router.callback_query(F.data == 'ignore')
async def ignore_handler(callback: CallbackQuery):
    await callback.answer('')

    
@router.callback_query(F.data == 'btrents')
async def btrents(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(RENT_INFO,
                                     reply_markup=await kb.rents())
    
    
@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите товар по категории',
                                     reply_markup=await kb.get_items(callback.data.split('_')[1]))
    
    
@router.callback_query(F.data.startswith("rent_"))
async def show_rent_description(callback: CallbackQuery):
    rent_id = int(callback.data.split("_")[1])
    description = await get_description_by_rents(rent_id)
    await callback.answer('')
    await callback.message.edit_text(description,
                                     reply_markup=await kb.back_to_rents())
    
    
@router.callback_query(F.data.startswith('item_'))
async def item_heandler(callback: CallbackQuery):
    item = await get_item(callback.data.split('_')[1])
    keyboard = await kb.item_keyboard(callback.from_user.id, item.id, item.category)
    await callback.answer('')
    await callback.message.edit_text(f'{item.name}\n\nЦена: {item.price}\n\n{item.description}',
                                  reply_markup=keyboard)
  

@router.callback_query(F.data.startswith('fav_add_'))
async def handle_add_fav(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[2])
    await add_to_favorites(callback.from_user.id, item_id)
    await callback.answer('Товар добавлен в избранное')
    
    item = await get_item(item_id)
    keyboard = await kb.item_keyboard(callback.from_user.id, item_id, item.category)
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data.startswith("fav_rm_"))
async def handle_rm_fav(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[2])
    await remove_from_favorites(callback.from_user.id, item_id)
    await callback.answer('Товар удален из избранного')
    
    item = await get_item(item_id)
    keyboard = await kb.item_keyboard(callback.from_user.id, item_id, item.category)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    
    
@router.callback_query(F.data == 'favourites')
async def handle_show_favorites(callback: CallbackQuery):
    favorites = await get_user_favorites(callback.from_user.id)
    if not favorites:
        await callback.answer('')
        await callback.message.edit_text('У вас пока нет избранных товаров',
                                         reply_markup=kb.btm)
    else:
        keyboard = await kb.favourites_keyboard(callback.from_user.id)
        await callback.answer('')
        await callback.message.edit_text('Ваши избранные товары:',
                                         reply_markup=keyboard)
    
