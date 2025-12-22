#任务一(ssd1306部分收尾)：菜单
from machine import Pin, I2C
import ssd1306
import time

# --- 1. 初始化 OLED ---
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# --- 2. 按键类 ---
class Button:
    def __init__(self, pin_num):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.last_state = 1
        self.debounce_time = 0

    def pressed(self):
        current_state = self.pin.value()
        is_pressed = False

        if current_state == 0 and self.last_state == 1:
            if time.ticks_diff(time.ticks_ms(), self.debounce_time) > 200:
                is_pressed = True
                self.debounce_time = time.ticks_ms()

        self.last_state = current_state
        return is_pressed

# --- 3. 菜单类 ---
class MenuItem:
    def __init__(self, text, action=None, children=None):
        self.text = text
        self.action = action
        self.children = children or []

class MenuSystem:
    def __init__(self, oled, items):
        self.oled = oled
        self.items = items
        self.current_items = items
        self.selected = 0
        self.scroll_pos = 0
        self.parent_stack = []

    def navigate(self, direction):
        if not self.current_items:
            return
        new_pos = self.selected + direction
        if 0 <= new_pos < len(self.current_items):
            self.selected = new_pos
            if self.selected >= self.scroll_pos + 4:
                self.scroll_pos = self.selected - 3
            elif self.selected < self.scroll_pos:
                self.scroll_pos = max(0, self.selected)

    def select(self):
        item = self.current_items[self.selected]
        if item.children:
            self.parent_stack.append((self.current_items, self.selected, self.scroll_pos))
            self.current_items = item.children
            self.selected = 0
            self.scroll_pos = 0
        elif item.action:
            if item.text == "Back":
                self.back()
            else:
                item.action()

    def back(self):
        if self.parent_stack:
            self.current_items, self.selected, self.scroll_pos = self.parent_stack.pop()

    def draw(self):
        self.oled.fill(0)
        visible_items = self.current_items[self.scroll_pos : self.scroll_pos + 4]
        for i, item in enumerate(visible_items):
            y = i * 16
            if i == (self.selected - self.scroll_pos):
                self.oled.fill_rect(0, y, 128, 16, 1)
                self.oled.text(">" + item.text, 0, y + 4, 0)
            else:
                self.oled.text(" " + item.text, 0, y + 4, 1)
        self.oled.show()

# --- 4. 菜单动作函数 ---
def show_msg(msg):
    oled.fill(0)
    oled.text(msg, 10, 30)
    oled.show()
    time.sleep(1)

# --- 5. 菜单结构 ---
main_menu = [
    MenuItem("System Info", lambda: show_msg("ESP32 v1.19")),
    #lambda是python中创建匿名函数的关键字，下面稍作解释
    #有参数lambda如add = lambda x, y: x + y，表示创建一个有两个参数x和y的函数，返回x+y的值
    #无参数lambda如这里的lambda: show_msg("ESP32 v1.19")，表示创建一个不带参数的函数，调用时会执行show_msg("ESP32 v1.19")
    #这里用来定义一个简单的函数，当选择"System Info"菜单项时调用show_msg函数显示信息
    MenuItem("Settings", children=[
        MenuItem("Brightness", lambda: show_msg("Bright: 100%")),
        MenuItem("Sound", lambda: show_msg("Sound: ON")),
        MenuItem("Back")#这么写Back无法正常返回，如何修改？答：需要在MenuItem的action中指定调用back方法，如下所示：
        # MenuItem("Back", lambda: menu.back())
    ]),
    MenuItem("Reboot", lambda: show_msg("Rebooting...")),
    MenuItem("About", lambda: show_msg("By Wokwi User"))
]

menu = MenuSystem(oled, main_menu)

# --- 6. 按键初始化 ---
btn_up = Button(18)
btn_down = Button(19)
btn_select = Button(23)

print("Menu System Started. Use buttons on GPIO 18, 19, 23")

# --- 7. 主循环 ---
while True:
    if btn_up.pressed():
        menu.navigate(-1)
        menu.draw()
    if btn_down.pressed():
        menu.navigate(1)
        menu.draw()
    if btn_select.pressed():
        menu.select()
        menu.draw()
    time.sleep_ms(50)




























