from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

navegador = webdriver.Chrome()
navegador.maximize_window()
navegador.get("https://store.playstation.com/pt-br/pages/latest")

webStoreTab = navegador.find_element(By.XPATH, '//*[@id="tertiary-menu-toggle"]/li[3]/a').click()
sleep(2)
todasPromocoes = navegador.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/section/header/div[2]/div[2]/a').click()
sleep(2)
plataforma = navegador.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div/div[3]/div/div/div/div[3]/div[2]/ul/li[4]/div/header/button').click()
sleep(2)
jogosPs4 = navegador.find_element(By.XPATH, '//*[@id="targetPlatforms:PS4"]').click()
sleep(2)

games = []

paginas = navegador.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div/div[2]/div[2]/div/nav/ol/li[5]/button')
sleep(2)
contador = int(paginas.get_property('value'))
print(contador)
sleep(2)
i = 1
while i < contador:
    i+=1
    navegador.find_element(By.XPATH, '//button[@aria-label="Ir para a próxima página"]').click()
    sleep(2)
    titulos = navegador.find_elements(By.XPATH, '//span[contains(@data-qa, "product-name")]')
    links = navegador.find_elements(By.XPATH, '//a[@class="psw-link psw-content-link"]')
    descontos = navegador.find_elements(By.XPATH, '//span[contains(@data-qa, "discount-badge")]')
    precoDescontos = navegador.find_elements(By.XPATH, '//span[@class="psw-m-r-3"]')
    precoCheios = navegador.find_elements(By.XPATH, '//s[@class="psw-c-t-2"]')
    for titulo, link, desconto, precoDesconto, precoCheio in zip(titulos, links, descontos, precoDescontos, precoCheios):
        games.append([titulo.text, link.get_attribute('href'), desconto.text, precoDesconto.text, precoCheio.text])
else:
    print("Chegou ao fim")

lista = pd.DataFrame(games, columns=['Título', 'Link da Oferta', 'Desconto', 'Preço Promocional', 'Preço Normal'])
lista.to_csv('psn.csv', index=False)