#本节课为综合实验课
#设计目标：使用dht22（测温度）,无源蜂鸣器，ssd1306，按键和舵机
#设计一鱼缸水温报警器与加冰装置
#夏天气温高，本系统使用dht22测量鱼缸水温，在温度高于40°C时，使用无源蜂鸣器进行报警，ssd1306显示“温度过高”（平时为正常显示温度）
#人听到报警声后按下按键，通过舵机向鱼缸中添加冰块



# #步骤一：测温并显示（直接把12月18日的代码拿来用）
# import dht 
# import framebuf
# from machine import Pin,I2C,PWM
# import time
# import utime
# import ssd1306
# from font import font16


# # 初始化 I2C 和 OLED（SSD1306）
# i2c = I2C(0,scl=Pin(22), sda=Pin(21))
# oled_width = 128
# oled_height = 64
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# # 配置DHT22 (GPIO4)
# sensor = dht.DHT22(Pin(4))

# # 将 GPIO15 设置为PWM输出引脚
# buzzer_pin = Pin(15)
# buzzer = PWM(buzzer_pin)

# temp_highth = 40


# def draw_chinese(oled, font, word, x, y):
#     for ch in word:
#         data = bytearray(font.get(ch, [0x00] * 32))
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
#         draw_chinese(oled, font16, '温度', 0, 12)
#         draw_chinese(oled, font16, '°', 80, 12)
#         oled.text(":{}  C".format(temp),30,16)
#         oled.text(":{}%".format( hum),30,32)
#         oled.show()
# time.sleep(2)  # DHT22要求至少2秒间隔
























# #步骤二：加上报警功能（蜂鸣器和显示屏，蜂鸣器参考12月22日代码）


# import dht 
# import framebuf
# from machine import Pin,I2C,PWM
# import time
# import utime
# import ssd1306
# from font import font16


# # 初始化 I2C 和 OLED（SSD1306）
# i2c = I2C(0,scl=Pin(22), sda=Pin(21))
# oled_width = 128
# oled_height = 64
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# # 配置DHT22 (GPIO4)
# sensor = dht.DHT22(Pin(4))


# temp_highth = 40
# # 将 GPIO15 设置为PWM输出引脚
# buzzer_pin = Pin(15)
# buzzer = PWM(buzzer_pin)

# # 音符频率表 (单位：赫兹 Hz)
# # 这是一个简化的音阶，C4就是中央C (Do)
# NOTE_C4 = 262
# NOTE_D4 = 294
# NOTE_E4 = 330
# NOTE_F4 = 349
# NOTE_G4 = 392

# def play_tone(frequency):
#     """以指定频率播放声音"""
#     if frequency > 0:
#         buzzer.freq(frequency)    # 设置频率（音高）
#         buzzer.duty_u16(32768)  # 设置占空比（音量），一半占空比通常音量最大
#     else:
#         stop_tone()

# def stop_tone():
#     """停止发声"""
#     buzzer.duty_u16(0) # 将占空比设为0即可静音





# def draw_chinese(oled, font, word, x, y):
#     for ch in word:
#         data = bytearray(font.get(ch, [0x00] * 32))
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
#         if temp < temp_highth:
#             draw_chinese(oled, font16, '温度', 0, 12)
#             draw_chinese(oled, font16, '°', 80, 12)
#             oled.text(":{}  C".format(temp),30,16)
#             oled.text(":{}%".format( hum),30,32)
#             stop_tone()
#             oled.show()
#         else:
#             draw_chinese(oled, font16, '温度过高 请加冰', 0, 12)
#             play_tone(NOTE_C4)
#             utime.sleep(0.5) # 持续0.5秒（替换time.sleep为utime.sleep）           
#             oled.show()
# time.sleep(2)  # DHT22要求至少2秒间隔

























# #步骤三：加入按键和舵机
# #注意按键需要消抖，参考11月24日代码，用非阻塞方式检测按键，按键按下时触发舵机旋转。
# #舵机控制部分参考12月22日代码，使用Wokwi的舵机模块，使用PWM控制角度，角度范围为0-180度，0度为舵机关闭状态。
# import dht 
# import framebuf
# from machine import Pin,I2C,PWM
# import time
# import utime
# import ssd1306
# from font import font16


