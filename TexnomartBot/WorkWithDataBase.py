# ----------------- Users ------------------
import sqlite3

# -------------------------------------------РЕГИСТРАЦИЯ-----------------------------------
def GetChatId(ChatId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT UserId FROM Users WHERE ChatId = ?
    ''', (ChatId,))
    UserId = Cursor.fetchone()
    DataBase.close()
    return UserId


def InsertUsers(ChatId, UserName, Phone):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    try:
        Cursor.execute('''
        INSERT INTO Users(ChatId, UserName, Phone)  VALUES (?,?,?)
        ''', (ChatId, UserName, Phone))
        DataBase.commit()
        return True
    except:
        Cursor.execute('''
        UPDATE Users SET Phone = ? WHERE ChatId = ?
        ''', (Phone, ChatId))
        DataBase.commit()
        return False
    finally:
        DataBase.close()


def GerUserId(ChatId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT UserId FROM Users WHERE ChatId = ?
    ''', (ChatId,))
    UserId = Cursor.fetchone()[0]
    return UserId

def InsertToUsersCart(UserId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    INSERT INTO Carts(UserId) VALUES (?)
    ''', (UserId,))
    DataBase.commit()
    DataBase.close()


def DeleteUserData(ChatId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    DELETE FROM Users WHERE ChatId = ?
    ''', (ChatId,))
    DataBase.commit()
    DataBase.close()




# -------------------------------------------КНОПКИ-----------------------------------------

# ----------КАТЕГОРИИ
def GetCategoriesForShowMenu():
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT CategoryId, CategoryName FROM Categories;
    ''')
    Categories = Cursor.fetchall()
    DataBase.close()
    return Categories


def GetCategoryLinkById(CategoryId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT CategoryLink FROM Categories WHERE CategoryId = ?;
    ''', (CategoryId,))
    CategoryLink = Cursor.fetchone()
    DataBase.close()
    return CategoryLink


def GetCategoryName(CategoryId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT CategoryName FROM Categories WHERE CategoryId = ?
    ''', (CategoryId,))
    CategoryName = Cursor.fetchone()
    DataBase.close()
    return CategoryName

# ----------САБКАТЕГОРИИ


def GetSubcategoriesByCategoryId(CategoryId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT SubcategoryId, SubcategoryName FROM Subcategories WHERE CategoryId = ?;
    ''', (CategoryId, ))
    Subcategories = Cursor.fetchall()
    DataBase.close()
    return Subcategories


def GetSubcategoryLinkById(SubcategoryId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT SubcategoryLink FROM Subcategories WHERE SubcategoryId = ?;
    ''', (SubcategoryId,))
    SubcategoryLink = Cursor.fetchone()
    DataBase.close()
    return SubcategoryLink


def GetSubcategoryName(SubcategoryId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT SubcategoryName FROM Subcategories WHERE SubcategoryId = ?
    ''', (SubcategoryId,))
    SubcategoryName = Cursor.fetchone()
    DataBase.close()
    return SubcategoryName


def GetCategoryId(SubcategoryId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT CategoryId FROM Subcategories WHERE  SubcategoryId = ?
    ''', (SubcategoryId,))
    CategoryId = Cursor.fetchone()
    DataBase.close()
    return CategoryId

def GetSubcategoryId(SubcategoryTypeId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT SubcategoryId FROM SubcategoryTypes WHERE SubcategoryTypeId = ?
    ''', (SubcategoryTypeId,))
    SubcategoryId = Cursor.fetchone()
    DataBase.close()
    return SubcategoryId


# ----------ВИДЫСАБКАТЕГОРИЕВ


def GetSubcategoryTypeById(SubcategoryId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT SubcategoryTypeId, SubcategoryTypeName FROM SubcategoryTypes WHERE SubcategoryId = ?;
    ''', (SubcategoryId,))
    SubcategoryTypes = Cursor.fetchall()
    DataBase.close()
    return SubcategoryTypes

def GetSubcategoryTypeName(SubcategoryTypeId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT SubcategoryTypeName FROM SubcategoryTypes WHERE SubcategoryTypeId = ?
    ''', (SubcategoryTypeId,))
    SubcategoryTypeName = Cursor.fetchone()
    DataBase.close()
    return SubcategoryTypeName


# ----------Товары


def ShowProductsBySubcategoryId(SubcategoryId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT ProductId, ProductName FROM Products WHERE ProductSubId = ? AND SubcategoryId = ?
    ''', (0, SubcategoryId))
    Products = Cursor.fetchall()
    DataBase.close()
    return Products

def GetProducts(SubcategoryTypeId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT ProductId, ProductName FROM Products WHERE ProductSubId = ?
    ''', (SubcategoryTypeId,))
    Products = Cursor.fetchall()
    DataBase.close()
    return Products

