# 这次我们综合之前设计的多级菜单、开锁游戏、贪吃蛇游戏等，制作一个多功能电子手表

# 步骤一:多级菜单
# 一级菜单有3个选项，分别是A、B、C，其中A和B有二级菜单，可通过Back返回一级菜单，C没有二级菜单，进入C的界面3s后自动返回一级菜单;进入A后有A1、A2、Back三个选项，进入B后有B1、B2、B3、Back四个选项
# 一级菜单分为FirstMenu_A、FirstMenu_B、FirstMenu_C三个状态，其中FirstMenu_A为初始状态
# 二级菜单分为SecondMenu_A1、SecondMenu_A2、SecondMenu_ABack,SecondMenu_B1、SecondMenu_B2、SecondMenu_B3、SecondMenu_BBack七个状态
# 点进C、A1、A2、B1、B2、B3选项后，进入对应的显示状态，分别为Display_C、Display_A1、Display_A2、Display_B1、Display_B2、Display_B3六个状态，3s后自动返回上一级菜单
# 有btn_up、bun_dn、btn_ok三个按键，分别用于菜单选项的上移、下移和确认选择

# from machine import Pin, I2C
# import ssd1306


# i2c = I2C(0, sda=Pin(21), scl=Pin(22))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)
# oled.fill(0)
# Menu_state = 'FirstMenu_A'  # 初始状态
# btn_up = Pin(19, Pin.IN, Pin.PULL_UP)
# btn_dn = Pin(18, Pin.IN, Pin.PULL_UP)
# btn_ok = Pin(5, Pin.IN, Pin.PULL_UP)
# def menu_StateMachine(oled, btn_up, btn_dn, btn_ok):
#     global Menu_state
#     if Menu_state == 'FirstMenu_A':
#         oled.fill(0)
#         oled.text('> A', 0, 0)
#         oled.text('  B', 0, 10)
#         oled.text('  C', 0, 20)
#         oled.show()
#         if not btn_up.value():
#             Menu_state = 'FirstMenu_C'
#         elif not btn_dn.value():
#             Menu_state = 'FirstMenu_B'
#         elif not btn_ok.value():
#             Menu_state = 'SecondMenu_A1'
#     elif Menu_state == 'FirstMenu_B':
#         oled.fill(0)
#         oled.text('  A', 0, 0)
#         oled.text('> B', 0, 10)
#         oled.text('  C', 0, 20)
#         oled.show()
#         if not btn_up.value():
#             Menu_state = 'FirstMenu_A'
#         elif not btn_dn.value():
#             Menu_state = 'FirstMenu_C'
#         elif not btn_ok.value():
#             Menu_state = 'SecondMenu_B1'
#     elif Menu_state == 'FirstMenu_C':
#         oled.fill(0)
#         oled.text('  A', 0, 0)
#         oled.text('  B', 0, 10)
#         oled.text('> C', 0, 20)
#         oled.show()
#         if not btn_up.value():
#             Menu_state = 'FirstMenu_B'
#         elif not btn_dn.value():
#             Menu_state = 'FirstMenu_A'
#         elif not btn_ok.value():
#             Menu_state = 'Display_C'
#     elif Menu_state == 'SecondMenu_A1':
#         oled.fill(0)
#         oled.text('> A1', 0, 0)
#         oled.text('  A2', 0, 10)
#         oled.text('Back', 0, 20)
#         oled.show()
#         if not btn_up.value():
#             Menu_state = 'SecondMenu_ABack'
#         elif not btn_dn.value():
#             Menu_state = 'SecondMenu_A2'
#         elif not btn_ok.value():
#             Menu_state = 'Display_A1'
#     elif Menu_state == 'SecondMenu_A2':
#         oled.fill(0)
#         oled.text('  A1', 0, 0)
#         oled.text('> A2', 0, 10)
#         oled.text('Back', 0, 20)
#         oled.show()
#         if not btn_up.value():
#             Menu_state = 'SecondMenu_A1'
#         elif not btn_dn.value():
#             Menu_state = 'SecondMenu_ABack'
#         elif not btn_ok.value():
#             Menu_state = 'Display_A2'
#     elif Menu_state == 'SecondMenu_ABack':
#         oled.fill(0)
#         oled.text('  A1', 0, 0)
#         oled.text('  A2', 0, 10)
#         oled.text('> Back', 0, 20)
#         oled.show()
#         if not btn_up.value():
#             Menu_state = 'SecondMenu_A2'
#         elif not btn_dn.value():
#             Menu_state = 'SecondMenu_A1'
#         elif not btn_ok.value():
#             Menu_state = 'FirstMenu_A'
#     elif Menu_state == 'SecondMenu_B1':
#         oled.fill(0)
#         oled.text('> B1', 0, 0)
#         oled.text('  B2', 0, 10)
#         oled.text('  B3', 0, 20)
#         oled.text('Back', 0, 30)
#         oled.show()
#         if not btn_up.value():
#             Menu_state = 'SecondMenu_BBack'
#         elif not btn_dn.value():
#             Menu_state = 'SecondMenu_B2'
#         elif not btn_ok.value():
#             Menu_state = 'Display_B1'
#     elif Menu_state == 'SecondMenu_B2':
#         oled.fill(0)
#         oled.text('  B1', 0, 0)
#         oled.text('> B2', 0, 10)
#         oled.text('  B3', 0, 20)
#         oled.text('Back', 0, 30)
#         oled.show()
#         if not btn_up.value():
#             Menu_state = 'SecondMenu_B1'
#         elif not btn_dn.value():
#             Menu_state = 'SecondMenu_B3'
#         elif not btn_ok.value():
#             Menu_state = 'Display_B2'
#     elif Menu_state == 'SecondMenu_B3':
#         oled.fill(0)
#         oled.text('  B1', 0, 0)
#         oled.text('  B2', 0, 10)
#         oled.text('> B3', 0, 20)
#         oled.text('Back', 0, 30)
#         oled.show()
#         if not btn_up.value():
#             Menu_state = 'SecondMenu_B2'
#         elif not btn_dn.value():
#             Menu_state = 'SecondMenu_BBack'
#         elif not btn_ok.value():
#             Menu_state = 'Display_B3'
#     elif Menu_state == 'SecondMenu_BBack':
#         oled.fill(0)
#         oled.text('  B1', 0, 0)
#         oled.text('  B2', 0, 10)
#         oled.text('  B3', 0, 20)
#         oled.text('> Back', 0, 30)
#         oled.show()
#         if not btn_up.value():
#             Menu_state = 'SecondMenu_B3'
#         elif not btn_dn.value():
#             Menu_state = 'SecondMenu_B1'
#         elif not btn_ok.value():
#             Menu_state = 'FirstMenu_B'
#     elif Menu_state == 'Display_C':
#         oled.fill(0)
#         oled.text('Displaying C', 0, 20)
#         oled.show()
#         if btn_ok.value() == 0:
#             Menu_state = 'FirstMenu_C'
#     elif Menu_state == 'Display_A1':
#         oled.fill(0)
#         oled.text('Displaying A1', 0, 20)
#         oled.show()
#         if btn_ok.value() == 0:
#             Menu_state = 'SecondMenu_A1'
#     elif Menu_state == 'Display_A2':
        
