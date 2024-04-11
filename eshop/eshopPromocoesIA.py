from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

class NintendoEshopScraper:
    def __init__(self):
        self.navegador = webdriver.Chrome()
        self.navegador.maximize_window()
        self.navegador.get("https://www.nintendo.com/pt-br/store/games/")

    def click_checkbox(self):
        checkbox = self.navegador.find_element(By.XPATH, '//*[@name="Promoções"]')
        checkbox.click()
        sleep(2)

    def scrape_games(self):
        games = []
        titulos = self.navegador.find_elements(By.CSS_SELECTOR, 'h2.iiGOlC')
        links = self.navegador.find_elements(By.CSS_SELECTOR, 'a.gDYrMS')
        datas = self.navegador.find_elements(By.CSS_SELECTOR, 'div.bvcBeK')
        precos_normal = self.navegador.find_elements(By.CSS_SELECTOR, 'span.iCuvmX')
        precos_desconto = self.navegador.find_elements(By.CSS_SELECTOR, 'span.gZmNpQ')
        descontos = self.navegador.find_elements(By.CSS_SELECTOR, 'div.csTVoz')
        periodos = self.navegador.find_elements(By.CSS_SELECTOR, 'div.gXVfCV')

        try:
            while True:
                for titulo, data, preco_normal, preco_desconto, desconto, periodo, link in zip(titulos, datas, precos_normal, precos_desconto, descontos, periodos, links):
                    games.append([titulo.text,
                                  data.text.replace('Data de lançamento ', ''),
                                  preco_normal.text.replace('Preço normal:\n', ''),
                                  preco_desconto.text.replace('Preço promocional:\n', ''),
                                  desconto.text,
                                  periodo.text.replace('A oferta termina em: ', ''),
                                  link.get_attribute('href')])
                sleep(1)
                carregar = self.navegador.find_element(By.CSS_SELECTOR, 'button.cwaeYW')
                carregar.click()
        except:
            print("Não há mais paginas a ser carregada!")

        return games

    def close_browser(self):
        self.navegador.quit()

if __name__ == "__main__":
    scraper = NintendoEshopScraper()
    scraper.click_checkbox()
    scraped_games = scraper.scrape_games()
    scraper.close_browser()

    lista = pd.DataFrame(scraped_games, columns=['Título', 'Data de Lançamento', 'Preço Normal', 'Preço Promocional', 'Desconto', 'A oferta termina em', 'Link da Oferta'])
    lista.to_csv('eshop.csv', index=False)
