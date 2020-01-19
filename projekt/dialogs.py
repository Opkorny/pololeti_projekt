from tkinter import *
from objects import *
import subprocess


class userDialog:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        v = StringVar()
        v.set("ahoj")
        top = self.top = Toplevel(parent)
        top.title("User log in")
        top.transient(parent)
        top.grab_set()
        top.focus_set()
        top.geometry("%dx%d+%d+%d" % (200, 130, self.parent.winfo_screenwidth() /
                                      2-100, self.parent.winfo_screenheight()/2-65))
        container = Frame(top, width=200, pady=10, padx=10)
        self.label = Label(container, text="User - %s" % self.user.name)
        self.label.pack(side=LEFT)
        container.pack(fill=BOTH)
        container1 = Frame(top, width=200, pady=10, padx=10)
        self.label = Label(container1, text="Password:")
        self.label.pack(side=LEFT)
        self.e = Entry(container1)
        self.e.pack(side=RIGHT)
        container1.pack(fill=BOTH)

        button_ok = Button(top, text="OK", command=self.ok)
        button_ok.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)
        button_cancel = Button(top, text="Cancel", command=self.cancel)
        button_cancel.pack(side=RIGHT, padx=10, pady=10,
                           fill=BOTH, expand=True)
        self.top.bind("<Return>", self.ok)

    def ok(self, event=None):
        if self.e.get() == self.user.password:
            self.user.logged = True
            self.top.destroy()
        else:
            self.e.config({"background": "salmon"})

    def cancel(self, event=None):
        self.top.destroy()


class startDialog:
    def __init__(self, parent, user):
        self.user = user
        self.parent = parent
        top = self.top = Toplevel(parent)
        top.title("")
        #top.attributes("-disabled", 1)
        top.protocol('WM_DELETE_WINDOW', 1)
        top.deiconify()
        top.transient(parent)
        top.grab_set_global()
        top.focus_set()
        top.geometry("%dx%d+%d+%d" %
                     (150, self.parent.winfo_screenheight(), -10, -40))

        button_reboot = Button(top, text="  Reboot  ", command=self.reboot)
        button_reboot.pack(side=BOTTOM, padx=10, pady=10, fill=BOTH)
        button_poweroff = Button(top, text=" Poweroff ", command=self.poweroff)
        button_poweroff.pack(side=BOTTOM, padx=10, pady=10, fill=BOTH)
        button_logout = Button(top, text="  Logout  ", command=self.logout)
        button_logout.pack(side=BOTTOM, padx=10, pady=10, fill=BOTH)
        self.top.bind("<ButtonPress-1>", self.destroy)
        self.top.bind("<ButtonPress-3>", self.destroy)

    def poweroff(self, event=None):
        subprocess.call([r'.\poweroff.bat'])

    def reboot(self, event=None):
        subprocess.call([r'.\reboot.bat'])

    def logout(self, event=None):
        self.user.logged = False
        self.top.destroy()

    def destroy(self, event):
        if event.x > 150:
            self.top.destroy()
        pass


class objectDialog:
    def __init__(self, parent, folder):
        self.parent = parent
        self.folder = folder
        top = self.top = Toplevel(parent)
        top.title("Creating name")
        top.transient(parent)
        top.grab_set_global()
        top.focus_set()
        top.geometry("%dx%d+%d+%d" % (150, 80, self.parent.winfo_screenwidth() /
                                      2-100, self.parent.winfo_screenheight()/2-65))
        container = Frame(top, width=200, pady=10, padx=10)
        container.pack(fill=BOTH)
        container1 = Frame(top, width=200, pady=10, padx=10)
        self.label = Label(container1, text="Name:")
        self.label.pack(side=LEFT)
        self.e = Entry(container1)
        self.e.pack(side=RIGHT)
        container1.pack(fill=BOTH)

        button_ok = Button(top, text="OK", command=self.ok)
        button_ok.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)
        button_cancel = Button(top, text="Cancel", command=self.cancel)
        button_cancel.pack(side=RIGHT, padx=10, pady=10,
                           fill=BOTH, expand=True)
        self.top.bind("<Return>", self.ok)

    def ok(self, event=None):
        self.folder.name = self.e.get()
        self.top.destroy()

    def cancel(self, event=None):
        if self.folder.name == None:
            self.folder.name = ""
        else:
            self.folder.name = self.folder.name
        self.top.destroy()


