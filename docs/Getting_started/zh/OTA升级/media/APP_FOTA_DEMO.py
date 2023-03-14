import app_fota
from misc import Power
import utime as time


files = ["000_Grey_Test.py"]

download_list = []
url = r'%s' % "http://112.31.84.164:8300/upload/Grey/"

for file in files:
    download_list.append({'url': (url + file), 'file_name': '/usr/%s' % file})

if download_list:
    print("downlist: %d\r\n" % len(download_list), download_list)
    fota = app_fota.new()
    result = fota.bulk_download(download_list)
    fota.set_update_flag()

    print("update ....", result)
    time.sleep(1)
    Power.powerRestart()  # 重启模块
