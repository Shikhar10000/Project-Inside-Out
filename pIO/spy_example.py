import spy
import time 
driver=spy.login("shikhar10000@live.com","1997shikhar")
spy.playlist("Inside Out 0.14",driver)
time.sleep(15)
spy.playlist("Inside Out 0.11",driver)
time.sleep(15)
spy.closedr(driver)