class openfile:
    def __init__(self, parent, file):
        self.parent = parent
        self.file = file
        self.screen_width = self.parent.winfo_screenwidth()/2
        self.screen_height = self.parent.winfo_screenheight()-50
        top = self.top = Toplevel(parent)
        top.title(self.file.name)
        top.transient(parent)
        top.grab_set_global()
        top.focus_set()
        top.geometry("%dx%d+%d+%d" % (self.screen_width, self.screen_height, self.screen_width/2, 0))
        container = Frame(top, width=self.screen_width)
        yscroll = Scrollbar(container)
        yscroll.pack(side=RIGHT, fill=Y)
        xscroll = Scrollbar(container, orient=HORIZONTAL)
        xscroll.pack(side=BOTTOM, fill=X)
        self.e = Text(container, width=int(self.screen_width), height=45, wrap=NONE, yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.e.insert(1.0, self.file.text)
        self.e.pack(side=RIGHT, ipady=20)
        container.pack(side=TOP, fill=BOTH)
        yscroll.config(command=self.e.yview)
        xscroll.config(command=self.e.xview)

        container1 = Frame(
            top, width=self.parent.winfo_screenwidth()/2, height=40)
        button_ok = Button(container1, text="Save", command=self.ok)
        button_ok.pack(side=LEFT, padx=5, pady=5, fill=BOTH, expand=True)
        button_cancel = Button(container1, text="Storno", command=self.cancel)
        button_cancel.pack(side=RIGHT, padx=5, pady=5, fill=BOTH, expand=True)
        container1.pack(side=BOTTOM, fill=BOTH)

    def ok(self, event=None):
        self.file.text = self.e.get(1.0, END)
        self.top.destroy()

    def cancel(self, event=None):
        self.top.destroy()


class openfolder:
    def __init__(self, parent, folder):
        self.parent = parent
        self.folder = folder
        self.object = None
        self.screen_width = self.parent.winfo_screenwidth()/2
        self.screen_height = self.parent.winfo_screenheight()-50
        top = self.top = Toplevel(parent)
        top.title(self.folder.name)
        top.transient(parent)
        top.grab_set()
        top.focus_set()
        top.geometry("%dx%d+%d+%d" % (self.screen_width, self.screen_height, self.screen_width/2, 0))
        self.menu = Menu(top, tearoff=0)
        createmenu = Menu(self.menu)
        self.menu.add_cascade(label='Nový...  ', menu=createmenu)
        createmenu.add_command(label='Složka', command=self.create_folder)
        createmenu.add_command(label='Soubor', command=self.create_file)
        self.edit = Menu(top, tearoff=0)
        self.edit.add_command(label='Otevřít', command=self.open_f)
        self.edit.add_command(label='Odstranit', command=self.delete)
        self.edit.add_command(label='Přejmenovat', command=self.rename)

        container = Frame(top, width=self.screen_width)
        self.c = Canvas(self.top, width=self.screen_width, height=self.screen_height-50, bg='azure')
        self.c.pack(fill=BOTH, expand=True)
        container.pack(side=TOP, fill=BOTH)

        container1 = Frame( top, width=self.screen_width, height=40)
        button_ok = Button(container1, text="Save", command=self.ok)
        button_ok.pack(side=LEFT, padx=5, pady=5, fill=BOTH, expand=True)
        button_cancel = Button(container1, text="Storno", command=self.cancel)
        button_cancel.pack(side=RIGHT, padx=5, pady=5, fill=BOTH, expand=True)
        container1.pack(side=BOTTOM, fill=BOTH)
        self.c.bind("<Motion>", self.on_mouse_move)
        self.c.bind("<ButtonRelease-3>", self.on_button_release)
        self.c.bind("<ButtonPress-1>", self.on_button_press)
        self.c.bind("<B1-Motion>", self.on_move_press)
        self.redraw_canvas()

    
    def clear_canvas(self):
        self.c.delete("all")

    def redraw_canvas(self):   
        self.clear_canvas()
        for f in self.folder.objects:
            f.draw(self.c) 

    def on_move_press(self, event):
        self.x = self.c.canvasx(event.x)
        self.y = self.c.canvasy(event.y)
        for f in self.folder.objects:
            if f.detect_cursor(self.point): 
                self.object = f
        if self.object:
            self.object.x = self.x if self.x <= self.screen_width else self.screen_width
            self.object.y = self.y if self.y <= self.screen_height-50 else self.screen_height-50
        self.redraw_canvas()

    def on_button_press(self, event):
        self.x = self.c.canvasx(event.x)
        self.y = self.c.canvasx(event.y)
        self.object = None
    
    def on_mouse_move(self, event):
        self.x = self.c.canvasx(event.x)
        self.y = self.c.canvasx(event.y)
        self.point = Point(self.x, self.y)
        for f in self.folder.objects:
            if f.detect_cursor(self.point): 
                self.object = f
        self.redraw_canvas()

    def on_button_release(self, event):
        self.x = self.c.canvasx(event.x)
        self.y = self.c.canvasx(event.y)
        if self.object == None:
            self.menu.post(event.x_root, event.y_root)
        else:
            self.edit.post(event.x_root, event.y_root)
        self.redraw_canvas()
        pass

    def create_folder(self):
        self.object = folder(self.x, self.y)
        self.folder.objects.append(self.object)
        createname = objectDialog(self.parent,self.object)
        self.parent.wait_window(createname.top)
        if(self.object.name == ""):
            self.folder.objects.pop(-1)
        self.redraw_canvas()

    def create_file(self):
        self.object = filetxt(self.x, self.y)
        self.folder.objects.append(self.object)
        createname = objectDialog(self.parent,self.object)
        self.parent.wait_window(createname.top)
        if(self.object.name == ""):
            self.folder.objects.pop(-1)
        self.redraw_canvas()

    def delete(self):
        i = 0
        for f in self.folder.objects:
            if f == self.object:
                self.folder.objects.pop(i)
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

    def ok(self, event=None):
        self.top.destroy()

    def cancel(self, event=None):
        self.top.destroy()
