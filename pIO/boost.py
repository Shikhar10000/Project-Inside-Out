from selenium import webdriver
import time 
import random
from selenium.webdriver.common.by import By
while 1:
	try:
		uname=['shikhar10000@live.com','stockedon@gmail.com']
		passw=['1997shikhar','1997shikhar']
		i=random.randint(0,1)
		driver = webdriver.Chrome(executable_path='./chromedriver.exe')
		url ='https://colab.research.google.com/'
		driver.get(url)
		time.sleep(1.5) 
		element = driver.find_element_by_xpath(("//a[contains(text(),'Sign in')]"))
		element.click()
		time.sleep(1.5)
		driver.find_element_by_xpath("//input[@id='identifierId']").send_keys(uname[i])
		driver.find_element_by_xpath(("//span[contains(text(),'Next')]")).click()
		time.sleep(1.5)
		driver.find_element_by_xpath("//input[@name='password']").send_keys(passw[i])
		driver.find_element_by_xpath(("//span[contains(text(),'Next')]")).click()
		driver.get('https://colab.research.google.com/drive/1ZWvMEBIZvyyXQV4FifTLwx1rMMh5NRKu?pli=1#forceEdit=true&sandboxMode=true')
		
			
		time.sleep(1.5)
		driver.find_element_by_xpath("//div[@class='cell-execution']").click()
		
		time.sleep(3)
		
		driver.find_element_by_xpath("//paper-button[@id='ok']").click()

		time.sleep(random.randint(60,200))
		driver.close()
	except:
		uname=['shikhar10000@live.com','stockedon@gmail.com']
		passw=['1997shikhar','1997shikhar']
		i=random.randint(0,1)
		driver = webdriver.Chrome(executable_path='./chromedriver.exe')
		url ='https://colab.research.google.com/'
		driver.get(url)
		time.sleep(1.5) 
		element = driver.find_element_by_xpath(("//a[contains(text(),'Sign in')]"))
		element.click()
		time.sleep(1.5)
		driver.find_element_by_xpath("//input[@id='identifierId']").send_keys(uname[i])
		driver.find_element_by_xpath(("//span[contains(text(),'Next')]")).click()
		time.sleep(1.5)
		driver.find_element_by_xpath("//input[@name='password']").send_keys(passw[i])
		driver.find_element_by_xpath(("//span[contains(text(),'Next')]")).click()
		driver.get('https://colab.research.google.com/drive/1ZWvMEBIZvyyXQV4FifTLwx1rMMh5NRKu?pli=1#forceEdit=true&sandboxMode=true')
		
			
		time.sleep(1.5)
		driver.find_element_by_xpath("//div[@class='cell-execution']").click()
		
		time.sleep(3)
		
		driver.find_element_by_xpath("//paper-button[@id='ok']").click()

		time.sleep(random.randint(60,200))
		driver.close()