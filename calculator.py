import random
import math
import time
import turtle

def slow(x):
    for i in x:
        print(i, end=""),time.sleep(0.03)

slow("Python Calculator")
print("\n")
num1 = eval(input("Enter 1st Number: "))
num2 = eval(input("Enter 2nd Number: "))
    

def add(num1,num2):
    add1 = num1 + num2
    print("\nSum: ",add1)
    
def subtract(num1, num2):
    if num1 < num2:
        num1,num2 = num2,num1
        sub1 = num1 - num2
        print("\nSubtraction: ",sub1)
    else:
        sub2 = num1 - num2
        print("\nSubtraction: ",sub2)

def multiplication(num1, num2):
    mul = num1 * num2
    print("\nMultiplication: ",mul)
    
def division(num1,num2):
    divide = num1/num2
    print("\nDivision: ",round(divide, 2))
    
def __main__():
    choice = str(input("Operation: "))
    
    if choice == '+':
        add(num1,num2)
        
    elif choice == '-':
        subtract(num1,num2)
        
    elif choice == '*':
        multiplication(num1,num2)
        
    elif choice == '/':
        division(num1,num2)
        


__main__()