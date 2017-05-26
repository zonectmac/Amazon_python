from get_config import get_downLoadPath, get_downLoadTemporaryPath, get_base_url, get_downLoadPathFinal, get_ff_profiles

TIMEOUT = 30
CONFIG = 'config.txt'
EMAIL_CONTENT = 'emailContent.txt'
MONTHLY_TRANSACTION = 'MonthlyTransaction'
MONTHLY_SUMMARY = 'MonthlySummary'
DOWNLOAD_TEMPORARY_PATH = get_downLoadTemporaryPath()
DOWNLOAD_PATH = get_downLoadPath()
DOWNLOAD_PATH_FINAL = get_downLoadPathFinal()
LOGIN_BASE_URL = get_base_url()
FF_PROFILES = get_ff_profiles()
