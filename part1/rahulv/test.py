import sys

try:
    a=input("enter first roll of die\n")
except SyntaxError:
    pass
if type(a)!='int' or a > 6 or a < 1 :
        print 'invalid input'
        exit()
