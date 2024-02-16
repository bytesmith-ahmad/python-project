class fish_console_view:

    var = "xxx"

    def __init__(self):  
        self.var += "yyy"

    def __str__(self):             # this is the equivalent of toString() in java
        return f"{self.var}"
    
    def myfunc(self):
        print("Hello my name is " + self.var)