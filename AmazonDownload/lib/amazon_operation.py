import os
import shutil
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

import config
from email_manager import EmailManager
from lib.date_util import currency_date_array, get_last_month
from lib.file_util import del_allfile, is_file_writing, getdoc_size, file_is_exist, del_file, zip_dir
from lib.ftp_file_operation import ftp_upload_one

site_list = []
screen_shot_list = []
screen_shot_location_list = []


def get_driver():
    # 'C:\\Users\\Administrator\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\yn80ouvt.default'
    firefox_profile = webdriver.FirefoxProfile(config.FF_PROFILES)
    mime_types = "application/octet-stream,text/plain,application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf," \
                 "application/vnd.adobe.xdp+xml,text/csv,application/zip,application/vnd.ms-excel"

    firefox_profile.set_preference('browser.download.dir', config.DOWNLOAD_TEMPORARY_PATH)
    firefox_profile.set_preference('browser.download.folderList', 2)
    firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
    firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', mime_types)
    firefox_profile.set_preference('plugin.disable_full_page_plugin_for_types', mime_types)
    firefox_profile.set_preference('pdfjs.disabled', True)
    return webdriver.Firefox(firefox_profile=firefox_profile)


driver = get_driver()


def clear_cookies():
    driver.delete_all_cookies()


def close_firefox():
    driver.quit()


def log_out():
    time.sleep(2)
    try:
        # report = driver.find_element_by_link_text('Settings')
        # payments = driver.find_element_by_link_text('Logout')
        # ActionChains(driver).move_to_element(report).click(payments).perform()
        driver.find_element_by_link_text('Settings').click()
        driver.find_element_by_link_text('Logout').click()
        time.sleep(2)
        print('------logout----')
    except Exception as e:
        print(traceback.print_exc())


def amazon_download(server_username, server_pwd, smtp_server, msg_to, msg_cc, msg_subject, msg_content, user, paw):
    file_name = currency_date_array()[0] + '_' + currency_date_array()[1] + '_' + currency_date_array()[2] + '_' + user
    login(user, paw)
    print(site_list)
    for site in site_list:
        Select(driver.find_element_by_id("sc-mkt-picker-switcher-select")).select_by_visible_text(site)
        while not is_element_present_by_id("sc-mkt-picker-switcher-select"):
            driver.refresh()
            time.sleep(3)
            print('---------while------')
        time.sleep(10)
        # report = driver.find_element_by_xpath(".//*[@id='sc-top-nav-root']/li[5]/a")
        # payments = driver.find_element_by_xpath(".//*[@id='sc-top-nav-root']/li[5]/ul/li[2]/a")
        # ActionChains(driver).move_to_element(report).click(payments).perform()
        driver.find_element_by_xpath(".//*[@id='sc-top-nav-root']/li[5]/a").click()
        time.sleep(5)
        # driver.find_element_by_xpath(".//*[@id='sc-top-nav-root']/li[5]/ul/li[2]/a").click()
        # time.sleep(5)
        if date_range_report(site):
            continue
        statement_view(site)
        all_statement(site)
    zip_dir(config.DOWNLOAD_PATH, config.DOWNLOAD_PATH + file_name + '.zip')
    time.sleep(3)
    # send_email(server_username, server_pwd, smtp_server, msg_to, msg_cc, msg_subject,
    #            config.DOWNLOAD_PATH + msg_content,
    #            config.DOWNLOAD_PATH + file_name)
    if ftp_upload_one(config.DOWNLOAD_PATH + file_name + '.zip', '/amazon'):
        time.sleep(3)
        del_allfile(config.DOWNLOAD_PATH)
    log_out()


def send_email(server_username, server_pwd, smtp_server, msg_to, msg_cc, msg_subject, msg_content, zipname):
    mail_cfg = {
        # 邮箱登录设置，使用SMTP登录
        'server_username': server_username,
        'server_pwd': server_pwd,
        'smtp_server': smtp_server,
        # 邮件内容设置
        'msg_to': [msg_to],  # 可以在此添加收件人
        'msg_cc': msg_cc,
        'msg_subject': msg_subject,
        'msg_date': time.strftime('%Y-%m-%d %X', time.localtime()),
        'msg_content': msg_content,

        # 附件
        'attach_file': zipname + '.zip'
    }
    email_manager = EmailManager(**mail_cfg)

    email_manager.run()


