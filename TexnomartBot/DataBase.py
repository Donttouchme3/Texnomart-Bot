import sqlite3


def CreateUsersCart():
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.executescript('''
    DROP TABLE IF EXISTS Carts;
    
    CREATE TABLE IF NOT EXISTS Carts(
        CartId INTEGER PRIMARY KEY AUTOINCREMENT,
        UserId INTEGER REFERENCES Users(UserId) UNIQUE,
        TotalProducts INTEGER DEFAULT 0,
        TotalPrice DECIMAL(12, 2) DEFAULT 0
    );
    ''')
    DataBase.commit()
    DataBase.close()


def CreateCartProductS():
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.executescript('''
    DROP TABLE IF EXISTS CartProducts;
    
    CREATE TABLE IF NOT EXISTS CartProducts(
        CartProductId INTEGER PRIMARY KEY AUTOINCREMENT,
        CartId INTEGER REFERENCES Carts(CartId),
        CartProductName TEXT,
        QUANTITY INTEGER DEFAULT 1,
        FinalPrice DECIMAL(12, 2),
        UNIQUE(CartId, CartProductName)
    );
    ''')
    DataBase.commit()
    DataBase.close()



def CreateUsersTable():
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.executescript('''
    DROP TABLE IF EXISTS Users;
    CREATE TABLE IF NOT EXISTS Users(
        UserId INTEGER PRIMARY KEY AUTOINCREMENT,
        ChatId BIGINT UNIQUE,
        UserName TEXT,
        Phone TEXT UNIQUE
    );
    ''')
    DataBase.commit()
    DataBase.close()


# CreateUsersCart()
# CreateUsersTable()

def CreateProductDetailTable():
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.executescript('''
    DROP TABLE IF EXISTS ProductDetail;
    
    CREATE TABLE IF NOT EXISTS ProductDetail(
        ProductId INTEGER REFERENCES Products(ProductId),
        ProductName TEXT UNIQUE,
        ProductLink TEXT,
        ProductImageLink TEXT,
        Characteristics TEXT,
        ProductPrice DECIMAL(12, 2)
    );
    ''')
    DataBase.commit()
    DataBase.close()


def CreateOrdersTable():
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.executescript('''
    DROP TABLE IF EXISTS Orders;
    
    CREATE TABLE IF NOT EXISTS Orders(
        OrderId BIGINT,
        UserId INTEGER REFERENCES Users(UserId),
        ProductName TEXT,
        Quantity INT,
        TotalQuantity INT,
        Price TEXT,
        TotalPrice DECIMAL(12, 2),
        UNIQUE(UserId, OrderId)
    );
    ''')
    DataBase.commit()
    DataBase.close()


def CreateHistoryTable():
    DataBase = sqlite3.connect('TexnomartBot.db')
    Cursor = DataBase.cursor()
    Cursor.executescript('''
    DROP TABLE IF EXISTS History;
    
    CREATE TABLE IF NOT EXISTS History(
        HistoryId INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderId TEXT,
        ChatId INTEGER REFERENCES Users(ChatId),
        Details TEXT,
        TotalProducts INT,
        TotalPrice DECIMAL(12, 2)
    );
    ''')
    DataBase.commit()
    DataBase.close()

