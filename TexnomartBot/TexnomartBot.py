import os
from aiogram import Dispatcher, executor, Bot
from aiogram.types import Message, CallbackQuery, ParseMode, LabeledPrice
import aiogram.utils.markdown as fmt

from dotenv import load_dotenv

from WorkWithDataBase import GetChatId, InsertUsers
from Keyboards import *
from GetProductsDetail import GetProductDetail
import re
from random import randint

load_dotenv()
BOT = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
dp = Dispatcher(BOT)


# ------------------------------------------------Аутентификация
@dp.message_handler(commands=['start', 'about', 'help'])
async def StartCommands(message: Message):
    if message.text == '/start':
        ChatId = message.chat.id
        if GetChatId(ChatId):
            await message.answer(f'Мы рады что вы вернулись.', reply_markup=GenerateMainMenu())
        else:
            await message.answer(f'{message.from_user.full_name}. Добро пожаловать в мир Engine.',
                                 reply_markup=GenerateContactButton())
    elif message.text == '/about':
        pass
    elif message.text == '/help':
        pass


@dp.message_handler(content_types=['contact'])
async def InsertToUsers(message: Message):
    UserName = message.from_user.full_name
    ChatId = message.chat.id
    Phone = message.contact.phone_number

    if InsertUsers(ChatId, UserName, Phone):
        CreateCartForUser(ChatId)
        await BOT.send_message(chat_id=ChatId, reply_markup=GenerateMainMenu(), text='Регистрация прошла успешно.')
    else:
        await BOT.send_message(chat_id=ChatId, text='Номер телефона успешно обновлен!')


def CreateCartForUser(ChaId):
    try:
        UserId = GerUserId(ChaId)
        InsertToUsersCart(UserId)
    except Exception as e:
        print(e)


# ------------------------------------------------КАТАЛОГ


@dp.message_handler(regexp=r'✔️Сделать заказ')
async def ShowCatalog(message: Message):
    await message.answer('Выберите категорию', reply_markup=GenerateCatalogMenu())


@dp.callback_query_handler(lambda call: 'next' in call.data)
async def NextCatalogPages(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, Count = call.data.split('_')
    Count = int(Count)
    Count += 10
    await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text='Выберите категорию',
                                reply_markup=GenerateNextCatalogPage(Count))


@dp.callback_query_handler(lambda call: 'previous' in call.data)
async def PreviousCatalogPage(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, Count = call.data.split('_')
    Count = int(Count)
    LastCount = Count
    Count -= 10
    await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text='Выберите категорию',
                                reply_markup=GeneratePreviousCatalogPage(LastCount, Count))


# ------------------------------------------------КАТЕГОРИИ


@dp.callback_query_handler(lambda call: 'category' in call.data)
async def ShowSubcategory(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, CategoryId = call.data.split('_')
    CategoryId = int(CategoryId)
    CategoryName = GetCategoryName(CategoryId)[0]
    await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId,
                                reply_markup=GenerateShowSubcategoryId(CategoryId),
                                text=f'{CategoryName}')


@dp.callback_query_handler(lambda call: 'MainMenu' in call.data)
async def ReturnToMainMenu(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text='Выберите категорию',
                                reply_markup=GenerateCatalogMenu())


# ------------------------------------------------САБКАТЕГОРИИ


@dp.callback_query_handler(lambda call: 'sub' in call.data)
async def ShowSubcategoryType(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, SubcategoryId = call.data.split('_')
    SubcategoryId = int(SubcategoryId)
    if GetSubcategoryTypeById(SubcategoryId) or ShowProductsBySubcategoryId(SubcategoryId):
        SubcategoryName = GetSubcategoryName(SubcategoryId)[0]
        await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text=f'{SubcategoryName}',
                                    reply_markup=GenerateSubcategoryTypesMenu(SubcategoryId))
    else:
        await BOT.answer_callback_query(call.id, text='В данной категории нет продуктов')


@dp.callback_query_handler(lambda call: '➕' in call.data)
async def NextSubcategoryTypePage(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, Count, SubcategoryId = call.data.split('_')
    SubcategoryName = GetSubcategoryName(SubcategoryId)[0]
    Count = int(Count)
    await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text=f'{SubcategoryName}',
                                reply_markup=GenerateNextSubcategoryType(Count, SubcategoryId))


@dp.callback_query_handler(lambda call: '➖' in call.data)
async def PreviousSubcategoryTypePage(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, Count, SubcategoryId = call.data.split('_')
    SubcategoryName = GetSubcategoryName(SubcategoryId)[0]
    Count = int(Count)
    await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text=f'{SubcategoryName}',
                                reply_markup=GeneratePreviousSubcategoryType(Count, SubcategoryId))


