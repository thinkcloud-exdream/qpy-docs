# ble-低功耗蓝牙相关功能

`ble`模块用于提供BLE GATT Server （从机）与 Client （主机）功能，基于BLE 4.2协议。

**示例**：

```python
#BLE Server

import ble
import utime


BLE_GATT_SYS_SERVICE = 0  # 0-删除系统默认的GAP和GATT服务  1-保留系统默认的GAP和GATT服务
BLE_SERVER_HANDLE = 0
_BLE_NAME = "Quectel_ble"


event_dict = {
    'BLE_START_STATUS_IND': 0,  # ble start
    'BLE_STOP_STATUS_IND': 1,   # ble stop
    'BLE_CONNECT_IND': 16,  # ble connect
    'BLE_DISCONNECT_IND': 17,   # ble disconnect
    'BLE_UPDATE_CONN_PARAM_IND': 18,    # ble update connection parameter
    'BLE_SCAN_REPORT_IND': 19,  # ble gatt client scan and report other devices
    'BLE_GATT_MTU': 20, # ble connection mtu
    'BLE_GATT_RECV_WRITE_IND': 21, # when ble client write characteristic value or descriptor,server get the notice
    'BLE_GATT_RECV_READ_IND': 22, # when ble client read characteristic value or descriptor,server get the notice
    'BLE_GATT_RECV_NOTIFICATION_IND': 23,   # client receive notification
    'BLE_GATT_RECV_INDICATION_IND': 24, # client receive indication
    'BLE_GATT_SEND_END': 25, # server send notification,and receive send end notice
}

class EVENT(dict):
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        raise ValueError("{} is read-only.".format(key))


event = EVENT(event_dict)


def ble_callback(args):
    global BLE_GATT_SYS_SERVICE
    global BLE_SERVER_HANDLE
    event_id = args[0]
    status = args[1]
    print('[ble_callback]: event_id={}, status={}'.format(event_id, status))

    if event_id == event.BLE_START_STATUS_IND:  # ble start
        if status == 0:
            print('[callback] BLE start success.')
            mac = ble.getPublicAddr()
            if mac != -1 and len(mac) == 6:
                addr = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(mac[5], mac[4], mac[3], mac[2], mac[1], mac[0])
                print('BLE public addr : {}'.format(addr))
            ret = ble_gatt_set_name()
            if ret != 0:
                ble_gatt_close()
                return
            ret = ble_gatt_set_param()
            if ret != 0:
                ble_gatt_close()
                return
            ret = ble_gatt_set_data()
            if ret != 0:
                ble_gatt_close()
                return
            ret = ble_gatt_set_rsp_data()
            if ret != 0:
                ble_gatt_close()
                return
            ret = ble_gatt_add_service()
            if ret != 0:
                ble_gatt_close()
                return
            ret = ble_gatt_add_characteristic()
            if ret != 0:
                ble_gatt_close()
                return
            ret = ble_gatt_add_characteristic_value()
            if ret != 0:
                ble_gatt_close()
                return
            ret = ble_gatt_add_characteristic_desc()
            if ret != 0:
                ble_gatt_close()
                return
            ret = ble_gatt_add_service_complete()
            if ret != 0:
                ble_gatt_close()
                return
            if BLE_GATT_SYS_SERVICE == 0:
                BLE_SERVER_HANDLE = 1
            else:
                BLE_SERVER_HANDLE = 16
            ret = ble_adv_start()
            if ret != 0:
                ble_gatt_close()
                return
        else:
            print('[callback] BLE start failed.')
    elif event_id == event.BLE_STOP_STATUS_IND:  # ble stop
        if status == 0:
            print('[callback] ble stop successful.')
            ble_status = ble.getStatus()
            print('ble status is {}'.format(ble_status))
            ble_gatt_server_release()
        else:
            print('[callback] ble stop failed.')
    elif event_id == event.BLE_CONNECT_IND:  # ble connect
        if status == 0:
            print('[callback] ble connect successful.')
            connect_id = args[2]
            addr = args[3]
            addr_str = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[0], addr[1], addr[2], addr[3], addr[4], addr[5])
            print('[callback] connect_id = {}, addr = {}'.format(connect_id, addr_str))

            ret = ble_gatt_send_notification()
            if ret == 0:
                print('[callback] ble_gatt_send_notification successful.')
            else:
                print('[callback] ble_gatt_send_notification failed.')
                ble_gatt_close()
                return
        else:
            print('[callback] ble connect failed.')
    elif event_id == event.BLE_DISCONNECT_IND:  # ble disconnect
        if status == 0:
            print('[callback] ble disconnect successful.')
            connect_id = args[2]
            addr = args[3]
            addr_str = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[0], addr[1], addr[2], addr[3], addr[4], addr[5])
            ble_gatt_close()
            print('[callback] connect_id = {}, addr = {}'.format(connect_id, addr_str))
        else:
            print('[callback] ble disconnect failed.')
            ble_gatt_close()
            return
    elif event_id == event.BLE_UPDATE_CONN_PARAM_IND:  # ble update connection parameter
        if status == 0:
            print('[callback] ble update parameter successful.')
            connect_id = args[2]
            max_interval = args[3]
            min_interval = args[4]
            latency = args[5]
            timeout = args[6]
            print('[callback] connect_id={},max_interval={},min_interval={},latency={},timeout={}'.format(connect_id, max_interval, min_interval, latency, timeout))
        else:
            print('[callback] ble update parameter failed.')
            ble_gatt_close()
            return
    elif event_id == event.BLE_GATT_MTU:  # ble connection mtu
        if status == 0:
            print('[callback] ble connect mtu successful.')
            handle = args[2]
            ble_mtu = args[3]
            print('[callback] handle = {:#06x}, ble_mtu = {}'.format(handle, ble_mtu))
        else:
            print('[callback] ble connect mtu failed.')
            ble_gatt_close()
            return
    elif event_id == event.BLE_GATT_RECV_WRITE_IND:
        if status == 0:
            print('[callback] ble recv successful.')
            data_len = args[2]
            data = args[3]  # 这是一个bytearray
            attr_handle = args[4]
            short_uuid = args[5]
            long_uuid = args[6]  # 这是一个bytearray
            print('len={}, data:{}'.format(data_len, data))
            print('attr_handle = {:#06x}'.format(attr_handle))
            print('short uuid = {:#06x}'.format(short_uuid))
            print('long uuid = {}'.format(long_uuid))
        else:
            print('[callback] ble recv failed.')
            ble_gatt_close()
            return
    elif event_id == event.BLE_GATT_RECV_READ_IND:
        if status == 0:
            print('[callback] ble recv read successful.')
            data_len = args[2]
            data = args[3]  # 这是一个bytearray
            attr_handle = args[4]
            short_uuid = args[5]
            long_uuid = args[6]  # 这是一个bytearray
            print('len={}, data:{}'.format(data_len, data))
            print('attr_handle = {:#06x}'.format(attr_handle))
            print('short uuid = {:#06x}'.format(short_uuid))
            print('long uuid = {}'.format(long_uuid))
        else:
            print('[callback] ble recv read failed.')
            ble_gatt_close()
            return
    elif event_id == event.BLE_GATT_SEND_END:
        if status == 0:
            print('[callback] ble send data successful.')
        else:
            print('[callback] ble send data failed.')
    else:
        print('unknown event id.')


def ble_gatt_server_init(cb):
    ret = ble.serverInit(cb)
    if ret != 0:
        print('ble_gatt_server_init failed.')
        return -1
    print('ble_gatt_server_init success.')
    return 0


def ble_gatt_server_release():
    ret = ble.serverRelease()
    if ret != 0:
        print('ble_gatt_server_release failed.')
        return -1
    print('ble_gatt_server_release success.')
    return 0


def ble_gatt_open():
    ret = ble.gattStart()
    if ret != 0:
        print('ble_gatt_open failed.')
        return -1
    print('ble_gatt_open success.')
    return 0


def ble_gatt_close():
    ret = ble.gattStop()
    if ret != 0:
        print('ble_gatt_close failed.')
        return -1
    print('ble_gatt_close success.')
    return 0


def ble_gatt_set_name():
    code = 0  # utf8
    name = _BLE_NAME
    ret = ble.setLocalName(code, name)
    if ret != 0:
        print('ble_gatt_set_name failed.')
        return -1
    print('ble_gatt_set_name success.')
    return 0


def ble_gatt_set_param():
    min_adv = 0x300
    max_adv = 0x320
    adv_type = 0  # 可连接的非定向广播，默认选择
    addr_type = 0  # 公共地址
    channel = 0x07
    filter_strategy = 0  # 处理所有设备的扫描和连接请求
    discov_mode = 2
    no_br_edr = 1
    enable_adv = 1
    ret = ble.setAdvParam(min_adv, max_adv, adv_type, addr_type, channel, filter_strategy, discov_mode, no_br_edr, enable_adv)
    if ret != 0:
        print('ble_gatt_set_param failed.')
        return -1
    print('ble_gatt_set_param success.')
    return 0


def ble_gatt_set_data():
    adv_data = [0x02, 0x01, 0x05]
    ble_name = _BLE_NAME
    length = len(ble_name) + 1
    adv_data.append(length)
    adv_data.append(0x09)
    name_encode = ble_name.encode('UTF-8')
    for i in range(0, len(name_encode)):
        adv_data.append(name_encode[i])
    print('set adv_data:{}'.format(adv_data))
    data = bytearray(adv_data)
    ret = ble.setAdvData(data)
    if ret != 0:
        print('ble_gatt_set_data failed.')
        return -1
    print('ble_gatt_set_data success.')
    return 0


def ble_gatt_set_rsp_data():
    adv_data = []
    ble_name = _BLE_NAME
    length = len(ble_name) + 1
    adv_data.append(length)
    adv_data.append(0x09)
    name_encode = ble_name.encode('UTF-8')
    for i in range(0, len(name_encode)):
        adv_data.append(name_encode[i])
    print('set adv_rsp_data:{}'.format(adv_data))
    data = bytearray(adv_data)
    ret = ble.setAdvRspData(data)
    if ret != 0:
        print('ble_gatt_set_rsp_data failed.')
        return -1
    print('ble_gatt_set_rsp_data success.')
    return 0


def ble_gatt_add_service():
    primary = 1
    server_id = 0x01
    uuid_type = 1  # 短UUID
    uuid_s = 0x180F
    uuid_l = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    ret = ble.addService(primary, server_id, uuid_type, uuid_s, uuid_l)
    if ret != 0:
        print('ble_gatt_add_service failed.')
        return -1
    print('ble_gatt_add_service success.')
    return 0


def ble_gatt_add_characteristic():
    server_id = 0x01
    chara_id = 0x01
    chara_prop = 0x02 | 0x10 | 0x20  # 0x02-可读 0x10-通知 0x20-指示
    uuid_type = 1  # 短UUID
    uuid_s = 0x2A19
    uuid_l = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    ret = ble.addChara(server_id, chara_id, chara_prop, uuid_type, uuid_s, uuid_l)
    if ret != 0:
        print('ble_gatt_add_characteristic failed.')
        return -1
    print('ble_gatt_add_characteristic success.')
    return 0


def ble_gatt_add_characteristic_value():
    data = []
    server_id = 0x01
    chara_id = 0x01
    permission = 0x0001 | 0x0002
    uuid_type = 1  # 短UUID
    uuid_s = 0x2A19
    uuid_l = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    for i in range(0, 244):
        data.append(0x00)
    value = bytearray(data)
    ret = ble.addCharaValue(server_id, chara_id, permission, uuid_type, uuid_s, uuid_l, value)
    if ret != 0:
        print('ble_gatt_add_characteristic_value failed.')
        return -1
    print('ble_gatt_add_characteristic_value success.')
    return 0


def ble_gatt_add_characteristic_desc():
    data = [0x00, 0x00]
    server_id = 0x01
    chara_id = 0x01
    permission = 0x0001 | 0x0002
    uuid_type = 1  # 短UUID
    uuid_s = 0x2902
    uuid_l = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    value = bytearray(data)
    ret = ble.addCharaDesc(server_id, chara_id, permission, uuid_type, uuid_s, uuid_l, value)
    if ret != 0:
        print('ble_gatt_add_characteristic_desc failed.')
        return -1
    print('ble_gatt_add_characteristic_desc success.')
    return 0


def ble_gatt_send_notification():
    global BLE_SERVER_HANDLE
    data = [0x39, 0x39, 0x39, 0x39, 0x39]  # 测试数据
    conn_id = 0
    attr_handle = BLE_SERVER_HANDLE + 2
    value = bytearray(data)
    ret = ble.sendNotification(conn_id, attr_handle, value)
    if ret != 0:
        print('ble_gatt_send_notification failed.')
        return -1
    print('ble_gatt_send_notification success.')
    return 0


def ble_gatt_add_service_complete():
    global BLE_GATT_SYS_SERVICE
    ret = ble.addOrClearService(1, BLE_GATT_SYS_SERVICE)
    if ret != 0:
        print('ble_gatt_add_service_complete failed.')
        return -1
    print('ble_gatt_add_service_complete success.')
    return 0


def ble_gatt_clear_service_complete():
    global BLE_GATT_SYS_SERVICE
    ret = ble.addOrClearService(0, BLE_GATT_SYS_SERVICE)
    if ret != 0:
        print('ble_gatt_clear_service_complete failed.')
        return -1
    print('ble_gatt_clear_service_complete success.')
    return 0


def ble_adv_start():
    ret = ble.advStart()
    if ret != 0:
        print('ble_adv_start failed.')
        return -1
    print('ble_adv_start success.')
    return 0


def ble_adv_stop():
    ret = ble.advStop()
    if ret != 0:
        print('ble_adv_stop failed.')
        return -1
    print('ble_adv_stop success.')
    return 0


def main():
    ret = ble_gatt_server_init(ble_callback)
    if ret == 0:
        ret = ble_gatt_open()
        if ret != 0:
            return -1
    else:
        return -1
    count = 0
    while True:
        utime.sleep(1)
        count += 1
        if count % 5 == 0:
            print('##### BLE running, count = {}......'.format(count))
        if count > 120:
            count = 0
            print('!!!!! stop BLE now !!!!!')
            ble_gatt_close()
            return 0


if __name__ == '__main__':
    main()

```

