import requests 
# names = ["Lohn", "Mary"]
# for name in names:
#     if name.startswith("J"):
#         print("Found")
#         break
# else:
#     print("Not found")


# guess = 0
# answer = 5

# while answer != guess:
#     guess = int(input("Guess: "))
# else:
#     print("You won")

# def increment(number: int, by:int=1) -> tuple:
#     return (number, number + by)


# print(increment(2, by=3))

# x = increment(2, by=3)

# for i in x:
#     print(i)

# def multiply(*list):
#     total = 1
#     for number in list:
#         total *= number
#     return total

# print(multiply(2,3,4,5))

# def addition(*list):
#     total = 0
#     for number in list:
#         total += number
#     return total

# range.
# print(addition(1,2,3,4,5,6,7,8,9))

# def save_user(**user):
#     print(user["name"])

# save_user(id=1, name="admin")

# bit.ly/pygist
# def multiply(*numbers):
#     total = 1
#     for number in numbers:
#         total *= number
#     return total

# print("start")
# print(multiply(1,2,3))
# print("finish")

# def fizz_buzz(input):
#     if (input % 3 == 0) and (input % 5 == 0):
#         return "FizzBuzz"
#     if input % 3 == 0:
#         return "Fizz"
#     if input % 5 == 0:
#         return "Buzz"
#     return input


# print(fizz_buzz(8))

# dictionary = {'hola': 1, 'que': 20, 'tal': 30}
# for palabra in dictionary:
#     print(palabra[0].upper())

my_request = requests.get('http://go.codeschool.com/spamvanmenu')
menu_list = my_request.json()
print(menu_list)
for item in menu_list:
    print(item['name'], ': ', item['desc'].title(), ', $', item['price'], sep='')

