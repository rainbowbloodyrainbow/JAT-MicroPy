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
    MenuItem("Settings", children=[
        MenuItem("Brightness", lambda: show_msg("Bright: 100%")),
        MenuItem("Sound", lambda: show_msg("Sound: ON")),
        MenuItem("Back")
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