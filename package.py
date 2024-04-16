#This is a comment

print(f'hello')
if 5 > 2:
    print("five is greater than two")
""" hey 
this is also a comment
"""

x = 'you'

def myfunc():
   global x #larger scope
   x = 'u'
   print("this is " + x)

myfunc()

print("this is " + x)