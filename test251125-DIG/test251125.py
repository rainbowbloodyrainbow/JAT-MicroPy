from machine import Pin
import time
led= [Pin(i, Pin.OUT, value=1) for i in (2,4,5,18,19,21,22)]
ledcom_1 = Pin(15, Pin.OUT, value=1)
ledcom_0 = Pin(23, Pin.OUT, value=1)

LED_Bits = {
    '0': [0,0,0,0,0,0,1],
    '1': [1,0,0,1,1,1,1],
    '2': [0,0,1,0,0,1,0],
    '3': [0,0,0,0,1,1,0],
    '4': [1,0,0,1,1,0,0],
    '5': [0,1,0,0,1,0,0],
    '6': [0,1,0,0,0,0,0],
    '7': [0,0,0,1,1,1,1],
    '8': [0,0,0,0,0,0,0],
    '9': [0,0,0,0,1,0,0]
}
duty=0.01
def display_two_numbers(num_tens,num_ones):
    times=50
    for i in range(times):
        ledcom_0.value(0)
        for j in range(7):
            led[j].value(LED_Bits[num_tens][j])
        ledcom_1.value(1)
        time.sleep(duty)
        ledcom_1.value(0)
        for j in range(7):
            led[j].value(LED_Bits[num_ones][j])
        ledcom_0.value(1)
        time.sleep(duty)
while True:
    display_two_numbers('0','0')
    display_two_numbers('0','1')
    display_two_numbers('0','2')
    display_two_numbers('0','3')
    display_two_numbers('0','4')
    display_two_numbers('0','5')
    display_two_numbers('0','6')
    display_two_numbers('0','7')
    display_two_numbers('0','8')
    display_two_numbers('0','9')
    display_two_numbers('1','0')
    display_two_numbers('1','1')
    display_two_numbers('1','2')
    display_two_numbers('1','3')
    display_two_numbers('1','4')
    display_two_numbers('1','5')
    display_two_numbers('1','6')
    display_two_numbers('1','7')
    display_two_numbers('1','8')
    display_two_numbers('1','9')
    display_two_numbers('2','0')
    display_two_numbers('2','1')
    display_two_numbers('2','2')
    display_two_numbers('2','3')
    display_two_numbers('2','4')
    display_two_numbers('2','5')
    display_two_numbers('2','6')
    display_two_numbers('2','7')
    display_two_numbers('2','8')
    display_two_numbers('2','9')
    display_two_numbers('3','0')
    display_two_numbers('3','1')
    display_two_numbers('3','2')
    display_two_numbers('3','3')
    display_two_numbers('3','4')
    display_two_numbers('3','5')
    display_two_numbers('3','6')
    display_two_numbers('3','7')
    display_two_numbers('3','8')
    display_two_numbers('3','9')
    display_two_numbers('4','0')
    display_two_numbers('4','1')
    display_two_numbers('4','2')
    display_two_numbers('4','3')
    display_two_numbers('4','4')
    display_two_numbers('4','5')
    display_two_numbers('4','6')
    display_two_numbers('4','7')
    display_two_numbers('4','8')
    display_two_numbers('4','9')
    display_two_numbers('5','0')
    display_two_numbers('5','1')
    display_two_numbers('5','2')
    display_two_numbers('5','3')
    display_two_numbers('5','4')
    display_two_numbers('5','5')
    display_two_numbers('5','6')
    display_two_numbers('5','7')
    display_two_numbers('5','8')
    display_two_numbers('5','9')
    display_two_numbers('6','0')
    display_two_numbers('6','1')
    display_two_numbers('6','2')
    display_two_numbers('6','3')
    display_two_numbers('6','4')
    display_two_numbers('6','5')
    display_two_numbers('6','6')
    display_two_numbers('6','7')
    display_two_numbers('6','8')
    display_two_numbers('6','9')
    display_two_numbers('7','0')
    display_two_numbers('7','1')
    display_two_numbers('7','2')
    display_two_numbers('7','3')
    display_two_numbers('7','4')
    display_two_numbers('7','5')
    display_two_numbers('7','6')
    display_two_numbers('7','7')
    display_two_numbers('7','8')
    display_two_numbers('7','9')
    display_two_numbers('8','0')
    display_two_numbers('8','1')
    display_two_numbers('8','2')
    display_two_numbers('8','3')
    display_two_numbers('8','4')
    display_two_numbers('8','5')
    display_two_numbers('8','6')
    display_two_numbers('8','7')
    display_two_numbers('8','8')
    display_two_numbers('8','9')
    display_two_numbers('9','0')
    display_two_numbers('9','1')
    display_two_numbers('9','2')
    display_two_numbers('9','3')
    display_two_numbers('9','4')
    display_two_numbers('9','5')
    display_two_numbers('9','6')
    display_two_numbers('9','7')
    display_two_numbers('9','8')
    display_two_numbers('9','9')
#这里有没有办法简化代码？
#答案：有，可以使用嵌套循环来简化代码，如下所示：
# while True:
#     for tens in range(10):
#         for ones in range(10):
#             display_two_numbers(str(tens), str(ones))
#             # 这里可以添加一个短暂的延时，以便观察数字变化
#             time.sleep(0.1)