@dp.callback_query_handler(lambda call: 'back' in call.data)
async def ReturnToSubcategories(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, SubcategoryId = call.data.split('_')
    SubcategoryId = int(SubcategoryId)
    CategoryId = GetCategoryId(SubcategoryId)[0]
    CategoryName = GetCategoryName(CategoryId)[0]
    await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text=f'{CategoryName}',
                                reply_markup=GenerateShowSubcategoryId(CategoryId))


# ------------------------------------------------ПРОДУКТЫ БЕЗ САБКАТЕГОРИИ


@dp.callback_query_handler(lambda call: call.data.startswith('NextProductPage'))
async def NextProductPageForSubcategory(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, count, subcategory_id = call.data.split('_')
    count = int(count)
    count += 10

    subcategory_name = GetSubcategoryName(subcategory_id)[0]
    await BOT.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'{subcategory_name}',
                                reply_markup=GenerateNextProductPage(count, subcategory_id))


@dp.callback_query_handler(lambda call: call.data.startswith('😏'))
async def PreviousProductPageForSubcategory(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, Count, SubcategoryId = call.data.split('_')
    SubcategoryName = GetSubcategoryName(SubcategoryId)[0]
    Count = int(Count)
    await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text=f'{SubcategoryName}',
                                reply_markup=GeneratePreviousProductPage(Count, SubcategoryId))


# ------------------------------------------------ПРОДУКТЫ


@dp.callback_query_handler(lambda call: 'type' in call.data)
async def ShowProducts(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, SubcategoryTypeId = call.data.split('_')
    if GetProducts(SubcategoryTypeId):
        SubcategoryTypeName = GetSubcategoryTypeName(SubcategoryTypeId)[0]
        await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text=f'{SubcategoryTypeName}',
                                    reply_markup=GenerateProductsMenu(SubcategoryTypeId))
    else:
        await BOT.answer_callback_query(call.id, text='В данной категории нет продуктов')


@dp.callback_query_handler(lambda call: call.data.startswith('⏫'))
async def ShowNextProductsPage(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, Count, SubcategoryTypeId = call.data.split('_')
    Count = int(Count)
    Count += 10
    SubcategoryTypeName = GetSubcategoryTypeName(SubcategoryTypeId)[0]
    await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text=f'{SubcategoryTypeName}',
                                reply_markup=GenerateNextProductsPage(Count, SubcategoryTypeId))


@dp.callback_query_handler(lambda call: '⏬' in call.data)
async def ShowPreviousProductsPage(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, Count, SubcategoryTypeId = call.data.split('_')
    Count = int(Count)
    if Count == 0:
        Count = Count
        SubcategoryTypeName = GetSubcategoryTypeName(SubcategoryTypeId)[0]
        await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text=f'{SubcategoryTypeName}',
                                    reply_markup=GeneratePreviousProductsPage(Count, SubcategoryTypeId))
    else:
        Count -= 10
        SubcategoryTypeName = GetSubcategoryTypeName(SubcategoryTypeId)[0]
        await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text=f'{SubcategoryTypeName}',
                                    reply_markup=GeneratePreviousProductsPage(Count, SubcategoryTypeId))


@dp.callback_query_handler(lambda call: '❗' in call.data)
async def ReturnToSubcategoryType(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, SubcategoryTypeId = call.data.split('_')
    SubcategoryTypeId = int(SubcategoryTypeId)
    SubcategoryId = GetSubcategoryId(SubcategoryTypeId)[0]
    SubcategoryName = GetSubcategoryName(SubcategoryId)[0]
    await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text=f'{SubcategoryName}',
                                reply_markup=GenerateSubcategoryTypesMenu(SubcategoryId))


# ------------------------------------------------ДеталиПродукта