# # 初始化 I2C 和 OLED（SSD1306）
# i2c = I2C(0,scl=Pin(22), sda=Pin(21))
# oled_width = 128
# oled_height = 64
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# def draw_chinese(oled, font, word, x, y):
#     for ch in word:
#         data = bytearray(font.get(ch, [0x00] * 32))
#         fb = framebuf.FrameBuffer(data, 16, 16, framebuf.MONO_HLSB)
#         oled.framebuf.blit(fb, x, y)  # 使用 oled.framebuf 的 blit
#         x += 16




# # 配置DHT22 (GPIO4)
# sensor = dht.DHT22(Pin(4))


# temp_highth = 40

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



# # 配置无源蜂鸣器
# buzzer_pin = Pin(15)
# buzzer = PWM(buzzer_pin)

# # 音符频率表 (单位：赫兹 Hz)
# # 这是一个简化的音阶，C4就是中央C (Do)
# NOTE_C4 = 262
# NOTE_D4 = 294
# NOTE_E4 = 330
# NOTE_F4 = 349
# NOTE_G4 = 392

# def play_tone(frequency):
#     """以指定频率播放声音"""
#     if frequency > 0:
#         buzzer.freq(frequency)    # 设置频率（音高）
#         buzzer.duty_u16(32768)  # 设置占空比（音量），一半占空比通常音量最大
#     else:
#         stop_tone()

# def stop_tone():
#     """停止发声"""
#     buzzer.duty_u16(0) # 将占空比设为0即可静音


# stop_tone()

# #配置按键，使用非阻塞按键检测与消抖
# class Button:
#     def __init__(self, pin_num, debounce_ms=50):
#         self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
#         self.debounce_ms = debounce_ms
#         self.last_state = self.pin.value()
#         self.last_change = time.ticks_ms()

#     def pressed(self):
#         current = self.pin.value()
#         now = time.ticks_ms()
        
#         if current != self.last_state:
#             self.last_change = now
#             self.last_state = current
# # 检测下降沿（按下）且已稳定
#         if (current == 0 and 
#             time.ticks_diff(now, self.last_change) >= self.debounce_ms):
#             # 重置状态防止重复触发
#             self.last_state = 1
#             return True
#         return False

# # 创建Button对象btn
# btn = Button(23)
# #使用范例如下：
# # while True:
# #     if btn.pressed():
# #         print("Button DEBOUNCED press!")









# #配置舵机,使用
# servo = PWM(Pin(13),freq=50)
# # ----- 核心逻辑：伺服电机角度控制函数-----
# def set_servo_angle(angle):
#     if 0 <= angle <= 180:
#         # 将角度(0-180)映射到脉冲宽度(500k-2.5M纳秒)，适配Wokwi舵机特性
#         duty_ns = int(500000 + (angle / 180) * 2000000)
#         servo.duty_ns(duty_ns)
# # ----- 关键修正：初始化位置-----
# # 确保电机启动后有明确位置
# print("初始化位置：关闭 (0度)")
# set_servo_angle(0)
# time.sleep(1) # 等待1秒，确保电机到位








# # 主循环
# while True:
#     temp, hum = read_sensor()
#     if temp is not None and hum is not None:
#         oled.fill(0)
#         if temp < temp_highth:
#             draw_chinese(oled, font16, '温度', 0, 12)
#             draw_chinese(oled, font16, '°', 80, 12)
#             oled.text(":{}  C".format(temp),30,16)
#             oled.text(":{}%".format( hum),30,32)
#             stop_tone()
#             oled.show()
#         else:
#             if btn.pressed():
#                 print("Button DEBOUNCED press!")
#                 set_servo_angle(70) # 舵机旋转到70度
#                 time.sleep(1) # 等待1秒，确保旋转完成
#                 set_servo_angle(0) # 舵机回到初始位置
#             else:
#                 set_servo_angle(0) # 舵机保持关闭状态
#                 draw_chinese(oled, font16, '温度过高 请加冰', 0, 12)
#                 play_tone(NOTE_C4)
#                 utime.sleep(0.5) # 持续0.5秒（替换time.sleep为utime.sleep）           
#                 oled.show()
# time.sleep(2)  # DHT22要求至少2秒间隔


