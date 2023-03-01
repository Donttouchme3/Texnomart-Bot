from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from WorkWithDataBase import *


def GenerateContactButton():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='Регистрация', request_contact=True)]
    ], resize_keyboard=True)


def GenerateMainMenu():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='✔️Сделать заказ')],
        [KeyboardButton(text='📔История'), KeyboardButton(text='🛒Корзина'), KeyboardButton(text='⚙️Настройки')]
    ], resize_keyboard=True)


# ------------------------------------------------КАТАЛОГ


def GenerateCatalogMenu(Count=0):
    Markup = InlineKeyboardMarkup(row_width=2)
    Categories = GetCategoriesForShowMenu()
    if len(Categories) > 10:
        Buttons = []
        for Category in Categories[:10]:
            Button = InlineKeyboardButton(text=f'{Category[1]}', callback_data=f'category_{Category[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='Следующая страница⏭️', callback_data=f'next_{Count}')
        )
        return Markup
    else:
        Buttons = []
        for Category in Categories:
            Button = InlineKeyboardButton(text=f'{Category[1]}', callback_data=f'category_{Category[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        return Markup


def GenerateNextCatalogPage(Count):
    Markup = InlineKeyboardMarkup(row_width=2)
    Categories = GetCategoriesForShowMenu()

    if (len(Categories) - Count) > 10:
        Buttons = []
        for Category in Categories[10:20]:
            Button = InlineKeyboardButton(text=f'{Category[1]}', callback_data=f'category_{Category[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='Следующая страница⏭️', callback_data=f'next_{Count}')
        )
        return Markup
    else:
        Buttons = []
        Len = len(Categories)
        for Category in Categories[Count: Len]:
            Button = InlineKeyboardButton(text=f'{Category[1]}', callback_data=f'category_{Category[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='⏮️Предыдущая страница', callback_data=f'previous_{Count}')
        )
        return Markup


def GeneratePreviousCatalogPage(LastCount, Count):
    Markup = InlineKeyboardMarkup(row_width=2)
    Categories = GetCategoriesForShowMenu()
    Buttons = []
    for Category in Categories[Count: LastCount]:
        Button = InlineKeyboardButton(text=f'{Category[1]}', callback_data=f'category_{Category[0]}')
        Buttons.append(Button)
    Markup.add(*Buttons)
    Markup.row(
        InlineKeyboardButton(text='Следующая страница⏭️', callback_data=f'next_{Count}')
    )
    return Markup


# ------------------------------------------------САБКАТЕГОРИИ


def GenerateShowSubcategoryId(CategoryId):
    Markup = InlineKeyboardMarkup(row_width=2)
    Subcategories = GetSubcategoriesByCategoryId(CategoryId)
    Buttons = []
    for Subcategory in Subcategories:
        Button = InlineKeyboardButton(text=f'{Subcategory[1]}', callback_data=f'sub_{Subcategory[0]}')
        Buttons.append(Button)
    Markup.add(*Buttons)
    Markup.row(
        InlineKeyboardButton(text='Назад', callback_data='MainMenu')
    )
    return Markup


# ------------------------------------------------ВИДЫСАБКАТЕГОРИИ


def GenerateSubcategoryTypesMenu(SubcategoryId, Count=0):
    Markup = InlineKeyboardMarkup(row_width=1)
    if GetSubcategoryTypeById(SubcategoryId):
        SubcategoryTypes = GetSubcategoryTypeById(SubcategoryId)
        if len(SubcategoryTypes) > 10:
            Buttons = []
            for SubcategoryType in SubcategoryTypes[:10]:
                Button = InlineKeyboardButton(text=f'{SubcategoryType[1]}', callback_data=f'type_{SubcategoryType[0]}')
                Buttons.append(Button)
            Markup.add(*Buttons)
            Markup.row(
                InlineKeyboardButton(text='Следующая страница⏭️', callback_data=f'➕_{Count+10}_{SubcategoryId}')
            )
            Markup.row(
                InlineKeyboardButton(text='Назад', callback_data=f'back_{SubcategoryId}')
            )
            return Markup
        else:
            Buttons = []
            for SubcategoryType in SubcategoryTypes:
                Button = InlineKeyboardButton(text=f'{SubcategoryType[1]}', callback_data=f'type_{SubcategoryType[0]}')
                Buttons.append(Button)
            Markup.add(*Buttons)
            Markup.row(
                InlineKeyboardButton(text='Назад', callback_data=f'back_{SubcategoryId}')
            )
            return Markup

    else:
        Products = ShowProductsBySubcategoryId(SubcategoryId)
        if len(Products) > 10:
            Buttons = []
            for Product in Products[:10]:
                Button = InlineKeyboardButton(text=f'{Product[1]}', callback_data=f'product_{Product[0]}')
                Buttons.append(Button)
            Markup.add(*Buttons)
            Markup.row(
                InlineKeyboardButton(text='Следующая страница⏭️',
                                     callback_data=f'NextProductPage_{Count}_{SubcategoryId}')
            )
            Markup.row(
                InlineKeyboardButton(text='К категориям', callback_data=f'back_{SubcategoryId}')
            )
            return Markup
        else:
            Buttons = []
            for Product in Products:
                Button = InlineKeyboardButton(text=f'{Product[1]}', callback_data=f'product_{Product[0]}')
                Buttons.append(Button)
            Markup.add(*Buttons)
            Markup.row(
                InlineKeyboardButton(text='К категориям', callback_data=f'back_{SubcategoryId}')
            )
            return Markup


def GenerateNextSubcategoryType(Count, SubcategoryId):
    SubcategoryTypes = GetSubcategoryTypeById(SubcategoryId)
    Markup = InlineKeyboardMarkup(row_width=1)
    if len(SubcategoryTypes) - Count > 10:
        Buttons = []
        for SubcategoryType in SubcategoryTypes[Count: Count + 10]:
            Button = InlineKeyboardButton(text=f'{SubcategoryType[1]}', callback_data=f'type_{SubcategoryType[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='⏮️Предыдущая',
                                 callback_data=f'➖_{Count-10}_{SubcategoryId}'),
            InlineKeyboardButton(text='Следующая⏭️',
                                 callback_data=f'➕_{Count+10}_{SubcategoryId}')
        )
        Markup.row(
            InlineKeyboardButton(text='Назад', callback_data=f'back_{SubcategoryId}')
        )
    else:
        Buttons = []
        for SubcategoryType in SubcategoryTypes[Count: len(SubcategoryTypes) + 1]:
            Button = InlineKeyboardButton(text=f'{SubcategoryType[1]}', callback_data=f'type_{SubcategoryType[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='⏮️Предыдущая страница',
                                 callback_data=f'➖_{Count - 10}_{SubcategoryId}'))
        Markup.row(
            InlineKeyboardButton(text='Назад', callback_data=f'back_{SubcategoryId}')
        )
    return Markup


