from lib.amazon_operation import clear_cookies, amazon_download, log_out, close_firefox
from lib.file_util import read_file_email
import traceback
import get_config

if __name__ == "__main__":
    a = 0
    paypalUser = get_config.get_User()
    for i in range(len(paypalUser)):
        flag = True
        while flag and a < 100:
            try:
                clear_cookies()
                amazon_download(get_config.get_emailFromSend(), get_config.get_emailPassword(),
                                get_config.get_smtpServer(),
                                get_config.get_emailTo(),
                                get_config.get_emailCc(), get_config.get_emailSubject(),
                                read_file_email(), get_config.get_User()[i],
                                get_config.get_Password()[i])
                flag = False
            except Exception as e:
                a += 1
                log_out()
                flag = True
                print(traceback.print_exc())
    close_firefox()
