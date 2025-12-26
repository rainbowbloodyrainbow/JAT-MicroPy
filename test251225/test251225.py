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

























#步骤三：加入按键和舵机
#注意按键需要消抖，参考11月24日代码，用非阻塞方式检测按键，按键按下时触发舵机旋转。
#舵机控制部分参考12月22日代码，使用Wokwi的舵机模块，使用PWM控制角度，角度范围为0-180度，0度为舵机关闭状态。
import dht 
import framebuf
from machine import Pin,I2C,PWM
import time
import utime
import ssd1306
from font import font16


# 初始化 I2C 和 OLED（SSD1306）
i2c = I2C(0,scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def draw_chinese(oled, font, word, x, y):
    for ch in word:
        data = bytearray(font.get(ch, [0x00] * 32))
        fb = framebuf.FrameBuffer(data, 16, 16, framebuf.MONO_HLSB)
        oled.framebuf.blit(fb, x, y)  # 使用 oled.framebuf 的 blit
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

# 音符频率表 (单位：赫兹 Hz)
# 这是一个简化的音阶，C4就是中央C (Do)
NOTE_C4 = 262
NOTE_D4 = 294
NOTE_E4 = 330
NOTE_F4 = 349
NOTE_G4 = 392

def play_tone(frequency):
    """以指定频率播放声音"""
    if frequency > 0:
        buzzer.freq(frequency)    # 设置频率（音高）
        buzzer.duty_u16(32768)  # 设置占空比（音量），一半占空比通常音量最大
    else:
        stop_tone()

def stop_tone():
    """停止发声"""
    buzzer.duty_u16(0) # 将占空比设为0即可静音




#配置按键，使用非阻塞按键检测与消抖
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
# 检测下降沿（按下）且已稳定
        if (current == 0 and 
            time.ticks_diff(now, self.last_change) >= self.debounce_ms):
            # 重置状态防止重复触发
            self.last_state = 1
            return True
        return False

# 创建Button对象btn
btn = Button(23)
#使用范例如下：
# while True:
#     if btn.pressed():
#         print("Button DEBOUNCED press!")









#配置舵机,使用
servo = PWM(Pin(15),freq=50)
# ----- 核心逻辑：伺服电机角度控制函数-----
def set_servo_angle(angle):
    if 0 <= angle <= 180:
        # 将角度(0-180)映射到脉冲宽度(500k-2.5M纳秒)，适配Wokwi舵机特性
        duty_ns = int(500000 + (angle / 180) * 2000000)
        servo.duty_ns(duty_ns)
# ----- 关键修正：初始化位置-----
# 确保电机启动后有明确位置
print("初始化位置：关闭 (0度)")
set_servo_angle(0)
time.sleep(1) # 等待1秒，确保电机到位








# 主循环
while True:
    temp, hum = read_sensor()
    if temp is not None and hum is not None:
        print("温度: {}°C, 湿度: {}%".format(temp, hum))
        oled.fill(0)
        if temp < temp_highth:
            draw_chinese(oled, font16, '温度', 0, 12)
            draw_chinese(oled, font16, '°', 80, 12)
            oled.text(":{}  C".format(temp),30,16)
            oled.text(":{}%".format( hum),30,32)
            stop_tone()
            oled.show()
        else:
            if btn.pressed():
                print("Button DEBOUNCED press!")
                set_servo_angle(70) # 舵机旋转到70度
                time.sleep(1) # 等待1秒，确保旋转完成
                set_servo_angle(0) # 舵机回到初始位置
            else:
                set_servo_angle(0) # 舵机保持关闭状态
                draw_chinese(oled, font16, '温度过高 请加冰', 0, 12)
                play_tone(NOTE_C4)
                utime.sleep(0.5) # 持续0.5秒（替换time.sleep为utime.sleep）           
                oled.show()
time.sleep(2)  # DHT22要求至少2秒间隔


