# bt - 经典蓝牙相关功能

`bt`模块提供经典蓝牙的相关功能，支持HFP、A2DP、AVRCP、SPP。

**示例**：

```python
#HFP 示例程序

"""
示例说明：本例程提供一个通过HFP自动接听电话的功能
运行平台：EC600UCN_LB 铀开发板
运行本例程后，通过手机A搜索到设备名并点击连接；然后通过手机B拨打电话给手机A，
当手机A开始响铃震动时，设备会自动接听电话
"""
import bt
import utime
import _thread
from queue import Queue
from machine import Pin

# 如果对应播放通道外置了PA，且需要引脚控制PA开启，则需要下面步骤
# 具体使用哪个GPIO取决于实际使用的引脚
gpio11 = Pin(Pin.GPIO11, Pin.OUT, Pin.PULL_DISABLE, 0)
gpio11.write(1)

BT_NAME = 'QuecPython-hfp'

BT_EVENT = {
    'BT_START_STATUS_IND': 0,           # bt/ble start
    'BT_STOP_STATUS_IND': 1,            # bt/ble stop
    'BT_HFP_CONNECT_IND': 40,           # bt hfp connected
    'BT_HFP_DISCONNECT_IND': 41,        # bt hfp disconnected
    'BT_HFP_CALL_IND': 42,              # bt hfp call state
    'BT_HFP_CALL_SETUP_IND': 43,        # bt hfp call setup state
    'BT_HFP_NETWORK_IND': 44,           # bt hfp network state
    'BT_HFP_NETWORK_SIGNAL_IND': 45,    # bt hfp network signal
    'BT_HFP_BATTERY_IND': 46,           # bt hfp battery level
    'BT_HFP_CALLHELD_IND': 47,          # bt hfp callheld state
    'BT_HFP_AUDIO_IND': 48,             # bt hfp audio state
    'BT_HFP_VOLUME_IND': 49,            # bt hfp volume type
    'BT_HFP_NETWORK_TYPE': 50,          # bt hfp network type
    'BT_HFP_RING_IND': 51,              # bt hfp ring indication
    'BT_HFP_CODEC_IND': 52,             # bt hfp codec type
}

HFP_CONN_STATUS = 0
HFP_CONN_STATUS_DICT = {
    'HFP_DISCONNECTED': 0,
    'HFP_CONNECTING': 1,
    'HFP_CONNECTED': 2,
    'HFP_DISCONNECTING': 3,
}
HFP_CALL_STATUS = 0
HFP_CALL_STATUS_DICT = {
    'HFP_NO_CALL_IN_PROGRESS': 0,
    'HFP_CALL_IN_PROGRESS': 1,
}

BT_IS_RUN = 0

msg_queue = Queue(30)


def get_key_by_value(val, d):
    for key, value in d.items():
        if val == value:
            return key
    return None

def bt_callback(args):
    global msg_queue
    msg_queue.put(args)

def bt_event_proc_task():
    global msg_queue
    global BT_IS_RUN
    global BT_EVENT
    global HFP_CONN_STATUS
    global HFP_CONN_STATUS_DICT
    global HFP_CALL_STATUS
    global HFP_CALL_STATUS_DICT

    while True:
        print('wait msg...')
        msg = msg_queue.get()  # 没有消息时会阻塞在这
        event_id = msg[0]
        status = msg[1]

        if event_id == BT_EVENT['BT_START_STATUS_IND']:
            print('event: BT_START_STATUS_IND')
            if status == 0:
                print('BT start successfully.')
                BT_IS_RUN = 1
                bt_status = bt.getStatus()
                if bt_status == 1:
                    print('BT status is 1, normal status.')
                else:
                    print('BT status is {}, abnormal status.'.format(bt_status))
                    bt.stop()
                    break

                retval = bt.getLocalName()
                if retval != -1:
                    print('The current BT name is : {}'.format(retval[1]))
                else:
                    print('Failed to get BT name.')
                    bt.stop()
                    break

                print('Set BT name to {}'.format(BT_NAME))
                retval = bt.setLocalName(0, BT_NAME)
                if retval != -1:
                    print('BT name set successfully.')
                else:
                    print('BT name set failed.')
                    bt.stop()
                    break

                retval = bt.getLocalName()
                if retval != -1:
                    print('The new BT name is : {}'.format(retval[1]))
                else:
                    print('Failed to get new BT name.')
                    bt.stop()
                    break

                # 设置蓝牙可见模式为：可以被发现并且可以被连接
                retval = bt.setVisibleMode(3)
                if retval == 0:
                    mode = bt.getVisibleMode()
                    if mode == 3:
                        print('BT visible mode set successfully.')
                    else:
                        print('BT visible mode set failed.')
                        bt.stop()
                        break
                else:
                    print('BT visible mode set failed.')
                    bt.stop()
                    break
            else:
                print('BT start failed.')
                bt.stop()
                break
        elif event_id == BT_EVENT['BT_STOP_STATUS_IND']:
            print('event: BT_STOP_STATUS_IND')
            if status == 0:
                BT_IS_RUN = 0
                print('BT stop successfully.')
            else:
                print('BT stop failed.')
            break
        elif event_id == BT_EVENT['BT_HFP_CONNECT_IND']:
            HFP_CONN_STATUS = msg[2]
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_CONNECT_IND, {}, hfp_conn_status:{}, mac:{}'.format(status, get_key_by_value(msg[2], HFP_CONN_STATUS_DICT), mac))
            if status != 0:
                print('BT HFP connect failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_HFP_DISCONNECT_IND']:
            HFP_CONN_STATUS = msg[2]
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_DISCONNECT_IND, {}, hfp_conn_status:{}, mac:{}'.format(status, get_key_by_value(msg[2], HFP_CONN_STATUS_DICT), mac))
            if status != 0:
                print('BT HFP disconnect failed.')
            bt.stop()
        elif event_id == BT_EVENT['BT_HFP_CALL_IND']:
            call_sta = msg[2]
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_CALL_IND, {}, hfp_call_status:{}, mac:{}'.format(status, get_key_by_value(msg[2], HFP_CALL_STATUS_DICT), mac))
            if status != 0:
                print('BT HFP call failed.')
                bt.stop()
                continue

            if call_sta == HFP_CALL_STATUS_DICT['HFP_NO_CALL_IN_PROGRESS']:
                if HFP_CALL_STATUS == HFP_CALL_STATUS_DICT['HFP_CALL_IN_PROGRESS']:
                    HFP_CALL_STATUS = call_sta
                    if HFP_CONN_STATUS == HFP_CONN_STATUS_DICT['HFP_CONNECTED']:
                        print('call ended, ready to disconnect hfp.')
                        retval = bt.hfpDisconnect(addr)
                        if retval == 0:
                            HFP_CONN_STATUS = HFP_CONN_STATUS_DICT['HFP_DISCONNECTING']
                        else:
                            print('Failed to disconnect hfp connection.')
                            bt.stop()
                            continue
            else:
                if HFP_CALL_STATUS == HFP_CALL_STATUS_DICT['HFP_NO_CALL_IN_PROGRESS']:
                    HFP_CALL_STATUS = call_sta
                    print('set audio output channel to 2.')
                    bt.setChannel(2)
                    print('set volume to 7.')
                    retval = bt.hfpSetVolume(addr, 7)
                    if retval != 0:
                        print('set volume failed.')
        elif event_id == BT_EVENT['BT_HFP_CALL_SETUP_IND']:
            call_setup_status = msg[2]
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_CALL_SETUP_IND, {}, hfp_call_setup_status:{}, mac:{}'.format(status, call_setup_status, mac))
            if status != 0:
                print('BT HFP call setup failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_HFP_CALLHELD_IND']:
            callheld_status = msg[2]
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_CALLHELD_IND, {}, callheld_status:{}, mac:{}'.format(status, callheld_status, mac))
            if status != 0:
                print('BT HFP callheld failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_HFP_NETWORK_IND']:
            network_status = msg[2]
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_NETWORK_IND, {}, network_status:{}, mac:{}'.format(status, network_status, mac))
            if status != 0:
                print('BT HFP network status failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_HFP_NETWORK_SIGNAL_IND']:
            network_signal = msg[2]
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_NETWORK_SIGNAL_IND, {}, signal:{}, mac:{}'.format(status, network_signal, mac))
            if status != 0:
                print('BT HFP network signal failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_HFP_BATTERY_IND']:
            battery_level = msg[2]
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_BATTERY_IND, {}, battery_level:{}, mac:{}'.format(status, battery_level, mac))
            if status != 0:
                print('BT HFP battery level failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_HFP_AUDIO_IND']:
            audio_status = msg[2]
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_AUDIO_IND, {}, audio_status:{}, mac:{}'.format(status, audio_status, mac))
            if status != 0:
                print('BT HFP audio failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_HFP_VOLUME_IND']:
            volume_type = msg[2]
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_VOLUME_IND, {}, volume_type:{}, mac:{}'.format(status, volume_type, mac))
            if status != 0:
                print('BT HFP volume failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_HFP_NETWORK_TYPE']:
            service_type = msg[2]
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_NETWORK_TYPE, {}, service_type:{}, mac:{}'.format(status, service_type, mac))
            if status != 0:
                print('BT HFP network service type failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_HFP_RING_IND']:
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_RING_IND, {}, mac:{}'.format(status, mac))
            if status != 0:
                print('BT HFP ring failed.')
                bt.stop()
                continue
            retval = bt.hfpAnswerCall(addr)
            if retval == 0:
                print('The call was answered successfully.')
            else:
                print('Failed to answer the call.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_HFP_CODEC_IND']:
            codec_type = msg[2]
            addr = msg[3]  # BT 主机端mac地址
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('BT_HFP_CODEC_IND, {}, codec_type:{}, mac:{}'.format(status, codec_type, mac))
            if status != 0:
                print('BT HFP codec failed.')
                bt.stop()
                continue
    print('Ready to release hfp.')
    bt.hfpRelease()
    bt.release()


def main():
    global BT_IS_RUN

    _thread.start_new_thread(bt_event_proc_task, ())

    retval = bt.init(bt_callback)
    if retval == 0:
        print('BT init successful.')
    else:
        print('BT init failed.')
        return -1
    retval = bt.hfpInit()
    if retval == 0:
        print('HFP init successful.')
    else:
        print('HFP init failed.')
        return -1
    retval = bt.start()
    if retval == 0:
        print('BT start successful.')
    else:
        print('BT start failed.')
        retval = bt.hfpRelease()
        if retval == 0:
            print('HFP release successful.')
        else:
            print('HFP release failed.')
        retval = bt.release()
        if retval == 0:
            print('BT release successful.')
        else:
            print('BT release failed.')
        return -1

    count = 0
    while True:
        utime.sleep(1)
        count += 1
        cur_time = utime.localtime()
        timestamp = "{:02d}:{:02d}:{:02d}".format(cur_time[3], cur_time[4], cur_time[5])

        if count % 5 == 0:
            if BT_IS_RUN == 1:
                print('[{}] BT HFP is running, count = {}......'.format(timestamp, count))
                print('')
            else:
                print('BT HFP has stopped running, ready to exit.')
                break


if __name__ == '__main__':
    main()

```

