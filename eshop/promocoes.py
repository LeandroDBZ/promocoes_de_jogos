from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

navegador = webdriver.Chrome()
navegador.maximize_window()
navegador.get("https://www.nintendo.com/pt-br/store/games/")

checkbox = navegador.find_element(By.XPATH, '//*[@name="Promoções"]').click()
sleep(2)
games = []
titulos = navegador.find_elements(By.CSS_SELECTOR, 'h2.iiGOlC')
links = navegador.find_elements(By.CSS_SELECTOR, 'a.gDYrMS')
datas = navegador.find_elements(By.CSS_SELECTOR, 'div.bvcBeK')
precos_normal = navegador.find_elements(By.CSS_SELECTOR, 'span.iCuvmX')
precos_desconto = navegador.find_elements(By.CSS_SELECTOR, 'span.gZmNpQ')
descontos = navegador.find_elements(By.CSS_SELECTOR, 'div.csTVoz')
periodos = navegador.find_elements(By.CSS_SELECTOR, 'div.gXVfCV ')

for titulo, data, preco_normal, preco_desconto, desconto, periodo, link in zip(titulos, datas, precos_normal, precos_desconto, descontos, periodos, links):
    games.append([titulo.text, 
                  data.text.replace('Data de lançamento ', ''), 
                  preco_normal.text.replace('Preço normal:\n', ''), 
                  preco_desconto.text.replace('Preço promocional:\n', ''), 
                  desconto.text, 
                  periodo.text.replace('A oferta termina em: ', ''),
                  link.get_attribute('href')])

lista = pd.DataFrame(games, columns=['Título','Data de Lançamento', 'Preço Normal', 'Preço Promocional', 'Desconto', 'A oferta termina em', 'Link da Oferta'])
lista.to_csv('eshop.csv', index=False)
