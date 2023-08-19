from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
import time



# # Configuração do WebDriver para o Firefox
servico = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=servico)

# # Acesse o Gmail e faça login
# driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dgoogle%26oq%3Dg%26aqs%3Dchrome.1.69i57j0i131i433i512l9.835j0j7%26sourceid%3Dchrome%26ie%3DUTF-8&ec=GAZAAQ&hl=pt-BR&ifkv=AXo7B7UZ2FDm9XXEaLOOzhDyWyE4HTF4AF1s40CZLQlPi7YuKS6NhN2WPJdyWyHt-Q7dWhZb7R2vcQ&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-955898890%3A1692383685644420")
# email_input = driver.find_element('xpath','//*[@id="identifierId"]')
# email_input.send_keys("fernando.a.rosa02@gmail.com")
# time.sleep(5)
# next_button = driver.find_element('xpath','/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button')
# next_button.send_keys(Keys.ENTER)
# time.sleep(5)  # Aguarda para carregar a próxima página
# driver.find_element('xpath','/html/body/div[1]/div[1]/div[2]/div/c-wiz/div[2]/div[2]/div/div[2]/div/div/div/div/div/a').send_keys(Keys.ENTER)
# driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dgoogle%26oq%3Dg%26aqs%3Dchrome.1.69i57j0i131i433i512l9.835j0j7%26sourceid%3Dchrome%26ie%3DUTF-8&ec=GAZAAQ&hl=pt-BR&ifkv=AXo7B7UZ2FDm9XXEaLOOzhDyWyE4HTF4AF1s40CZLQlPi7YuKS6NhN2WPJdyWyHt-Q7dWhZb7R2vcQ&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-955898890%3A1692383685644420")

# # Encerre a sessão do driver

def criar_email():
 # criar o email temporario
    name = "roberto"

    driver.get("https://www.mohmal.com/pt")
    time.sleep(5)
    driver.find_element('xpath','//*[@id="choose"]').click()
    driver.find_element('xpath','/html/body/div[1]/main/div[1]/form/div[1]/div[1]/input').send_keys(name)
    time.sleep(2)
    driver.find_element('xpath','//*[@id="next"]').click()
    time.sleep(2)
    driver.find_element('xpath','//*[@id="create"]').click()
    time.sleep(5)

def testar_login():

    driver.get("http://127.0.0.1:5000")
    time.sleep(5)


criar_email()