#         oled.fill(0)
#         oled.text('Displaying A2', 0, 20)
#         oled.show()
#         if btn_ok.value() == 0:
#             Menu_state = 'SecondMenu_A2'
#     elif Menu_state == 'Display_B1':
#         oled.fill(0)
#         oled.text('Displaying B1', 0, 20)
#         oled.show()
#         if btn_ok.value() == 0:
#             Menu_state = 'SecondMenu_B1'
#     elif Menu_state == 'Display_B2':
#         oled.fill(0)
#         oled.text('Displaying B2', 0, 20)
#         oled.show()
#         if btn_ok.value() == 0:
#             Menu_state = 'SecondMenu_B2'
#     elif Menu_state == 'Display_B3':
#         oled.fill(0)
#         oled.text('Displaying B3', 0, 20)
#         oled.show()
#         if btn_ok.value() == 0:
#             Menu_state = 'SecondMenu_B3'



# while True:
#     menu_StateMachine(oled, btn_up, btn_dn, btn_ok)








































# 步骤二:开锁游戏

# import math
# import time
# from machine import Pin, I2C, ADC
# import ssd1306
# import random

# # 初始化 OLED 
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)


# # 配置按键
# btn = Pin(23, Pin.IN, Pin.PULL_UP)


# # 配置 ADC 
# adc = ADC(Pin(35))
# adc.atten(ADC.ATTN_11DB)  # 最大输入电压约 3.3V

# # # 初始化开锁角度
# # lock_angle = random.randint(0, 30)


# # # 初始化开锁状态机
# # The_Lock = "idle"
# # start_time = time.ticks_ms()

# # btn_count = 0


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