```python
#BLE Client

import ble
import utime
import _thread
import checkNet
from queue import Queue

PROJECT_NAME = "QuecPython_BLE_Client_Example"
PROJECT_VERSION = "1.0.0"
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

event_dict = {
    'BLE_START_STATUS_IND': 0,  # ble start
    'BLE_STOP_STATUS_IND': 1,   # ble stop
    'BLE_CONNECT_IND': 16,  # ble connect
    'BLE_DISCONNECT_IND': 17,   # ble disconnect
    'BLE_UPDATE_CONN_PARAM_IND': 18,    # ble update connection parameter
    'BLE_SCAN_REPORT_IND': 19,  # ble gatt client scan and report other devices
    'BLE_GATT_MTU': 20, # ble connection mtu
    'BLE_GATT_RECV_NOTIFICATION_IND': 23,   # client receive notification
    'BLE_GATT_RECV_INDICATION_IND': 24, # client receive indication
    'BLE_GATT_START_DISCOVER_SERVICE_IND': 26,  # start discover service
    'BLE_GATT_DISCOVER_SERVICE_IND': 27,    # discover service
    'BLE_GATT_DISCOVER_CHARACTERISTIC_DATA_IND': 28,    # discover characteristic
    'BLE_GATT_DISCOVER_CHARA_DESC_IND': 29, # discover characteristic descriptor
    'BLE_GATT_CHARA_WRITE_WITH_RSP_IND': 30,    # write characteristic value with response
    'BLE_GATT_CHARA_WRITE_WITHOUT_RSP_IND': 31, # write characteristic value without response
    'BLE_GATT_CHARA_READ_IND': 32,  # read characteristic value by handle
    'BLE_GATT_CHARA_READ_BY_UUID_IND': 33,  # read characteristic value by uuid
    'BLE_GATT_CHARA_MULTI_READ_IND': 34,    # read multiple characteristic value
    'BLE_GATT_DESC_WRITE_WITH_RSP_IND': 35, # write characteristic descriptor
    'BLE_GATT_DESC_READ_IND': 36,   # read characteristic descriptor
    'BLE_GATT_ATT_ERROR_IND': 37,   # attribute error
}

gatt_status_dict = {
    'BLE_GATT_IDLE' : 0,
    'BLE_GATT_DISCOVER_SERVICE': 1,
    'BLE_GATT_DISCOVER_INCLUDES': 2,
    'BLE_GATT_DISCOVER_CHARACTERISTIC': 3,
    'BLE_GATT_WRITE_CHARA_VALUE': 4,
    'BLE_GATT_WRITE_CHARA_DESC': 5,
    'BLE_GATT_READ_CHARA_VALUE': 6,
    'BLE_GATT_READ_CHARA_DESC': 7,
}

class EVENT(dict):
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        raise ValueError("{} is read-only.".format(key))


class BleClient(object):
    def __init__(self):
        self.ble_server_name = 'Quectel_ble' #目标设备ble名称
        self.connect_id = 0
        self.connect_addr = 0
        self.gatt_statue = 0
        self.discover_service_mode = 0 # 0-discover all service, 1-discover service by uuid

        self.scan_param = {
            'scan_mode' : 1, # 积极扫描
            'interval' : 0x100,
            'scan_window' : 0x50,
            'filter_policy' : 0,
            'local_addr_type' : 0,
        }

        self.scan_report_info = {
            'event_type' : 0,
            'name' : '',
            'addr_type' : 0,
            'addr' : 0, # 初始化时，用0表示无效值，实际存放bytearray
            'rssi' : 0,
            'data_len' : 0,
            'raw_data' : 0,
        }

        self.target_service = {
            'start_handle' : 0,
            'end_handle' : 0,
            'uuid_type' : 1, # 短uuid
            'short_uuid' : 0x180F, # 电池电量服务
            'long_uuid' : bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        }

        self.characteristic_list = []
        self.descriptor_list = []
        self.characteristic_count = 0   # ql_ble_gatt_chara_count
        self.chara_descriptor_count = 0 # ql_ble_gatt_chara_desc_count
        self.characteristic_index = 0   # ql_ble_gatt_chara_desc_index
        self.current_chara_index = 0    # ql_ble_gatt_cur_chara
        self.current_desc_index = 0     # ql_ble_gatt_chara_cur_desc
        self.ble_short_uuid_pair_len = 7
        self.ble_long_uuid_pair_len = 21

        ret = ble.clientInit(self.ble_client_callback)
        if ret != 0:
            print('ble client initialize failed.')
            raise ValueError("BLE Client Init failed.")
        else:
            print('ble client initialize successful.')
        print('')

    @staticmethod
    def gatt_open():
        ret = ble.gattStart()
        if ret != 0:
            print('ble open failed.')
        else:
            print('ble open successful.')
        print('')
        return ret

    @staticmethod
    def gatt_close():
        ret = ble.gattStop()
        if ret != 0:
            print('ble close failed.')
        else:
            print('ble close successful.')
        print('')
        return ret

    @staticmethod
    def gatt_get_status():
        return ble.getStatus()

    @staticmethod
    def release():
        ret = ble.clientRelease()
        if ret != 0:
            print('ble client release failed.')
        else:
            print('ble client release successful.')
        print('')
        return ret

    def set_scan_param(self):
        scan_mode = self.scan_param['scan_mode']
        interval = self.scan_param['interval']
        scan_time = self.scan_param['scan_window']
        filter_policy = self.scan_param['filter_policy']
        local_addr_type = self.scan_param['local_addr_type']
        ret = ble.setScanParam(scan_mode, interval, scan_time, filter_policy, local_addr_type)
        if ret != 0:
            print('ble client set scan-parameters failed.')
        else:
            print('ble client set scan-parameters successful.')
        print('')
        return ret

    @staticmethod
    def start_scan():
        ret = ble.scanStart()
        if ret != 0:
            print('ble client scan failed.')
        else:
            print('ble client scan successful.')
        print('')
        return ret

    @staticmethod
    def stop_scan():
        ret = ble.scanStop()
        if ret != 0:
            print('ble client failed to stop scanning.')
        else:
            print('ble client scan stopped successfully.')
        print('')
        return ret

    def connect(self):
        print('start to connect.....')
        addr_type = self.scan_report_info['addr_type']
        addr = self.scan_report_info['addr']
        if addr != 0 and len(addr) == 6:
            addr_str = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[0], addr[1], addr[2], addr[3], addr[4], addr[5])
            print('addr_type : {}, addr : {}'.format(addr_type, addr_str))
            ret = ble.connect(addr_type, addr)
            if ret != 0:
                print('ble client connect failed.')
            else:
                print('ble client connect successful.')
            print('')
            return ret

    def cancel_connect(self):
        ret = ble.cancelConnect(self.scan_report_info['addr'])
        if ret != 0:
            print('ble client cancel connect failed.')
        else:
            print('ble client cancel connect successful.')
        print('')
        return ret

    def disconnect(self):
        ret = ble.disconnect(self.connect_id)
        if ret != 0:
            print('ble client disconnect failed.')
        else:
            print('ble client disconnect successful.')
        print('')
        return ret

    def discover_all_service(self):
        ret = ble.discoverAllService(self.connect_id)
        if ret != 0:
            print('ble client discover all service failed.')
        else:
            print('ble client discover all service successful.')
        print('')
        return ret

    def discover_service_by_uuid(self):
        connect_id = self.connect_id
        uuid_type = self.target_service['uuid_type']
        short_uuid = self.target_service['short_uuid']
        long_uuid = self.target_service['long_uuid']
        ret = ble.discoverByUUID(connect_id, uuid_type, short_uuid, long_uuid)
        if ret != 0:
            print('ble client discover service by uuid failed.')
        else:
            print('ble client discover service by uuid successful.')
        print('')
        return ret

    def discover_all_includes(self):
        connect_id = self.connect_id
        start_handle = self.target_service['start_handle']
        end_handle = self.target_service['end_handle']
        ret = ble.discoverAllIncludes(connect_id, start_handle, end_handle)
        if ret != 0:
            print('ble client discover all includes failed.')
        else:
            print('ble client discover all includes successful.')
        print('')
        return ret

    def discover_all_characteristic(self):
        connect_id = self.connect_id
        start_handle = self.target_service['start_handle']
        end_handle = self.target_service['end_handle']
        ret = ble.discoverAllChara(connect_id, start_handle, end_handle)
        if ret != 0:
            print('ble client discover all characteristic failed.')
        else:
            print('ble client discover all characteristic successful.')
        print('')
        return ret

    def discover_all_characteristic_descriptor(self):
        connect_id = self.connect_id
        index = self.characteristic_index
        start_handle = self.characteristic_list[index]['value_handle'] + 1

        if self.characteristic_index == (self.characteristic_count - 1):
            end_handle = self.target_service['end_handle']
            print('[1]start_handle = {:#06x}, end_handle = {:#06x}'.format(start_handle - 1, end_handle))
            ret = ble.discoverAllCharaDesc(connect_id, start_handle, end_handle)
        else:
            end_handle = self.characteristic_list[index+1]['handle'] - 1
            print('[2]start_handle = {:#06x}, end_handle = {:#06x}'.format(start_handle - 1, end_handle))
            ret = ble.discoverAllCharaDesc(connect_id, start_handle, end_handle)
        self.characteristic_index += 1
        if ret != 0:
            print('ble client discover all characteristic descriptor failed.')
        else:
            print('ble client discover all characteristic descriptor successful.')
        print('')
        return ret

    def read_characteristic_by_uuid(self):
        connect_id = self.connect_id
        index = self.current_chara_index   # 根据需要改变该值
        start_handle = self.characteristic_list[index]['handle']
        end_handle = self.characteristic_list[index]['value_handle']
        uuid_type = 1
        short_uuid = self.characteristic_list[index]['short_uuid']
        long_uuid = bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

        ret = ble.readCharaByUUID(connect_id, start_handle, end_handle, uuid_type, short_uuid, long_uuid)
        if ret != 0:
            print('ble client read characteristic by uuid failed.')
        else:
            print('ble client read characteristic by uuid successful.')
        print('')
        return ret

    def read_characteristic_by_handle(self):
        connect_id = self.connect_id
        index = self.current_chara_index  # 根据需要改变该值
        handle = self.characteristic_list[index]['value_handle']
        offset = 0
        is_long = 0

        ret = ble.readCharaByHandle(connect_id, handle, offset, is_long)
        if ret != 0:
            print('ble client read characteristic by handle failed.')
        else:
            print('ble client read characteristic by handle successful.')
        print('')
        return ret

    def read_characteristic_descriptor(self):
        connect_id = self.connect_id
        index = self.current_desc_index  # 根据需要改变该值
        handle = self.descriptor_list[index]['handle']
        print('handle = {:#06x}'.format(handle))
        is_long = 0
        ret = ble.readCharaDesc(connect_id, handle, is_long)
        if ret != 0:
            print('ble client read characteristic descriptor failed.')
        else:
            print('ble client read characteristic descriptor successful.')
        print('')
        return ret

    def write_characteristic(self):
        connect_id = self.connect_id
        index = self.current_chara_index  # 根据需要改变该值
        handle = self.characteristic_list[index]['value_handle']
        offset = 0
        is_long = 0
        data = bytearray([0x40, 0x00])
        print('value_handle = {:#06x}, uuid = {:#06x}'.format(handle, self.characteristic_list[index]['short_uuid']))
        ret = ble.writeChara(connect_id, handle, offset, is_long, data)
        if ret != 0:
            print('ble client write characteristic failed.')
        else:
            print('ble client read characteristic successful.')
        print('')
        return ret

    def write_characteristic_no_rsp(self):
        connect_id = self.connect_id
        index = self.current_chara_index  # 根据需要改变该值
        handle = self.characteristic_list[index]['value_handle']
        data = bytearray([0x20, 0x00])
        print('value_handle = {:#06x}, uuid = {:#06x}'.format(handle, self.characteristic_list[index]['short_uuid']))
        ret = ble.writeCharaNoRsp(connect_id, handle, data)
        if ret != 0:
            print('ble client write characteristic no rsp failed.')
        else:
            print('ble client read characteristic no rsp successful.')
        print('')
        return ret

    def write_characteristic_descriptor(self):
        connect_id = self.connect_id
        index = self.current_desc_index  # 根据需要改变该值
        handle = self.descriptor_list[index]['handle']
        data = bytearray([0x01, 0x02])
        print('handle = {:#06x}'.format(handle))

        ret = ble.writeCharaDesc(connect_id, handle, data)
        if ret != 0:
            print('ble client write characteristic descriptor failed.')
        else:
            print('ble client read characteristic descriptor successful.')
        print('')
        return ret

    @staticmethod
    def ble_client_callback(args):
        global msg_queue
        msg_queue.put(args)


def ble_gatt_client_event_handler():
    global msg_queue
    old_time = 0

    while True:
        cur_time = utime.localtime()
        timestamp = "{:02d}:{:02d}:{:02d}".format(cur_time[3], cur_time[4], cur_time[5])
        if cur_time[5] != old_time and cur_time[5] % 5 == 0:
            old_time = cur_time[5]
            print('[{}]event handler running.....'.format(timestamp))
            print('')
        msg = msg_queue.get()  # 没有消息时会阻塞在这
        # print('msg : {}'.format(msg))
        event_id = msg[0]
        status = msg[1]

        if event_id == event.BLE_START_STATUS_IND:
            print('')
            print('event_id : BLE_START_STATUS_IND, status = {}'.format(status))
            if status == 0:
                print('BLE start successful.')
                ble_status = ble_client.gatt_get_status()
                if ble_status == 0:
                    print('BLE Status : stopped.')
                    break
                elif ble_status == 1:
                    print('BLE Status : started.')
                else:
                    print('get ble status error.')
                    ble_client.gatt_close()
                    break

                ret = ble_client.set_scan_param()
                if ret != 0:
                    ble_client.gatt_close()
                    break
                ret = ble_client.start_scan()
                if ret != 0:
                    ble_client.gatt_close()
                    break
            else:
                print('BLE start failed.')
                break
        elif event_id == event.BLE_STOP_STATUS_IND:
            print('')
            print('event_id : BLE_STOP_STATUS_IND, status = {}'.format(status))
            if status == 0:
                print('ble stop successful.')
            else:
                print('ble stop failed.')
                break
        elif event_id == event.BLE_CONNECT_IND:
            print('')
            print('event_id : BLE_CONNECT_IND, status = {}'.format(status))
            if status == 0:
                ble_client.connect_id = msg[2]
                ble_client.connect_addr = msg[3]
                addr = ble_client.connect_addr
                addr_str = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[0], addr[1], addr[2], addr[3], addr[4], addr[5])
                print('connect_id : {:#x}, connect_addr : {}'.format(ble_client.connect_id, addr_str))
            else:
                print('ble connect failed.')
                break
        elif event_id == event.BLE_DISCONNECT_IND:
            print('')
            print('event_id : BLE_DISCONNECT_IND, status = {}'.format(status))
            if status == 0:
                ble_client.connect_id = msg[2]
                ble_client.connect_addr = msg[3]
                addr = ble_client.connect_addr
                addr_str = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[0], addr[1], addr[2], addr[3], addr[4], addr[5])
                print('connect_id : {:#x}, connect_addr : {}'.format(ble_client.connect_id, addr_str))
            else:
                print('ble disconnect failed.')
            ble_client.gatt_close()
            break
        elif event_id == event.BLE_UPDATE_CONN_PARAM_IND:
            print('')
            print('event_id : BLE_UPDATE_CONN_PARAM_IND, status = {}'.format(status))
            if status == 0:
                connect_id = msg[2]
                max_interval = msg[3]
                min_interval = msg[4]
                latency = msg[5]
                timeout = msg[6]
                print('connect_id={},max_interval={},min_interval={},latency={},timeout={}'.format(connect_id,max_interval,min_interval,latency,timeout))
            else:
                print('ble update parameter failed.')
                ble_client.gatt_close()
                break
        elif event_id == event.BLE_SCAN_REPORT_IND:
            if status == 0:
                # print(' ble scan successful.')

                ble_client.scan_report_info['event_type'] = msg[2]
                ble_client.scan_report_info['name'] = msg[3]
                ble_client.scan_report_info['addr_type'] = msg[4]
                ble_client.scan_report_info['addr'] = msg[5]
                ble_client.scan_report_info['rssi'] = msg[6]
                ble_client.scan_report_info['data_len'] = msg[7]
                ble_client.scan_report_info['raw_data'] = msg[8]

                device_name = ble_client.scan_report_info['name']
                addr = ble_client.scan_report_info['addr']
                rssi = ble_client.scan_report_info['rssi']
                addr_type = ble_client.scan_report_info['addr_type']
                addr_str = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[0], addr[1], addr[2], addr[3], addr[4], addr[5])
                if device_name != '' and rssi != 0:
                    print('name: {}, addr: {}, rssi: {}, addr_type: {}'.format(device_name, addr_str, rssi, addr_type))
                    print('raw_data: {}'.format(ble_client.scan_report_info['raw_data']))

                if device_name == ble_client.ble_server_name: # 扫描到目标设备后就停止扫描
                    ret = ble_client.stop_scan()
                    if ret != 0:
                        ble_client.gatt_close()
                        break

                    ret = ble_client.connect()
                    if ret != 0:
                        ble_client.gatt_close()
                        break
            else:
                print('ble scan failed.')
                ret = ble_client.stop_scan()
                if ret != 0:
                    ble_client.gatt_close()
                    break
        elif event_id == event.BLE_GATT_MTU:
            print('')
            print('event_id : BLE_GATT_MTU, status = {}'.format(status))
            if status == 0:
                handle = msg[2]
                ble_mtu = msg[3]
                print('handle = {:#06x}, ble_mtu = {}'.format(handle, ble_mtu))
            else:
                print('ble connect mtu failed.')
                ble_client.gatt_close()
                break
        elif event_id == event.BLE_GATT_RECV_NOTIFICATION_IND:
            print('')
            print('event_id : BLE_GATT_RECV_NOTIFICATION_IND, status = {}'.format(status))
            if status == 0:
                data_len = msg[2]
                data = msg[3]
                print('len={}, data:{}'.format(data_len, data))
                handle = (data[1] << 8) | data[0]
                print('handle = {:#06x}'.format(handle))
            else:
                print('ble receive notification failed.')
                break
        elif event_id == event.BLE_GATT_RECV_INDICATION_IND:
            print('')
            print('event_id : BLE_GATT_RECV_INDICATION_IND, status = {}'.format(status))
            if status == 0:
                data_len = msg[2]
                data = msg[3]
                print('len={}, data:{}'.format(data_len, data))
            else:
                print('ble receive indication failed.')
                break
        elif event_id == event.BLE_GATT_START_DISCOVER_SERVICE_IND:
            print('')
            print('event_id : BLE_GATT_START_DISCOVER_SERVICE_IND, status = {}'.format(status))
            if status == 0:
                ble_client.characteristic_count = 0
                ble_client.chara_descriptor_count = 0
                ble_client.characteristic_index = 0
                ble_client.gatt_statue = gatt_status.BLE_GATT_DISCOVER_SERVICE

                if ble_client.discover_service_mode == 0:
                    print('execute the function discover_all_service.')
                    ret = ble_client.discover_all_service()
                else:
                    print('execute the function discover_service_by_uuid.')
                    ret = ble_client.discover_service_by_uuid()
                if ret != 0:
                    print('Execution result: Failed.')
                    ble_client.gatt_close()
                    break
            else:
                print('ble start discover service failed.')
                ble_client.gatt_close()
                break
        elif event_id == event.BLE_GATT_DISCOVER_SERVICE_IND:
            print('')
            print('event_id : BLE_GATT_DISCOVER_SERVICE_IND, status = {}'.format(status))
            if status == 0:
                start_handle = msg[2]
                end_handle = msg[3]
                short_uuid = msg[4]
                print('start_handle = {:#06x}, end_handle = {:#06x}, short_uuid = {:#06x}'.format(start_handle, end_handle, short_uuid))
                if ble_client.discover_service_mode == 0: # discover service all
                    if ble_client.target_service['short_uuid'] == short_uuid: # 查找到所有服务后，按指定uuid查找特征值
                        ble_client.target_service['start_handle'] = start_handle
                        ble_client.target_service['end_handle'] = end_handle
                        ble_client.gatt_statue = gatt_status.BLE_GATT_DISCOVER_CHARACTERISTIC
                        print('execute the function discover_all_characteristic.')
                        ret = ble_client.discover_all_characteristic()
                        if ret != 0:
                            print('Execution result: Failed.')
                            ble_client.gatt_close()
                            break
                else:
                    ble_client.target_service['start_handle'] = start_handle
                    ble_client.target_service['end_handle'] = end_handle
                    ble_client.gatt_statue = gatt_status.BLE_GATT_DISCOVER_CHARACTERISTIC
                    print('execute the function discover_all_characteristic.')
                    ret = ble_client.discover_all_characteristic()
                    if ret != 0:
                        print('Execution result: Failed.')
                        ble_client.gatt_close()
                        break
            else:
                print('ble discover service failed.')
                ble_client.gatt_close()
                break
        elif event_id == event.BLE_GATT_DISCOVER_CHARACTERISTIC_DATA_IND:
            print('')
            print('event_id : BLE_GATT_DISCOVER_CHARACTERISTIC_DATA_IND, status = {}'.format(status))
            if status == 0:
                data_len = msg[2]
                data = msg[3]
                pair_len = data[0]
                print('pair_len={}, len={}, data:{}'.format(pair_len, data_len, data))
                if data_len > 0:
                    if ble_client.gatt_statue == gatt_status.BLE_GATT_DISCOVER_CHARACTERISTIC:
                        i = 0
                        while i < (data_len - 1) / pair_len:
                            chara_dict = {
                                'handle': (data[i * pair_len + 2] << 8) | data[i * pair_len + 1],
                                'properties': data[i * pair_len + 3],
                                'value_handle': (data[i * pair_len + 5] << 8) | data[i * pair_len + 4],
                                'uuid_type': 0,
                                'short_uuid': 0x0000,
                                'long_uuid': bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
                            }
                            print('handle={:#06x}, properties={:#x}, value_handle={:#06x}'.format(chara_dict['handle'], chara_dict['properties'], chara_dict['value_handle']))
                            if pair_len == ble_client.ble_short_uuid_pair_len:
                                chara_dict['uuid_type'] = 1
                                chara_dict['short_uuid'] = (data[i * pair_len + 7] << 8) | data[i * pair_len + 6]
                                print('short_uuid:{:#06x}'.format(chara_dict['short_uuid']))
                            elif pair_len == ble_client.ble_long_uuid_pair_len:
                                start_index = i * pair_len + 6
                                end_index = start_index + 16
                                chara_dict['uuid_type'] = 0
                                chara_dict['long_uuid'] = data[start_index : end_index]
                                print('long_uuid:{}'.format(chara_dict['long_uuid']))
                            i += 1
                            if ble_client.characteristic_count < 5:
                                ble_client.characteristic_list.append(chara_dict)
                                ble_client.characteristic_count = len(ble_client.characteristic_list)
                            print('characteristic_list len = {}'.format(ble_client.characteristic_count))
                    elif ble_client.gatt_statue == gatt_status.BLE_GATT_READ_CHARA_VALUE:
                        print('data_len = {}'.format(data_len))
                        print('pay_load = {:02x},{:02x},{:02x},{:02x}'.format(data[0], data[1], data[2], data[3]))
            else:
                print('ble discover characteristic failed.')
                ble_client.gatt_close()
                break
        elif event_id == event.BLE_GATT_DISCOVER_CHARA_DESC_IND:
            print('')
            print('event_id : BLE_GATT_DISCOVER_CHARA_DESC_IND, status = {}'.format(status))
            if status == 0:
                data_len = msg[2]
                data = msg[3]
                fmt = data[0]
                print('fmt={}, len={}, data:{}'.format(fmt, data_len, data))
                if data_len > 0:
                    i = 0
                    if fmt == 1:  # 16 bit uuid
                        while i < (data_len - 1) / 4:
                            descriptor_dict = {
                                'handle': (data[i * 4 + 2] << 8) | data[i * 4 + 1],
                                'short_uuid': (data[i * 4 + 4] << 8) | data[i * 4 + 3],
                            }
                            print('handle={:#06x}, uuid={:#06x}'.format(descriptor_dict['handle'], descriptor_dict['short_uuid']))
                            i += 1
                            if ble_client.chara_descriptor_count < 5:
                                ble_client.descriptor_list.append(descriptor_dict)
                                ble_client.chara_descriptor_count = len(ble_client.descriptor_list)
                            print('descriptor_list len = {}'.format(ble_client.chara_descriptor_count))
                if ble_client.characteristic_index == ble_client.characteristic_count:
                    print('execute the function read_characteristic_by_uuid.')
                    # ble_client.gatt_statue = gatt_status.BLE_GATT_WRITE_CHARA_VALUE
                    # ret = ble_client.write_characteristic()
                    # ret = ble_client.write_characteristic_no_rsp()

                    ble_client.gatt_statue = gatt_status.BLE_GATT_READ_CHARA_VALUE
                    ret = ble_client.read_characteristic_by_uuid()
                    # ret = ble_client.read_characteristic_by_handle()

                    # ble_client.gatt_statue = gatt_status.BLE_GATT_READ_CHARA_DESC
                    # ret = ble_client.read_characteristic_descriptor()

                    # ble_client.gatt_statue = gatt_status.BLE_GATT_WRITE_CHARA_DESC
                    # ret = ble_client.write_characteristic_descriptor()
                else:
                    print('execute the function discover_all_characteristic_descriptor.')
                    ret = ble_client.discover_all_characteristic_descriptor()
                if ret != 0:
                    print('Execution result: Failed.')
                    ble_client.gatt_close()
                    break
            else:
                print('ble discover characteristic descriptor failed.')
                ble_client.gatt_close()
                break
        elif event_id == event.BLE_GATT_CHARA_WRITE_WITH_RSP_IND:
            print('')
            print('event_id : BLE_GATT_CHARA_WRITE_WITH_RSP_IND, status = {}'.format(status))
            if status == 0:
                if ble_client.gatt_statue == gatt_status.BLE_GATT_WRITE_CHARA_VALUE:
                    pass
                elif ble_client.gatt_statue == gatt_status.BLE_GATT_WRITE_CHARA_DESC:
                    pass
            else:
                print('ble write characteristic with response failed.')
                break
        elif event_id == event.BLE_GATT_CHARA_WRITE_WITHOUT_RSP_IND:
            print('')
            print('event_id : BLE_GATT_CHARA_WRITE_WITHOUT_RSP_IND, status = {}'.format(status))
            if status == 0:
                print('write characteristic value without response successful.')
            else:
                print('write characteristic value without response failed.')
                break
        elif event_id == event.BLE_GATT_CHARA_READ_IND:
            print('')
            # read characteristic value by handle
            print('event_id : BLE_GATT_CHARA_READ_IND, status = {}'.format(status))
            if status == 0:
                data_len = msg[2]
                data = msg[3]
                print('data_len = {}, data : {}'.format(data_len, data))
                if ble_client.gatt_statue == gatt_status.BLE_GATT_READ_CHARA_VALUE:
                    # print('read characteristic value by handle.')
                    pass
            else:
                print('ble read characteristic failed.')
                break
        elif event_id == event.BLE_GATT_CHARA_READ_BY_UUID_IND:
            print('')
            # read characteristic value by uuid
            print('event_id : BLE_GATT_CHARA_READ_BY_UUID_IND, status = {}'.format(status))
            if status == 0:
                data_len = msg[2]
                data = msg[3]
                print('data_len = {}, data : {}'.format(data_len, data))
                handle = (data[2] << 8) | data[1]
                print('handle = {:#06x}'.format(handle))
            else:
                print('ble read characteristic by uuid failed.')
                break
        elif event_id == event.BLE_GATT_CHARA_MULTI_READ_IND:
            print('')
            # read multiple characteristic value
            print('event_id : BLE_GATT_CHARA_MULTI_READ_IND, status = {}'.format(status))
            if status == 0:
                data_len = msg[2]
                data = msg[3]
                print('data_len = {}, data : {}'.format(data_len, data))
            else:
                print('ble read multiple characteristic by uuid failed.')
                break
        elif event_id == event.BLE_GATT_DESC_WRITE_WITH_RSP_IND:
            print('')
            print('event_id : BLE_GATT_DESC_WRITE_WITH_RSP_IND, status = {}'.format(status))
            if status == 0:
                if ble_client.gatt_statue == gatt_status.BLE_GATT_WRITE_CHARA_VALUE:
                    pass
                elif ble_client.gatt_statue == gatt_status.BLE_GATT_WRITE_CHARA_DESC:
                    pass
            else:
                print('ble write characteristic descriptor failed.')
                break
        elif event_id == event.BLE_GATT_DESC_READ_IND:
            print('')
            # read characteristic descriptor
            print('event_id : BLE_GATT_DESC_READ_IND, status = {}'.format(status))
            if status == 0:
                data_len = msg[2]
                data = msg[3]
                print('data_len = {}, data : {}'.format(data_len, data))
                if ble_client.gatt_statue == gatt_status.BLE_GATT_READ_CHARA_DESC:
                    # print('read characteristic descriptor.')
                    pass
            else:
                print('ble read characteristic descriptor failed.')
                break
        elif event_id == event.BLE_GATT_ATT_ERROR_IND:
            print('')
            print('event_id : BLE_GATT_ATT_ERROR_IND, status = {}'.format(status))
            if status == 0:
                errcode = msg[2]
                print('errcode = {:#06x}'.format(errcode))
                if ble_client.gatt_statue == gatt_status.BLE_GATT_DISCOVER_INCLUDES:
                    ble_client.gatt_statue = gatt_status.BLE_GATT_DISCOVER_CHARACTERISTIC
                    print('execute the function discover_all_characteristic.')
                    ret = ble_client.discover_all_characteristic()
                    if ret != 0:
                        print('Execution result: Failed.')
                        ble_client.gatt_close()
                        break
                elif ble_client.gatt_statue == gatt_status.BLE_GATT_DISCOVER_CHARACTERISTIC:
                    ble_client.gatt_statue = gatt_status.BLE_GATT_IDLE
                    print('execute the function discover_all_characteristic_descriptor.')
                    ret = ble_client.discover_all_characteristic_descriptor()
                    if ret != 0:
                        print('Execution result: Failed.')
                        ble_client.gatt_close()
                        break
            else:
                print('ble attribute error.')
                ble_client.gatt_close()
                break
        else:
            print('unknown event id : {}.'.format(event_id))

    # ble_client.release()


event = EVENT(event_dict)
gatt_status = EVENT(gatt_status_dict)
msg_queue = Queue(50)
ble_client = BleClient()


def main():
    checknet.poweron_print_once()
    print('create client event handler task.')
    _thread.start_new_thread(ble_gatt_client_event_handler, ())
    # ble.setScanFilter(0) # 关闭扫描过滤功能
    ret = ble_client.gatt_open()
    if ret != 0:
        return -1

    count = 0
    while True:
        utime.sleep(1)
        count += 1
        cur_time = utime.localtime()
        timestamp = "{:02d}:{:02d}:{:02d}".format(cur_time[3], cur_time[4], cur_time[5])
        if count % 5 == 0:
            print('[{}] BLE Client running, count = {}......'.format(timestamp, count))
            print('')
        if count > 130: # 这里设置计数是为了程序运行一会自己退出，方便测试，实际根据用户需要来处理
            count = 0
            print('!!!!! stop BLE Client now !!!!!')
            ble_status = ble_client.gatt_get_status()
            if ble_status == 1:
                ble_client.gatt_close()
            ble_client.release()
            break
        else:
            ble_status = ble_client.gatt_get_status()
            if ble_status == 0: # stopped
                print('BLE connection has been disconnected.')
                ble_client.release()
                break

if __name__ == '__main__':
    main()

```

