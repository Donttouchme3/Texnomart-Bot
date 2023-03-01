import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from WorkWithDataBase import GetProductLink


def GetUserAgent():
    UA = UserAgent()
    Headers = {
        'User-Agent': f'{UA.random}'
    }
    return Headers


def GetProductDetail(ProductsId):
    ProductLink = GetProductLink(ProductsId)[0]

    Html = requests.get(ProductLink, headers=GetUserAgent()).text
    Soup = BeautifulSoup(Html, 'html.parser')
    try:
        ProductDetail = Soup.find('div', class_='product-detail')
        ProductName = ProductDetail.find('h1', class_='product__name').get_text(strip=True)
        # --------ProductPrice

        ProductSite = ProductDetail.find('div', class_='product-detail__middle')
        ProductPriceSite = ProductSite.find('div', class_='middle__right')
        ProductPrice = ProductPriceSite.find('div', class_='price').get_text(strip=True)

        # --------ProductImage

        ProductImageLink = ProductDetail.find('div', class_='middle__left').find('div', class_='product__slider') \
            .find('div', class_='swiper-wrapper').find('div', class_='gallery-top__item').find('img').get('src')

        # --------ProductCharacteristics

        Characteristics = []
        ProductCharacteristicsItems = ProductDetail.find('div', class_='middle__center') \
            .find('ul', class_='characteristic__wrap').find_all('li', class_='characteristic__item')
        for ProductData in ProductCharacteristicsItems:
            ProductInfo = ProductData.find('span').get_text(strip=True)
            ProductValue = ProductData.find('span', class_='characteristic__value').get_text(strip=True)
            Data = f'{ProductInfo}: {ProductValue}'
            Characteristics.append(Data)
        return ProductLink, ProductName, ProductPrice, ProductImageLink, Characteristics

    except:
        print('Нету данных по продукту')
