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
        















# # 步骤二：加上电位器(adc)控制当前角度

# import math
# import time
# from machine import Pin, I2C, ADC
# import ssd1306

# # 初始化 OLED (请根据你的实际引脚修改 SDA/SCL)
# # 假设使用的是 ESP32 默认 I2C
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)



# # 配置 ADC 
# adc = ADC(Pin(35))
# adc.atten(ADC.ATTN_11DB)  # 最大输入电压约 3.3V

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
#     raw_value = adc.read()
#     temp = raw_value * 30 / 4095
#     # 模拟从 0 到 30 的变化
#     oled.fill(0)
#     # 将圆心向下移一点 (y=60)，形成拱形仪表盘
#     draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
#     oled.text(f"temp: {temp:.2f}", 0, 8)
#     oled.show()
#     time.sleep_ms(50)















# # 步骤三：加上按键选中角度
# import math
# import time
# from machine import Pin, I2C, ADC
# import ssd1306

# # 初始化 OLED 
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)


# # 配置按键
# btn = Pin(23, Pin.IN, Pin.PULL_UP)



# # 配置 ADC 
# adc = ADC(Pin(35))
# adc.atten(ADC.ATTN_11DB)  # 最大输入电压约 3.3V

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
#     raw_value = adc.read()
#     temp = raw_value * 30 / 4095
#     # 模拟从 0 到 30 的变化
#     oled.fill(0)
#     # 将圆心向下移一点 (y=60)，形成拱形仪表盘
#     draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
#     oled.text(f"temp: {temp:.2f}", 0, 8)
#     oled.show()
#     if btn.value() == 0:
#         print("按下按键")
#     time.sleep_ms(50)
















# # 步骤四：加上开锁逻辑:设定角度为10，当前角度与设定角度差值delta小于等于3，则显示开锁(unlocked)；delta大于3而小于等于8，则显示接近(near)；delta大于8，则显示远远不够(far)
# import math
# import time
# from machine import Pin, I2C, ADC
# import ssd1306

# # 初始化 OLED 
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)


# # 配置按键
# btn = Pin(23, Pin.IN, Pin.PULL_UP)



# # 配置 ADC 
# adc = ADC(Pin(35))
# adc.atten(ADC.ATTN_11DB)  # 最大输入电压约 3.3V

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



# # 初始化开锁角度
# lock_angle = 10




# # --- 主循环测试 ---
# while True:
#     raw_value = adc.read()
#     temp = raw_value * 30 / 4095
#     # 模拟从 0 到 30 的变化
#     oled.fill(0)
#     # 将圆心向下移一点 (y=60)，形成拱形仪表盘
#     draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
#     oled.text(f"temp: {temp:.2f}", 0, 8)
#     if btn.value() == 0:
#         print("按下按键")
#         if abs(lock_angle - norm_val) <= 3:
#             oled.text("unlocked", 0, 20)
#         elif abs(lock_angle - norm_val) <= 8:
#             oled.text("near", 0, 20)
#         else:
#             oled.text("far", 0, 20)
#     oled.show()
#     time.sleep_ms(50)























# # 步骤五：把主循环改写为状态机，分为idle,unlocked,near,far状态，分别对应初始状态、开锁、接近、远远不够状态
# # 初始为idle状态，若delta小于等于3且按键按下，则由idle变为unlocked;若delta大于3且小于等于8且按键按下,则由idle变为near;若delta大于8且按键按下,则由idle变为far；后三种状态3s后自动变为idle状态
# import math
# import time
# from machine import Pin, I2C, ADC
# import ssd1306

# # 初始化 OLED 
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)


# # 配置按键
# btn = Pin(23, Pin.IN, Pin.PULL_UP)



# # 配置 ADC 
# adc = ADC(Pin(35))
# adc.atten(ADC.ATTN_11DB)  # 最大输入电压约 3.3V

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



# # 初始化开锁角度
# lock_angle = 10



# # 初始化开锁状态机
# The_Lock = "idle"
# start_time = time.ticks_ms()


# # --- 主循环测试 ---
# while True:
#     if The_Lock == "idle":
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
#     if The_Lock == "unlocked":
#             raw_value = adc.read()
#             temp = raw_value * 30 / 4095
#             # 模拟从 0 到 30 的变化
#             oled.fill(0)
#             # 将圆心向下移一点 (y=60)，形成拱形仪表盘
#             draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
#             oled.text(f"temp: {temp:.2f}", 0, 8)
#             oled.text("unlocked", 0, 20)
#             oled.show()
#             if time.ticks_ms() - start_time >= 3000:
#                 The_Lock = "idle"
#     if The_Lock == "near":
#             raw_value = adc.read()
#             temp = raw_value * 30 / 4095
#             # 模拟从 0 到 30 的变化
#             oled.fill(0)
#             # 将圆心向下移一点 (y=60)，形成拱形仪表盘
#             draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
#             oled.text(f"temp: {temp:.2f}", 0, 8)
#             oled.text("near", 0, 20)
#             oled.show()
#             if time.ticks_ms() - start_time >= 3000:
#                 The_Lock = "idle"
#     if The_Lock == "far":
#             raw_value = adc.read()
#             temp = raw_value * 30 / 4095
#             # 模拟从 0 到 30 的变化
#             oled.fill(0)
#             # 将圆心向下移一点 (y=60)，形成拱形仪表盘
#             draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
#             oled.text(f"temp: {temp:.2f}", 0, 8)
#             oled.text("far", 0, 20)
#             oled.show()
#             if time.ticks_ms() - start_time >= 3000:
#                 The_Lock = "idle"








