# def Lockpick_game(oled, btn, adc):
#     lock_angle = random.randint(0, 30)
#     The_Lock = "idle"
#     start_time = time.ticks_ms()
#     btn_count = 0
#     while True:
#         if The_Lock == "idle":
#             raw_value = adc.read()
#             temp = raw_value * 30 / 4095
#             # 模拟从 0 到 30 的变化
#             oled.fill(0)
#             # 将圆心向下移一点 (y=60)，形成拱形仪表盘
#             draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
#             oled.text(f"temp: {temp:.2f}", 0, 8)
#             oled.show()
#             # time.sleep_ms(50) # 事实上，我们真的需要一个sleep_ms吗？我想不出它有什么用
#             if btn.value() == 0:
#                 if abs(lock_angle - temp) <= 3:
#                     The_Lock = "unlocked"
#                     start_time = time.ticks_ms()
#                 elif abs(lock_angle - temp) <= 8:
#                     The_Lock = "near"
#                     start_time = time.ticks_ms()
#                 else:
#                     The_Lock = "far"
#                     start_time = time.ticks_ms()
#             btn_count = 1
#         if The_Lock == "unlocked":
#             oled.fill(0)
#             oled.text("unlocked!", 0, 0)
#             oled.show()
#             if time.ticks_ms() - start_time >= 8000:
#                 break # 游戏结束8s后退出循环
            
#         if The_Lock == "near":
#             raw_value = adc.read()
#             temp = raw_value * 30 / 4095
#             # 模拟从 0 到 30 的变化
#             oled.fill(0)
#             # 将圆心向下移一点 (y=60)，形成拱形仪表盘
#             draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
#             oled.text(f"temp: {temp:.2f}", 0, 8)
#             oled.text("near", 0, 20)
#             oled.show()
#             if btn.value() == 0:
#                  btn_count += 1
#                  if btn_count >= 5:
#                      The_Lock = "broken"
#             if time.ticks_ms() - start_time >= 3000:
#                 The_Lock = "idle"
#         if The_Lock == "far":
#             raw_value = adc.read()
#             temp = raw_value * 30 / 4095
#             # 模拟从 0 到 30 的变化
#             oled.fill(0)
#             # 将圆心向下移一点 (y=60)，形成拱形仪表盘
#             draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
#             oled.text(f"temp: {temp:.2f}", 0, 8)
#             oled.text("far", 0, 20)
#             oled.show()
#             if btn.value() == 0:
#                  btn_count += 1
#                  if btn_count >= 3:
#                      The_Lock = "broken"
#             if time.ticks_ms() - start_time >= 3000:
#                 The_Lock = "idle"
#         if The_Lock == "broken":
#             oled.fill(0)
#             oled.text("broken!", 0, 0)
#             oled.show()
#             if time.ticks_ms() - start_time >= 8000:
#                 break # 游戏结束8s后退出循环





# while True:
#     Lockpick_game(oled, btn, adc)






















































# 步骤三:将开锁游戏封装，用它代替多级菜单中的oled.text('Displaying A1', 0, 20)，开锁游戏中的按键即btn_ok

from machine import Pin, I2C, ADC
import ssd1306
import time
import math
import random
from otherfunc import Lockpick_game


# 初始化
i2c = I2C(0, sda=Pin(21), scl=Pin(22))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
Menu_state = 'FirstMenu_A'  # 菜单初始状态
btn_up = Pin(19, Pin.IN, Pin.PULL_UP)
btn_dn = Pin(18, Pin.IN, Pin.PULL_UP)
btn_ok = Pin(5, Pin.IN, Pin.PULL_UP)
adc = ADC(Pin(35))
adc.atten(ADC.ATTN_11DB)  # 最大输入电压约 3.3V
































