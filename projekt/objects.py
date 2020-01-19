from abc import ABC , abstractmethod

DEFAULT_CONFIG = {"fill":"white",
      "outline":"white",
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
        self.name = None

    def __repr__(self):
        return "Object(type: {},x: {},y: {},width: {},height: {},fill: {})".format(self.type,self.x, self.y,self.width,self.height,self.fill)

    def __getitem__(self, type):
        return self.type[0:]

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self,value):
        if value < 0:
            self.__x = 0
            return
        self.__x = float(value)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self,value):
        if value < 0:
            self.__y = 0
            return
        self.__y = float(value)

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self,value):
        if value < 0:
            self.__width = 0
            return
        self.__width = float(value)

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self,value):
        if value < 0:
            self.__height = 0
            return
        self.__height = float(value)

    @abstractmethod
    def draw(self, canvas):
        pass

    @abstractmethod
    def detect_cursor(self, point):
        pass

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

class folder(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fill = "yellow"
        self.width = float(60)
        self.height = float(60)
        self.outline_color = "black"
        self.outline_width= "2"
        self.name = None
        self.objects = []
    
    def draw(self,canvas):
        folder = canvas.create_rectangle(self.x - self.width/2, self.y - self.height/2,self.x + self.width/2,self.y + self.height/2, fill=self.fill, outline=self.outline_color, width=self.outline_width)
        folder += canvas.create_rectangle(self.x - self.width/2, self.y - self.height/2 + 10 ,self.x + self.width/2 - 10,self.y + self.height/2, fill=self.fill, outline=self.outline_color, width=self.outline_width)
        folder += canvas.create_text(self.x - 2.5*len(self.name),self.y + 40, anchor='w', text="%s" % self.name)
        return folder

    def detect_cursor(self,point):
        return (self.x - self.width/2 <= point.x <= self.x + self.width/2 and self.y - self.height/2 <= point.y <= self.y + self.height/2)

class filetxt(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fill = "white"
        self.width = float(60)
        self.height = float(60)
        self.outline_color = "black"
        self.outline_width= "2"
        self.name = None
        self.text = ""
    
    def draw(self,canvas):
        filetxt = canvas.create_rectangle(self.x - self.width/2, self.y - self.height/2,self.x + self.width/2,self.y + self.height/2, fill=self.fill, outline=self.outline_color, width=self.outline_width)
        filetxt += canvas.create_line(self.x - 20, self.y - 20,self.x + 20,self.y - 20, fill='black', width=3)
        filetxt += canvas.create_line(self.x - 20, self.y - 10,self.x + 20,self.y - 10, fill='black', width=3)
        filetxt += canvas.create_line(self.x - 20, self.y,self.x + 20,self.y, fill='black', width=3)
        filetxt += canvas.create_line(self.x - 20, self.y + 10,self.x + 20,self.y + 10, fill='black', width=3)
        filetxt += canvas.create_line(self.x - 20, self.y + 20,self.x + 20,self.y + 20, fill='black', width=3)
        filetxt += canvas.create_text(self.x - 2.5*len(self.name),self.y + 40, anchor='w', text="%s" % self.name)
        return filetxt

    def detect_cursor(self,point):
        return (self.x - self.width/2 <= point.x <= self.x + self.width/2 and self.y - self.height/2 <= point.y <= self.y + self.height/2)
