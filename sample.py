def mydecorator(funcarg):
    def func():
        print('Before')
        funcarg()
        print('after')
    return func

@mydecorator
def func1():
    print('Function')

func1()
