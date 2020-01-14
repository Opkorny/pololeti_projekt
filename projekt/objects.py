from abc import ABC , abstractmethod

DEFAULT_CONFIG = {"fill":"white",
      "outline":"black",
      "width":"3",}

class Point():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
                
    def getX(self): return self.x
    def getY(self): return self.y

class Shape(ABC):
    def __init__(self,x,y):
        self.type = self.__class__.__name__
        self.x = float(x)
        self.y = float(y)
        self.width = float(80)
        self.height = float(80)
        self.outline_color = DEFAULT_CONFIG['outline']
        self.outline_width = DEFAULT_CONFIG['width']
        self.fill = DEFAULT_CONFIG['fill']

    def __repr__(self):
        return "Shape(x: {},y: {},width: {},height: {},fill: {})".format(self.x, self.y,self.width,self.height,self.fill)


class user(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fill = "lightblue"
        self.name = 'student'
        self.password = 'student'
        self.logged = False

    def draw(self,canvas):
        user = canvas.create_rectangle(self.x - self.width/2, self.y - self.height/2 ,self.x + self.width/2,self.y + self.height/2, fill=self.fill, outline=self.outline_color, width=self.outline_width)
        user += canvas.create_oval(self.x - 20, self.y - 20,self.x + 20,self.y + 20, fill='white', outline='white', width=4)
        user += canvas.create_line(self.x, self.y,self.x - 20,self.y + 38, fill='white', width=5)
        user += canvas.create_line(self.x, self.y,self.x + 20,self.y + 38, fill='white', width=5)
        return user

    def detect_cursor(self,point):
        return (self.x - self.width/2 <= point.x <= self.x + self.width/2 and self.y - self.height/2 <= point.y <= self.y + self.height/2)