@dp.callback_query_handler(lambda call: 'product' in call.data)
async def SendProductDetails(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, ProductId = call.data.split('_')
    if CheckIfExistsProductInDataBase(ProductId):
        ProductDetails = GetProductDetailFromDataBase(ProductId)
        Text = f'''<b>{ProductDetails[1]}</b>

{ProductDetails[4]}

Цена: {ProductDetails[5]}'''
        await BOT.send_photo(chat_id=ChatId, photo=ProductDetails[3], caption=Text,
                             reply_markup=GenerateBuyButton(ProductId))
    else:
        ProductLink, ProductName, ProductPrice, ProductImageLink, Characteristics = GetProductDetail(ProductId)
        CharacteristicsText = ''
        for i in Characteristics:
            CharacteristicsText += f'{str(i)}\n'
        InsertProductDetail(ProductId, ProductName, ProductLink, ProductImageLink, CharacteristicsText, ProductPrice)
        Text = f'''<b>{ProductName}</b>
        
{CharacteristicsText}
        
Цена: {ProductPrice}'''
        await BOT.send_photo(chat_id=ChatId, photo=ProductImageLink, caption=Text,
                             reply_markup=GenerateBuyButton(ProductId))


@dp.callback_query_handler(lambda call: '⛔' in call.data)
async def ReturnToProducts(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    await BOT.delete_message(ChatId, MessageId)


@dp.callback_query_handler(lambda call: '🛎️' in call.data)
async def GetQuantity(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    await BOT.delete_message(ChatId, MessageId)
    _, ProductId = call.data.split('_')
    ProductId = int(ProductId)
    ProductDetails = GetProductDetailFromDataBase(ProductId)
    Text = f'''<b>{ProductDetails[1]}</b>
Цена: {ProductDetails[5]}

Выберите количество:'''
    await BOT.send_photo(chat_id=ChatId, photo=ProductDetails[3], caption=Text,
                         reply_markup=GenerateQuantityButton(ProductId))


@dp.callback_query_handler(lambda call: '⬅️' in call.data)
async def DecreaseQuantity(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    await BOT.delete_message(chat_id=ChatId, message_id=MessageId)
    _, ProductId, Quantity = call.data.split('_')
    ProductId = int(ProductId)
    Quantity = int(Quantity)
    if Quantity == 1:
        Quantity = Quantity
        ProductDetails = GetProductDetailFromDataBase(ProductId)
        Text = f'''<b>{ProductDetails[1]}</b>
Цена: {ProductDetails[5]}

Выберите количество:'''
        await BOT.send_photo(chat_id=ChatId, photo=ProductDetails[3], caption=Text,
                             reply_markup=GenerateQuantityButton(ProductId, Quantity))
    else:
        Quantity -= 1
        ProductDetails = GetProductDetailFromDataBase(ProductId)
        Text = f'''<b>{ProductDetails[1]}</b>
Цена: {ProductDetails[5]}

Выберите количество:'''
        await BOT.send_photo(chat_id=ChatId, photo=ProductDetails[3], caption=Text,
                             reply_markup=GenerateQuantityButton(ProductId, Quantity))


@dp.callback_query_handler(lambda call: '➡️' in call.data)
async def IncreaseQuantity(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    await BOT.delete_message(chat_id=ChatId, message_id=MessageId)
    _, ProductId, Quantity = call.data.split('_')
    Quantity = int(Quantity)
    ProductId = int(ProductId)
    Quantity += 1
    ProductDetails = GetProductDetailFromDataBase(ProductId)
    Text = f'''<b>{ProductDetails[1]}</b>
Цена: {ProductDetails[5]}

Выберите количество:'''
    await BOT.send_photo(chat_id=ChatId, photo=ProductDetails[3], caption=Text,
                         reply_markup=GenerateQuantityButton(ProductId, Quantity))


@dp.callback_query_handler(lambda call: '🎫' in call.data)
async def AddToCartProducts(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, ProductId, Quantity = call.data.split('_')
    CartId = GetCartId(ChatId)[0]
    ProductDetails = GetProductDetailFromDataBase(ProductId)
    ProductPrice = re.search(r'[А-Яа-яA-Za-z]+', ProductDetails[-1])[0]
    Price = ProductDetails[-1].replace(ProductPrice, '')
    Price1 = Price.replace(' ', '')
    FinalPrice = int(Quantity) * int(Price1)

    if InsertOrUpdateToCartProducts(CartId, ProductDetails[1], int(Quantity), FinalPrice):
        await BOT.answer_callback_query(call.id, text='Продукт успешно добавлен в корзину')
    else:
        await BOT.answer_callback_query(call.id, text='Количество успешно изменено')


@dp.message_handler(regexp='🛒Корзина')
async def Cart(message: Message):
    ChatId = message.chat.id
    CartId = GetCartId(ChatId)[0]
    UpdateUserCart(CartId)
    TotalProducts, TotalPrice = GetUserCart(CartId)
    Data = GetCartProductsData(CartId)
    Text = f'''<b>Корзина</b>

'''
    i = 0
    for CartProductId, ProductName, Quantity, FinalPrice in Data:
        i += 1
        Text += f'''{i}.{ProductName}
Количество: {Quantity}
Общая стоимость: {FinalPrice}

'''
    Text += f'''
Общая количество товара: {0 if TotalProducts is None else TotalProducts}
Общая стоимость: {0 if TotalPrice is None else TotalPrice} сум
'''
    await BOT.send_message(chat_id=ChatId, text=Text, reply_markup=GenerateCartButtons(CartId))


@dp.callback_query_handler(lambda call: '☠️' in call.data)
async def DeleteProductFromCartProducts(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    _, CartId, CartProductIt = call.data.split('_')
    DeleteCartProduct(CartId, CartProductIt)
    await BOT.answer_callback_query(call.id, text='Продукт успешно удален')
    UpdateUserCart(CartId)
    TotalProducts, TotalPrice = GetUserCart(CartId)
    Data = GetCartProductsData(CartId)
    Text = f'''<b>Корзина</b>

'''
    i = 0
    for CartProductId, ProductName, Quantity, FinalPrice in Data:
        i += 1
        Text += f'''{i}.{ProductName}
    Количество: {Quantity}
    Общая стоимость: {FinalPrice}

'''
    Text += f'''
Общая количество товара: {0 if TotalProducts is None else TotalProducts} 
Общая стоимость: {0 if TotalPrice is None else TotalPrice} сум
'''
    await BOT.edit_message_text(chat_id=ChatId, message_id=MessageId, text=Text,
                                reply_markup=GenerateCartButtons(CartId))


@dp.callback_query_handler(lambda call: '🔒' in call.data)
async def Order(call: CallbackQuery):
    ChatId = call.message.chat.id
    MessageId = call.message.message_id
    await BOT.delete_message(ChatId, MessageId)
    _, CartId = call.data.split('_')
    UpdateUserCart(CartId)
    TotalProducts, TotalPrice = GetUserCart(CartId)
    Data = GetCartProductsData(CartId)

    QuantityForOrder = ''
    ProductsForOrder = ''
    FinalPriceForOrder = ''
    for i in Data:
        ProductsForOrder += f'{i[1]}\n'
    for i in Data:
        QuantityForOrder += f'{i[2]} '
    for i in Data:
        FinalPriceForOrder += f'{i[3]} '

    OrderId = InsertToOrdersTable(ChatId, ProductsForOrder, QuantityForOrder, TotalProducts, FinalPriceForOrder,
                                  TotalPrice)

    Text = ''
    i = 0
    for CartProductId, ProductName, Quantity, FinalPrice in Data:
        i += 1
        Text += f'''

{i}.{ProductName}
Количество: {Quantity}
Общая стоимость: {FinalPrice}

    '''
    Text += f'''
Общая количество товара: {0 if TotalProducts is None else TotalProducts} 
Общая стоимость: {0 if TotalPrice is None else TotalPrice} сум
    '''

    if TotalPrice is not None:
        try:
            InsertToHistoryTable(OrderId, ChatId, Text, TotalProducts, TotalPrice)
            await BOT.send_invoice(chat_id=ChatId, title=f'Заказ №{OrderId}', description=Text,
                                   payload='bot-defined invoice-payload', provider_token=os.getenv('PAYMENT'),
                                   currency='UZS',
                                   prices=[
                                       LabeledPrice(label='Общая стоимость', amount=int(TotalPrice * 100))
                                   ])
        except Exception as e:
            print(e)
    else:
        await BOT.answer_callback_query(call.id, 'Ваша корзина пуста')


def InsertToOrdersTable(ChatId, ProductName, Quantity, TotalQuantity, Price, TotalPrice):
    OrderId = randint(1, 100000000)
    InsertToOrders(OrderId, ChatId, ProductName, Quantity, TotalQuantity, Price, TotalPrice)
    return OrderId


# ------------------------------------------------Настройки


@dp.message_handler(regexp=r'⚙️Настройки')
async def Settings(message: Message):
    ChatId = message.chat.id
    await BOT.send_message(chat_id=ChatId, text='Выберите направление.', reply_markup=GenerateSettingsButton(ChatId))


@dp.callback_query_handler(lambda call: '👟' in call.data)
async def ChangeUserNumber(call: CallbackQuery):
    _, ChatId = call.data.split('_')
    await BOT.send_message(ChatId, 'Отправьте контакт.', )


@dp.callback_query_handler(lambda call: '🏳️' in call.data)
async def DeleteUser(call: CallbackQuery):
    _, ChatId = call.data.split('_')

    DeleteUserData(ChatId)
    await BOT.answer_callback_query(callback_query_id=call.id, text='Данные удалены')
    await call.message.answer(f'{call.message.from_user.full_name}. Добро пожаловать в мир Engine.',
                              reply_markup=GenerateContactButton())


# ------------------------------------------------История


@dp.message_handler(regexp=r'📔История')
async def ShowHistory(message: Message):
    ChatId = message.chat.id
    UserHistoryData = GetHistoryData(ChatId)
    for i in UserHistoryData:
        await BOT.send_message(ChatId, f'''{fmt.hbold('Заказ№')}{fmt.hbold(i[1])}
{i[3]}
''')




def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
