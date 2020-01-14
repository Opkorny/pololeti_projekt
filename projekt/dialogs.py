from tkinter import *


class userDialog:
    def __init__(self, parent, user):
        self.user = user
        top = self.top = Toplevel(parent)
        top.title("Přihlášení uživatele")
        top.transient(parent)
        top.grab_set()
        top.focus_set()
        x = parent.winfo_x()
        y = parent.winfo_y()
        top.geometry("%dx%d+%d+%d" % (200, 130, 850, 500))
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
