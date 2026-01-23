# from machine import Pin, I2C, ADC
# import time
# import math
# import random
# 如果主程序中已经import了以上这些模块，那这里还需要吗？
# 答:不需要，因为main.py已经导入了这些模块，所以这里不需要再导入一次。
# 注:ai胡说八道呢，需要！！！

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












def draw_gauge(oled, value, min_val=0, max_val=100, x=64, y=32, radius=28):

    norm_val = (value - min_val) / (max_val - min_val) * 100
    norm_val = max(0, min(100, norm_val))
    draw_circle(oled, x, y, radius, 1)
    
    for i in range(0, 101, 10):
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




