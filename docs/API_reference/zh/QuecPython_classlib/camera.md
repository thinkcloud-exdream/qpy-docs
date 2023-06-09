# camera  - 摄像头

该模块包含了摄像头预览，照相机，扫码功能。

> 目前支持型号：EC600N系列、EC800N系列、EC600M系列、EC800M系列、EC600U-CN系列、EC200U-CN系列。
>
> 如果需要预览，在初始化camera对象之前，请先参照[machine模块的lcd类的内容](machine.LCD.md)正确初始化LCD对象。

**示例：**

```python
# -*- coding: UTF-8 -*-
from machine import LCD
import camera

# 如果需要预览，请先参照machine模块的lcd类的内容正确初始化LCD对象
# lcd = LCD()
# lcd.lcd_init(*args)

# 摄像头预览功能
preview = camera.camPreview(0,640,480,240,240,1)
preview.open()
preview.close()

# 摄像头扫码功能
def scan_callback(para):
    # para[0] 识别结果 	0：成功 其它：失败
    print("scan result is ", para[0])		
    # para[1] 识别内容
    if para[0] == 0:
        print("decode content is ", para[1]) 

scaner = camera.camScandecode(0,1,640,480,1,240,240)
scaner.open()
scaner.callback(scan_callback)
scaner.start()
scaner.stop()
scaner.close()

# 摄像头照相功能
def cam_callback(para):
    # para[0] 拍照结果 	0：成功 其它：失败
    print("cam capture result is ", para[0])		
    # para[1] 保存图片的名称
    if para[0] == 0:
        print("image {} has been saved".format(para[1])) 

cam = camera.camCapture(0,640,480,1,240,240)
cam.open()
cam.callback(cam_callback)
cam.start(240, 240, "image_demo")
cam.close()
```



## Classes

- [class CamPreview - 摄像头预览](./camera.CamPreview.md)

- [class CamDecoder - 摄像头扫码](camera.CamDecoder.md)

- [class CamCapture - 摄像头拍照](camera.CamCapture.md)