import time

from bs4 import BeautifulSoup
from selenium import webdriver


class Pyme:

    def __init__(self, TitlePymes, DescrPymes, imgPymes, urlSearchPyme):
        self.TitlePymes = TitlePymes
        self.DescrPymes = DescrPymes
        self.imgPymes = imgPymes
        self.urlSearchPyme = urlSearchPyme

    def __str__(self):
        return "[+] Title: {0} \n[+] Description: {1} \n[+] ImgUrl: {2} \n[+] SearchUrl: {3}" \
            .format(self.TitlePymes, self.DescrPymes, self.imgPymes, self.urlSearchPyme)


driver = webdriver.Chrome("../chromedriver.exe")
driver.get("https://www.comprapyme.cl/search")
time.sleep(5)
htmlSource = driver.page_source
soup = BeautifulSoup(htmlSource)

# Se hace click en boton para cargar mas pymes
submit_button = driver.find_elements_by_xpath('//*[@id="root"]/div/div[4]/div[2]/div[2]/div/button')[0]
submit_button.click()

# se espera 5seg para que cargen las nuevas pymes
time.sleep(5)

# Se toma nueamente el html
htmlSource = driver.page_source
soup = BeautifulSoup(htmlSource)

results = soup.find(id='root')
divImgPymes = results.find_all('img', class_='img-square')
divTitlePymes = results.find_all('div', class_="item-box-description l-p-10")
divDescrPymes = results.find_all('span', class_="card-special-factor")

print("======================================================================")
print("[+] Pymes totales: " + str(len(divImgPymes)))
print("======================================================================")

listPymes = []
i = 0

while i <= ((len(divImgPymes)) - 1):
    imgPymes = str(divImgPymes[i].get('src'))
    # print(imgPymes)
    if imgPymes.endswith(".svg"):
        urlSearchPyme = ""
        imgPymes = "X.svg"
        pass
    else:
        urlSearchPyme = imgPymes[0:(imgPymes.index('.image'))]
    TitlePymes = str(divTitlePymes[i].find('strong').contents[0])

    # Se utiliza titulo de pyme con _ para la URL de busqueda
    urlSearchPyme = \
        TitlePymes \
            .replace(" ", "_") \
            .replace("&", "_") \
            .replace("@", "") \
            .replace(",", "") \
            .replace(";", "") \
            .lower()
    try:
        DescrPymes = str(divDescrPymes[i].contents[0])
    except IndexError:
        DescrPymes = TitlePymes
        pass
    i = i + 1;
    pymeTmp = Pyme(TitlePymes, DescrPymes, imgPymes, urlSearchPyme);
    listPymes.append(pymeTmp)

print("Pymes validas: ", len(listPymes))

# =========== Se crean las querys a partir de las pymes validas ===========

file = open("INSERT_PYMES.sql", "w+")

QUERY_PART_INSERT = "INSERT INTO `pyme_markets`.`pyme_profile` (`PymeProf_Name`, `PymeProf_Icon_Url`, `PymeProf_Img_Url`, `PymeProf_Search_Url`, `PyProf_Date_Created`)"
QUERY_PART_VALUES = " VALUES ('{0}', '{1}', '{2}', '{3}', NOW());"
QUERY = ""
QUOT = "\n"


def setInsertValues(pyme):
    QUERY = QUERY_PART_INSERT + QUERY_PART_VALUES.format(pyme.TitlePymes, pyme.imgPymes, pyme.imgPymes,
                                                         pyme.urlSearchPyme)
    file.write(QUERY)
    file.write(QUOT)


# Se eliminan pymes que tengas imagen por defecto
for pyme in listPymes:
    if pyme.imgPymes.endswith('.svg'):
        listPymes.remove(pyme)

# Se crea la querys
for pyme in listPymes:
    setInsertValues(pyme)
