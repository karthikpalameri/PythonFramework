import logging
import time
import traceback
from pathlib import Path

from utilities import custom_logger as cl


class Util():
    log = cl.customLogger(logLevel=logging.DEBUG)

    def get_project_root(self):
        """Returns Project root folder"""
        return Path(__file__).parent.parent

    def sleep(self, sec, info=""):
        if info is not None:
            self.log.info("Wait :: {} seconds for {}".format(sec, info))

        try:
            time.sleep(sec)
        except:
            traceback.print_exc()

    def verifyTextContains(self, actualText, expectedText):
        """
        Verify expectedText contains in actualText
        :param actualText:
        :param expectedText:
        :return:boolean
        """
        self.log.info("Actual text from webapplication UI -> :: {}".format(actualText))
        self.log.info("Expected text from webapplication UI -> :: {}".format(expectedText))
        if expectedText.lower() in actualText.lower():
            self.log.info("### Verification contains")
            return True

        else:
            self.log.info("### VERIFICATION DOES NOT CONTAINS!!!")
            return False

# """
# odd numbers even number print
# """
#
# mylist = [x for x in range(1, 10) if x % 2 == 0]
# print("Even numbers")
# print(mylist)
#
# """
# prime numbers print
#
# """
# num = 5
#
#
# def checkPrime(num):
#     for i in range(2, num):
#         if (num % i) == 0:
#             print("{} is NOT prime".format(num))
#             break
#     else:
#         print("{} is prime ".format(num))
#         return num
#
#
# li = [i for i in range(1, 10) if checkPrime(i)]
# print("Prime List:")
# print(li)
#
#
#
# """
# To find factorial of a number
# """
#
# num = input("Enter number to find factorial")
# x = int(num)
# facto = 1
# if x is 0:
#     print("Factorial of {} is : 1".format(x))
# elif x < 0:
#     print("Factorial doesn't exist if its less than 0")
# else:
#     for i in range(1, x + 1):
#         facto = facto * i
#     print("Factorial of {} is {}".format(x, facto))


# """
# Multiplication table
# """
# num = int(input("Enter any number for its nmultiplication table"))
#
# for i in range(1, 11):
#     print("{} x {} = {}".format(num, i, num * i))


# """
# Fibonacci series
# 0,1,1,2,3,5
# """
#
# num1 = 0
# num2 = 1
# temp = 1
# count = 5
# result = 1
# for i in range(0, count ):
#     if i == 0 :
#         print(num1)
#     elif i == 1:
#         print(num2)
#     else:
#         temp = num1 + num2
#         print(temp)
#         num1 = num2
#         num2 = temp

#
# """
# filter() method filter the given sequence with the help of a function that
# tests each element in the sequence to be true or not
#
# filter(function, sequence)
#
# sequence can be list, tuple, or any iterators
#
# :returns : iterator
#
# """
#
# def fun(var):
#     vowels=['a','e','i','o','u']
#     if var in vowels:
#         return True
#     else:
#         return False
#
# test_list=['a','b','c','d','e','f','g']
#
# filtered_Result=filter(fun,test_list)
#
# res="".join(filtered_Result)
# print(res)


# """
# filter even numbers only from the list using lamda function and filter function
# lamda function can have only 1 expression
# filter is always used with lamda to seperate list , tuple or set
#
# elegant way to filter out all the elements of a sequence “sequence”,
#  for which the function returns True
#
# """
#
# number_list = [1, 3, 5, 2, 5, 7, 98, 34, 64]
#
# even_numbers_only = filter(lambda x: x % 2 == 0, number_list)
#
# print(list(even_numbers_only))

#
# """
# split
#
# string.split("delimiter")
#
# """
#
# string_to_be_broken = "hello python world"
# res = string_to_be_broken.split(" ")
# print(res)


# """
# use of lamda() with map()
#
# the map function takes in a function and a list and a new list is returned
#
# map(function,list)
# returns:new list is returned with modified value
#
# """
#
#
# lis=[1,2,3,1,2,3]
#
# ressss= map(lambda x:x+1 , lis)
# print(list(ressss))


#
# """
# random.choice(sequence)
#
# """
#
# test_Strin="helloPython"
# import random
# listz=list(test_Strin)
#
# print(listz)
# print(random.choice(listz))
# print(random.choice(test_Strin))


# """
# string.ascii_lowercase will give the lowercase letters ‘abcdefghijklmnopqrstuvwxyz’.
# """
# import string
#
# print(string.ascii_lowercase)

# """
# check for lowercase in the passed Value
# return : boolean
# """
#
# import string
#
#
# def checkIfLowerCase(value):
#     not_lower = list(filter(lambda x: x not in string.ascii_lowercase, value))
#     if len(list(not_lower)) is not 0:
#         notLowerString="".join(not_lower)
#         print("{} is not in Lower Case from the value {}".format(notLowerString,value))
#         return False
#     else:
#         return True
#
#
# print(checkIfLowerCase("dafjdafT"))

#
# """
# create random String of printable character
# """
# import random
# import string
# def getAlphaNumeric(length, type="mix"):
#     """
#     Create random String of printable character
#     :param length: length of the random string to generate
#     :param type: mix,lower,upper,digits,specialcharacter
#     :return:
#     """
#     switch = {
#         "lower": string.ascii_lowercase,
#         "upper": string.ascii_uppercase,
#         "digits": string.digits,
#         "specialcharacters": string.punctuation,
#         "mix": string.printable
#
#     }
#     result_string = switch.get(type, string.printable)
#     string_to_return = ''
#
#     return string_to_return.join(random.choice(result_string) for i in range(length))
#
#
# print(getAlphaNumeric(9, type="mix"))