def GetProductLink(ProductId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT ProductLink FROM Products WHERE ProductId = ?
    ''', (ProductId,))
    ProductLink = Cursor.fetchone()
    DataBase.close()
    return ProductLink

def InsertProductDetail(ProductId,  ProductName, ProductLink,  ProductImageLink, Characteristics, ProductPrice):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    INSERT INTO ProductDetail(ProductId, ProductName, ProductLink, ProductImageLink, Characteristics, ProductPrice)
    VALUES (?,?,?,?,?,?)
    ''', (ProductId,  ProductName, ProductLink,  ProductImageLink, Characteristics, ProductPrice))
    DataBase.commit()
    DataBase.close()


def CheckIfExistsProductInDataBase(ProductId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT ProductId FROM ProductDetail WHERE ProductId = ?
    ''', (ProductId,))
    ProductId1 = Cursor.fetchone()
    DataBase.close()
    return ProductId1


def GetProductDetailFromDataBase(ProductId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT * FROM ProductDetail WHERE ProductId = ?
    ''', (ProductId,))
    ProductDetail = Cursor.fetchone()
    DataBase.close()
    return ProductDetail

# ----------Корзина

def GetCartId(ChatId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT CartId FROM Carts WHERE UserId = (SELECT UserId FROM Users WHERE ChatId = ?)
    ''', (ChatId,))
    CartId = Cursor.fetchone()
    DataBase.close()
    return CartId

def InsertOrUpdateToCartProducts(CartId, ProductName, Quantity, FinalPrice):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    try:
        Cursor.execute('''
        INSERT INTO CartProducts(CartId, CartProductName, QUANTITY, FinalPrice)
        VALUES (?,?,?,?)
        ''', (CartId, ProductName, Quantity, FinalPrice))
        DataBase.commit()
        return True
    except:
        Cursor.execute('''
        UPDATE CartProducts
        SET QUANTITY = ?, FinalPrice = ? WHERE CartId = ?
        ''', (Quantity, FinalPrice, CartId))
        DataBase.commit()
        return False
    finally:
        DataBase.close()

def UpdateUserCart(CartId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    UPDATE Carts SET 
    TotalProducts = (SELECT SUM(QUANTITY) FROM CartProducts WHERE CartId = :CartId),
    TotalPrice = (SELECT SUM(FinalPrice) FROM CartProducts WHERE CartId = :CartId) 
    WHERE CartId = :CartId
    ''', {'CartId': CartId})
    DataBase.commit()
    DataBase.close()

def GetUserCart(CartId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT TotalProducts, TotalPrice FROM Carts WHERE CartId = ?
    ''', (CartId,))
    TotalProducts, TotalPrice = Cursor.fetchone()
    DataBase.close()
    return TotalProducts, TotalPrice


def GetCartProductsData(CartId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT CartProductId, CartProductName, QUANTITY, FinalPrice FROM CartProducts WHERE CartId = ?
    ''', (CartId,))
    Data = Cursor.fetchall()
    DataBase.close()
    return Data


def GetCartProductName(CartId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT CartProductId, CartProductName FROM CartProducts WHERE CartId = ?
    ''', (CartId,))
    CartProductNames = Cursor.fetchall()
    DataBase.close()
    return CartProductNames


def DeleteCartProduct(CartId, CartProductIt):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    DELETE FROM CartProducts WHERE CartId = ? AND CartProductId = ?
    ''', (CartId, CartProductIt))
    DataBase.commit()
    DataBase.close()


# ----------Заказы


def InsertToOrders(OrderId, ChatId, ProductName, Quantity, TotalQuantity, Price, TotalPrice):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    INSERT INTO Orders(OrderId, UserId, ProductName, Quantity, TotalQuantity, Price, TotalPrice)
    VALUES (?, (SELECT UserId FROM Users WHERE ChatId = ?), ?, ?, ?, ?, ?)
    ''', (OrderId, ChatId, ProductName, Quantity, TotalQuantity, Price, TotalPrice))
    DataBase.commit()
    DataBase.close()



def InsertToHistoryTable(OrderId, ChatId, Text, TotalProducts, TotalPrice):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    INSERT INTO History(OrderId, ChatId, Details, TotalProducts, TotalPrice) 
    VALUES (?,?,?,?,?)
    ''', (OrderId, ChatId, Text, TotalProducts, TotalPrice))
    DataBase.commit()
    DataBase.close()


def GetHistoryData(ChatId):
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.execute('''
    SELECT * FROM History WHERE ChatId = ? ORDER BY HistoryId DESC LIMIT 5
    ''', (ChatId,))
    History = Cursor.fetchall()
    DataBase.close()
    return History


