**注意**：

当前仅EC200U/EC600U/EG915U/EG912U平台支持`ble`功能。

## 初始化相关功能

### ble.gattStart

```python
ble.gattStart()
```

开启 BLE GATT 功能。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.gattStop

```python
ble.gattStop()
```

关闭 BLE GATT 功能。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.getStatus

```python
ble.getStatus()
```

获取 BLE 的状态。

**返回值描述：**

- 0 - BLE处于停止状态。1 - BLE处于开启状态。-1 - 获取状态失败。

### ble.getPublicAddr

```python
ble.getPublicAddr()
```

获取 BLE 协议栈正在使用的公共地址。该接口需要在BLE已经初始化完成并启动成功后才能调用，比如在回调中收到 event_id 为0的事件之后，即 start 成功后，去调用。

**返回值描述：**

- 执行成功返回bytearray类型的BLE地址，大小6个byte，失败返回整型-1。

**示例**：

```python
>>> addr = ble.getPublicAddr()
>>> print(addr)
b'\xdb3\xf5\x1ek\xac'
>>> mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
>>> print('mac = [{}]'.format(mac))
mac = [ac:6b:1e:f5:33:db]
```

**注意**：

如果有出厂设置默认蓝牙MAC地址，那么该接口获取的MAC地址和默认的蓝牙MAC地址是一致的；如果没有设置，那么该接口获取的地址，将是蓝牙启动后随机生成的静态地址，因此在每次重新上电运行蓝牙功能时都不相同。

