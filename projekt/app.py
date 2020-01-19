from tkinter import *
from tkinter import messagebox, colorchooser
from objects import *
from dialogs import *
import datetime
import sys
import json


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
        self.object = None
        self.objects = []
        self.screen_width = self.parent.winfo_screenwidth()
        self.screen_height = self.parent.winfo_screenheight()
        self.passwd = None
        self.time = None
        self.json_neco = None
        self.drawWidgets()
        self.open()

    def drawWidgets(self):
        self.canvas = Canvas(self.parent, width=self.screen_width,height=self.screen_height, bg=self.color_bg)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-3>", self.on_button_release)
        self.canvas.bind("<ButtonPress-3>", self.right_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.focus_set()
        self.container = Frame(
            self.parent, width=self.screen_width, height=40, bg="gray")
        self.container.pack(side=BOTTOM, fill=BOTH)
        start_button = Button(
            self.container, text="   Start   ", command=self.start_menu)
        start_button.pack(side=LEFT)
        self.systime = Label(self.container, text="%s" %
                             (self.time), fg='white', bg='gray')
        self.systime.pack(side=RIGHT)
        self.menu = Menu(root, tearoff=0)
        createmenu = Menu(self.menu)
        self.menu.add_cascade(label='Nový...  ', menu=createmenu)
        createmenu.add_command(label='Složka', command=self.create_folder)
        createmenu.add_command(label='Soubor', command=self.create_file)

        self.edit = Menu(root, tearoff=0)
        self.edit.add_command(label='Otevřít', command=self.open_f)
        self.edit.add_command(label='Odstranit', command=self.delete)
        self.edit.add_command(label='Přejmenovat', command=self.rename)
        self.redraw_canvas()


    def object_decoder(self, obj):
        if obj['type'] == 'folder':
            f = folder(obj['_Shape__x'], obj['_Shape__y'])
            for i in obj['objects']:
                print(i)
                f.objects = json.loads(i,object_hook=self.object_decoder)
        if obj['type'] == 'filetxt':  
            f = filetxt(obj['_Shape__x'], obj['_Shape__y'])
            f.text = obj['text']
        f.width = obj['_Shape__width']
        f.height = obj['_Shape__height']
        f.name = obj['name']
        f.outline_color = obj['outline_color']
        f.outline_width = obj['outline_width']
        f.fill = obj['fill']
        return f

    def open(self):
        try:
            my_file = open("objects.json", "r")
            self.objects = json.loads(my_file.read(),object_hook=self.object_decoder)
            print(self.objects)
            self.redraw_canvas()
        except:
            pass

    def save(self):
        json_data = ([ob.__dict__ for ob in self.objects])
        for f in self.objects:
            if f.__getitem__(type) == 'folder':
                try:
                    self.json_neco = ([ob.__dict__ for ob in f.objects])
                except:
                    pass
        for i in json_data:
            if i['type'] == 'folder' and self.json_neco:
                i['objects'] = self.json_neco
        json_dump = json.dumps(json_data)
        my_file = open("objects.json", "w")
        my_file.write(json_dump)

    def start_menu(self):
        for u in self.users:
            self.user = u
            if u.logged == True:
                self.start = startDialog(self.parent,self.user)
                self.parent.wait_window(self.start.top)
                self.redraw_canvas()

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
            for f in self.objects:
                f.draw(self.canvas) 
            self.save()
        

    def on_mouse_move(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasx(event.y)
        self.point = Point(self.x, self.y)
        if self.logged == False:
            for u in self.users:
                if u.detect_cursor(self.point): 
                    self.user = u
                else: self.user = None
        else:
            for f in self.objects:
                if f.detect_cursor(self.point): 
                    self.object = f
            


    def on_button_press(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasx(event.y)
        if(self.user != None and self.logged == False):
            dialog = userDialog(self.parent, self.user)
            self.parent.wait_window(dialog.top)
            self.redraw_canvas()
        else:
            self.object = None

    def right_button_press(self, event):
        pass

    def create_folder(self):
        self.object = folder(self.x, self.y)
        self.objects.append(self.object)
        createname = objectDialog(self.parent,self.object)
        self.parent.wait_window(createname.top)
        if(self.object.name == ""):
            self.objects.pop(-1)

    def create_file(self):
        self.object = filetxt(self.x, self.y)
        self.objects.append(self.object)
        createname = objectDialog(self.parent,self.object)
        self.parent.wait_window(createname.top)
        if(self.object.name == ""):
            self.objects.pop(-1)

    def on_button_release(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasx(event.y)
        if self.logged == True:
            if self.object == None:
                self.menu.post(event.x_root, event.y_root)
            else:
                self.edit.post(event.x_root, event.y_root)
        pass

    def on_move_press(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasy(event.y)
        for f in self.objects:
            if f.detect_cursor(self.point): 
                self.object = f
        if self.object:
            self.object.x = self.x if self.x <= self.screen_width else self.screen_width
            self.object.y = self.y if self.y <= self.screen_height else self.screen_height

    def delete(self):
        i = 0
        for f in self.objects:
            if f == self.object:
                self.objects.pop(i)
            i += 1
        self.object = None
        self.redraw_canvas()

    def rename(self):
        changename = objectDialog(self.parent,self.object)
        self.parent.wait_window(changename.top)
        self.redraw_canvas()
        pass

    def open_f(self):
        if self.object.__getitem__(type) == 'filetxt':
            obj = openfile(self.parent,self.object)
            self.parent.wait_window(obj.top)
        else:
            obj = openfolder(self.parent,self.object)
            self.parent.wait_window(obj.top)

root = Tk()
root.attributes("-fullscreen", True)
myapp = MyApp(root)
while True:
    if(myapp.logged != False):
        myapp.redraw_canvas()
    root.update()
    pass
root.mainloop()