#任务二:ADC
#补充一些理论知识：ADC转换采集的时候，为什么会有损失？    #答：ADC（模数转换器）在将模拟信号转换为数字信号时会引入一些误差和损失，主要原因包括以下几点：
#分辨率限制：ADC的分辨率决定了它能够区分的电压级别数量。较低分辨率的ADC会导致量化误差，因为输入信号被映射到有限数量的数字值上，无法精确表示连续的模拟信号。
#采样率限制：如果ADC的采样率不足以捕捉输入信号的变化，可能会导致混叠现象，从而失去高频信息，影响信号的准确性。
#非线性失真：理想情况下，ADC的输入输出关系应该是线性的，但实际中可能存在非线性失真，导致输出值偏离真实输入值。    
#噪声干扰：环境噪声、电源噪声等都会影响ADC的测量结果，导致采集到的信号包含噪声成分。
#温度漂移：ADC的性能可能会随着温度变化而变化，导致测量误差。
#采样频率最少应大于信号频率的两倍，这样才能完整还原信号，这个叫奈奎斯特采样定理。
from machine import Pin, ADC
import time
pot = ADC(Pin(36),atten=ADC.ATTN_11DB)#创建ADC对象，连接到GPIO36引脚，并设置衰减为11dB，表示输入电压范围为0-3.6V
#为什么选择36号引脚？答：ESP32的ADC引脚有特定的编号，GPIO36是ADC1通道0，适合用于模拟输入采集
#还有别的引脚可选吗？答：32~39都可以，
pot.width(ADC.WIDTH_12BIT)#设置ADC分辨率为12位，即0-4095
while True:
    pot_value1 = pot.read()#读取ADC值，范围0-4095
    pot_value2 = pot.read_u16()#读取ADC值，范围0-65535
    pot_value3 = pot.read_uv()#读取ADC值，单位微伏，范围0-3600000
    # print(pot_value1, pot_value2, pot_value3/1000000)
    print("采样值1={:5d},转换值={:.2f}V".format(pot_value1, pot_value1/4095*3.3))
    print("采样值2={:5d},转换值={:.2f}V".format(pot_value2, pot_value2/65535*3.3))
    print("采样值3={:5d},转换值={:.2f}V\r\n".format(pot_value3, pot_value3/1000000))
    time.sleep(1)























#任务三：光敏电阻与电位器
from machine import ADC, Pin
import time

# 初始化 ADC 引脚
pot_adc = ADC(Pin(36))   # 电位器接 GPIO36
ldr_adc = ADC(Pin(39))   # 光敏电阻接 GPIO39

# 设置衰减为 11dB（支持 0~3.3V 输入）
pot_adc.atten(ADC.ATTN_11DB)
ldr_adc.atten(ADC.ATTN_11DB)

# （可选）设置12位精度（ESP32 默认即为12位）
# pot_adc.width(ADC.WIDTH_12BIT)
# ldr_adc.width(ADC.WIDTH_12BIT)

def read_pot():
    """读取电位器电压"""
    raw = pot_adc.read()
    voltage = raw * 3.3 / 4095
    return voltage, raw

def read_ldr():
    """读取光敏电阻并判断光照等级"""
    raw = ldr_adc.read()
    # 光敏特性：光照越强，阻值越小 → 分压越低 → raw 越小
    if raw > 3000:
        level = "Dark"
    elif raw > 1500:
        level = "Dim"
    elif raw > 500:
        level = "Medium"
    else:
        level = "Bright"
    return raw, level

# 主循环
print("Reading Potentiometer and LDR...")
print("-" * 40)
while True:
    pot_v, pot_raw = read_pot()
    ldr_raw, light_level = read_ldr()

    print("Pot: {:.2f} V (Raw: {})".format(pot_v, pot_raw))
    print("LDR: Raw={} → {}".format(ldr_raw, light_level))
    print("-" * 40)
    
    time.sleep(1)




