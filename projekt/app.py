from tkinter import *
from tkinter import messagebox, colorchooser
from objects import *
from dialogs import *
import datetime
import sys
import json

#
#
# Nefunguje ukládání + načítaní souboru JSON
# Není zařízeno více uživatelů 
# (nedostal jsem se k tomu -> zamotal jsem se do problému JSONu... a už nebyl moc čas a ani nálada)
#
#

#Objekt... aplikace
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
        self.open()
        self.drawWidgets()

#Nastaveni okna + canvas + menu
    def drawWidgets(self):
        self.canvas = Canvas(self.parent, width=self.screen_width,height=self.screen_height, bg=self.color_bg)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
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

#převede objekty z JSONu do objektu v Pythonu (NEFUNGUJE převod objektu ve foldrech) 
    def object_decoder(self, obj):
        if obj['type'] == 'folder':
            f = folder(obj['_Shape__x'], obj['_Shape__y'])
            for i in obj['objects']:
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

#Otevřeni souboru JSON a načteni dat
    def open(self):
        try:
            my_file = open("objects.json", "r")
            self.objects = json.loads(my_file.read(),object_hook=self.object_decoder)
            print(self.objects)
            self.redraw_canvas()
        except:
            pass
    
#Nekonečný loop který převede všechny objekty do formatu pythonu (NEFUNGUJE)
    def load(self, obj):
        if obj.__getitem__(type) == 'folder':
            for f in obj.objects:
                self.load(f)
                json_data = ([ob.__dict__ for ob in obj.objects])
                obj.objects = json_data
        else:
            pass

#Uložení objektů do souboru JSON
    def save(self):
        for f in self.objects:
            self.load(f)
        json_dump = json.dumps([ob.__dict__ for ob in self.objects])
        my_file = open("objects.json", "w")
        my_file.write(json_dump)

#Otevře dialogove okno představujíví nabídku start
    def start_menu(self):
        for u in self.users:
            self.user = u
            if u.logged == True:
                self.start = startDialog(self.parent,self.user)
                self.parent.wait_window(self.start.top)
                self.redraw_canvas()

#Vymaže všechny objekty z canvasu
    def clear_canvas(self):
        self.canvas.delete("all")

#Vykreslí všechny uživatele (nedostal jsem se k možnosti vytvoření více uživatelů -> neřeším vykreslování více uživatelů)
    def login_screen(self):
        self.user = user(self.screen_width/2,self.screen_height/2)
        self.users.append(self.user)
        for u in self.users:
            u.draw(self.canvas) 

#Vykreslí určité objekty na canvas (podle toho zda je nějaký uživatel přihlášen nebo ne)
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
            try:
                self.save()
            except:
                pass
        
#detekuje zda se kurzor ocitne na určitém objektu
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
                else: self.object = None
            
#Při kliknutí na uživatele nabídne dialogové okno pro přihlášení + vymaže objekt z "focusu"
    def on_button_press(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasx(event.y)
        if(self.user != None and self.logged == False):
            dialog = userDialog(self.parent, self.user)
            self.parent.wait_window(dialog.top)
            self.redraw_canvas()
        else:
            self.object = None

#Nabidne menu pro praci se soubory (objekty -> složky, soubory txt)
    def right_button_press(self, event):
        for f in self.objects:
            if f.detect_cursor(self.point): 
                self.object = f
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasx(event.y)
        if self.logged == True:
            if self.object == None:
                self.menu.post(event.x_root, event.y_root)
            else:
                self.edit.post(event.x_root, event.y_root)

#Vytvoří objekt folder -> složku
    def create_folder(self):
        self.object = folder(self.x, self.y)
        self.objects.append(self.object)
        createname = objectDialog(self.parent,self.object)
        self.parent.wait_window(createname.top)
        if(self.object.name == ""):
            self.objects.pop(-1)
        self.object = None

#Vytvoří objekt filetxt -> soubor txt
    def create_file(self):
        self.object = filetxt(self.x, self.y)
        self.objects.append(self.object)
        createname = objectDialog(self.parent,self.object)
        self.parent.wait_window(createname.top)
        if(self.object.name == ""):
            self.objects.pop(-1)
        self.object = None

#Zajišťuje přesouvání objektů
    def on_move_press(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasy(event.y)
        for f in self.objects:
            if f.detect_cursor(self.point): 
                self.object = f
        if self.object:
            self.object.x = self.x if self.x <= self.screen_width else self.screen_width
            self.object.y = self.y if self.y <= self.screen_height else self.screen_height

#Zajišťuje mazání objektů
    def delete(self):
        i = 0
        for f in self.objects:
            if f == self.object:
                self.objects.pop(i)
            i += 1
        self.object = None
        self.redraw_canvas()

#Zajišťuje přejmenování objektů
    def rename(self):
        changename = objectDialog(self.parent,self.object)
        self.parent.wait_window(changename.top)
        self.redraw_canvas()
        pass

#Zajišťuje otevření objektů
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
#Nekonečný loop, který zajišťuje neustálé překreslování canvasu + updatuje okno
while True:
    if(myapp.logged != False):
        myapp.redraw_canvas()
    root.update()
    pass
root.mainloop()
