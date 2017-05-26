from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

fp = webdriver.FirefoxProfile()
# mime_types = "application/octet-stream,text/plain,application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf," \
#              "application/vnd.adobe.xdp+xml,text/csv,application/zip,application/vnd.ms-excel"
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.dir", "C:\\pabank2")
# fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/octet-stream,text/plain")

fp.set_preference('browser.helperApps.neverAsk.saveToDisk', "text/plain, application/vnd.ms-excel, text/csv, text/comma-separated-values, application/octet-stream")
fp.set_preference("browser.helperApps.alwaysAsk.force", False)
fp.set_preference("browser.download.manager.showWhenStarting",False)
# fp.set_preference('plugin.disable_full_page_plugin_for_types', mime_types)

driver = webdriver.Firefox(firefox_profile=fp)
#
# file_path = 'file:///' + "C:\\Users\\Administrator\\Desktop\\modal.html"
# driver.get(file_path)
# driver.find_element_by_link_text('ddd').click()
driver.get("https://sellercentral.amazon.com")
driver.find_element_by_id('ap_email').clear()
driver.find_element_by_id('ap_email').send_keys('tokyomkt@hotmail.com')
driver.find_element_by_id('ap_password').clear()
driver.find_element_by_id('ap_password').send_keys('tokyomkt01')
driver.find_element_by_id('signInSubmit').click()
time.sleep(15)
# driver.find_element_by_xpath(".//*[@id='sc-top-nav-root']/li[5]/a").click()
# time.sleep(5)
# driver.find_element_by_link_text('All Statements').click()
# time.sleep(5)
# driver.find_element_by_xpath(".//*[@id='content-main-entities']/table[2]/tbody/tr[3]/td[8]/div[2]/a/span/span").click()
driver.find_element_by_link_text('Settings').click()
driver.find_element_by_link_text('Logout').click()