def login(user, paw):
    driver.implicitly_wait(config.TIMEOUT)
    driver.get(config.LOGIN_BASE_URL)
    driver.find_element_by_id('ap_email').clear()
    driver.find_element_by_id('ap_email').send_keys(user)
    driver.find_element_by_id('ap_password').clear()
    driver.find_element_by_id('ap_password').send_keys(paw)
    driver.find_element_by_id('signInSubmit').click()
    time.sleep(10)
    print('---title--' + driver.title)
    while '出错' in driver.title:
        print('---------------------re')
        # driver.find_element_by_id('netErrorButtonContainer').click()
        login(user, paw)
        time.sleep(5)
        # driver.refresh()
    # WebDriverWait(driver, config.TIMEOUT).until(
    #     EC.presence_of_element_located((By.ID, "leftnav.fsr"))
    # )
    time.sleep(3)
    while not is_element_present_by_id("sc-mkt-picker-switcher-select"):
        driver.refresh()
        time.sleep(3)
        print('---------while------')
    site_select = Select(driver.find_element_by_id("sc-mkt-picker-switcher-select"))
    print([option.text for option in site_select.options])
    for option in site_select.options:
        site_list.append(option.text)


def all_statement(site):
    driver.find_element_by_link_text('All Statements').click()
    time.sleep(5)
    for index_select in range(len(screen_shot_location_list)):
        all_statement_download(index_select, site)
        time.sleep(5)


def all_statement_download(index_select, site):
    del_allfile(config.DOWNLOAD_TEMPORARY_PATH)
    time.sleep(1)
    downloading(index_select)
    time.sleep(3)
    file_dir = os.listdir(config.DOWNLOAD_TEMPORARY_PATH)
    for tm in file_dir:
        if os.path.exists(config.DOWNLOAD_TEMPORARY_PATH + tm) and os.path.isfile(
                        config.DOWNLOAD_TEMPORARY_PATH + tm):
            while getdoc_size(config.DOWNLOAD_TEMPORARY_PATH + tm) == 0 and not file_is_exist(
                    config.DOWNLOAD_TEMPORARY_PATH, tm):
                del_file(config.DOWNLOAD_TEMPORARY_PATH + tm)
                del_file(config.DOWNLOAD_TEMPORARY_PATH + tm + '.part')
                time.sleep(3)
                downloading(index_select)
                del_file(config.DOWNLOAD_TEMPORARY_PATH + tm + '.part')
    tofile = config.get_downLoadPath() + site + screen_shot_list[index_select] + '.xls'
    print('-------aftername------' + tofile)
    time.sleep(5)
    for tmp in file_dir:
        if os.path.exists(config.DOWNLOAD_TEMPORARY_PATH + tmp) and os.path.isfile(
                        config.DOWNLOAD_TEMPORARY_PATH + tmp):
            if os.path.splitext(config.DOWNLOAD_TEMPORARY_PATH + tmp)[1] == '.txt':
                shutil.move(config.DOWNLOAD_TEMPORARY_PATH + tmp, tofile)
    time.sleep(10)


def downloading(index_select):
    print('down')
    driver.find_element_by_xpath(
        ".//*[@id='content-main-entities']/table[2]/tbody/tr[" + str(screen_shot_location_list[index_select])
        + "]/td[8]/div[2]/a/span/span").click()
    time.sleep(3)
    file_dir = os.listdir(config.DOWNLOAD_TEMPORARY_PATH)
    for tmp in file_dir:
        if os.path.exists(config.DOWNLOAD_TEMPORARY_PATH + tmp) and os.path.isfile(
                        config.DOWNLOAD_TEMPORARY_PATH + tmp):
            if os.path.splitext(config.DOWNLOAD_TEMPORARY_PATH + tmp)[1] == '.part':
                while is_file_writing(config.DOWNLOAD_TEMPORARY_PATH + tmp):
                    time.sleep(1)
                    print('----while--4-')


def statement_view(site):
    driver.find_element_by_xpath(".//*[@id='PaymentTabs']/div/ul/li[1]/a").click()
    time.sleep(5)
    statement_select = Select(driver.find_element_by_id("groups"))
    print([option.text for option in statement_select.options])
    print(statement_select.options[0])
    screen_shot_list.clear()
    screen_shot_location_list.clear()
    inde_id = -1
    for option in statement_select.options:
        inde_id += 1
        if get_last_month() in option.text \
                and currency_date_array()[2] in option.text \
                and 'Open' not in option.text:
            screen_shot_list.append(option.text)
            screen_shot_location_list.append(inde_id + 2)
            print(inde_id)
    print('-----screen----' + str(screen_shot_list))
    print('-----screen--lll--' + str(screen_shot_location_list))
    for select in screen_shot_list:
        select_and_screen_shot(select, site)
        time.sleep(3)
    time.sleep(10)


def select_and_screen_shot(select, site):
    Select(driver.find_element_by_id("groups")).select_by_visible_text(select)
    time.sleep(10)
    driver.save_screenshot(config.DOWNLOAD_PATH + site + '_' + select + '.png')


def date_range_report(site):
    driver.find_element_by_xpath(".//*[@id='PaymentTabs']/div/ul/li[4]/a").click()
    time.sleep(5)
    if not driver.find_element_by_id('reportsTable').is_displayed():
        print('return')
        return True
    id_list = ["drrReportTypeRadioSummary", "drrReportTypeRadioTransaction"]
    for i in range(len(id_list)):
        generate_report(id_list[i])
        time.sleep(3)
    time.sleep(10)
    if driver.find_element_by_id('mt-header-count-value').text == '0':
        print('report count' + driver.find_element_by_id('mt-header-count-value').text)
        return True
    date_rang_click_download(site)
    time.sleep(5)
    return False