def GeneratePreviousSubcategoryType(Count, SubcategoryId):
    SubcategoryTypes = GetSubcategoryTypeById(SubcategoryId)
    Markup = InlineKeyboardMarkup(row_width=1)
    if Count == 0:
        Buttons = []
        for SubcategoryType in SubcategoryTypes[:Count+10]:
            Button = InlineKeyboardButton(text=f'{SubcategoryType[1]}', callback_data=f'type_{SubcategoryType[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='Следующая страница⏭️', callback_data=f'➕_{Count + 10}_{SubcategoryId}')
        )
        Markup.row(
            InlineKeyboardButton(text='Назад', callback_data=f'back_{SubcategoryId}')
        )
    else:
        Buttons = []
        for SubcategoryType in SubcategoryTypes[Count: Count+10]:
            Button = InlineKeyboardButton(text=f'{SubcategoryType[1]}', callback_data=f'type_{SubcategoryType[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='⏮️Предыдущая',
                                 callback_data=f'➖_{Count - 10}_{SubcategoryId}'),
            InlineKeyboardButton(text='Следующая⏭️',
                                 callback_data=f'➕_{Count + 10}_{SubcategoryId}')
        )
        Markup.row(
            InlineKeyboardButton(text='Назад', callback_data=f'back_{SubcategoryId}')
        )
    return Markup