#现阶段问题1：由于time.sleep(2)的原因，只有在程序开始运行后2s,4s,6s等特定的时间按下按键才能被检测
#现阶段问题2: 开头蜂鸣器自动发出声音，原因未知，在while循环之前加上stop_tone()解决。
#现阶段问题3：软件设计不够健壮，需要考虑各种异常情况，如传感器异常、舵机异常、按键异常等。

















# # 步骤四：改为非阻塞，把几乎所有time.sleep换成if time.ticks_diff( t1, t2 ) >= delta time:的形式，这样就避免了time.sleep的阻塞，可以实现精准的定时。
# # 为什么ai建议我用utime.sleep呢？真笨，它们本质上都会造成阻塞，我希望我的ai能聪明一些

# import dht 
# import framebuf
# from machine import Pin, I2C, PWM
# import time
# import utime
# import ssd1306
# from font import font16

# # --- 初始化 OLED ---
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# def draw_chinese(oled, font, word, x, y):
#     for ch in word:
#         data = bytearray(font.get(ch, [0x00] * 32))
#         fb = framebuf.FrameBuffer(data, 16, 16, framebuf.MONO_HLSB)
#         oled.framebuf.blit(fb, x, y)
#         x += 16

# # --- 初始化 DHT22 ---
# sensor = dht.DHT22(Pin(4))
# temp_highth = 40  # 报警阈值

# # --- 初始化 蜂鸣器 ---
# buzzer_pin = Pin(15)
# buzzer = PWM(buzzer_pin)
# NOTE_C4 = 262

# def play_tone(frequency):
#     if frequency > 0:
#         buzzer.freq(frequency)
#         buzzer.duty_u16(32768)
#     else:
#         stop_tone()

# def stop_tone():
#     buzzer.duty_u16(0)

# stop_tone()

# # --- 优化后的按键类 ---
# class Button:
#     def __init__(self, pin_num, debounce_ms=50):
#         self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
#         self.debounce_ms = debounce_ms
#         self.last_press_time = 0
#         self.prev_state = 1 # 初始状态为高电平（未按下）

#     def pressed(self):
#         current_state = self.pin.value()
#         now = time.ticks_ms()
        
#         # 检测下降沿（从1变0）
#         is_pressed = False
#         if current_state == 0 and self.prev_state == 1:
#             # 只有距离上次触发超过消抖时间，才算有效
#             if time.ticks_diff(now, self.last_press_time) > self.debounce_ms:
#                 self.last_press_time = now
#                 is_pressed = True
        
#         self.prev_state = current_state
#         return is_pressed

# btn = Button(23)

# # --- 初始化 舵机 ---
# servo = PWM(Pin(13), freq=50)
# def set_servo_angle(angle):
#     if 0 <= angle <= 180:
#         duty_ns = int(500000 + (angle / 180) * 2000000)
#         servo.duty_ns(duty_ns)

# # 初始位置归零
# set_servo_angle(0)
# time.sleep(0.5) 

# # ================= 主程序逻辑 =================

# # 1. 定义时间戳变量
# last_sensor_time = 0     # 上次读取传感器的时间
# sensor_interval = 2000   # 传感器读取间隔 2000ms

# last_beep_time = 0       # 上次蜂鸣器响的时间
# beep_interval = 500      # 报警声间隔 500ms
# beep_state = False       # 蜂鸣器当前状态

# # 2. 全局存储当前的温湿度
# current_temp = 0
# current_hum = 0
# sensor_ready = False # 标志位：是否成功读取过一次数据

# while True:
#     current_time = time.ticks_ms() # 获取当前时间

