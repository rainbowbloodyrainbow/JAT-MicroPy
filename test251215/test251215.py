# #任务四：任务三的基础上，增加一个 LED 灯，根据光敏电阻的光照等级调整 LED 亮度：
# # Dark（黑暗）：LED 关闭
# # Dim（昏暗）：LED 亮度为 25%，即duty=256
# # Medium（中等）：LED 亮度为 50%，即duty=512
# # Bright（明亮）：LED 亮度为 100%，即duty=1023
# from machine import ADC, Pin,PWM
# import time

# # 初始化 ADC 引脚
# pot_adc = ADC(Pin(36))   # 电位器接 GPIO36
# ldr_adc = ADC(Pin(39))   # 光敏电阻接 GPIO39
# led_pwm = PWM(Pin(21),freq = 500)
# # 设置衰减为 11dB（支持 0~3.3V 输入）
# pot_adc.atten(ADC.ATTN_11DB)
# ldr_adc.atten(ADC.ATTN_11DB)

# # （可选）设置12位精度（ESP32 默认即为12位）
# # pot_adc.width(ADC.WIDTH_12BIT)
# # ldr_adc.width(ADC.WIDTH_12BIT)

# def read_pot():
#     """读取电位器电压"""
#     raw = pot_adc.read()
#     voltage = raw * 3.3 / 4095
#     return voltage, raw#raw是原始采样值

# def read_ldr():
#     """读取光敏电阻并判断光照等级"""
#     raw = ldr_adc.read()
#     # 光敏特性：光照越强，阻值越小 → 分压越低 → raw 越小
#     if raw > 3000:
#         level = "Dark"
#         duty = 0
#     elif raw > 1500:
#         level = "Dim"
#         duty = 256
#     elif raw > 500:
#         level = "Medium"
#         duty = 512
#     else:
#         level = "Bright"
#         duty = 1023
#     #或者我们也可以根据raw值的范围来线性映射duty值，duty = int((4095 - raw) / 4095 * 1023)
#     return raw, level,duty

# #或者我们想要不用if判断，而是用ldr的数值直接映射到led的亮度，可以用下面的代码
# # def read_ldr():
# #     """读取光敏电阻并映射到LED亮度"""
# #     raw = ldr_adc.read()
# #     # 将 raw 映射到 0-1023 范围
# #     
# #     return raw, duty

# # 主循环
# print("Reading Potentiometer and LDR...")
# print("-" * 40)
# while True:
#     pot_v, pot_raw = read_pot()
#     ldr_raw, light_level,duty = read_ldr()
#     #pot_raw和ldr_raw有什么区别？答：pot_raw是电位器的原始ADC采样值，ldr_raw是光敏电阻的原始ADC采样值，它们分别反映了各自传感器的模拟输入电压水平
#     print("Pot: {:.2f} V (Raw: {})".format(pot_v, pot_raw))
#     print("LDR: Raw={} → {}".format(ldr_raw, light_level))
#     print("Setting LED duty to: {}".format(duty))
#     print("-" * 40)
#     led_pwm.duty(duty)
#     time.sleep(1)























# #任务五：任务三的基础上,用ssd1306代替print打印输出

# from machine import ADC, Pin, I2C
# import time
# import ssd1306

# # 初始化 ADC（光敏电阻）
# adc_pin = Pin(34)
# adc = ADC(adc_pin)
# adc.atten(ADC.ATTN_11DB)  # 设置满量程约 3.6V

# # 初始化 I2C 和 OLED（SSD1306）
# i2c = I2C(scl=Pin(22), sda=Pin(21))
# oled_width = 128
# oled_height = 64
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# # 读取光敏电阻值
# def read_light():
#     adc_value = adc.read()
#     # 光照越强，ADC 值越小（因为光敏电阻阻值下降）
#     light_percentage = (4095 - adc_value) / 4095 * 100
#     return adc_value, max(0, min(100, light_percentage))  # 限制在 0~100%

# # 主循环
# while True:
#     adc_val, light_pct = read_light()
#     oled.fill(0)
#     oled.text("Light Sensor", 0, 0)
#     oled.text("ADC: {}".format(adc_val), 0, 16)
#     oled.show()
#     # 打印到串口
#     print("ADC Value:", adc_val, "Light:", round(light_pct, 2), "%")


#作业
from machine import ADC, Pin, PWM, I2C
import time
import ssd1306

# 初始化 I2C 和 OLED（SSD1306）
i2c = I2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# 配置 ADC 和 LED
adc = ADC(Pin(36))
adc.atten(ADC.ATTN_11DB)  # 最大输入电压约 3.6V

led = PWM(Pin(33), freq=1000)

# 电压阈值设置 (单位：伏特)
LOW_THRESHOLD = 1.0
HIGH_THRESHOLD = 2.5

def check_voltage(voltage):
    """检查电压状态"""
    if voltage < LOW_THRESHOLD:
        return "LOW"
    elif voltage > HIGH_THRESHOLD:
        return "HIGH"
    else:
        return "NORMAL"

def get_led_pattern(status):
    """根据状态获取LED亮度（0-1023）"""
    patterns = {
        "LOW": 1023,    # 常亮（高亮度）
        "HIGH": 0,      # 常灭
        "NORMAL": 512   # 中等亮度
    }
    return patterns.get(status, 0)

# 主循环
while True:
    # 读取并转换电压
    raw_value = adc.read()
    voltage = raw_value * 3.3 / 4095
    
    # 检查电压状态
    status = check_voltage(voltage)
    
    # 设置LED亮度
    brightness = get_led_pattern(status)
    led.duty(brightness)
    
    # 显示状态
    oled.fill(0)
    oled.text("Voltage: {:.4f}".format(voltage),0,16)
    oled.text("Status: {}".format(status),0,32)
    oled.show()
























#任务六:移动平均滤波
from machine import ADC, Pin
import time

# 配置ADC
adc = ADC(Pin(36))
adc.atten(ADC.ATTN_11DB)

# 窗口大小
SAMPLE_SIZE = 10

# 使用普通列表替代 deque
samples = []

def moving_average_filter(new_value):
    """移动平均滤波"""
    # 1. 添加新数据
    samples.append(new_value)
    
    # 2. 如果数据超过窗口大小，移除最老的一个 (实现先进先出)
    if len(samples) > SAMPLE_SIZE:
        samples.pop(0)
    
    # 3. 计算平均值
    return sum(samples) / len(samples)

# 显示滤波效果对比
print("Raw\tFiltered")
while True:
    raw_value = adc.read()
    filtered_value = moving_average_filter(raw_value)
    
    print("{:4d}\t{:4.1f}".format(raw_value, filtered_value))
    time.sleep_ms(1000)