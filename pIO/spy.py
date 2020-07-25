from selenium import webdriver
import time 
from selenium.webdriver.common.by import By
def login(uname,passw):
	driver = webdriver.Chrome(executable_path='./chromedriver.exe')
	url ='https://open.spotify.com/browse/featured'
	driver.get(url)
	element=element = driver.find_element_by_xpath(("//button[contains(text(),'Log in')]"))
	element.click()
	time.sleep(1.5) 
	driver.find_element_by_xpath("//input[@placeholder='Email address or username']").send_keys(uname)
	driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(passw)
	driver.find_element_by_id("login-button").click()
	return driver
def playlist(name,driver):
	time.sleep(1.5) 
	driver.find_element_by_xpath(("//span[contains(text(),'"+name.strip()+"')]")).click()
	time.sleep(1.5) 
	driver.find_element_by_xpath("//button[contains(text(),'PLAY')]").click()
	
def closedr(driver):
	driver.close()