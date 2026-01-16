# 突然想写一个oled多级菜单，试试用状态机的方式实现
# 使用状态机编程的话，只要知道一共有多少个状态，每个状态下的行为是什么，状态之间如何切换，剩下的就是无脑敲代码了
# 首先先构思一下吧，假设一级菜单有3个选项，分别是A、B、C，其中A和B有二级菜单，可通过Back返回一级菜单，C没有二级菜单，进入C的界面3s后自动返回一级菜单;进入A后有A1、A2、Back三个选项，进入B后有B1、B2、B3、Back四个选项
# 一级菜单分为FirstMenu_A、FirstMenu_B、FirstMenu_C三个状态，其中FirstMenu_A为初始状态
# 二级菜单分为SecondMenu_A1、SecondMenu_A2、SecondMenu_ABack,SecondMenu_B1、SecondMenu_B2、SecondMenu_B3、SecondMenu_BBack七个状态
# 点进C、A1、A2、B1、B2、B3选项后，进入对应的显示状态，分别为Display_C、Display_A1、Display_A2、Display_B1、Display_B2、Display_B3六个状态，3s后自动返回上一级菜单
# 有btn_up、bun_dn、btn_ok三个按键，分别用于菜单选项的上移、下移和确认选择
# FirstMenu_A状态下，btn_up按下后切换到FirstMenu_C状态，btn_dn按下后切换到FirstMenu_B状态，btn_ok按下后切换到SecondMenu_A1状态
# FirstMenu_B状态下，btn_up按下后切换到FirstMenu_A状态，btn_dn按下后切换到FirstMenu_C状态，btn_ok按下后切换到SecondMenu_B1状态
# FirstMenu_C状态下，btn_up按下后切换到FirstMenu_B状态，btn_dn按下后切换到FirstMenu_A状态，btn_ok按下后切换到Display_C状态
# SecondMenu_A1状态下，btn_up按下后切换到SecondMenu_ABack状态，btn_dn按下后切换到SecondMenu_A2状态，btn_ok按下后切换到Display_A1状态
# SecondMenu_A2状态下，btn_up按下后切换到SecondMenu_A1状态，btn_dn按下后切换到SecondMenu_ABack状态，btn_ok按下后切换到Display_A2状态
# SecondMenu_ABack状态下，btn_up按下后切换到SecondMenu_A2状态，btn_dn按下后切换到SecondMenu_A1状态，btn_ok按下后切换到FirstMenu_A状态
# SecondMenu_B1状态下，btn_up按下后切换到SecondMenu_BBack状态，btn_dn按下后切换到SecondMenu_B2状态，btn_ok按下后切换到Display_B1状态
# SecondMenu_B2状态下，btn_up按下后切换到SecondMenu_B1状态，btn_dn按下后切换到SecondMenu_B3状态，btn_ok按下后切换到Display_B2状态
# SecondMenu_B3状态下，btn_up按下后切换到SecondMenu_B2状态，btn_dn按下后切换到SecondMenu_BBack状态，btn_ok按下后切换到Display_B3状态
# SecondMenu_BBack状态下，btn_up按下后切换到SecondMenu_B3状态，btn_dn按下后切换到SecondMenu_B1状态，btn_ok按下后切换到FirstMenu_B状态
# Display_C、Display_A1、Display_A2、Display_B1、Display_B2、Display_B3状态下，等待3s后自动切换到上一级菜单状态
from machine import Pin, I2C
import ssd1306
from time import sleep_ms

i2c = I2C(0, sda=Pin(21), scl=Pin(22))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
Menu_state = 'FirstMenu_A'  # 初始状态
btn_up = Pin(19, Pin.IN, Pin.PULL_UP)
btn_dn = Pin(18, Pin.IN, Pin.PULL_UP)
btn_ok = Pin(5, Pin.IN, Pin.PULL_UP)

while True:
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
        sleep_ms(3000)
        Menu_state = 'FirstMenu_C'
    elif Menu_state == 'Display_A1':
        oled.fill(0)
        oled.text('Displaying A1', 0, 20)
        oled.show()
        sleep_ms(3000)
        Menu_state = 'SecondMenu_A1'
    elif Menu_state == 'Display_A2':
        oled.fill(0)
        oled.text('Displaying A2', 0, 20)
        oled.show()
        sleep_ms(3000)
        Menu_state = 'SecondMenu_A2'
    elif Menu_state == 'Display_B1':
        oled.fill(0)
        oled.text('Displaying B1', 0, 20)
        oled.show()
        sleep_ms(3000)
        Menu_state = 'SecondMenu_B1'
    elif Menu_state == 'Display_B2':
        oled.fill(0)
        oled.text('Displaying B2', 0, 20)
        oled.show()
        sleep_ms(3000)
        Menu_state = 'SecondMenu_B2'
    elif Menu_state == 'Display_B3':
        oled.fill(0)
        oled.text('Displaying B3', 0, 20)
        oled.show()
        sleep_ms(3000)
        Menu_state = 'SecondMenu_B3'
    