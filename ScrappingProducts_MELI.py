import urllib.request
from random import randint

from bs4 import BeautifulSoup

QUERY_PART_INSERT = "INSERT INTO `product` (`Product_PymeProf_Id`, `Product_CatProd_Id`, `Product_Name`, `Product_Description`, `Product_Img_Url`, `Product_Search_Url`, `Product_Unit_Price`, `Product_Offer`, `Product_Date_Created`, `Product_Last_Update`, `Product_Is_Free_Shipping`)"
QUERY_PART_VALUES = " VALUES ({}, 6, '{}', '{}', '{}', '{}', {}, {}, NOW(), NOW(), {});"
QUERY = ""
QUOT = "\n"
html = urllib.request.urlopen("https://listado.mercadolibre.cl/cafe#D[A:cafe]").read().decode()
soup = BeautifulSoup(html)
results = soup.find(id='root-app')

liProducts = results.find_all('li', class_='ui-search-layout__item')
print("Length de LiProducts: " + str(len(liProducts)))

file = open("INSERT_PRODUCTS2.sql", "w+")


def setInsertValues(randomPyme, titleProduct, descProduct, dataSrc, urlSearch, priceProduct, discount, isFreeShipping):
    QUERY = QUERY_PART_INSERT + QUERY_PART_VALUES.format(randomPyme, titleProduct, descProduct, dataSrc, urlSearch,
                                                         priceProduct, discount, isFreeShipping)
    file.write(QUERY)
    file.write(QUOT)


for liProd in liProducts:
    div = liProd.find('div',
                      class_='andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core '
                             'andes-card--padding-default')
    if div is None:
        div = liProd.find('div',
                          class_='andes-card andes-card--flat andes-card--default ui-search-result '
                                 'ui-search-result--core ui-search-result--advertisement andes-card--padding-default')

    # Obtain title of product
    divWrapperDesc = div.find('div', class_='ui-search-result__content-wrapper')
    divWrapperDescH2 = divWrapperDesc.find('h2', class_='ui-search-item__title')
    discountSpan = divWrapperDesc.find('span', class_='ui-search-price__discount')
    priceSpan = divWrapperDesc.find('span', class_='price-tag-fraction')
    freeShippingP = divWrapperDesc.find('p', class_='ui-search-item__shipping ui-search-item__shipping--free')
    isFreeShipping = 0
    if freeShippingP is not None:
        isFreeShipping = 1
    discount = 0
    if discountSpan is not None:
        discount = discountSpan.contents[0]
        discount = discount[0:2]
    divImg = div.find('div', class_='slick-slide slick-active')
    img = divImg.find('img')

    titleProduct = divWrapperDescH2.contents[0]
    descProduct = img.get('alt')
    dataSrc = img.get('data-src')
    urlSearch = dataSrc.split("/")[-1].replace(".jpg", "")
    priceProduct = priceSpan.contents[0].replace(".", "")
    randomPyme = randint(1, 2)

    setInsertValues(randomPyme, titleProduct, descProduct, dataSrc, urlSearch, priceProduct, discount, isFreeShipping)

file.close()
