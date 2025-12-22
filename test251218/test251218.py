# #任务一：DHT22温湿度传感器读取
# #注意：传感器读取时间至少间隔2s，以避免读取错误
# import dht 
# from machine import Pin
# import time
# # 配置DHT22 (GPIO4)
# sensor = dht.DHT22(Pin(4))
# def read_sensor():
#     """读取温湿度数据"""
#     try:
#         sensor.measure()
#         temperature = sensor.temperature()
#         humidity = sensor.humidity()
#         return temperature, humidity
#     except OSError as e:
#         print("读取传感器失败:", e)
#         return None, None

# # 主循环
# while True:
#     temp, hum = read_sensor()
#     if temp is not None and hum is not None:
#         print("温度: {}°C, 湿度: {}%".format(temp, hum))
# time.sleep(2)  # DHT22要求至少2秒间隔
#     oled.fill(0)
#     oled.text("Voltage: {:.4f}".format(voltage),0,16)
#     oled.text("Status: {}".format(status),0,32)
#     oled.show()















# #任务一拓展：加上OLED显示
# import dht 
# from machine import Pin,I2C
# import time
# import ssd1306

# # 初始化 I2C 和 OLED（SSD1306）
# i2c = I2C(0,scl=Pin(22), sda=Pin(21))
# oled_width = 128
# oled_height = 64
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# # 配置DHT22 (GPIO4)
# sensor = dht.DHT22(Pin(4))
# def read_sensor():
#     """读取温湿度数据"""
#     try:
#         sensor.measure()
#         temperature = sensor.temperature()
#         humidity = sensor.humidity()
#         return temperature, humidity
#     except OSError as e:
#         print("读取传感器失败:", e)
#         return None, None

# # 主循环
# while True:
#     temp, hum = read_sensor()
#     if temp is not None and hum is not None:
#         print("温度: {}°C, 湿度: {}%".format(temp, hum))
#         oled.fill(0)
#         oled.text("temp:{}C".format(temp),0,16)
#         oled.text("hum:{}%".format( hum),0,32)
#         oled.show()
# time.sleep(2)  # DHT22要求至少2秒间隔

















# #任务一拓展的拓展：OLED显示汉字
# import dht 
# import framebuf
# from machine import Pin,I2C
# import time
# import ssd1306
# from font import font16


# # 初始化 I2C 和 OLED（SSD1306）
# i2c = I2C(0,scl=Pin(22), sda=Pin(21))
# oled_width = 128
# oled_height = 64
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# # 配置DHT22 (GPIO4)
# sensor = dht.DHT22(Pin(4))

# def draw_chinese(oled, font, word, x, y):
#     for ch in word:#ch只是一个名字，代表字符串word中的每一个字符，叫什么都可以，重点是要和下面的font.get(ch...)对应上
#         data = bytearray(font.get(ch, [0x00] * 32))
#         #bytearray()函数将一个可迭代对象转换为字节数组
#         fb = framebuf.FrameBuffer(data, 16, 16, framebuf.MONO_HLSB)
#         oled.framebuf.blit(fb, x, y)  # 使用 oled.framebuf 的 blit
#         x += 16


# def read_sensor():
#     """读取温湿度数据"""
#     try:
#         sensor.measure()
#         temperature = sensor.temperature()
#         humidity = sensor.humidity()
#         return temperature, humidity
#     except OSError as e:
#         print("读取传感器失败:", e)
#         return None, None

# # 主循环
# while True:
#     temp, hum = read_sensor()
#     if temp is not None and hum is not None:
#         print("温度: {}°C, 湿度: {}%".format(temp, hum))
#         oled.fill(0)
#         # oled.text("wen:{}C".format(temp),0,16)
#         # oled.text("shi:{}%".format( hum),0,32)
#         # oled.text(":{}    C".format(temp),30,16)
#         # oled.text(":{}%".format( hum),30,32)
#         draw_chinese(oled, font16, '温度', 0, 12)
#         draw_chinese(oled, font16, '湿度', 0, 28)
#         draw_chinese(oled, font16, '°', 80, 12)
#         oled.text(":{}  C".format(temp),30,16)
#         oled.text(":{}%".format( hum),30,32)
#         oled.show()
# time.sleep(2)  # DHT22要求至少2秒间隔





















#任务二：逻辑分析仪
# 该代码主要用于 Wokwi 仿真环境中的时序分析
# 实际读取仍使用 dht 模块，这里仅用于演示时序测量
# 仿真结束后，会生成一vcd文件，可用pulseview等工具打开分析

from machine import Pin, Timer
import time

data_pin = Pin(4, Pin.IN, Pin.PULL_UP)
pulse_times = []

def capture_pulses():
    """捕获脉冲序列 (仅用于 Wokwi 分析)"""
    # 在 Wokwi 中，我们使用逻辑分析仪直接捕获信号
    # 这里仅模拟数据收集过程
    print("请在 Wokwi 中启动逻辑分析仪捕获 DHT22 通信过程")
    print("设置采样率至少为 100kHz 以捕获微秒级信号")
    
    # 模拟触发传感器（复用 GPIO4）
    trigger_pin = Pin(4, Pin.OUT)
    trigger_pin.value(0)
    time.sleep_ms(20)          # 拉低 >18ms 触发 DHT22
    trigger_pin.init(Pin.IN, Pin.PULL_UP)  # 释放总线
    
    # 等待传感器完成通信（约 4-5ms），留足时间供逻辑分析仪捕获
    time.sleep(1)

# 使用说明
print("=" * 50)
print("DHT22 时序分析指南")
print("=" * 50)
print("1. 在 Wokwi 中添加逻辑分析仪并连接到 GPIO4")
print("2. 设置采样率: 100kHz")
print("3. 运行此代码触发传感器读取")
print("4. 在逻辑分析仪中查看捕获的信号")
print("5. 使用测量工具分析各阶段时序")

# 执行触发
capture_pulses()