def generate_report(generate_id):
    driver.find_element_by_xpath(".//*[@id='drrGenerateReportButton']/span/input").click()
    # WebDriverWait(driver, config.TIMEOUT).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "a-modal-scroller"))
    # )
    time.sleep(5)
    link = driver.find_element_by_class_name('a-modal-scroller').find_element_by_id(generate_id)
    driver.execute_script('$(arguments[0]).click()', link)
    time.sleep(2)
    link2 = driver.find_element_by_class_name('a-modal-scroller').find_element_by_xpath(
        ".//*[@id='drrGenerateReportsGenerateButton']/span/input")
    driver.execute_script('$(arguments[0]).click()', link2)


def date_rang_click_download(site):
    while 'In Progress' in driver.find_element_by_xpath(".//*[@id='0-ddrAction']").text:
        print('--------action-------' + driver.find_element_by_xpath(".//*[@id='0-ddrAction']").text)
        driver.find_element_by_xpath(".//*[@id='0-ddrAction']/div/a[1]").click()
        time.sleep(5)
    time.sleep(5)
    date_rang_download(site)


def date_rang_download(site):
    if not (os.path.exists(config.DOWNLOAD_TEMPORARY_PATH) and os.path.isdir(config.DOWNLOAD_TEMPORARY_PATH)):
        os.makedirs(config.DOWNLOAD_TEMPORARY_PATH)
    if not (os.path.exists(config.DOWNLOAD_PATH) and os.path.isdir(config.DOWNLOAD_PATH)):
        os.makedirs(config.DOWNLOAD_PATH)
    if not (os.path.exists(config.DOWNLOAD_PATH_FINAL) and os.path.isdir(config.DOWNLOAD_PATH_FINAL)):
        os.makedirs(config.DOWNLOAD_PATH_FINAL)
    date_range_download_file(0, config.MONTHLY_TRANSACTION, '.csv')
    copy_file('.csv', config.MONTHLY_TRANSACTION, 0, site)
    time.sleep(5)
    date_range_download_file(1, config.MONTHLY_SUMMARY, '.pdf')
    copy_file('.pdf', config.MONTHLY_SUMMARY, 1, site)


def date_range_download_file(id_index, name, file_type):
    del_allfile(config.DOWNLOAD_TEMPORARY_PATH)
    if driver.find_element_by_xpath(".//*[@id='" + str(id_index) + "-ddrAction']").find_element_by_xpath(
            ".//*[@id='downloadButton-announce']").text == 'Download':
        driver.find_element_by_xpath(".//*[@id='" + str(id_index) + "-ddrAction']").find_element_by_xpath(
            ".//*[@id='downloadButton-announce']").click()
        time.sleep(5)
        while is_file_writing(config.DOWNLOAD_TEMPORARY_PATH + currency_date_array()[
            2] + get_last_month() + name + file_type + '.part'):
            time.sleep(1)
            print('-----1---while-----------')
        time.sleep(3)


def copy_file(file_type, name, id_index, site):
    file_name = currency_date_array()[2] + get_last_month() + name + file_type
    while getdoc_size(config.DOWNLOAD_TEMPORARY_PATH + file_name) == 0 and not file_is_exist(
            config.DOWNLOAD_PATH, file_name):
        del_file(config.DOWNLOAD_TEMPORARY_PATH + file_name)
        del_file(config.DOWNLOAD_TEMPORARY_PATH + file_name + '.part')
        driver.find_element_by_xpath(".//*[@id='" + str(id_index) + "-ddrAction']").find_element_by_xpath(
            ".//*[@id='downloadButton-announce']").click()
        time.sleep(10)
        while is_file_writing(config.DOWNLOAD_TEMPORARY_PATH + file_name + '.part'):
            time.sleep(1)
            print('-----2---while-----------')
        del_file(config.DOWNLOAD_TEMPORARY_PATH + file_name + '.part')
        print('-----3---while-----------')
    before_name = config.DOWNLOAD_TEMPORARY_PATH + file_name
    if file_type == '.csv':
        file_type = '.xls'
    to_file = config.DOWNLOAD_PATH + site + '_' + currency_date_array()[2] + get_last_month() + '_' + name + file_type
    print('----before_name-----' + before_name)
    print('----to_file-----' + to_file)
    time.sleep(2)
    shutil.move(before_name, to_file)
    print('--copyfile--')


def is_element_present_by_xpath(element):
    try:
        driver.find_element_by_xpath(element)
    except NoSuchElementException as e:
        return False
    return True


def is_element_present_by_id(element):
    try:
        driver.find_element_by_id(element)
    except NoSuchElementException as e:
        return False
    return True
