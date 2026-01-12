# # 自娱自乐小设计：模仿辐射3，新维加斯和老滚5的开锁游戏
# # 步骤一：ssd1306显示开锁界面(使用之前上课的仪表盘显示代码)

# import math
# import time
# from machine import Pin, I2C
# import ssd1306

# # 初始化 OLED (请根据你的实际引脚修改 SDA/SCL)
# # 假设使用的是 ESP32 默认 I2C
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# # --- 1. 手动实现画圆函数 ---
# def draw_circle(oled, x0, y0, radius, col=1):
#     x = radius
#     y = 0
#     err = 0
#     while x >= y:
#         oled.pixel(x0 + x, y0 + y, col)
#         oled.pixel(x0 + y, y0 + x, col)
#         oled.pixel(x0 - y, y0 + x, col)
#         oled.pixel(x0 - x, y0 + y, col)
#         oled.pixel(x0 - x, y0 - y, col)
#         oled.pixel(x0 - y, y0 - x, col)
#         oled.pixel(x0 + y, y0 - x, col)
#         oled.pixel(x0 + x, y0 - y, col)
        
#         y += 1
#         if err <= 0:
#             err += 2*y + 1
#         else:
#             x -= 1
#             err += 2*(y-x) + 1

# # --- 2. 修正后的仪表盘函数 ---
# def draw_gauge(oled, value, min_val=0, max_val=100, x=64, y=32, radius=28):
#     # 规范化值到 0-100
#     norm_val = (value - min_val) / (max_val - min_val) * 100
#     norm_val = max(0, min(100, norm_val))
    
#     # --- 绘制表盘外圈 ---
#     draw_circle(oled, x, y, radius, 1)
    
#     # --- 绘制刻度 ---
#     # 这里的角度逻辑：
#     # math.pi (180度) 是左边 (9点钟方向)
#     # 0 是右边 (3点钟方向)
#     # math.pi/2 是上方 (12点钟方向)
#     # 下面的公式是画一个从左(西)到右(东)的半圆拱形
#     for i in range(0, 101, 10):
#         # 刻度角度：从 180度(左) 转到 0度(右)
#         angle = math.pi - (math.pi * i / 100)
        
#         tick_len = 3 # 刻度长度
#         sx = int(x + (radius - tick_len) * math.cos(angle))
#         sy = int(y - (radius - tick_len) * math.sin(angle)) # y轴在屏幕上是向下的，所以减去sin
#         ex = int(x + radius * math.cos(angle))
#         ey = int(y - radius * math.sin(angle))
#         oled.line(sx, sy, ex, ey, 1)

#     # --- 计算并绘制指针 ---
#     # 注意：这里必须使用独立的变量名，不能和刻度循环里的变量混用
#     # 指针角度
#     needle_angle = math.pi - (math.pi * norm_val / 100)
    
#     needle_x = int(x + (radius - 5) * math.cos(needle_angle))
#     needle_y = int(y - (radius - 5) * math.sin(needle_angle))
    
#     oled.line(x, y, needle_x, needle_y, 1)
    
#     # --- 显示数值 ---
#     # 居中显示
#     text = f"{int(value)}"
#     text_x = x - (len(text) * 4) # 简易居中计算
#     oled.text(text, text_x, y + 5)

# # --- 主循环测试 ---
# while True:
#     # 模拟从 0 到 30 的变化
#     oled.fill(0)
#     # 将圆心向下移一点 (y=60)，形成拱形仪表盘
#     draw_gauge(oled, 30, 0, 30, x=64, y=60, radius=30)
#     oled.show()
#     time.sleep_ms(50)
        















# 步骤二：加上电位器(adc)控制当前角度

import math
import time
from machine import Pin, I2C, ADC
import ssd1306

# 初始化 OLED (请根据你的实际引脚修改 SDA/SCL)
# 假设使用的是 ESP32 默认 I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)



# 配置 ADC 
adc = ADC(Pin(35))
adc.atten(ADC.ATTN_11DB)  # 最大输入电压约 3.3V

# --- 1. 手动实现画圆函数 ---
def draw_circle(oled, x0, y0, radius, col=1):
    x = radius
    y = 0
    err = 0
    while x >= y:
        oled.pixel(x0 + x, y0 + y, col)
        oled.pixel(x0 + y, y0 + x, col)
        oled.pixel(x0 - y, y0 + x, col)
        oled.pixel(x0 - x, y0 + y, col)
        oled.pixel(x0 - x, y0 - y, col)
        oled.pixel(x0 - y, y0 - x, col)
        oled.pixel(x0 + y, y0 - x, col)
        oled.pixel(x0 + x, y0 - y, col)
        
        y += 1
        if err <= 0:
            err += 2*y + 1
        else:
            x -= 1
            err += 2*(y-x) + 1

# --- 2. 修正后的仪表盘函数 ---
def draw_gauge(oled, value, min_val=0, max_val=100, x=64, y=32, radius=28):
    # 规范化值到 0-100
    norm_val = (value - min_val) / (max_val - min_val) * 100
    norm_val = max(0, min(100, norm_val))
    
    # --- 绘制表盘外圈 ---
    draw_circle(oled, x, y, radius, 1)
    
    # --- 绘制刻度 ---
    # 这里的角度逻辑：
    # math.pi (180度) 是左边 (9点钟方向)
    # 0 是右边 (3点钟方向)
    # math.pi/2 是上方 (12点钟方向)
    # 下面的公式是画一个从左(西)到右(东)的半圆拱形
    for i in range(0, 101, 10):
        # 刻度角度：从 180度(左) 转到 0度(右)
        angle = math.pi - (math.pi * i / 100)
        
        tick_len = 3 # 刻度长度
        sx = int(x + (radius - tick_len) * math.cos(angle))
        sy = int(y - (radius - tick_len) * math.sin(angle)) # y轴在屏幕上是向下的，所以减去sin
        ex = int(x + radius * math.cos(angle))
        ey = int(y - radius * math.sin(angle))
        oled.line(sx, sy, ex, ey, 1)

    # --- 计算并绘制指针 ---
    # 注意：这里必须使用独立的变量名，不能和刻度循环里的变量混用
    # 指针角度
    needle_angle = math.pi - (math.pi * norm_val / 100)
    
    needle_x = int(x + (radius - 5) * math.cos(needle_angle))
    needle_y = int(y - (radius - 5) * math.sin(needle_angle))
    
    oled.line(x, y, needle_x, needle_y, 1)
    
    # --- 显示数值 ---
    # 居中显示
    text = f"{int(value)}"
    text_x = x - (len(text) * 4) # 简易居中计算
    oled.text(text, text_x, y + 5)

# --- 主循环测试 ---
while True:
    raw_value = adc.read()
    temp = raw_value * 30 / 4095
    # 模拟从 0 到 30 的变化
    oled.fill(0)
    # 将圆心向下移一点 (y=60)，形成拱形仪表盘
    draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
    oled.text(f"temp: {temp:.2f}", 0, 8)
    oled.show()
    time.sleep_ms(50)

