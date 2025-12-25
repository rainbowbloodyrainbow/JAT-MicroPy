#本节课为综合实验课
#设计目标：使用dht22（测温度）,无源蜂鸣器，ssd1306，按键和舵机
#设计一鱼缸水温报警器与加冰装置
#夏天气温高，本系统使用dht22测量鱼缸水温，在温度高于40°C时，使用无源蜂鸣器进行报警，ssd1306显示“温度过高”（平时为正常显示温度）
#人听到报警声后按下按键，通过舵机向鱼缸中添加冰块

import dht 
import framebuf
from machine import Pin,I2C
import time
import ssd1306
from font import font16


# 初始化 I2C 和 OLED（SSD1306）
i2c = I2C(0,scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# 配置DHT22 (GPIO4)
sensor = dht.DHT22(Pin(4))

temp_highth = 40


def draw_chinese(oled, font, word, x, y):
    for ch in word:
        data = bytearray(font.get(ch, [0x00] * 32))
        fb = framebuf.FrameBuffer(data, 16, 16, framebuf.MONO_HLSB)
        oled.framebuf.blit(fb, x, y)  # 使用 oled.framebuf 的 blit
        x += 16


def read_sensor():
    """读取温湿度数据"""
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        return temperature, humidity
    except OSError as e:
        print("读取传感器失败:", e)
        return None, None

# 主循环
while True:
    temp, hum = read_sensor()
    if temp is not None and hum is not None:
        print("温度: {}°C, 湿度: {}%".format(temp, hum))
        oled.fill(0)
        draw_chinese(oled, font16, '温度', 0, 12)
        draw_chinese(oled, font16, '°', 80, 12)
        oled.text(":{}  C".format(temp),30,16)
        oled.text(":{}%".format( hum),30,32)
        oled.show()
time.sleep(2)  # DHT22要求至少2秒间隔