```python
#A2DP/AVRCP 示例程序

"""
示例说明：本例程提供一个通过A2DP/AVRCP实现的简易蓝牙音乐播放控制功能
运行本例程后，通过手机搜索到设备名并点击连接；然后打开手机上的音乐播放软件，
回到例程运行界面，根据提示菜单输入对应的控制命令来实现音乐的播放、暂停、上一首、
下一首以及设置音量的功能
"""
import bt
import utime
import _thread
from queue import Queue
from machine import Pin

BT_STATUS_DICT = {
    'BT_NOT_RUNNING': 0,
    'BT_IS_RUNNING': 1
}

A2DP_AVRCP_CONNECT_STATUS = {
    'DISCONNECTED': 0,
    'CONNECTING': 1,
    'CONNECTED': 2,
    'DISCONNECTING': 3
}

host_addr = 0
msg_queue = Queue(10)

# 如果对应播放通道外置了PA，且需要引脚控制PA开启，则需要下面步骤
# 具体使用哪个GPIO取决于实际使用的引脚
gpio11 = Pin(Pin.GPIO11, Pin.OUT, Pin.PULL_DISABLE, 0)
gpio11.write(1)


def cmd_proc(cmd):
    cmds = ('1', '2', '3', '4', '5')
    vols = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11')

    if cmd in cmds:
        if cmd == '5':
            while True:
                tmp = input('Please input volume: ')
                if len(tmp) != 1:
                    vol = tmp.split('Please input volume: ')[1]
                else:
                    vol = tmp
                if vol in vols:
                    return cmd, int(vol)
                else:
                    print('Volume should be in [0,11], try again.')
        else:
            return cmd, 0
    else:
        print('Command {} is not supported!'.format(cmd))
        return -1

def avrcp_play(args):
    return bt.avrcpStart()

def avrcp_pause(args):
    return bt.avrcpPause()

def avrcp_prev(args):
    return bt.avrcpPrev()

def avrcp_next(args):
    return bt.avrcpNext()

def avrcp_set_volume(vol):
    return bt.avrcpSetVolume(vol)

def bt_callback(args):
    pass

def bt_a2dp_avrcp_proc_task():
    global msg_queue

    cmd_handler = {
        '1': avrcp_play,
        '2': avrcp_pause,
        '3': avrcp_prev,
        '4': avrcp_next,
        '5': avrcp_set_volume,
    }
    while True:
        # print('wait msg...')
        msg = msg_queue.get()
        print('recv msg: {}'.format(msg))
        cmd_handler.get(msg[0])(msg[1])


def main():
    global host_addr
    global msg_queue

    _thread.start_new_thread(bt_a2dp_avrcp_proc_task, ())
    bt.init(bt_callback)
    bt.setChannel(2)
    retval = bt.a2dpavrcpInit()
    if retval == 0:
        print('BT A2DP/AVRCP initialization succeeded.')
    else:
        print('BT A2DP/AVRCP initialization failed.')
        return -1

    retval = bt.start()
    if retval != 0:
        print('BT start failed.')
        return -1

    utime.sleep_ms(1500)

    old_name = bt.getLocalName()
    if old_name == -1:
        print('Get BT name error.')
        return -1
    print('The current BT name is {}'.format(old_name[1]))
    new_name = 'QuecPython-a2dp'
    print('Set new BT name to {}'.format(new_name))
    retval = bt.setLocalName(0, new_name)
    if retval == -1:
        print('Set BT name failed.')
        return -1
    cur_name = bt.getLocalName()
    if cur_name == -1:
        print('Get new BT name error.')
        return -1
    else:
        if cur_name[1] == new_name:
            print('BT name changed successfully.')
        else:
            print('BT name changed failed.')

    visible_mode = bt.getVisibleMode()
    if visible_mode != -1:
        print('The current BT visible mode is {}'.format(visible_mode))
    else:
        print('Get BT visible mode error.')
        return -1

    print('Set BT visible mode to 3.')
    retval = bt.setVisibleMode(3)
    if retval == -1:
        print('Set BT visible mode error.')
        return -1

    print('BT reconnect check start......')    
    bt.reconnect_set(25, 2)
    bt.reconnect()

    count = 0
    while True:
        count += 1
        if count % 5 == 0:
            print('waiting to be connected...')
        if count >= 10000:
            count = 0
        a2dp_status = bt.a2dpGetConnStatus()
        avrcp_status = bt.avrcpGetConnStatus()
        if a2dp_status == A2DP_AVRCP_CONNECT_STATUS['CONNECTED'] and avrcp_status == A2DP_AVRCP_CONNECT_STATUS['CONNECTED']:
            print('========== BT connected! =========')
            addr = bt.a2dpGetAddr()
            if addr != -1:
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
                print('The BT address on the host side: {}'.format(mac))
                host_addr = addr
            else:
                print('Get BT addr error.')
                return -1
            print('Please open the music player software on your phone first.')
            print('Please enter the following options to select a function:')
            print('========================================================')
            print('1 : play')
            print('2 : pause')
            print('3 : prev')
            print('4 : next')
            print('5 : set volume')
            print('6 : exit')
            print('========================================================')
            while True:
                tmp = input('> ')
                if len(tmp) != 1:
                    cmd = tmp.split('> ')[1]
                else:
                    cmd = tmp
                if cmd == '6':
                    break
                retval = cmd_proc(cmd)
                if retval != -1:
                    msg_queue.put(retval)
            break
        else:
            utime.sleep_ms(1000)
    print('Ready to disconnect a2dp.')
    retval = bt.a2dpDisconnect(host_addr)
    if retval == 0:
        print('a2dp connection disconnected successfully')
    else:
        print('Disconnect a2dp error.')
    print('Ready to stop BT.')
    retval = bt.stop()
    if retval == 0:
        print('BT has stopped.')
    else:
        print('BT stop error.')
    bt.a2dpavrcpRelease()
    bt.release()


if __name__ == '__main__':
    main()
```

