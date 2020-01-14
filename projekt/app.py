from tkinter import *
from tkinter import messagebox, colorchooser
from objects import *
from dialogs import *

class MyApp:
    def __init__(self, parent):
        self.x = 0
        self.y = 0
        self.color_bg = 'lightgreen'
        self.parent = parent
        self.logged = False
        self.user = None
        self.users = []
        self.screen_width = self.parent.winfo_screenwidth()
        self.screen_height = self.parent.winfo_screenheight()
        self.passwd = None
        self.drawWidgets()

    def drawWidgets(self):
        self.canvas = Canvas(self.parent, width=self.screen_width, height=self.screen_height, bg=self.color_bg)
        self.canvas.pack(fill=BOTH,expand=True)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.focus_set()
        self.container = Frame(self.parent, width=self.screen_width, height=45, bg="gray")
        self.container.pack(side=BOTTOM,fill=BOTH)
        start_button = Button(self.container, text="   Start   ", command=self.start_menu)
        start_button.pack(side=LEFT)


    def start_menu(self):
        self.container1 = Frame(self.parent, width=100, height=100, bg="gray")
        self.container1.pack(side=BOTTOM,fill=BOTH)
        self.redraw_canvas()

    def clear_canvas(self):
        self.canvas.delete("all")

    def login_screen(self):
        self.user = user(self.screen_width/2,self.screen_height/2)
        self.users.append(self.user)
        for u in self.users:
            u.draw(self.canvas) 
        print("facha to")

    def redraw_canvas(self):   
        self.clear_canvas()
        for u in self.users:
            if u.logged == True:
                self.user = u
                self.logged = True
        if (self.logged == False):
            self.login_screen()
        else: 
            self.color_bg = 'lightblue'
            self.canvas['bg']=self.color_bg
            self.canvas['height']=self.screen_height-34
            self.drawWidgets()
            print("Prihlasen!!")

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
        else: pass

#
#    def info_box(self):
#        messagebox.showinfo('Message title', 'Message content')
#        print("Zobrazí info")

root = Tk()
root.attributes("-fullscreen", True)
myapp = MyApp(root)
myapp.redraw_canvas()
root.mainloop()