## BLE Server相关功能

### ble.serverInit

```python
ble.serverInit(user_cb)
```

初始化 BLE Server 并注册回调函数。

**参数描述：**

- `user_cb`-回调函数，类型为function。回调函数参数含义：args[0] 固定表示event_id，args[1]固定 表示状态，0表示成功，非0表示失败。回调函数的参数个数并不是固定2个，而是根据第一个参数args[0]来决定的，下表中列出了不同事件ID对应的参数个数及说明。

| event_id | 参数个数 | 参数说明                                                     |
| :------: | :------: | ------------------------------------------------------------ |
|    0     |    2     | args[0] ：event_id，表示 BT/BLE start<br>args[1] ：status，表示操作的状态，0-成功，非0-失败 |
|    1     |    2     | args[0] ：event_id，表示 BT/BLE stop<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败 |
|    16    |    4     | args[0] ：event_id，表示 BLE connect<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：connect_id<br/>args[3] ：addr，BT/BLE address，bytearray类型数据 |
|    17    |    4     | args[0] ：event_id，表示 BLE disconnect<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：connect_id，<br/>args[3] ：addr，BT/BLE address，bytearray类型数据 |
|    18    |    7     | args[0] ：event_id，表示 BLE update connection parameter<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：connect_id<br/>args[3] ：max_interval，最大的间隔，间隔：1.25ms，取值范围：6-3200，时间范围：7.5ms\ ~ 4s<br/>args[4] ：min_interval，最小的间隔，间隔：1.25ms，取值范围：6-3200，时间范围：7.5ms\ ~ 4s<br/>args[5] ：latency，从机忽略连接状态事件的时间。需满足：（1+latecy)\*max_interval\*2\*1.25<timeout\*10<br/>args[6] ：timeout，没有交互，超时断开时间，间隔：10ms，取值范围：10-3200ms，时间范围：100ms ~ 32s |
|    20    |    4     | args[0] ：event_id，表示 BLE connection mtu<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：handle<br/>args[3] ：mtu值 |
|    21    |    7     | args[0] ：event_id，表示 BLE server : when ble client write characteristic value or descriptor,server get the notice<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：data_len，获取数据的长度<br/>args[3] ：data，一个数组，存放获取的数据<br/>args[4] ：attr_handle，属性句柄，整型值<br/>args[5] ：short_uuid，整型值<br/>args[6] ：long_uuid，一个16字节数组，存放长UUID |
|    22    |    7     | args[0] ：event_id，表示 server : when ble client read characteristic value or descriptor,server get the notice<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：data_len，获取数据的长度<br/>args[3] ：data，一个数组，存放获取的数据<br/>args[4] ：attr_handle，属性句柄，整型值<br/>args[5] ：short_uuid，整型值<br/>args[6] ：long_uuid，一个16字节数组，存放长UUID |
|    25    |    2     | args[0] ：event_id，表示 server send notification,and recieve send end notice<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败 |

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