```python
#SPP 示例程序

"""
示例说明：本例程提供一个通过SPP实现与手机端进行数据传输的功能
（1）运行之前，需要先在手机端（安卓）安装蓝牙串口APP，如BlueSPP，然后打开该软件；
（2）修改本例程中的目标设备的蓝牙名称，即 DST_DEVICE_INFO['dev_name'] 的值改为用户准备连接的手机的蓝牙名称；
（3）运行本例程，例程中会先发起搜索周边设备的操作，直到搜索到目标设备，就会结束搜索，然后向目标设备发起SPP连接请求；
（4）用户注意查看手机界面是否弹出蓝牙配对请求的界面，当出现时，点击配对；
（5）配对成功后，用户即可进入到蓝牙串口界面，发送数据给设备，设备在收到数据后会回复“I have received the data you sent.”
（6）手机端APP中点击断开连接，即可结束例程；
"""
import bt
import utime
import _thread
from queue import Queue


BT_NAME = 'QuecPython-SPP'

BT_EVENT = {
    'BT_START_STATUS_IND': 0,          # bt/ble start
    'BT_STOP_STATUS_IND': 1,           # bt/ble stop
    'BT_SPP_INQUIRY_IND': 6,           # bt spp inquiry ind
    'BT_SPP_INQUIRY_END_IND': 7,       # bt spp inquiry end ind
    'BT_SPP_RECV_DATA_IND': 14,        # bt spp recv data ind
    'BT_SPP_CONNECT_IND': 61,          # bt spp connect ind
    'BT_SPP_DISCONNECT_IND': 62,       # bt spp disconnect ind
}

DST_DEVICE_INFO = {
    'dev_name': 'HUAWEI Mate40 Pro', # 要连接设备的蓝牙名称
    'bt_addr': None
}

BT_IS_RUN = 0
msg_queue = Queue(30)


def bt_callback(args):
    global msg_queue
    msg_queue.put(args)


def bt_event_proc_task():
    global msg_queue
    global BT_IS_RUN
    global DST_DEVICE_INFO

    while True:
        print('wait msg...')
        msg = msg_queue.get()  # 没有消息时会阻塞在这
        event_id = msg[0]
        status = msg[1]

        if event_id == BT_EVENT['BT_START_STATUS_IND']:
            print('event: BT_START_STATUS_IND')
            if status == 0:
                print('BT start successfully.')
                BT_IS_RUN = 1

                print('Set BT name to {}'.format(BT_NAME))
                retval = bt.setLocalName(0, BT_NAME)
                if retval != -1:
                    print('BT name set successfully.')
                else:
                    print('BT name set failed.')
                    bt.stop()
                    continue

                retval = bt.setVisibleMode(3)
                if retval == 0:
                    mode = bt.getVisibleMode()
                    if mode == 3:
                        print('BT visible mode set successfully.')
                    else:
                        print('BT visible mode set failed.')
                        bt.stop()
                        continue
                else:
                    print('BT visible mode set failed.')
                    bt.stop()
                    continue

                retval = bt.startInquiry(15)
                if retval != 0:
                    print('Inquiry error.')
                    bt.stop()
                    continue
            else:
                print('BT start failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_STOP_STATUS_IND']:
            print('event: BT_STOP_STATUS_IND')
            if status == 0:
                BT_IS_RUN = 0
                print('BT stop successfully.')
            else:
                print('BT stop failed.')

            retval = bt.sppRelease()
            if retval == 0:
                print('SPP release successfully.')
            else:
                print('SPP release failed.')
            retval = bt.release()
            if retval == 0:
                print('BT release successfully.')
            else:
                print('BT release failed.')
            break
        elif event_id == BT_EVENT['BT_SPP_INQUIRY_IND']:
            print('event: BT_SPP_INQUIRY_IND')
            if status == 0:
                rssi = msg[2]
                name = msg[4]
                addr = msg[5]
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
                print('name: {}, addr: {}, rssi: {}'.format(name, mac, rssi))

                if name == DST_DEVICE_INFO['dev_name']:
                    print('The target device is found, device name {}'.format(name))
                    DST_DEVICE_INFO['bt_addr'] = addr
                    retval = bt.cancelInquiry()
                    if retval != 0:
                        print('cancel inquiry failed.')
                        continue
            else:
                print('BT inquiry failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_SPP_INQUIRY_END_IND']:
            print('event: BT_SPP_INQUIRY_END_IND')
            if status == 0:
                print('BT inquiry has ended.')
                inquiry_sta = msg[2]
                if inquiry_sta == 0:
                    if DST_DEVICE_INFO['bt_addr'] is not None:
                        print('Ready to connect to the target device : {}'.format(DST_DEVICE_INFO['dev_name']))
                        retval = bt.sppConnect(DST_DEVICE_INFO['bt_addr'])
                        if retval != 0:
                            print('SPP connect failed.')
                            bt.stop()
                            continue
                    else:
                        print('Not found device [{}], continue to inquiry.'.format(DST_DEVICE_INFO['dev_name']))
                        bt.cancelInquiry()
                        bt.startInquiry(15)
            else:
                print('Inquiry end failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_SPP_RECV_DATA_IND']:
            print('event: BT_SPP_RECV_DATA_IND')
            if status == 0:
                datalen = msg[2]
                data = msg[3]
                print('recv {} bytes data: {}'.format(datalen, data))
                send_data = 'I have received the data you sent.'
                print('send data: {}'.format(send_data))
                retval = bt.sppSend(send_data)
                if retval != 0:
                    print('send data faied.')
            else:
                print('Recv data failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_SPP_CONNECT_IND']:
            print('event: BT_SPP_CONNECT_IND')
            if status == 0:
                conn_sta = msg[2]
                addr = msg[3]
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
                print('SPP connect successful, conn_sta = {}, addr {}'.format(conn_sta, mac))
            else:
                print('Connect failed.')
                bt.stop()
                continue
        elif event_id == BT_EVENT['BT_SPP_DISCONNECT_IND']:
            print('event: BT_SPP_DISCONNECT_IND')
            conn_sta = msg[2]
            addr = msg[3]
            mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
            print('SPP disconnect successful, conn_sta = {}, addr {}'.format(conn_sta, mac))
            bt.stop()
            continue


def main():
    global BT_IS_RUN

    _thread.start_new_thread(bt_event_proc_task, ())
    retval = bt.init(bt_callback)
    if retval == 0:
        print('BT init successful.')
    else:
        print('BT init failed.')
        return -1
    retval = bt.sppInit()
    if retval == 0:
        print('SPP init successful.')
    else:
        print('SPP init failed.')
        return -1
    retval = bt.start()
    if retval == 0:
        print('BT start successful.')
    else:
        print('BT start failed.')
        retval = bt.sppRelease()
        if retval == 0:
            print('SPP release successful.')
        else:
            print('SPP release failed.')
        return -1

    count = 0
    while True:
        utime.sleep(1)
        count += 1
        cur_time = utime.localtime()
        timestamp = "{:02d}:{:02d}:{:02d}".format(cur_time[3], cur_time[4], cur_time[5])

        if count % 5 == 0:
            if BT_IS_RUN == 1:
                print('[{}] BT SPP is running, count = {}......'.format(timestamp, count))
                print('')
            else:
                print('BT SPP has stopped running, ready to exit.')
                break


if __name__ == '__main__':
    main()
```