def menu_StateMachine(oled, btn_up, btn_dn, btn_ok):
    global Menu_state
    if Menu_state == 'FirstMenu_A':
        oled.fill(0)
        oled.text('> A', 0, 0)
        oled.text('  B', 0, 10)
        oled.text('  C', 0, 20)
        oled.show()
        if not btn_up.value():
            Menu_state = 'FirstMenu_C'
        elif not btn_dn.value():
            Menu_state = 'FirstMenu_B'
        elif not btn_ok.value():
            Menu_state = 'SecondMenu_A1'
    elif Menu_state == 'FirstMenu_B':
        oled.fill(0)
        oled.text('  A', 0, 0)
        oled.text('> B', 0, 10)
        oled.text('  C', 0, 20)
        oled.show()
        if not btn_up.value():
            Menu_state = 'FirstMenu_A'
        elif not btn_dn.value():
            Menu_state = 'FirstMenu_C'
        elif not btn_ok.value():
            Menu_state = 'SecondMenu_B1'
    elif Menu_state == 'FirstMenu_C':
        oled.fill(0)
        oled.text('  A', 0, 0)
        oled.text('  B', 0, 10)
        oled.text('> C', 0, 20)
        oled.show()
        if not btn_up.value():
            Menu_state = 'FirstMenu_B'
        elif not btn_dn.value():
            Menu_state = 'FirstMenu_A'
        elif not btn_ok.value():
            Menu_state = 'Display_C'
    elif Menu_state == 'SecondMenu_A1':
        oled.fill(0)
        oled.text('> A1', 0, 0)
        oled.text('  A2', 0, 10)
        oled.text('Back', 0, 20)
        oled.show()
        if not btn_up.value():
            Menu_state = 'SecondMenu_ABack'
        elif not btn_dn.value():
            Menu_state = 'SecondMenu_A2'
        elif not btn_ok.value():
            Menu_state = 'Display_A1'
    elif Menu_state == 'SecondMenu_A2':
        oled.fill(0)
        oled.text('  A1', 0, 0)
        oled.text('> A2', 0, 10)
        oled.text('Back', 0, 20)
        oled.show()
        if not btn_up.value():
            Menu_state = 'SecondMenu_A1'
        elif not btn_dn.value():
            Menu_state = 'SecondMenu_ABack'
        elif not btn_ok.value():
            Menu_state = 'Display_A2'
    elif Menu_state == 'SecondMenu_ABack':
        oled.fill(0)
        oled.text('  A1', 0, 0)
        oled.text('  A2', 0, 10)
        oled.text('> Back', 0, 20)
        oled.show()
        if not btn_up.value():
            Menu_state = 'SecondMenu_A2'
        elif not btn_dn.value():
            Menu_state = 'SecondMenu_A1'
        elif not btn_ok.value():
            Menu_state = 'FirstMenu_A'
    elif Menu_state == 'SecondMenu_B1':
        oled.fill(0)
        oled.text('> B1', 0, 0)
        oled.text('  B2', 0, 10)
        oled.text('  B3', 0, 20)
        oled.text('Back', 0, 30)
        oled.show()
        if not btn_up.value():
            Menu_state = 'SecondMenu_BBack'
        elif not btn_dn.value():
            Menu_state = 'SecondMenu_B2'
        elif not btn_ok.value():
            Menu_state = 'Display_B1'
    elif Menu_state == 'SecondMenu_B2':
        oled.fill(0)
        oled.text('  B1', 0, 0)
        oled.text('> B2', 0, 10)
        oled.text('  B3', 0, 20)
        oled.text('Back', 0, 30)
        oled.show()
        if not btn_up.value():
            Menu_state = 'SecondMenu_B1'
        elif not btn_dn.value():
            Menu_state = 'SecondMenu_B3'
        elif not btn_ok.value():
            Menu_state = 'Display_B2'
    elif Menu_state == 'SecondMenu_B3':
        oled.fill(0)
        oled.text('  B1', 0, 0)
        oled.text('  B2', 0, 10)
        oled.text('> B3', 0, 20)
        oled.text('Back', 0, 30)
        oled.show()
        if not btn_up.value():
            Menu_state = 'SecondMenu_B2'
        elif not btn_dn.value():
            Menu_state = 'SecondMenu_BBack'
        elif not btn_ok.value():
            Menu_state = 'Display_B3'
    elif Menu_state == 'SecondMenu_BBack':
        oled.fill(0)
        oled.text('  B1', 0, 0)
        oled.text('  B2', 0, 10)
        oled.text('  B3', 0, 20)
        oled.text('> Back', 0, 30)
        oled.show()
        if not btn_up.value():
            Menu_state = 'SecondMenu_B3'
        elif not btn_dn.value():
            Menu_state = 'SecondMenu_B1'
        elif not btn_ok.value():
            Menu_state = 'FirstMenu_B'
    elif Menu_state == 'Display_C':
        oled.fill(0)
        oled.text('Displaying C', 0, 20)
        oled.show()
        if btn_ok.value() == 0:
            Menu_state = 'FirstMenu_C'
    elif Menu_state == 'Display_A1':
        oled.fill(0)
        oled.text('Displaying A1', 0, 20)
        oled.show()
        if btn_ok.value() == 0:
            Menu_state = 'SecondMenu_A1'
    elif Menu_state == 'Display_A2':
        
        oled.fill(0)
        oled.text('Displaying A2', 0, 20)
        oled.show()
        if btn_ok.value() == 0:
            Menu_state = 'SecondMenu_A2'
    elif Menu_state == 'Display_B1':
        Lockpick_game(oled, btn_ok, adc)
        Menu_state = 'SecondMenu_B1'
    elif Menu_state == 'Display_B2':
        oled.fill(0)
        oled.text('Displaying B2', 0, 20)
        oled.show()
        if btn_ok.value() == 0:
            Menu_state = 'SecondMenu_B2'
    elif Menu_state == 'Display_B3':
        oled.fill(0)
        oled.text('Displaying B3', 0, 20)
        oled.show()
        if btn_ok.value() == 0:
            Menu_state = 'SecondMenu_B3'



while True:
    menu_StateMachine(oled, btn_up, btn_dn, btn_ok)