```python
def ble_callback(args):
    event_id = args[0]
    status = args[1]
    print('[ble_callback]: event_id={}, status={}'.format(event_id, status))

    if event_id == 0:  # ble start
        if status == 0:
            print('[callback] BLE start success.')
        else:
            print('[callback] BLE start failed.')
    elif event_id == 1:  # ble stop
        if status == 0:
            print('[callback] ble stop successful.')
        else:
            print('[callback] ble stop failed.')
    elif event_id == 16:  # ble connect
        if status == 0:
            print('[callback] ble connect successful.')
            connect_id = args[2]
            addr = args[3] # 这是一个bytearray类型
            addr_str = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[0], addr[1], addr[2], addr[3], addr[4], addr[5])
            print('[callback] connect_id = {}, addr = {}'.format(connect_id, addr_str))
        else:
            print('[callback] ble connect failed.')
    elif event_id == 17:  # ble disconnect
        if status == 0:
            print('[callback] ble disconnect successful.')
            connect_id = args[2]
            addr = args[3] # 这是一个bytearray类型
            addr_str = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[0], addr[1], addr[2], addr[3], addr[4], addr[5])
            print('[callback] connect_id = {}, addr = {}'.format(connect_id, addr_str))
        else:
            print('[callback] ble disconnect failed.')
            ble.gattStop()
            return
    elif event_id == 18:  # ble update connection parameter
        if status == 0:
            print('[callback] ble update parameter successful.')
            connect_id = args[2]
            max_interval = args[3]
            min_interval = args[4]
            latency = args[5]
            timeout = args[6]
            print('[callback] connect_id={},max_interval={},min_interval={},latency={},timeout={}'.format(connect_id, max_interval, min_interval, latency, timeout))
        else:
            print('[callback] ble update parameter failed.')
            ble.gattStop()
            return
    elif event_id == 20:  # ble connection mtu
        if status == 0:
            print('[callback] ble connect mtu successful.')
            handle = args[2]
            ble_mtu = args[3]
            print('[callback] handle = {:#06x}, ble_mtu = {}'.format(handle, ble_mtu))
        else:
            print('[callback] ble connect mtu failed.')
            ble.gattStop()
            return
    elif event_id == 21:  # server:when ble client write characteristic value or descriptor,server get the notice
        if status == 0:
            print('[callback] ble recv successful.')
            data_len = args[2]
            data = args[3]  # 这是一个bytearray类型
            attr_handle = args[4]
            short_uuid = args[5]
            long_uuid = args[6]  # 这是一个bytearray类型
            print('len={}, data:{}'.format(data_len, data))
            print('attr_handle = {:#06x}'.format(attr_handle))
            print('short uuid = {:#06x}'.format(short_uuid))
            print('long uuid = {}'.format(long_uuid))
        else:
            print('[callback] ble recv failed.')
            ble.gattStop()
            return
    elif event_id == 22:  # server:when ble client read characteristic value or descriptor,server get the notice
        if status == 0:
            print('[callback] ble recv read successful.')
            data_len = args[2]
            data = args[3]  # 这是一个bytearray类型
            attr_handle = args[4]
            short_uuid = args[5]
            long_uuid = args[6]  # 这是一个bytearray类型
            print('len={}, data:{}'.format(data_len, data))
            print('attr_handle = {:#06x}'.format(attr_handle))
            print('short uuid = {:#06x}'.format(short_uuid))
            print('long uuid = {}'.format(long_uuid))
        else:
            print('[callback] ble recv read failed.')
            ble.gattStop()
            return
    elif event_id == 25:  # server send notification,and recieve send end notice
        if status == 0:
            print('[callback] ble send data successful.')
        else:
            print('[callback] ble send data failed.')
    else:
        print('unknown event id.')

ble.serverInit(ble_callback)
```