**注意**：

当前仅EC200U/EC600U/EG915U/EG912U平台支持`bt`功能。

## 初始化相关功能

### bt.init

```python
bt.init(user_cb)
```

蓝牙初始化并注册回调函数。

**参数描述：**

- `user_cb`-回调函数，类型为function。回调函数参数含义：args[0] 固定表示event_id，args[1] 固定表示状态，0表示成功，非0表示失败。回调函数的参数个数并不是固定2个，而是根据第一个参数args[0]来决定的，下表中列出了不同事件ID对应的参数个数及说明。

| event_id | 参数个数 | 参数说明                                                     |
| :------: | :------: | ------------------------------------------------------------ |
|    0     |    2     | args[0] ：event_id，表示 BT/BLE start 事件<br>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败 |
|    1     |    2     | args[0] ：event_id，表示 BT/BLE stop<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败 |
|    6     |    6     | args[0] ：event_id，表示 BT inquiry 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：rssi，搜索到的设备的信号强度；<br/>args[3] ：device_class <br/>args[4] ：device_name，设备名称，字符串类型<br/>args[5] ：addr，搜到的蓝牙设备的mac地址 |
|    7     |    3     | args[0] ：event_id，表示 BT inquiry end 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：end_status，0 - 正常结束搜索，8 - 强制结束搜索 |
|    14    |    4     | args[0] ：event_id，表示 BT spp recv 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：data_len，收到的数据长度<br/>args[3] ：data，收到的数据，bytearray类型数据 |
|    40    |    4     | args[0] ：event_id，表示 BT HFP connect 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：hfp_connect_status，表示hfp的连接状态；<br/>                 0 - 已经断开连接<br/>                 1 - 连接中<br/>                 2 - 已经连接<br/>                 3 - 断开连接中<br/>args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    41    |    4     | args[0] ：event_id，表示 BT HFP disconnect 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：hfp_connect_status，表示hfp的连接状态；<br/>                 0 - 已经断开连接<br/>                 1 - 连接中<br/>                 2 - 已经连接<br/>                 3 - 断开连接中<br/>args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    42    |    4     | args[0] ：event_id，表示 BT HFP call status 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：hfp_call_status，表示hfp的通话状态；<br/>                 0 - 当前没有正在进行的通话<br/>                 1 - 当前至少有一个正在进行的通话<br/> args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    43    |    4     | args[0] ：event_id，表示 BT HFP call setup status 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：hfp_call_setup_status，表示hfp的call setup状态；<br/>                 0 - 表示没有电话需要接通<br/>                 1 - 表示有一个拨进来的电话还未接通<br/>                 2 - 表示有一个拨出去的电话还没有接通<br/>                 3 - 表示拨出电话的蓝牙连接的另一方正在响铃<br/> args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    44    |    4     | args[0] ：event_id，表示 BT HFP network status 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：hfp_network_status，表示AG的网络状态；<br/>                 0 - 表示网络不可用<br/>                 1 - 表示网络正常<br/>args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    45    |    4     | args[0] ：event_id，表示 BT HFP network signal 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：hfp_network_signal，表示AG的信号，范围 0~5<br/>args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    46    |    4     | args[0] ：event_id，表示 BT HFP battery level 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：hfp_battery_level，表示AG端的电池电量，范围 0~5<br/>args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    47    |    4     | args[0] ：event_id，表示 BT HFP call held status 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：hfp_call_held_status，表示hfp的call held状态；<br/>                 0 - 表示没有保持呼叫<br/>                 1 - 表示呼叫被暂停或活动/保持呼叫交换<br/>                 2 - 表示呼叫暂停，没有活动呼叫<br/>args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    48    |    4     | args[0] ：event_id，表示 BT HFP audio status 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：hfp_audio_status，表示audio连接状态；<br/>                 0 - 表示audio已经断开连接<br/>                 1 - 表示audio正在连接中<br/>                 2 - 表示audio已经连接成功<br/>                 3 - 表示audio正在断开连接<br>args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    49    |    4     | args[0] ：event_id，表示 BT HFP volume type 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：hfp_volume_type<br/>                 0 - 表示volume type为speaker<br/>                 1 - 表示volume type为microphone<br/>args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    50    |    4     | args[0] ：event_id，表示 BT HFP service type 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：hfp_service_type，表示当前AG的网络服务模式；<br/>                 0 - 表示AG当前为正常网络模式<br/>                 1 - 表示AG当前处于漫游模式<br/>args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    51    |    4     | args[0] ：event_id，表示 BT HFP ring 事件，即来电时响铃事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：当前无实际意义，保留<br/>args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    52    |    4     | args[0] ：event_id，表示 BT HFP codec type 事件，即编解码模式<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：hfp_codec_type，表示当前使用哪个编解码模式；<br/>                 1 - 表示 CVDS，采用8kHz采样率<br/>                 2 - 表示mSBC，采用16kHz采样率<br/>args[3] ：addr，BT 主设备的地址，bytearray类型数据 |
|    61    |    4     | args[0] ：event_id，表示 BT SPP connect 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：spp_connect_status，表示spp的连接状态；<br/>                 0 - 已经断开连接<br/>                 1 - 连接中<br/>                 2 - 已经连接<br/>                 3 - 断开连接中<br/> args[3] ：addr，对端设备的mac地址，bytearray类型数据 |
|    62    |    4     | args[0] ：event_id，表示 BT SPP disconnect 事件<br/>args[1] ：status，表示操作的状态，0 - 成功，非0 - 失败<br/>args[2] ：spp_connect_status，表示spp的连接状态；<br/>                 0 - 已经断开连接<br/>                 1 - 连接中<br/>                 2 - 已经连接<br/>                 3 - 断开连接中<br/> args[3] ：addr，对端设备的mac地址，bytearray类型数据 |

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

