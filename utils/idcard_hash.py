weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
table = ['1', '0', 'x', '9', '8', '7', '6', '5', '4', '3', '2']

id_num = input("Please input your ID number: ")

sum = 0
for i, num in enumerate(id_num):
    if i >= len(weight):
        break
    sum += int(num) * weight[i]

hash_num = table[sum % 11]
print('The hash num is: ', hash_num)