### ble.serverRelease

```python
ble.serverRelease()
```

BLE Server 资源释放。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.setLocalName

```python
ble.setLocalName(code, name)
```

设置 BLE 名称。

**参数描述：**

- `code`-编码模式，类型为整型。0 - UTF8，1 - GBK。
- `name`-编码模式，类型为string。BLE 名称，名称最长不能超过29个字节。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

```python
>>> ble.setLocalName(0, 'QuecPython-BLE')
0
```

**注意**：

对于BLE，设备在广播时，如果希望扫描软件扫描时，能看到广播设备的名称，是需要在广播数据中包含蓝牙名称的，或者在扫描回复数据中包含设备名称。

### ble.setAdvParam

```python
ble.setAdvParam(min_adv,max_adv,adv_type,addr_type,channel,filter_policy,discov_mode,no_br_edr,enable_adv)
```

设置广播参数。

**参数描述：**

- 参数含义如下表。

| 参数          | 类型       | 说明                                                         |
| ------------- | ---------- | ------------------------------------------------------------ |
| min_adv       | 无符号整型 | 最小广播间隔，范围0x0020-0x4000，计算如下：<br>时间间隔 = min_adv \* 0.625，单位ms |
| max_adv       | 无符号整型 | 最大广播间隔，范围0x0020-0x4000，计算如下：<br/>时间间隔 = max_adv \* 0.625，单位ms |
| adv_type      | 无符号整型 | 广播类型，取值范围如下：<br>0 - 可连接的非定向广播，默认选择<br>1 - 可连接高占空比的定向广播<br>2 - 可扫描的非定向广播<br>3 - 不可连接的非定向广播<br>4 - 可连接低占空比的定向广播 |
| addr_type     | 无符号整型 | 本地地址类型，取值范围如下：<br>0 - 公共地址<br>1 - 随机地址 |
| channel       | 无符号整型 | 广播通道，取值范围如下：<br>1 - 37信道<br>2 - 38信道<br>4 - 39信道<br>7 - 上述3个通道都选择，默认该选项 |
| filter_policy | 无符号整型 | 广播过滤策略，取值范围如下：<br>0 - 处理所有设备的扫描和连接请求<br/>1 - 处理所有设备的连接请求和只处理白名单设备的扫描请求（暂不支持）<br/>2 - 处理所有设备的扫描请求和只处理白名单设备的连接请求（暂不支持）<br/>3 - 只处理白名单设备的连接和扫描请求（暂不支持） |
| discov_mode   | 无符号整型 | 发现模式，GAP协议使用，默认为2<br/>1 - 有限可发现模式<br/>2 - 一般可发现模式 |
| no_br_edr     | 无符号整型 | 不用BR/EDR，默认为1，如果用则为0                             |
| enable_adv    | 无符号整型 | 使能广播，默认为1，不使能则为0                               |

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

```python
def ble_gatt_set_param():
    min_adv = 0x300
    max_adv = 0x320
    adv_type = 0  # 可连接的非定向广播，默认选择
    addr_type = 0  # 公共地址
    channel = 0x07
    filter_strategy = 0  # 处理所有设备的扫描和连接请求
    discov_mode = 2
    no_br_edr = 1
    enable_adv = 1
    ret = ble.setAdvParam(min_adv, max_adv, adv_type, addr_type, channel, filter_strategy, discov_mode, no_br_edr, enable_adv)
    if ret != 0:
        print('ble_gatt_set_param failed.')
        return -1
    print('ble_gatt_set_param success.')
    return 0
```

### ble.setAdvData

```python
ble.setAdvData(data)
```

设置广播数据内容。

**参数描述：**

- `data`-广播数据，最长不超过31个字节，类型为bytearray。广播数据的内容，采用 length+type+data 的格式。一条广播数据中可以包含多个这种格式数据的组合，如下示例中包含了两个数据组合，第一个是 "0x02, 0x01, 0x05"，0x02表示后面有两个数据，分别是0x01和0x05，0x01即type，0x05表示具体数据；第二个是ble名称数据组合， length为ble名称长度加1、type为0x09，具体数据为name对应的具体编码值。关于type具体值代表的含义，请参考蓝牙协议官方标准文档。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

```python
def ble_gatt_set_data():
    adv_data = [0x02, 0x01, 0x05]
    ble_name = "Quectel_ble"
    length = len(ble_name) + 1
    adv_data.append(length)
    adv_data.append(0x09)
    name_encode = ble_name.encode('UTF-8')
    for i in range(0, len(name_encode)):
        adv_data.append(name_encode[i])
    print('set adv_data:{}'.format(adv_data))
    data = bytearray(adv_data)
    ret = ble.setAdvData(data)
    if ret != 0:
        print('ble_gatt_set_data failed.')
        return -1
    print('ble_gatt_set_data success.')
    return 0
```

### ble.setAdvRspData

```python
ble.setAdvRspData(data)
```

设置扫描回复数据。

**参数描述：**

- `data`-扫描回复数据，最长不超过31个字节，类型为bytearray。 格式和上面设置广播数据内容接口一致。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

```python
def ble_gatt_set_rsp_data():
    adv_data = []
    ble_name = "Quectel_ble"
    length = len(ble_name) + 1
    adv_data.append(length)
    adv_data.append(0x09)
    name_encode = ble_name.encode('UTF-8')
    for i in range(0, len(name_encode)):
        adv_data.append(name_encode[i])
    print('set adv_rsp_data:{}'.format(adv_data))
    data = bytearray(adv_data)
    ret = ble.setAdvRspData(data)
    if ret != 0:
        print('ble_gatt_set_rsp_data failed.')
        return -1
    print('ble_gatt_set_rsp_data success.')
    return 0
```

**注意**：

当client设备扫描方式为积极扫描时，设置扫描回复数据才有意义。

### ble.addService

```python
ble.addService(primary, server_id, uuid_type, uuid_s, uuid_l)
```

增加一个服务。

**参数描述：**

- `primary`-服务类型，1表示主要服务，其他值表示次要服务，类型为整型。
- `server_id`-服务ID，用来确定某一个服务，类型为整型。 
- `uuid_type`-uuid类型，0 - 长UUID，128bit；1 - 短UUID，16bit。类型为整型。 
- `uuid_s`-短UUID，2个字节（16bit），类型为整型，当uuid_type为0时，该值给0。
- `uuid_l`-长UUID，16个字节（128bit），类型为bytearray，当uuid_type为1时，该值填 bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])。 

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