```python
def bt_callback(args):
	event_id = args[0]  # 第一个参数固定是 event_id
	status = args[1] # 第二个参数固定是状态，表示某个操作的执行结果是成功还是失败
	......
```

### bt.release

```python
bt.release()
```

蓝牙资源释放。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.start

```python
bt.start()
```

开启蓝牙功能。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.stop

```python
bt.stop()
```

关闭蓝牙功能。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.getStatus

```python
bt.getStatus()
```

获取蓝牙的状态。

**返回值描述：**

- 蓝牙状态：类型为整型，0-蓝牙处于停止状态，1-蓝牙正常运行中，-1-获取状态失败。

### bt.getLocalAddr

```python
bt.getLocalAddr()
```

获取蓝牙地址。

**返回值描述：**

- 蓝牙地址：执行成功返回类型为bytearray的蓝牙地址，大小6字节，失败返回整型-1。

**示例**：

```python
>>> addr = bt.getLocalAddr()
>>> print(addr)
b'\xc7\xa13\xf8\xbf\x1a'
>>> mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
>>> print('mac = [{}]'.format(mac))
mac = [1a:bf:f8:33:a1:c7]
```

**注意**：

该接口需要在蓝牙已经初始化完成并启动成功后才能调用，比如在回调中收到 event_id 为0的事件之后，即 start 成功后，去调用。