#     # --- 任务一：读取传感器 (每2秒执行一次) ---
#     if time.ticks_diff(current_time, last_sensor_time) >= sensor_interval:
#         try: #try except 是python中处理异常的一种方式，可以避免程序崩溃
#             sensor.measure()
#             current_temp = sensor.temperature()
#             current_hum = sensor.humidity()
#             sensor_ready = True
#             # print("传感器更新:", current_temp, current_hum)
#         except OSError:
#             print("传感器读取错误")
#         last_sensor_time = current_time
        
#         # 顺便刷新一下屏幕（不需要太频繁，跟着传感器刷新即可）
#         oled.fill(0)
#         if sensor_ready:
#             if current_temp < temp_highth:
#                 # 正常温度显示
#                 draw_chinese(oled, font16, '温度', 0, 12)
#                 draw_chinese(oled, font16, '°', 80, 12)
#                 oled.text(":{} C".format(current_temp), 30, 16)
#                 oled.text(":{}%".format(current_hum), 30, 32)
#             else:
#                 # 高温显示
#                 draw_chinese(oled, font16, '温度过高 请加冰', 0, 12)
#         oled.show()

#     # --- 任务二：按键检测 (每一轮循环都极速检测) ---
#     # 只要温度过高，或者你想随时允许加冰，都可以检测按键
#     # 这里根据你的逻辑：只有高温时才检测按键，或者你可以改成随时检测
#     if sensor_ready and current_temp >= temp_highth: 
#         if btn.pressed():
#             print("按键按下，执行加冰")
#             stop_tone() # 动作时先静音
#             set_servo_angle(70)
#             time.sleep(1) # 舵机动作需要物理时间，这里可以用阻塞sleep，因为是用户主动触发
#             set_servo_angle(0)
#             # 动作完成后，重置报警计时，避免立刻尖叫
#             last_beep_time = time.ticks_ms()

#     # --- 任务三：报警蜂鸣器逻辑 (非阻塞滴答声) ---
#     if sensor_ready and current_temp >= temp_highth:
#         # 使用时间差来制造 "滴-滴-滴" 的效果，而不是用 sleep
#         if time.ticks_diff(current_time, last_beep_time) >= beep_interval:
#             last_beep_time = current_time
#             if beep_state:
#                 stop_tone()
#                 beep_state = False
#             else:
#                 play_tone(NOTE_C4)
#                 beep_state = True
#     else:
#         # 温度正常，确保蜂鸣器关闭
#         stop_tone()
#         beep_state = False











# 对比版本
import dht 
import framebuf
from machine import Pin,I2C,PWM
import time
import utime
import ssd1306
from font import font16

# ... (前面的初始化代码保持不变，为了节省篇幅略过，从主循环前的变量定义开始) ...