# # 步骤六：在状态机中增加状态"broken"，当far状态下按键按下3次及以上，则由far变为broken；当near状态下按键按下5次及以上，则由near变为broken；broken状态下oled屏只显示"broken!"一行字，且无法回到idle状态。
# # 对了，其实unlocked状态也不应该回到idle
# # 按照以上想法，我们需要记录按键按下的次数，并在状态机中增加相应的判断条件。
# # 我们需要在状态机中增加一个变量"btn_count"，初始值为0，每当按键按下，则加1，每当按键松开，则减1。
# import math
# import time
# from machine import Pin, I2C, ADC
# import ssd1306

# # 初始化 OLED 
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)


# # 配置按键
# btn = Pin(23, Pin.IN, Pin.PULL_UP)



# # 配置 ADC 
# adc = ADC(Pin(35))
# adc.atten(ADC.ATTN_11DB)  # 最大输入电压约 3.3V

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



# # 初始化开锁角度
# lock_angle = 10



# # 初始化开锁状态机
# The_Lock = "idle"
# start_time = time.ticks_ms()

# btn_count = 0

# # --- 主循环测试 ---
# while True:
#     if The_Lock == "idle":
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
#     if The_Lock == "unlocked":
#             oled.fill(0)
#             oled.text("unlocked!", 0, 0)
#             oled.show()
            
#     if The_Lock == "near":
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
#     if The_Lock == "far":
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
#     if The_Lock == "broken":
#             oled.fill(0)
#             oled.text("broken!", 0, 0)
#             oled.show()





























# # 步骤七：把开锁角度换成0~30内的随机数
# # 可以import random模块，使用它的randint函数生成一个0~30的随机数，作为开锁角度。
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



# # 初始化开锁角度
# lock_angle = random.randint(0, 30)


# # 初始化开锁状态机
# The_Lock = "idle"
# start_time = time.ticks_ms()

# btn_count = 0

# # --- 主循环测试 ---
# while True:
#     if The_Lock == "idle":
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
#     if The_Lock == "unlocked":
#             oled.fill(0)
#             oled.text("unlocked!", 0, 0)
#             oled.show()
            
#     if The_Lock == "near":
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
#     if The_Lock == "far":
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
#     if The_Lock == "broken":
#             oled.fill(0)
#             oled.text("broken!", 0, 0)
#             oled.show()









































# 步骤八：把它封装成函数Lockpick_game()
import math
import time
from machine import Pin, I2C, ADC
import ssd1306
import random

# 初始化 OLED 
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)


# 配置按键
btn = Pin(23, Pin.IN, Pin.PULL_UP)


# 配置 ADC 
adc = ADC(Pin(35))
adc.atten(ADC.ATTN_11DB)  # 最大输入电压约 3.3V

# # 初始化开锁角度
# lock_angle = random.randint(0, 30)


# # 初始化开锁状态机
# The_Lock = "idle"
# start_time = time.ticks_ms()

# btn_count = 0


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


def Lockpick_game(oled, btn, adc):
    lock_angle = random.randint(0, 30)
    The_Lock = "idle"
    start_time = time.ticks_ms()
    btn_count = 0
    while True:
        if The_Lock == "idle":
            raw_value = adc.read()
            temp = raw_value * 30 / 4095
            # 模拟从 0 到 30 的变化
            oled.fill(0)
            # 将圆心向下移一点 (y=60)，形成拱形仪表盘
            draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
            oled.text(f"temp: {temp:.2f}", 0, 8)
            oled.show()
            # time.sleep_ms(50) # 事实上，我们真的需要一个sleep_ms吗？我想不出它有什么用
            if btn.value() == 0:
                if abs(lock_angle - temp) <= 3:
                    The_Lock = "unlocked"
                    start_time = time.ticks_ms()
                elif abs(lock_angle - temp) <= 8:
                    The_Lock = "near"
                    start_time = time.ticks_ms()
                else:
                    The_Lock = "far"
                    start_time = time.ticks_ms()
            btn_count = 1
        if The_Lock == "unlocked":
            oled.fill(0)
            oled.text("unlocked!", 0, 0)
            oled.show()
            if time.ticks_ms() - start_time >= 8000:
                break # 游戏结束8s后退出循环
            
        if The_Lock == "near":
            raw_value = adc.read()
            temp = raw_value * 30 / 4095
            # 模拟从 0 到 30 的变化
            oled.fill(0)
            # 将圆心向下移一点 (y=60)，形成拱形仪表盘
            draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
            oled.text(f"temp: {temp:.2f}", 0, 8)
            oled.text("near", 0, 20)
            oled.show()
            if btn.value() == 0:
                 btn_count += 1
                 if btn_count >= 5:
                     The_Lock = "broken"
            if time.ticks_ms() - start_time >= 3000:
                The_Lock = "idle"
        if The_Lock == "far":
            raw_value = adc.read()
            temp = raw_value * 30 / 4095
            # 模拟从 0 到 30 的变化
            oled.fill(0)
            # 将圆心向下移一点 (y=60)，形成拱形仪表盘
            draw_gauge(oled, temp, 0, 30, x=64, y=60, radius=30)
            oled.text(f"temp: {temp:.2f}", 0, 8)
            oled.text("far", 0, 20)
            oled.show()
            if btn.value() == 0:
                 btn_count += 1
                 if btn_count >= 3:
                     The_Lock = "broken"
            if time.ticks_ms() - start_time >= 3000:
                The_Lock = "idle"
        if The_Lock == "broken":
            oled.fill(0)
            oled.text("broken!", 0, 0)
            oled.show()
            if time.ticks_ms() - start_time >= 8000:
                break # 游戏结束8s后退出循环





while True:
    Lockpick_game(oled, btn, adc)