from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

class PSNStoreScraper:
    def __init__(self):
        self.navegador = webdriver.Chrome()
        self.navegador.maximize_window()
        self.navegador.get("https://store.playstation.com/pt-br/pages/latest")

    def navigate_to_promotions(self):
        webStoreTab = self.navegador.find_element(By.XPATH, '//*[@id="tertiary-menu-toggle"]/li[3]/a').click()
        sleep(2)
        todasPromocoes = self.navegador.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/section/header/div[2]/div[2]/a').click()
        sleep(2)

    def filter_by_platform(self):
        plataforma = self.navegador.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div/div[3]/div/div/div/div[3]/div[2]/ul/li[4]/div/header/button').click()
        sleep(2)
        jogosPs4 = self.navegador.find_element(By.XPATH, '//*[@id="targetPlatforms:PS4"]').click()
        sleep(2)

    def scrape_games(self):
        games = []
        paginas = self.navegador.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div/div[2]/div[2]/div/nav/ol/li[5]/button')
        contador = int(paginas.get_property('value'))
        print(contador)
        sleep(2)
        i = 1
        while i < contador:
            i += 1
            self.navegador.find_element(By.XPATH, '//button[@aria-label="Ir para a próxima página"]').click()
            sleep(2)
            titulos = self.navegador.find_elements(By.XPATH, '//span[contains(@data-qa, "product-name")]')
            links = self.navegador.find_elements(By.XPATH, '//a[@class="psw-link psw-content-link"]')
            descontos = self.navegador.find_elements(By.XPATH, '//span[contains(@data-qa, "discount-badge")]')
            precoDescontos = self.navegador.find_elements(By.XPATH, '//span[@class="psw-m-r-3"]')
            precoCheios = self.navegador.find_elements(By.XPATH, '//s[@class="psw-c-t-2"]')
            for titulo, link, desconto, precoDesconto, precoCheio in zip(titulos, links, descontos, precoDescontos, precoCheios):
                games.append([titulo.text, link.get_attribute('href'), desconto.text, precoDesconto.text, precoCheio.text])
        else:
            print("Chegou ao fim")
        return games

    def close_browser(self):
        self.navegador.quit()
        print("Data scraped successfully and saved to psn.csv")

if __name__ == "__main__":
    psn_scraper = PSNStoreScraper()
    psn_scraper.navigate_to_promotions()
    psn_scraper.filter_by_platform()
    scraped_games = psn_scraper.scrape_games()
    lista = pd.DataFrame(scraped_games, columns=['Título', 'Link da Oferta', 'Desconto', 'Preço Promocional', 'Preço Normal'])
    lista.to_csv('psn.csv', index=False)
    psn_scraper.close_browser()