# ------------------------------------------------ПРОДУКТЫ БЕЗ САБКАТЕГОРИИ


def GenerateNextProductPage(count, subcategory_id):
    markup = InlineKeyboardMarkup(row_width=1)
    products = ShowProductsBySubcategoryId(subcategory_id)
    if (len(products) - count) > 10:
        buttons = []
        for product in products[count: count + 10]:
            button = InlineKeyboardButton(text=f'{product[1]}', callback_data=f'product_{product[0]}')
            buttons.append(button)
        markup.add(*buttons)
        markup.row(
            InlineKeyboardButton(text='⏮️Предыдущая страница',
                                 callback_data=f'😏_{count}_{subcategory_id}')
        )
        return markup
    else:
        buttons = []
        for product in products[count: len(products) + 1]:
            button = InlineKeyboardButton(text=f'{product[1]}', callback_data=f'product_{product[0]}')
            buttons.append(button)
        markup.add(*buttons)
        markup.row(
            InlineKeyboardButton(text='⏮️Предыдущая страница',
                                 callback_data=f'😏_{count}_{subcategory_id}')
        )
        return markup


def GeneratePreviousProductPage(Count, SubcategoryId):
    Products = ShowProductsBySubcategoryId(SubcategoryId)
    Markup = InlineKeyboardMarkup(row_width=1)
    Buttons = []
    for Product in Products[Count - 10: Count]:
        Button = InlineKeyboardButton(text=f'{Product[1]}', callback_data=f'product_{Product[0]}')
        Buttons.append(Button)
    Markup.add(*Buttons)
    Markup.row(
        InlineKeyboardButton(text='Следующая страница⏭️', callback_data=f'NextProductPage_{Count - 10}_{SubcategoryId}')
    )
    Markup.row(
        InlineKeyboardButton(text='К категориям', callback_data=f'back_{SubcategoryId}')
    )
    return Markup


# ------------------------------------------------Товары


def GenerateProductsMenu(SubcategoryTypeId, Count=0):
    Products = GetProducts(SubcategoryTypeId)
    Markup = InlineKeyboardMarkup(row_width=1)
    if len(Products) > 10:
        Buttons = []
        for Product in Products[:10]:
            Button = InlineKeyboardButton(text=f'{Product[1]}', callback_data=f'product_{Product[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='Следующая страница⏭️',
                                 callback_data=f'⏫_{Count}_{SubcategoryTypeId}')
        )
        Markup.row(
            InlineKeyboardButton(text='Назад', callback_data=f'❗_{SubcategoryTypeId}')
        )
    else:
        Buttons = []
        for Product in Products[:10]:
            Button = InlineKeyboardButton(text=f'{Product[1]}', callback_data=f'product_{Product[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='Назад', callback_data=f'❗_{SubcategoryTypeId}')
        )
    return Markup


def GenerateNextProductsPage(Count, SubcategoryTypeId):
    Products = GetProducts(SubcategoryTypeId)
    Markup = InlineKeyboardMarkup(row_width=1)
    if len(Products) - Count > 10:
        Buttons = []
        for Product in Products[Count: Count + 10]:
            Button = InlineKeyboardButton(text=f'{Product[1]}', callback_data=f'product_{Product[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='⏮️Предыдущая',
                                 callback_data=f'⏬_{Count}_{SubcategoryTypeId}'),
            InlineKeyboardButton(text='Следующая⏭️',
                                 callback_data=f'⏫_{Count}_{SubcategoryTypeId}')

        )
        Markup.row(
            InlineKeyboardButton(text='Назад', callback_data=f'❗_{SubcategoryTypeId}')
        )
    else:
        Buttons = []
        for Product in Products[Count: len(Products) + 1]:
            Button = InlineKeyboardButton(text=f'{Product[1]}', callback_data=f'product_{Product[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='⏮️Предыдущая страница',
                                 callback_data=f'⏬_{Count}_{SubcategoryTypeId}')
        )
        Markup.row(
            InlineKeyboardButton(text='Назад', callback_data=f'❗_{SubcategoryTypeId}')
        )
    return Markup


