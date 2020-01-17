from tkinter import *
from tkinter import messagebox, colorchooser
from objects import *
from dialogs import *
import datetime, sys


class MyApp:
    def __init__(self, parent):
        self.x = 0
        self.y = 0
        self.color_bg = 'lightgreen'
        self.parent = parent
        self.logged = False
        self.start = None
        self.user = None
        self.users = []
        self.screen_width = self.parent.winfo_screenwidth()
        self.screen_height = self.parent.winfo_screenheight()
        self.passwd = None
        self.time = None
        self.drawWidgets()

    def drawWidgets(self):
        self.canvas = Canvas(self.parent, width=self.screen_width, height=self.screen_height, bg=self.color_bg)
        self.canvas.pack(fill=BOTH,expand=True)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.focus_set()
        self.container = Frame(self.parent, width=self.screen_width, height=40, bg="gray")
        self.container.pack(side=BOTTOM,fill=BOTH)
        start_button = Button(self.container, text="   Start   ", command=self.start_menu)
        start_button.pack(side=LEFT)
        self.systime = Label(self.container, text="%s" % (self.time), fg='white', bg='gray')
        self.systime.pack(side=RIGHT)
        self.redraw_canvas()

    def start_menu(self):
        for u in self.users:
            self.user = u
            if u.logged == True:
                self.start = startDialog(self.parent,self.user)
                self.parent.wait_window(self.start.top)
                print("Start")
                self.redraw_canvas()
                pass

    def clear_canvas(self):
        self.canvas.delete("all")

    def login_screen(self):
        self.user = user(self.screen_width/2,self.screen_height/2)
        self.users.append(self.user)
        for u in self.users:
            u.draw(self.canvas) 

    def redraw_canvas(self):   
        self.clear_canvas()
        for u in self.users:
            self.user = u
            if u.logged == True:
                self.logged = True
            else:
                self.logged = False
        if (self.logged == False):
            self.color_bg = 'lightgreen'
            self.canvas['bg']=self.color_bg
            self.canvas['height']=self.screen_height
            self.login_screen()
        else: 
            self.color_bg = 'lightblue'
            self.canvas['bg']=self.color_bg
            self.canvas['height']=self.screen_height-34
            self.time = datetime.datetime.now().strftime("%B %d, %Y | %H:%M:%S  ")
            self.systime['text']="%s" % (self.time)

    def on_mouse_move(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasx(event.y)
        point = Point(self.x, self.y)
        for u in self.users:
            if u.detect_cursor(point): 
                self.user = u
            else: self.user = None

    def on_button_press(self, event):
        if(self.user != None and self.logged == False):
            dialog = userDialog(self.parent, self.user)
            self.parent.wait_window(dialog.top)
            self.redraw_canvas()
        else:
            pass
    

root = Tk()
root.attributes("-fullscreen", True)
myapp = MyApp(root)
while True:
    myapp.redraw_canvas()
    root.update()
root.mainloop()