# 初始化 I2C 和 OLED（SSD1306）
i2c = I2C(0,scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def draw_chinese(oled, font, word, x, y):
    for ch in word:
        data = bytearray(font.get(ch, [0x00] * 32))
        fb = framebuf.FrameBuffer(data, 16, 16, framebuf.MONO_HLSB)
        oled.framebuf.blit(fb, x, y) 
        x += 16

# 配置DHT22 (GPIO4)
sensor = dht.DHT22(Pin(4))
temp_highth = 40

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

# 配置无源蜂鸣器
buzzer_pin = Pin(15)
buzzer = PWM(buzzer_pin)
NOTE_C4 = 262 # 频率

def play_tone(frequency):
    if frequency > 0:
        buzzer.freq(frequency) 
        buzzer.duty_u16(32768) 
    else:
        stop_tone()

def stop_tone():
    buzzer.duty_u16(0) 

stop_tone()

# 配置按键 (Button类保持不变)
class Button:
    def __init__(self, pin_num, debounce_ms=50):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.debounce_ms = debounce_ms
        self.last_state = self.pin.value()
        self.last_change = time.ticks_ms()

    def pressed(self):
        current = self.pin.value()
        now = time.ticks_ms()
        if current != self.last_state:
            self.last_change = now
            self.last_state = current
        if (current == 0 and 
            time.ticks_diff(now, self.last_change) >= self.debounce_ms):
            self.last_state = 1
            return True
        return False

btn = Button(23)

# 配置舵机
servo = PWM(Pin(13),freq=50)
def set_servo_angle(angle):
    if 0 <= angle <= 180:
        duty_ns = int(500000 + (angle / 180) * 2000000)
        servo.duty_ns(duty_ns)

print("初始化位置：关闭 (0度)")
set_servo_angle(0)
time.sleep(1) 

# ==========================================
#      注意：这里开始是主要的修改区域
# ==========================================

# [修改后] 新增：为了不使用sleep，我们需要记录上一次执行动作的时间
last_read_time = 0      # 上次读取传感器的时间
last_beep_time = 0      # 上次报警响的时间
beep_state = False      # 蜂鸣器当前是响还是停
temp = 0                # 缓存温度变量
hum = 0                 # 缓存湿度变量

# 主循环
while True:
    # [修改后] 新增：获取当前系统运行时间
    current_time = time.ticks_ms()

    # [原始内容] temp, hum = read_sensor()
    # [修改后] 只有当距离上次读取超过2000ms时，才真正去读传感器
    if time.ticks_diff(current_time, last_read_time) >= 2000:
        temp, hum = read_sensor()
        last_read_time = current_time # 更新读取时间
        # [修改后] 只有读取了新数据才刷新这一部分的屏幕，避免闪烁
        if temp is not None and hum is not None:
             oled.fill(0) # 暂时简单处理，每次读传感器清屏重绘
             # 把原本在下面的绘图逻辑放这里，因为不需要每毫秒都画
             if temp < temp_highth:
                draw_chinese(oled, font16, '温度', 0, 12)
                draw_chinese(oled, font16, '°', 80, 12)
                oled.text(":{}  C".format(temp),30,16)
                oled.text(":{}%".format( hum),30,32)
                stop_tone()
             else:
                draw_chinese(oled, font16, '温度过高 请加冰', 0, 12)
                draw_chinese(oled, font16, '温度', 0, 30)
                draw_chinese(oled, font16, '°', 80, 30)
                oled.text(":{}  C".format(temp),30,34)
             oled.show()

    # [修改后] 此时 temp 可能为 None (刚启动时)，加个判断
    if temp is not None and hum is not None:
        # [原始内容] oled.fill(0) (移动到了上面定时读取的代码块里)
        
        # [原始内容] if temp < temp_highth:
        # [原始内容]    ...绘制正常界面...
        # [原始内容] else:
        
        # [修改后] 直接判断高温情况下的逻辑，因为正常逻辑已经在上面定时块里处理了
        if temp >= temp_highth:
            # [修改后] 在高温时，按键检测每一轮循环都执行，不再被sleep阻塞！
            if btn.pressed():
                stop_tone()
                print("按键按下 执行加冰")
                set_servo_angle(70) 
                # [注] 这里可以用 sleep(1)，因为加冰是机械动作，用户愿意等待
                time.sleep(1) 
                set_servo_angle(0) 
            else:
                set_servo_angle(0) 
                # [原始内容] draw_chinese(oled, font16, '温度过高 请加冰', 0, 12) (已移至上方)
                
                # ----- 报警声音的修改 -----
                # [原始内容] play_tone(NOTE_C4)
                # [原始内容] utime.sleep(0.5) <--- 以前就是这一句卡住了按键
                # [原始内容] oled.show()
                
                # [修改后] 使用非阻塞的“滴答”逻辑
                if time.ticks_diff(current_time, last_beep_time) >= 500: # 每500ms切换一次状态
                    last_beep_time = current_time
                    if beep_state:
                        stop_tone()   # 响了500ms，停一下
                        beep_state = False
                    else:
                        play_tone(NOTE_C4) # 停了500ms，响一下
                        beep_state = True
        else:
            # [修改后] 温度正常时，确保蜂鸣器安静
             stop_tone()
             beep_state = False

    # [原始内容] time.sleep(2)  # DHT22要求至少2秒间隔
    # [修改后] 删除！因为我们在开头用了 if time.ticks_diff(...) 控制了频率
    # 这里什么都不写，循环会以最快速度运行，时刻准备检测按键