def GeneratePreviousProductsPage(Count, SubcategoryTypeId):
    Products = GetProducts(SubcategoryTypeId)
    Markup = InlineKeyboardMarkup(row_width=1)
    if Count == 0:
        Buttons = []
        for Product in Products[:Count+10]:
            Button = InlineKeyboardButton(text=f'{Product[1]}', callback_data=f'product_{Product[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='Следующая страница⏭️',
                                 callback_data=f'⏫_{Count}_{SubcategoryTypeId}')
        )
        Markup.row(
            InlineKeyboardButton(text='Назад', callback_data=f'❗_{SubcategoryTypeId}')
        )
    else:
        Buttons = []
        for Product in Products[Count:Count + 10]:
            Button = InlineKeyboardButton(text=f'{Product[1]}', callback_data=f'product_{Product[0]}')
            Buttons.append(Button)
        Markup.add(*Buttons)
        Markup.row(
            InlineKeyboardButton(text='⏮️Предыдущая',
                                 callback_data=f'⏬_{Count}_{SubcategoryTypeId}'),
            InlineKeyboardButton(text='Следующая⏭️',
                                 callback_data=f'⏫_{Count}_{SubcategoryTypeId}')

        )
        Markup.row(
            InlineKeyboardButton(text='Назад', callback_data=f'❗_{SubcategoryTypeId}')
        )
    return Markup


def GenerateBuyButton(ProductId):
    Markup = InlineKeyboardMarkup()
    Markup.row(
        InlineKeyboardButton(text='Добавить в корзину', callback_data=f'🛎️_{ProductId}')
    )
    Markup.row(
        InlineKeyboardButton(text='Вернуться назад', callback_data=f'⛔')
    )
    return Markup


def GenerateQuantityButton(ProductId, Quantity=1):
    Markup = InlineKeyboardMarkup()
    Buttons = [
        InlineKeyboardButton(text='<', callback_data=f'⬅️_{ProductId}_{Quantity}'),
        InlineKeyboardButton(text=f'{Quantity}', callback_data=f'🎫_{ProductId}_{Quantity}'),
        InlineKeyboardButton(text='>', callback_data=f'➡️_{ProductId}_{Quantity}'),
        InlineKeyboardButton(text='🚫', callback_data=f'⛔')
    ]
    Markup.add(*Buttons)
    return Markup

# ------------------------------------------------Корзина


def GenerateCartButtons(CartId):
    Markup = InlineKeyboardMarkup(row_width=1)
    Buttons = []
    CartProductData = GetCartProductName(CartId)
    for i in CartProductData:
        Button = InlineKeyboardButton(text=f'❌ {i[1]}', callback_data=f'☠️_{CartId}_{i[0]}')
        Buttons.append(Button)
    Markup.add(*Buttons)
    Markup.row(
        InlineKeyboardButton(text='🎁 Оформить заказ', callback_data=f'🔒_{CartId}')
    )
    return Markup


def GenerateSettingsButton(ChatId):
    Markup = InlineKeyboardMarkup()
    Markup.row(
        InlineKeyboardButton(text='✍🏽Изменить номер', callback_data=f'👟_{ChatId}'),
        InlineKeyboardButton(text='💀Удалить аккаунт', callback_data=f'🏳️_{ChatId}')
    )
    return Markup