### bt.setLocalName

```python
bt.setLocalName(code, name)
```

设置蓝牙名称。

**参数描述：**

- `code`-编码模式，类型为整型，0 - UTF8，1 - GBK。
- `name`-蓝牙名称，类型为string，最大长度22字节。

**返回值描述：**

- 蓝牙地址：执行成功返回类型为bytearray的蓝牙地址，大小6字节，失败返回整型-1。

**示例**：

```python
>>> bt.setLocalName(0, 'QuecPython-BT')
0
```

### bt.getLocalName

```python
bt.getLocalName()
```

获取蓝牙名称。

**返回值描述：**

- 执行成功返回一个元组`(code, name)`，包含名称编码模式和蓝牙名称，失败返回整型-1。


**示例**：

```python
>>> bt.getLocalName()
(0, 'QuecPython-BT')
```

### bt.setVisibleMode

```python
bt.setVisibleMode(mode)
```

设置蓝牙可见模式，即做从机时，被扫描时，是否可见以及可连接。

**参数描述：**

- `mode`-可见模式，类型为整型，具体含义如下表。

| 值   | 含义                     |
| ---- | ------------------------ |
| 0    | 不可被发现，不可被连接   |
| 1    | 可以被发现，但不可被连接 |
| 2    | 不可被发现，但可被连接   |
| 3    | 可以被发现，可被连接     |