```python
def ble_gatt_add_service():
    primary = 1
    server_id = 0x01
    uuid_type = 1  # 短UUID
    uuid_s = 0x180F
    uuid_l = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    ret = ble.addService(primary, server_id, uuid_type, uuid_s, uuid_l)
    if ret != 0:
        print('ble_gatt_add_service failed.')
        return -1
    print('ble_gatt_add_service success.')
    return 0
```

### ble.addChara

```python
ble.addChara(server_id, chara_id, chara_prop, uuid_type, uuid_s, uuid_l)
```

在服务里增加一个特征。

**参数描述：**

- `server_id`-服务ID，用来确定某一个服务，类型为整型。
- `chara_id`-特征ID，类型为整型。 
- `chara_prop`-特征的属性，十六进制数，可通过“或运算”同时指定多个属性，值具体含义如下表，类型为整型。 

| 值   | 含义                          |
| ---- | ----------------------------- |
| 0x01 | 广播                          |
| 0x02 | 可读                          |
| 0x04 | 0x04 - 可写且不需要链路层应答 |
| 0x08 | 可写                          |
| 0x10 | 通知                          |
| 0x20 | 指示                          |
| 0x40 | 认证签名写                    |
| 0x80 | 扩展属性                      |

- `uuid_type`-uuid类型，0 - 长UUID，128bit；1 - 短UUID，16bit。类型为整型。
- `uuid_s`-短UUID，2个字节（16bit），类型为整型，当uuid_type为0时，该值给0。
- `uuid_l`-长UUID，16个字节（128bit），类型为bytearray，当uuid_type为1时，该值填 bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])。 

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

```python
def ble_gatt_add_characteristic():
    server_id = 0x01
    chara_id = 0x01
    chara_prop = 0x02 | 0x10 | 0x20  # 0x02-可读 0x10-通知 0x20-指示
    uuid_type = 1  # 短UUID
    uuid_s = 0x2A19
    uuid_l = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    ret = ble.addChara(server_id, chara_id, chara_prop, uuid_type, uuid_s, uuid_l)
    if ret != 0:
        print('ble_gatt_add_characteristic failed.')
        return -1
    print('ble_gatt_add_characteristic success.')
    return 0
```

### ble.addCharaValue

```python
ble.addCharaValue(server_id, chara_id, permission, uuid_type, uuid_s, uuid_l, value)
```

在特征里增加一个特征值。

**参数描述：**

- `server_id`-服务ID，用来确定某一个服务，类型为整型。
- `chara_id`-特征ID，类型为整型。 
- `permission`-特征值的权限，2个字节，十六进制数，可通过“或运算”同时指定多个属性，值具体含义如下表，类型为整型。 

| 值     | 含义           |
| ------ | -------------- |
| 0x0001 | 可读权限       |
| 0x0002 | 可写权限       |
| 0x0004 | 读需要认证     |
| 0x0008 | 读需要授权     |
| 0x0010 | 读需要加密     |
| 0x0020 | 读需要授权认证 |
| 0x0040 | 写需要认证     |
| 0x0080 | 写需要授权     |
| 0x0100 | 写需要加密     |
| 0x0200 | 写需要授权认证 |

- `uuid_type`-uuid类型，0 - 长UUID，128bit；1 - 短UUID，16bit。类型为整型。
- `uuid_s`-短UUID，2个字节（16bit），类型为整型，当uuid_type为0时，该值给0。
- `uuid_l`-长UUID，16个字节（128bit），类型为bytearray，当uuid_type为1时，该值填 bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])。 
- `value`-特征值数据。类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

```python
def ble_gatt_add_characteristic_value():
    data = []
    server_id = 0x01
    chara_id = 0x01
    permission = 0x0001 | 0x0002
    uuid_type = 1  # 短UUID
    uuid_s = 0x2A19
    uuid_l = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    for i in range(0, 244):
        data.append(0x00)
    value = bytearray(data)
    ret = ble.addCharaValue(server_id, chara_id, permission, uuid_type, uuid_s, uuid_l, value)
    if ret != 0:
        print('ble_gatt_add_characteristic_value failed.')
        return -1
    print('ble_gatt_add_characteristic_value success.')
    return 0
```

### ble.changeCharaValue

```python
ble.changeCharaValue(server_id, chara_id, value)
```

修改特征值。

**参数描述：**

- `server_id`-服务ID，用来确定某一个服务，类型为整型。
- `chara_id`-特征ID，类型为整型。  

- `value`-特征值数据。类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.addCharaDesc

```python
ble.addCharaDesc(server_id, chara_id, permission, uuid_type, uuid_s, uuid_l, value)
```

在特征里增加一个特征描述，注意特征描述和特征值同属与一个特征。

**参数描述：**

- `server_id`-服务ID，用来确定某一个服务，类型为整型。
- `chara_id`-特征ID，类型为整型。 
- `permission`-特征值的权限，2个字节，十六进制数，可通过“或运算”同时指定多个属性，值具体含义如下表，类型为整型。 

| 值     | 含义           |
| ------ | -------------- |
| 0x0001 | 可读权限       |
| 0x0002 | 可写权限       |
| 0x0004 | 读需要认证     |
| 0x0008 | 读需要授权     |
| 0x0010 | 读需要加密     |
| 0x0020 | 读需要授权认证 |
| 0x0040 | 写需要认证     |
| 0x0080 | 写需要授权     |
| 0x0100 | 写需要加密     |
| 0x0200 | 写需要授权认证 |

- `uuid_type`-uuid类型，0 - 长UUID，128bit；1 - 短UUID，16bit。类型为整型。
- `uuid_s`-短UUID，2个字节（16bit），类型为整型，当uuid_type为0时，该值给0。
- `uuid_l`-长UUID，16个字节（128bit），类型为bytearray，当uuid_type为1时，该值填 bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])。 
- `value`-特征描述数据。类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

```python
def ble_gatt_add_characteristic_desc():
    data = [0x00, 0x00]
    server_id = 0x01
    chara_id = 0x01
    permission = 0x0001 | 0x0002
    uuid_type = 1  # 短UUID
    uuid_s = 0x2902
    uuid_l = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    value = bytearray(data)
    ret = ble.addCharaDesc(server_id, chara_id, permission, uuid_type, uuid_s, uuid_l, value)
    if ret != 0:
        print('ble_gatt_add_characteristic_desc failed.')
        return -1
    print('ble_gatt_add_characteristic_desc success.')
    return 0
```

### ble.addOrClearService

```python
ble.addOrClearService(option, mode)
```

增加前面已添加的所有服务信息到模块，或者删除模块中已增加的所有服务信息。

**参数描述：**

- `option`-操作类型，类型为整型。0 - 删除服务，1 - 增加服务。
- `mode`-是否保留系统默认服务，类型为整型。 0 - 删除系统默认的GAP和GATT服务，1 - 保留系统默认的GAP和GATT服务。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.sendNotification

```python
ble.sendNotification(connect_id, attr_handle, value)
```

发送通知。

**参数描述：**

- `connect_id`-连接ID，类型为整型。
- `attr_handle`-属性句柄，类型为整型。 
- `value`-要发送的数据，发送数据长度不要超过MTU，类型为bytearray。 

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.sendIndication

```python
ble.sendIndication(connect_id, attr_handle, value)
```

发送指示。

**参数描述：**

- `connect_id`-连接ID，类型为整型。
- `attr_handle`-属性句柄，类型为整型。 
- `value`-要发送的数据，发送数据长度不要超过MTU，类型为bytearray。 

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.advStart

```python
ble.advStart()
```

开启广播。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.advStop

```python
ble.advStop()
```

停止广播。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

## BLE Client相关功能

### ble.clientInit

```python
ble.clientInit(user_cb)
```

初始化 BLE Client 并注册回调函数。

**参数描述：**

- `user_cb`-回调函数，类型为function。回调函数参数含义：args[0] 固定表示event_id，args[1] 固定表示状态，0表示成功，非0表示失败。回调函数的参数个数并不是固定2个，而是根据第一个参数args[0]来决定的，下表中列出了不同事件ID对应的参数个数及说明。

