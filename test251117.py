# for i in range(1, 10):
#     for j in range(1,i+1):
#         print("%d * %d = %d\t" % (i, j, i*j), end='')

# sum = 0

# for k in range(1, 100):
#     if k % 2 == 0:
#         sum = sum - k
#         print("%d" % (sum))
#     else:
#         sum = sum + k
#         print("%d" % (sum))

# instr = input("输入： ")

# sum_letters = 0
# sum_spaces = 0
# sum_nums = 0
# other = 0
# for m in range(0,Len(instr)):
#     slice = instr[m]
#     if slice.isalpha():
#         sum_letters += 1
#     elif slice.isspace():
#         sum_spaces += 1
#     elif slice.isdigit():
#         sum_nums += 1
#     else:
#         other += 1
# print("字母个数：%d, 空格个数：%d, 数字个数：%d" % (sum_letters, sum_spaces, sum_nums))

dic = {'1':'2123','2':'5324'}
newId = input("新学号：")
dic['2'] = int(newId)
print("修改之后学号为%d" %dic['2'])