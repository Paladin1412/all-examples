def hello():
    """
    fab hello
    """
    print("hello world")

def param(x, y):
    """
    fab param:x=hello,y=world
    """
    print(x + ' ' + y)

from fabric.api import local

def ls_local():
    """
    执行本地命令
    """
    local('ls .')