| event_id | 参数个数 | 参数说明                                                     |
| :------: | :------: | ------------------------------------------------------------ |
|    0     |    2     | args[0] ：event_id，表示 BT/BLE start<br>args[1] ：status，表示操作的状态，0-成功，非0-失败 |
|    1     |    2     | args[0] ：event_id，表示 BT/BLE stop<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败 |
|    16    |    4     | args[0] ：event_id，表示 BLE connect<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：connect_id<br/>args[3] ：addr，BT/BLE address，bytearray类型数据 |
|    17    |    4     | args[0] ：event_id，表示 BLE disconnect<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：connect_id，<br/>args[3] ：addr，BT/BLE address，bytearray类型数据 |
|    18    |    7     | args[0] ：event_id，表示 BLE update connection parameter<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：connect_id<br/>args[3] ：max_interval，最大的间隔，间隔：1.25ms，取值范围：6-3200，时间范围：7.5ms ~ 4s<br/>args[4] ：min_interval，最小的间隔，间隔：1.25ms，取值范围：6-3200，时间范围：7.5ms ~ 4s<br/>args[5] ：latency，从机忽略连接状态事件的时间。需满足：（1+latecy)\*max_interval\*2\*1.25<timeout\*10<br/>args[6] ：timeout，没有交互，超时断开时间，间隔：10ms，取值范围：10-3200，时间范围：100ms ~ 32s |
|    19    |    9     | args[0] ：event_id，表示 BLE scan report<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：event_type<br/>args[3] ：扫描到的设备名称<br/>args[4] ：设备地址类型<br/>args[5] ：设备地址，bytearray类型数据<br/>args[6] ：rssi，信号强度<br/>args[7] ：data_len，扫描的原始数据长度<br/>args[8] ：data，扫描的原始数据 |
|    20    |    4     | args[0] ：event_id，表示 BLE connection mtu<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：handle<br/>args[3] ：mtu值 |
|    23    |    4     | args[0] ：event_id，表示 client recieve notification，即接收通知<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：data_len，数据长度<br/>args[3] ：data，包含句柄等数据的原始数据，数据格式及解析见最后的综合示例程序 |
|    24    |    4     | args[0] ：event_id，表示 client recieve indication，即接收指示<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：data_len，数据长度<br/>args[3] ：data，包含indication的原始数据，数据格式及解析见最后的综合示例程序 |
|    26    |    2     | args[0] ：event_id，表示 start discover service，即开始查找服务<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败 |
|    27    |    5     | args[0] ：event_id，表示 discover service，即查找到服务<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：start_handle，表示service的开始句柄<br/>args[3] ：end_handle，表示service的结束句柄<br/>args[4] ：UUID，表示service的UUID（短UUID） |
|    28    |    4     | args[0] ：event_id，表示 discover characteristic，即查找服务特征<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：data_len，数据长度<br/>args[3] ：data，包含句柄、属性、UUID等数据的原始数据，数据格式及解析见最后的综合示例程序 |
|    29    |    4     | args[0] ：event_id，表示 discover characteristic descriptor，即查找特征描述<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：data_len，数据长度<br/>args[3] ：data，包含句柄、UUID等数据的原始数据，数据格式及解析见最后的综合示例程序 |
|    30    |    2     | args[0] ：event_id，表示 write characteristic value with response，即写入特征值并需要链路层确认<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败 |
|    31    |    2     | args[0] ：event_id，表示 write characteristic value without response，即写入特征值，无需链路层确认<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败 |
|    32    |    4     | args[0] ：event_id，表示 read characteristic value by handle，即通过句柄来读取特征值<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：data_len，数据长度<br/>args[3] ：data，原始数据 |
|    33    |    4     | args[0] ：event_id，表示 read characteristic value by uuid，即通过UUID来读取特征值<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：data_len，数据长度<br/>args[3] ：data，原始数据 |
|    34    |    4     | args[0] ：event_id，表示 read miltiple characteristic value，即读取多个特征值<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：data_len，数据长度<br/>args[3] ：data，原始数据 |
|    35    |    2     | args[0] ：event_id，表示 wirte characteristic descriptor，即写入特征描述，需链路层确认<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败 |
|    36    |    4     | args[0] ：event_id，表示 read characteristic descriptor，即读特征描述<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：data_len，数据长度<br/>args[3] ：data，原始数据 |
|    37    |    3     | args[0] ：event_id，表示 attribute error，即属性错误<br/>args[1] ：status，表示操作的状态，0-成功，非0-失败<br/>args[2] ：errcode，错误码 |

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.clientRelease

```python
ble.clientRelease()
```

BLE Client 资源释放。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.setScanParam

```python
ble.setScanParam(scan_mode, interval, scan_window, filter_policy, addr_type)
```

设置扫描参数。

**参数描述：**

- `scan_mode`-扫描模式，类型为整型。扫描模式，默认为积极扫描。0 - 消极扫描，1 - 积极扫描。
- `interval`-扫描间隔，类型为整型。范围0x0004-0x4000，时间间隔 = interval \* 0.625，单位ms。
- `scan_window`-一次扫描的时间，类型为整型。范围0x0004-0x4000，扫描时间 = scan_window\* 0.625，单位ms。
- `filter_policy`-扫描过滤策略，类型为整型。默认为0。0 - 除了不是本设备的定向广播，其他所有的广播包，1 - 除了不是本设备的定向广播，白名单设备的广播包，2 - 非定向广播，指向本设备的定向广播或使用Resolvable private address的定向广播，3 - 白名单设备非定向广播，指向本设备的定向广播或使用Resolvable private address的定向广播。
- `addr_type`-本地地址类型，类型为整型。0 - 公共地址，1 - 随机地址。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**注意**：

扫描时间 `scan_window` 不能大于扫描间隔 `interval` 。如果两者相等，则表示连续不停的扫描。此时 BLE 的 Controller 会连续运行扫描，占满系统资源而导致无法执行其他任务。所以不允许设置连续扫描。并且不建议将时间设置的太短，扫描越频繁则功耗越高。

### ble.scanStart

```python
ble.scanStart()
```

开始扫描。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.scanStop

```python
ble.scanStop()
```

停止扫描。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.setScanFilter

```python
ble.setScanFilter(act)
```

打开或者关闭扫描过滤。如果打开，那么扫描设备的广播数据时，同一个设备的广播数据只会上报一次；如果关闭，则同一个设备的所有的广播数据都会上报。

**参数描述：**

- `act`-扫描过滤开关，类型为整型。0 - 关闭扫描过滤功能，1 - 打开扫描过滤功能。默认打开过滤功能。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.connect

```python
ble.connect(addr_type, addr)
```

根据指定的设备地址去连接设备。

**参数描述：**

- `addr_type`-地址类型，类型为整型。0 - 公共地址，1 - 随机地址。
- `addr`-BLE地址，类型为bytearray，大小为6字节。  

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.cancelConnect

```python
ble.cancelConnect(addr)
```

取消正在建立的连接。

**参数描述：**

- `addr`-BLE地址，类型为bytearray，大小为6字节。  

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.disconnect

```python
ble.disconnect(connect_id)
```

断开已建立的连接。

**参数描述：**

- `connect_id`-连接ID，建立连接时得到的连接ID，类型为整型。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.discoverAllService

```python
ble.discoverAllService(connect_id)
```

扫描所有的服务。

**参数描述：**

- `connect_id`-连接ID，建立连接时得到的连接ID，类型为整型。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.discoverByUUID

```python
ble.discoverByUUID(connect_id, uuid_type, uuid_s, uuid_l)
```

扫描指定UUID的服务。

**参数描述：**

- `connect_id`-连接ID，建立连接时得到的连接ID，类型为整型。
- `uuid_type`-uuid类型，0 - 长UUID，128bit；1 - 短UUID，16bit。类型为整型。
- `uuid_s`-短UUID，2个字节（16bit），类型为整型，当uuid_type为0时，该值给0。
- `uuid_l`-长UUID，16个字节（128bit），类型为bytearray，当uuid_type为1时，该值填 bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.discoverAllIncludes

```python
ble.discoverAllIncludes(connect_id, start_handle, end_handle)
```

扫描所有的引用，start_handle和end_handle要属于同一个服务。

**参数描述：**

- `connect_id`-连接ID，建立连接时得到的连接ID，类型为整型。
- `start_handle`-开始句柄，从这个句柄开始寻找引用，类型为整型。
- `end_handle`-结束句柄，从这个句柄结束寻找引用，类型为整型。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.discoverAllChara

```python
ble.discoverAllChara(connect_id, start_handle, end_handle)
```

扫描所有的特征，start_handle和end_handle要属于同一个服务。

**参数描述：**

- `connect_id`-连接ID，建立连接时得到的连接ID，类型为整型。
- `start_handle`-开始句柄，从这个句柄开始寻找特征，类型为整型。
- `end_handle`-结束句柄，从这个句柄结束寻找特征，类型为整型。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.discoverAllCharaDesc

```python
ble.discoverAllCharaDesc(connect_id, start_handle, end_handle)
```

扫描所有特征的描述，start_handle和end_handle要属于同一个服务。

**参数描述：**

- `connect_id`-连接ID，建立连接时得到的连接ID，类型为整型。
- `start_handle`-开始句柄，从这个句柄开始寻找特征描述，类型为整型。
- `end_handle`-结束句柄，从这个句柄结束寻找特征描述，类型为整型。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.readCharaByUUID

```python
ble.readCharaByUUID(connect_id, start_handle, end_handle, uuid_type, uuid_s, uuid_l)
```

读取指定UUID的特征值，start_handle和end_handle必须要包含一个特征值句柄。

**参数描述：**

- `connect_id`-连接ID，建立连接时得到的连接ID，类型为整型。
- `start_handle`-开始句柄，一定要属于同一个特征的句柄，类型为整型。
- `end_handle`-结束句柄，结束句柄，一定要属于同一个特征的句柄，类型为整型。
- `uuid_type`-uuid类型，0 - 长UUID，128bit；1 - 短UUID，16bit。类型为整型。
- `uuid_s`-短UUID，2个字节（16bit），类型为整型，当uuid_type为0时，该值给0。
- `uuid_l`-长UUID，16个字节（128bit），类型为bytearray，当uuid_type为1时，该值填 bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.readCharaByHandle

```python
ble.readCharaByHandle(connect_id, handle, offset, is_long)
```

读取指定句柄的特征值。

**参数描述：**

- `connect_id`-连接ID，建立连接时得到的连接ID，类型为整型。
- `handle`-特征值句柄，类型为整型。
- `offset`-偏移位置，类型为整型。
- `is_long`-长特征值标志，0-短特征值，一次可以读取完；1-长特征值，分多次读取。类型为整型。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.readCharaDesc

```python
ble.readCharaDesc(connect_id, handle, is_long)
```

读取特征描述。

**参数描述：**

- `connect_id`-连接ID，建立连接时得到的连接ID，类型为整型。
- `handle`-特征值句柄，类型为整型。
- `is_long`-长特征值标志，0-短特征值，一次可以读取完；1-长特征值，分多次读取。类型为整型。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.writeChara

```python
ble.writeChara(connect_id, handle, offset, is_long, data)
```

写入特征值，需要对端应答。

**参数描述：**

- `connect_id`-连接ID，建立连接时得到的连接ID，类型为整型。
- `handle`-特征值句柄，类型为整型。
- `offset`-偏移位置，类型为整型。
- `is_long`-长特征值标志，0-短特征值，一次可以读取完；1-长特征值，分多次读取。类型为整型。
- `data`-特征值数据，类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.writeCharaNoRsp

```python
ble.writeCharaNoRsp(connect_id, handle, data)
```

写入特征值，不需要对端应答。

**参数描述：**

- `connect_id`-连接ID，建立连接时得到的连接ID，类型为整型。
- `handle`-特征值句柄，类型为整型。
- `data`-特征值数据，类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### ble.writeCharaDesc

```python
ble.writeCharaDesc(connect_id, handle, data)
```

写入特征描述。

**参数描述：**

- `connect_id`-连接ID，建立连接时得到的连接ID，类型为整型。
- `handle`-特征描述句柄，类型为整型。
- `data`-特征描述数据，类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。