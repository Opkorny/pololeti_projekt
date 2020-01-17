from tkinter import *
import subprocess

class userDialog:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        top = self.top = Toplevel(parent)
        top.title("Přihlášení uživatele")
        top.transient(parent)
        top.grab_set()
        top.focus_set()
        top.geometry("%dx%d+%d+%d" % (200, 130, self.parent.winfo_screenwidth()/2-100, self.parent.winfo_screenheight()/2-65))
        container = Frame(top, width = 200, pady=10, padx=10)
        self.label = Label(container, text="Uživatel - %s" % self.user.name)
        self.label.pack(side=LEFT)
        container.pack(fill=BOTH)
        container1 = Frame(top, width = 200, pady=10, padx=10)
        self.label = Label(container1, text="Heslo:")
        self.label.pack(side=LEFT)
        self.e = Entry(container1)
        self.e.pack(side=RIGHT)
        container1.pack(fill=BOTH)

        button_ok = Button(top, text="OK", command=self.ok)
        button_ok.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)
        button_cancel = Button(top, text="Cancel", command=self.cancel)
        button_cancel.pack(side=RIGHT, padx=10, pady=10, fill=BOTH, expand=True)

    def ok(self, event=None):
        if self.e.get() == self.user.password:
            self.user.logged = True
        self.top.destroy()

    def cancel(self, event=None):
        self.top.destroy()


class startDialog:
    def __init__(self, parent, user):
        self.user = user
        self.parent = parent
        top = self.top = Toplevel(parent)
        top.title("")
        #top.attributes("-disabled", 1)
        top.protocol('WM_DELETE_WINDOW',1)
        top.deiconify()
        top.transient(parent)
        top.grab_set_global()
        top.focus_set()
        top.geometry("%dx%d+%d+%d" % (150, self.parent.winfo_screenheight(),-10, -40))

        button_reboot = Button(top, text="  Reboot  ", command=self.reboot)
        button_reboot.pack(side=BOTTOM, padx=10, pady=10, fill=BOTH)
        button_poweroff = Button(top, text=" Poweroff ", command=self.poweroff)
        button_poweroff.pack(side=BOTTOM, padx=10, pady=10, fill=BOTH)
        button_logout = Button(top, text="  Logout  ", command=self.logout)
        button_logout.pack(side=BOTTOM, padx=10, pady=10, fill=BOTH)
        self.top.bind("<ButtonPress-1>", self.destroy)
        
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