**返回值描述：**

- 蓝牙地址：执行成功返回类型为bytearray的蓝牙地址，大小6字节，失败返回整型-1。

**示例**：

```python
>>> bt.setVisibleMode(3)
0
```

### bt.getVisibleMode

```python
bt.getVisibleMode()
```

获取蓝牙可见模式。

**返回值描述：**

- 执行成功返回蓝牙当前的可见模式值，失败返回整型-1。

**示例**：

```python
>>> bt.getVisibleMode()
3
```

### bt.startInquiry

```python
bt.startInquiry(mode)
```

开始搜索周边的蓝牙设备。

**参数描述：**

- `mode`-搜索类型。表示查询哪一类设备，当前直接写15，表示搜索所有。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

```python
bt.startInquiry(15)
```

### bt.cancelInquiry

```python
bt.cancelInquiry()
```

取消搜索操作。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.setChannel

```python
bt.setChannel(channel)
```

设置音频输出通道，使用场景为蓝牙接听电话或者播放音频时。

**参数描述：**

- `channel`-音频通道，类型为整型。0 - 听筒，1 - 耳机，2 - 喇叭。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.reconnect_set

```python
bt.reconnect_set(max_count, period)
```

配置尝试重连的最大次数和相邻2次尝试重连的时间间隔，使用场景为模块和蓝牙设备距离拉远后断开连接时。

**参数描述：**

- `max_count`-尝试重连的最大次数，类型为整型，设置0则关闭自动重连功能。
- `period`-相邻2次尝试重连的时间间隔，单位秒，类型为整型。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

```python
bt.reconnect_set(25, 2)#配置尝试重连的最大次数为25，每次尝试重连的间隔为2秒
```

### bt.reconnect

```python
bt.reconnect()
```

模组主动重连上次配对过的设备，如手机。使用场景为模组重启后重新初始化打开蓝牙、或者模组不重启仅关闭蓝牙再重新打开蓝牙。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

**示例**：

参考A2DP示例程序。

## HFP相关功能

提供蓝牙通话相关功能。

### bt.hfpInit

```python
bt.hfpInit()
```

HFP 功能初始化 。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.hfpRelease

```python
bt.hfpRelease()
```

HFP 资源释放。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.hfpConnect

```python
bt.hfpConnect(addr)
```

连接AG，建立HFP连接。

**参数描述：**

- `addr`-AG端蓝牙地址，6个字节，类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.hfpDisonnect

```python
bt.hfpDisonnect(addr)
```

断开HFP连接。

**参数描述：**

- `addr`-AG端蓝牙地址，6个字节，类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.hfpSetVolume

```python
bt.hfpSetVolume(addr, vol)
```

设置蓝牙通话时的音量。

**参数描述：**

- `addr`-AG端蓝牙地址，6个字节，类型为bytearray。
- `vol`-通话音量，类型为整型，范围 1-15。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.hfpRejectAfterAnswer

```python
bt.hfpRejectAfterAnswer(addr)
```

挂断接通的电话。

**参数描述：**

- `addr`-AG端蓝牙地址，6个字节，类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.hfpRejectCall

```python
bt.hfpRejectCall(addr)
```

拒接电话。

**参数描述：**

- `addr`-AG端蓝牙地址，6个字节，类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.hfpAnswerCall

```python
bt.hfpAnswerCall(addr)
```

接听电话。

**参数描述：**

- `addr`-AG端蓝牙地址，6个字节，类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.hfpEnableVR

```python
bt.hfpEnableVR(addr)
```

开启语音助手。

**参数描述：**

- `addr`-AG端蓝牙地址，6个字节，类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.hfpDisableVR

```python
bt.hfpDisableVR(addr)
```

关闭语音助手。

**参数描述：**

- `addr`-AG端蓝牙地址，6个字节，类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.hfpDisableVR

```python
bt.hfpDisableVR(addr, cmd)
```

三方通话控制。

**参数描述：**

- `addr`-AG端蓝牙地址，6个字节，类型为bytearray。
- `cmd`-控制命令，类型为整型。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

## A2DP/AVRCP相关功能

提供蓝牙音乐相关功能。

### bt.a2dpavrcpInit

```python
bt.a2dpavrcpInit()
```

A2DP和AVRCP功能初始化。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.a2dpavrcpRelease

```python
bt.a2dpavrcpRelease()
```

A2DP和AVRCP 资源释放。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.a2dpDisconnect

```python
bt.a2dpDisconnect(addr)
```

断开A2DP连接。

**参数描述：**

- `addr`-A2DP主机蓝牙地址，6个字节，类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.a2dpGetAddr

```python
bt.a2dpGetAddr()
```

获取A2DP主机蓝牙地址。

**返回值描述：**

- 执行成功返回bytearray类型的A2DP主机蓝牙地址，6字节，失败返回整型-1。

### bt.a2dpGetConnStatus

```python
bt.a2dpGetConnStatus()
```

获取A2DP连接状态。

**返回值描述：**

- A2DP连接状态，具体含义如下表。

| 值   | 类型 | 含义         |
| ---- | ---- | ------------ |
| -1   | int  | 获取失败     |
| 0    | int  | 连接已断开   |
| 1    | int  | 正在连接中   |
| 2    | int  | 已连接       |
| 3    | int  | 正在断开连接 |

### bt.avrcpStart

```python
bt.avrcpStart()
```

控制主机开始播放。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.avrcpPause

```python
bt.avrcpPause()
```

控制主机停止播放。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.avrcpPrev

```python
bt.avrcpPrev()
```

控制主机播放上一首。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.avrcpNext

```python
bt.avrcpNext()
```

控制主机播放下一首。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.avrcpSetVolume

```python
bt.avrcpSetVolume(vol)
```

设置主机播放音量。

**参数描述：**

- `vol`-播放音量，类型为整型，范围 0 - 11。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.avrcpGetVolume

```python
bt.avrcpGetVolume()
```

获取主机播放音量。

**返回值描述：**

- 执行成功返回整形音量值，失败返回整型-1。

### bt.avrcpGetPlayStatus

```python
bt.avrcpGetPlayStatus()
```

获取主机播放状态。

**返回值描述：**

- 播放状态，具体含义如下表。

| 值   | 类型 | 说明           |
| ---- | ---- | -------------- |
| -1   | int  | 获取失败       |
| 0    | int  | 没有播放       |
| 1    | int  | 正在播放       |
| 2    | int  | 暂停播放       |
| 3    | int  | 正在切换下一首 |
| 4    | int  | 正在切换下一首 |

### bt.avrcpGetConnStatus

```python
bt.avrcpGetConnStatus()
```

通过AVRCP协议获取主机连接状态。

**返回值描述：**

- 连接状态，具体含义如下表。

| 值   | 类型 | 说明         |
| ---- | ---- | ------------ |
| -1   | int  | 获取失败     |
| 0    | int  | 连接已断开   |
| 1    | int  | 正在连接中   |
| 2    | int  | 已连接       |
| 3    | int  | 正在断开连接 |

## SPP相关功能

提供蓝牙传输相关功能。

### bt.sppInit

```python
bt.sppInit()
```

SPP 功能初始化。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.sppRelease

```python
bt.sppRelease()
```

SPP 资源释放。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.sppConnect

```python
bt.sppConnect(addr)
```

建立SPP连接。

**参数描述：**

- `addr`-蓝牙地址，类型为bytearray，6个字节。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.sppDisconnect

```python
bt.sppDisconnect()
```

断开SPP连接。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

### bt.sppSend

```python
bt.sppSend(data)
```

**参数描述：**

- `data`-待发送的数据，类型为bytearray。

**返回值描述：**

- 执行成功返回整型0，失败返回整型-1。

