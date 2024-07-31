"""Importing Modules"""
import sys
import datetime  # Select valid Date
import sqlite3 as sql  # Storing all data used
from tkinter import *  # For GUI Interface
from tkinter import ttk
from tkinter.messagebox import *

import matplotlib.pyplot as plt  # For Bar Graph and Pie Chart
import numpy as np  # For Bar Graph

base = '''A Python Based Money Tracking Program
in  which  you  can  manage  your  Income,
Expenses  and  can  add  your  savings  all
at one place.

Visualize Your Money with MoneyTrack
only at one click away'''


def on_exit(root):
    alpha = root.attributes("-alpha")
    if alpha > 0.01:
        alpha -= .01
        root.attributes("-alpha", alpha)
        root.after(10, lambda: on_exit(root))
    else:
        root.destroy()
        exit()


def on_closing(b):
    """If user tries to Exit program"""
    if askyesno("Quit", "Do you want to exit?"):
        on_exit(b)


def start(query):
    """For every time the Database is used it requires connection"""
    con = sql.connect("DO_NOT_DELETE.db")
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    t = cur.fetchall()
    return t


def start_screen(a):
    """Front Screen or About Screen"""
    screen = Tk()
    screen.resizable(False, False)
    screen.geometry('515x535+250+80')
    screen.title('Welcome To MoneyTrack')
    screen.config(bg='lemon chiffon', highlightthickness='3')
    screen.iconbitmap('\\images_used\\MoneyTrack.ico')

    Label(screen, text='Welcome to MoneyTrack', font=('Calibri', '30', 'bold', 'underline'),
          background='lemon chiffon', foreground='red').place(x=45, y=20)
    ttk.Label(screen, text=base, font=('Calibri', '18'), background='lemon chiffon',
              foreground='dark blue').place(x=50, y=85)

    canvas = Canvas(screen, width=400, height=110, highlightbackground="red",
                    highlightthicknes=1, bg='lemon chiffon')
    canvas.place(x=245, y=375, anchor='center')
    canvas.create_text(200, 20, fill="tomato", font="Times 16",
                       text='''Note: We care for your privacy!''')
    canvas.create_text(200, 65, fill="dark violet", font="Times 14 italic",
                       text='''To ensure this, MoneyTrack is
                               Offline and Password Protected''')
    if a == 1:
        chk = Checkbutton(screen, text="Always show this window on start", font='Calibri 12',
                          fg="#120000", activebackground='lemon chiffon',
                          onvalue=True, offvalue=False, bg='lemon chiffon')
        chk.var = BooleanVar()
        chk['variable'] = chk.var
        chk.place(x=45, y=450)

        canvas2 = Canvas(width=130, height=42, bg='lemon chiffon', highlightthickness=0)
        canvas2.place(x=335, y=465)
        # img = PhotoImage(file="images_used\\signature.png")
        # canvas2.create_image(70, 26, image=img)

        def check():
            if chk.var.get() is False:
                start("insert into show values(1)")
            screen.destroy()

        ttk.Button(screen, text='Next>', command=check).place(x=379, y=420)
    elif a == 0:
        ttk.Button(screen, text='Ok', command=screen.destroy).place(x=379, y=420)
    screen.mainloop()


def password():
    """Password is required to open the Program"""

    def on_enter(*_arg):
        """ On entering the Password (either correct or wrong)"""
        if root.PasswordTries <= 2:
            p = entry.get()  # get password from entry
            if p == 'rickroll':
                root.destroy()
            if root.PasswordTries >= 0:
                # noinspection PyBroadException
                try:
                    Label(root, text='The Password entered by you is wrong!',
                          bg='light cyan', fg='red').place(x=44, y=70)
                    Label(root, text='Try Again! You have {0} more attempt(s) left.'.format(3 - root.PasswordTries),
                          bg='light cyan', fg='red').place(x=37, y=90)
                    entry.delete(0, END)
                except Exception:
                    pass
            root.PasswordTries += 1
        else:
            showerror('Unknown User', "Sorry! we can't give you access to the program")
            sys.exit()

    def hide_password():
        """This will keep password hidden till not clicked"""
        if checkbutton.var.get():
            entry['show'] = "*"
        else:
            entry['show'] = ""

    root = Tk()
    root.configure(background='light cyan')
    root.geometry('300x200+350+220')
    root.title("Enter your password")
    root.resizable(False, False)
    root.iconbitmap('images_used\\lock.ico')
    root.focus_force()
    root.PasswordTries = 0

    Label(root, text='Password :', bg='light cyan').place(x=50, y=25)

    entry = Entry(root)
    entry.bind("<Return>", on_enter)
    entry.default_show_val = entry['show']
    entry.place(x=115, y=27)
    entry['show'] = "*"
    entry.focus()

    checkbutton = Checkbutton(root, text="Hide password", onvalue=True, offvalue=False,
                              bg='light cyan', activebackground='light cyan',
                              command=hide_password)
    checkbutton.var = BooleanVar(value=True)
    checkbutton['variable'] = checkbutton.var
    checkbutton.place(x=120, y=49)

    Button(root, height='1', width='10', text='Enter', bg='light blue1',
           font=('helvetica', '12', 'bold'), activebackground='Steelblue1',
           command=on_enter).place(x=98, y=130)

    canvas = Canvas(root, width=30, height=30, bg='light cyan', highlightthickness=0)
    canvas.place(x=23, y=25)
    img = PhotoImage(file="images_used\\lock_image.png")
    canvas.create_image(10, 11, image=img)

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    mainloop()


def notepad():
    start("create table If not exists note(notes varchar(256))")
    root = Tk()
    root.geometry('305x410')
    root.minsize(300, 200)
    root.title('Notepad')
    root.iconbitmap('images_used\\notepad.ico')

    def get_text_input():
        start("delete from note")
        start("insert into note values('{0}')".format(text1.get('1.0', 'end-1c')))
        root.destroy()

    text1 = Text(root, height=25, width=35)
    try:
        text1.insert(END, start("select * from note")[0][0])
    except IndexError:
        pass
    text1.focus()
    scroll = Scrollbar(root, command=text1.yview)
    text1.configure(yscrollcommand=scroll.set)
    text1.pack(side=LEFT, expand=True, fill=BOTH)
    scroll.pack(side=RIGHT, fill=Y)
    root.focus_force()

    root.protocol("WM_DELETE_WINDOW", get_text_input)
    root.mainloop()


def calculator():
    def frame():
        frm = Frame(root, borderwidth=4, bd=1, bg="light cyan")
        frm.pack(side=TOP, expand=YES, fill=BOTH)
        return frm

    def button(source, text, command=None):
        btn = Button(source, text=text, font='arial 20 bold', command=command)
        btn.pack(side=LEFT, expand=YES, fill=BOTH)
        return btn

    root = Tk()
    root.iconbitmap('images_used\\calculator.ico')
    cal = Frame(root)
    cal.pack()
    cal.master.title('Calculator')
    cal.master.geometry('300x500')

    display = Entry(cal, relief=RIDGE, font='arial 20 bold',
                    justify='right', bd=25, bg="#d1e2e3")
    display.pack(side=TOP)

    button(frame(), "C", lambda: display.delete(0, END))

    for numButton in ("789/", "456*", "123-", "0.+"):
        FunctionNum = frame()
        for iEquals in numButton:
            button(FunctionNum, iEquals, lambda q=iEquals: display.insert(END, q))

    def calc(dis):
        try:
            a = eval(dis.get())
            display.delete(0, END)
            display.insert(0, a)
        except (ZeroDivisionError, NameError, ValueError, SyntaxError):
            dis.delete(0, END)
            dis.insert(0, "ERROR")

    button(frame(), '=', command=lambda: calc(display))
    mainloop()


def get_total(query):
    """To get the total amount as per table"""
    con = sql.connect("DO_NOT_DELETE.db")
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()[0][0]


def valid_date(var, rely):
    Label(text='Date :', font='Calibri 40', bg='light cyan').place(relx=0.29, rely=rely, anchor=W)

    def focusin_date(_):
        if var.get() == 'In DD-MM-YYYY format':
            var.delete(0, "end")  # delete all the text in the entry
            var.config(fg='black')

    def focusout_date(_):
        if var.get() == '':
            var.insert(0, 'In DD-MM-YYYY format')
            var.config(fg='grey')

    var.insert(0, 'In DD-MM-YYYY format')
    var.bind('<FocusIn>', focusin_date)
    var.bind('<FocusOut>', focusout_date)
    var.config(fg='grey')
    var.place(relx=0.54, rely=rely, anchor=W)


def valid_amt(master, var, relx, rely, text, size):
    def check(p):
        tex = p
        parts = tex.split('.')
        parts_number = len(parts)

        if parts_number > 2:
            return False

        if parts_number > 1 and parts[1]:  # don't check empty string
            if not parts[1].isdecimal() or len(parts[1]) > 2:
                return False

        if parts_number > 0 and parts[0]:  # don't check empty string
            if not parts[0].isdecimal() or len(parts[0]) > 8:
                return False

        return True

    vcd = (master.register(check), '%P')

    def focusin_amt(_):
        if var.get() == 'In Rs.':
            var.delete(0, "end")  # delete all the text in the entry
            var.config(fg='black')

    Label(text=text, font='Calibri {0}'.format(size), bg='light cyan').place(relx=relx, rely=rely, anchor=W)
    var.insert(0, 'In Rs.')
    var.bind('<FocusIn>', focusin_amt)
    var.config(fg='grey')
    var.place(relx=0.54, rely=rely, anchor=W)
    var.config(validate='key', validatecommand=vcd)


def valid_desc(master, var, relx, rely, text, text2, relx2):
    Label(master, text=text2, font='Calibri 40', bg='light cyan').place(relx=relx2, rely=rely, anchor=W)

    def focusin_desc(_):
        if var.get() == text:
            var.delete(0, "end")
            var.config(fg='black')

    def focusout_desc(_):
        if var.get() == '':
            var.insert(0, text)
            var.config(fg='grey')

    var.insert(0, text)
    var.bind('<FocusIn>', focusin_desc)
    var.bind('<FocusOut>', focusout_desc)
    var.config(fg='grey')
    var.place(relx=(relx + 0.42), rely=(rely + 0.01), anchor=W)


def pie_exp():
    nonzero_amt, nonzero_cat, amt_cat, size = [], [], [], []
    for category in list_category:
        amt_cat.append(start('select sum(amount) from expense where category = "{0}"'.format(category))[0][0])

    for i in range(len(amt_cat)):
        if amt_cat[i] is not None:
            nonzero_cat.append(list_category[i])
            nonzero_amt.append(amt_cat[i])

    for i in range(len(nonzero_amt)):
        size.append(nonzero_amt[i] / (start('select sum(amount) from expense')[0][0]))

    plt.figure("Expense- Pie Chart")
    plt.pie(size, labels=nonzero_cat, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.show()


def exp_bar():
    amt_cat = []
    for category in list_category:
        amt_cat.append(start('select sum(amount) from expense where category = "{0}"'.format(category))[0][0])
    for n, i in enumerate(amt_cat):
        if i is None:
            amt_cat[n] = 0
    plt.figure("Expense- Bar Graph")
    y_pos = np.arange(len(list_category))
    plt.bar(y_pos, amt_cat, alpha=0.5)
    plt.xticks(y_pos, list_category)
    plt.ylabel('Amount')
    plt.show()


def show_all(place, frame2, command, typed, wid1, wid2, wid3, height, command2=None):
    frame = Frame()
    frame.place(rely=0.5, relx=0.5, anchor=CENTER)

    def scroll(*args):
        listbox.yview(*args)
        listbox2.yview(*args)
        listbox3.yview(*args)
        if var_show_all == 'b':
            listbox4.yview(*args)

    listbox = Listbox(frame, width=wid1, height=height, font=("Helvetica", 18))
    listbox.pack(side="left", fill="y")

    listbox2 = Listbox(frame, width=wid2, height=height, font=("Helvetica", 18))
    listbox2.pack(side="left", fill="y")

    listbox3 = Listbox(frame, width=wid3, height=height, font=("Helvetica", 18))
    listbox3.pack(side="left", fill="y")

    scrollbar = Scrollbar(frame, command=scroll)
    scrollbar.pack(side="right", fill="y")

    lst = []
    con = sql.connect("DO_NOT_DELETE.db")
    cur = con.cursor()
    cur.execute("select * from {0}".format(typed))
    con.commit()
    t = cur.fetchall()
    for row in t:
        lst.append(row)

    total_row = len(lst)

    if var_show_all == 'b':
        listbox4 = Listbox(frame, width=20, height=10, font=("Helvetica", 18))
        listbox4.pack(side="left", fill="y")
        listbox4.config(yscrollcommand=scrollbar.set)
        for j in range(total_row):
            listbox4.insert(END, lst[j][3])

    listbox.config(yscrollcommand=scrollbar.set)
    listbox2.config(yscrollcommand=scrollbar.set)
    listbox3.config(yscrollcommand=scrollbar.set)

    for j in range(total_row):
        listbox.insert(END, lst[j][0])
    for j in range(total_row):
        listbox2.insert(END, lst[j][1])
    for j in range(total_row):
        listbox3.insert(END, lst[j][2])

    # noinspection PyUnboundLocalVariable

    def get_var():
        if listbox.curselection():
            clicked_items = listbox.curselection()
        elif listbox2.curselection():
            clicked_items = listbox2.curselection()
        elif var_show_all == 'b':
            clicked_items = listbox4.curselection()
        else:
            clicked_items = listbox3.curselection()

        for item in clicked_items:
            w = listbox.get(item)
            x = listbox2.get(item)
            y = listbox3.get(item)
            if var_show_all == 'b':
                z = listbox4.get(item)
        if var_show_all in ('a', 'c'):
            return w, x, y
        elif var_show_all == 'b':
            return w, x, y, z

    def delete_txn():
        def delete_inc():
            try:
                if var_show_all == 'b':
                    w, x, y, z = get_var()
                    start('delete from expense where c_date = "{0}" and '
                          'amount = {1} and category = "{2}" and desc = "{3}"'.format(w, x, y, z))
                elif var_show_all == 'a':
                    w, x, y = get_var()
                    start('delete from income where c_date = "{0}" and amount = {1} and desc = "{2}"'.format(w, x, y))
                place.master.switch_frame(command2)
            except NameError:
                lbl = Label(text='Please select respective data to delete row.',
                            fg='red', bg='light cyan', font='24')
                lbl.place(rely=0.75, relx=0.5, anchor=CENTER)
                lbl.after(4000, lbl.place_forget)

        def callback():
            if askyesno('Clear All', 'Are you sure you want to Delete all the Transactions?'):
                start('delete from {0}'.format(typed))
            place.master.switch_frame(command2)

        Button(text='Delete Transaction', height=1, width=15, font='Helvetica 14 bold', fg='brown', bg='white',
               cursor='hand2', command=delete_inc).place(rely=0.85, relx=0.5, anchor=CENTER)
        Button(place, text='+ Add', height=1, width=12, font='Helvetica 14 bold', fg='blue', bg='white',
               cursor='hand2', command=lambda: frame2.switch_frame(command)).place(rely=0.85, relx=0.2, anchor=CENTER)
        Button(text='Clear All', height=1, width=12, font='Helvetica 14 bold', fg='red', bg='white', cursor='hand2',
               command=callback).place(rely=0.85, relx=0.8, anchor=CENTER)

    if var_show_all in ('a', 'b'):
        delete_txn()
    elif var_show_all == 'c':
        amount = Entry(width=20, font=('Arial', 16))
        valid_amt(frame2, amount, 0.2, 0.7, 'Amount :', 28)

        def add_sav():
            if amount.get() in ('In Rs.', ''):
                lbl = Label(text='Please enter a Savings amount', font='24', fg='red', bg='light cyan')
                lbl.place(relx=0.5, rely=0.75, anchor=CENTER)
                lbl.after(4000, lbl.place_forget)
            else:
                try:
                    w, x, y = get_var()
                    if askyesno('Add a saving', 'Are you sure want to add Rs.{} for {}?'.
                                format(float(amount.get()), w)):
                        start('update saving set c_amount = (c_amount+{0})'
                              'where title = "{1}" and target = {2} and c_amount = {3}'.
                              format(float(amount.get()), w, x, y))
                        showinfo('Add success', 'Rs.{} has been added successfully for {}'.
                                 format(float(amount.get()), w))
                        place.master.switch_frame(command2)
                except NameError:
                    lbl = Label(text='Please select data of respective row', font='24', fg='red', bg='light cyan')
                    lbl.place(relx=0.5, rely=0.75, anchor=CENTER)
                    lbl.after(4000, lbl.place_forget)

        def del_sav():
            try:
                w, x, y = get_var()
                if askyesno('Remove saving', 'Do you really want to remove saving for {}?'.
                            format(w)):
                    start('delete from saving where title = "{0}" and target = {1} and c_amount = {2}'.
                          format(w, x, y))
                    showinfo('Remove success', 'Saving for {} has been removed successfully'.
                             format(w))
                    place.master.switch_frame(command2)
            except NameError:
                lbl = Label(text='Please select data of respective row', font='24', fg='red', bg='light cyan')
                lbl.place(relx=0.5, rely=0.75, anchor=CENTER)
                lbl.after(4000, lbl.place_forget)

        Button(text='Add Savings', command=add_sav, height=1, width=12, fg='blue',
               bg='#ffff14', font=('Calibri', '20', 'bold')).place(anchor=CENTER, rely=0.85, relx=0.5)
        Button(text='Remove Saving', command=del_sav, height=1, width=14, fg='red',
               bg='#ffff14', font=('Calibri', '20', 'bold')).place(anchor=CENTER, rely=0.85, relx=0.8)


def back_btn(place, frame, command):
    Button(place, text='<- Back', height=1, width=6, font=('Arial Rounded MT Bold', 11), cursor="hand2",
           bg='white', fg='black', relief=RAISED,
           command=lambda: frame.switch_frame(command)).place(relx=0.1, rely=0.05, anchor='n')


def balance_label(master, relx, rely):
    k = 0
    for i in (start('select sum(amount) from expense'),
              start('select sum(c_amount) from saving')):
        j = i[0][0]
        if j is None:
            j = 0.00
        k += j
    inc = start('select sum(amount) from income')[0][0]
    if inc is None:
        inc = 0.00
    bal = inc - k
    lbl = Label(master, text='Balance : Rs. {}'.format(bal), bg='light cyan', fg='blue',
                font=('Calibri', '25', 'bold'))
    lbl.place(relx=relx, rely=rely, anchor="e")
    if bal < 0:
        lbl.config(fg='red')


def table(master, text, fg, font):
    label = Label(master, text=text, width=14, fg=fg, relief=SOLID,
                  bg='light cyan', font=font, borderwidth=1)
    return label


def show_table(query, master=None):
    lst = []
    con = sql.connect("DO_NOT_DELETE.db")
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    t = cur.fetchall()
    for row in t:
        lst.append(row)
    if master is not None:
        total_row = len(lst)
        total_column = len(lst[0])
        for i in range(total_row):
            for j in range(total_column):
                e = table(master, lst[i][j], 'blue', ('Arial', 18))
                e.grid(row=i + 1, column=j, pady=1, padx=1)
    return lst


start("create table If not exists income(C_date date, amount float, desc varchar(20))")
start("create table if not exists expense(C_date date, amount float, category varchar(8), desc varchar(20))")
start("create table If not exists saving(title varchar(20), target float, c_amount float)")
start("create table if not exists show(yes_or_no binary)")
list_category = ['Food', 'Travel', 'Entertainment', 'Fuel', 'Health', 'Misc']
var_show_all = 'no value'
try:
    start("select * from show")
except IndexError:
    start_screen(1)
password()


class App(Tk):
    """tkinter App creation for main program, basic functions"""

    def __init__(self):
        Tk.__init__(self)
        self.geometry("710x500+160+110")  # Size of window
        self.minsize(720, 520)  # Minimum size possible for window
        self.state('zoomed')  # Window should be full screened at first
        self.iconbitmap('images_used\\MoneyTrack.ico')  # App logo
        self._frame = None  # No frame at start
        self.switch_frame(StartPage)  # Then change it to StartPAge
        menu = Menu(self)
        self.config(menu=menu)
        self.protocol("WM_DELETE_WINDOW", lambda: on_closing(self))

        filemenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Notepad", command=notepad)
        filemenu.add_command(label="Calculator", command=calculator)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=lambda: on_closing(self))

        helpmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=lambda: start_screen(0))

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(expand=True, fill=BOTH)


class StartPage(Frame):
    """Front Page of the program"""

    def __init__(self, master):
        master.title('MoneyTrack')  # Title of Window
        label_name = 'MoneyTrack'

        def typewriter_effect(counter=1):
            label.config(text=label_name[:counter])
            master.after(120, lambda: typewriter_effect(counter + 1))

        Frame.__init__(self, master, bg='light cyan')  # Frame Specification
        self.inc_photo = PhotoImage(file="images_used\\income.png")  # Image1 (Income)
        self.exp_photo = PhotoImage(file="images_used\\expense.png")  # Image2 (Expense)
        self.sav_photo = PhotoImage(file="images_used\\savings.png")  # Image3 (Saving)
        balance_label(self, 0.9, 0.4)
        label = Label(bg='light cyan', fg='red3', font=('Eras Bold ITC', '75', 'bold'))
        label.place(relx=0.5, rely=0.18, anchor="center")
        typewriter_effect()
        Button(self, height='182', width='188', bd=4, cursor='hand2', image=self.inc_photo,
               command=lambda: master.switch_frame(IncomeFront)).place(relx=0.2, rely=0.7, anchor="center")
        Button(self, height='182', width='188', bd=4, cursor='hand2', image=self.exp_photo,
               command=lambda: master.switch_frame(ExpenseFront)).place(relx=0.5, rely=0.7, anchor="center")
        Button(self, height='182', width='188', bd=4, cursor='hand2', image=self.sav_photo,
               command=lambda: master.switch_frame(SavingFront)).place(relx=0.8, rely=0.7, anchor="center")


class IncomeFront(Frame):
    def __init__(self, master):
        master.title('Income')
        inc_amt_ttl = get_total("select sum(amount) from income")
        if inc_amt_ttl is None:
            inc_amt_ttl = '0.00'

        Frame.__init__(self, master, bg='light cyan')
        back_btn(self, master, StartPage)
        balance_label(self, 0.9, 0.1)
        Label(self, text='Total Income : Rs. {0}'.format(inc_amt_ttl),
              font='Arial 35 bold', bg='light cyan', fg='red').place(relx=0.5, rely=0.22, anchor='center')
        Button(self, text='+ Add', height=1, width=8, font=('Arial Rounded MT Bold', 14, 'bold'),
               cursor="hand2", bg='white', fg='#4287f5', relief=RAISED,
               command=lambda: master.switch_frame(IncomeAdd)).place(relx=0.9, rely=0.34, anchor='e')
        Label(self, text="Recent Transactions :", bg='light cyan', fg='dark green',
              font=('Calibri', '26', 'bold')).place(relx=0.07, rely=0.39, anchor="w")

        frame2 = Frame(bg='light cyan')
        frame2.place(relx=0.43, rely=0.7, anchor=CENTER)

        try:
            show_table("select * from income order by c_date desc limit 7", frame2)
            table(frame2, 'Date', 'black', ('Arial', 17, 'bold')).grid(row=0, column=0, pady=1, padx=1)
            table(frame2, 'Amount', 'black', ('Arial', 17, 'bold')).grid(row=0, column=1, pady=1, padx=1)
            table(frame2, 'Description', 'black', ('Arial', 17, 'bold')).grid(row=0, column=2, pady=1, padx=1)

            show = Label(self, text='Show All', fg='#3399ff', bg='light cyan', font=('Calibri', '20', 'underline'),
                         cursor="hand2")
            show.place(x=140, relx=0.8, rely=0.87, anchor='e')

            show.bind("<Button-1>", lambda one: master.switch_frame(ShowIncome))

        except IndexError:
            Label(frame2, text='No Transactions Added Yet.', fg='red',
                  bg='light cyan', font=('Arial', 18)).grid()


class IncomeAdd(Frame):
    def __init__(self, master):
        master.title('Add Income')
        Frame.__init__(self, master, bg='light cyan')

        date = Entry(width=20, font=('Arial', 16))
        valid_date(date, 0.18)

        amount = Entry(width=20, font=('Arial', 16))
        valid_amt(master, amount, 0.2, 0.38, 'Amount :', 40)

        def limit_size_day(*_arg):
            value = dayValue.get()
            if len(value) > 20:
                dayValue.set(value[:20])

        dayValue = StringVar()
        dayValue.trace('w', limit_size_day)
        desc = Entry(width=20, font=('Arial', 16), textvariable=dayValue)
        valid_desc(master, desc, 0.12, 0.58, '(Optional)', 'Description :', 0.12)
        '''---------------------------------------------------'''

        def add_inc():
            try:
                try:
                    day, month, year = (date.get()).split('-')
                except ValueError:
                    day, month, year = (date.get()).split('/')
                datetime.datetime(int(year), int(month), int(day))
                date_inc = "{0}-{1}-{2}".format(day, month, year)
                if desc.get() == '(Optional)':
                    desc.delete(0, "end")
                try:
                    start("insert into income values('{0}',{1},'{2}')".
                          format(date_inc, float(amount.get()), desc.get()))
                    showinfo('Income added',
                             'Your income of Rs.{0} has been added successfully'.format(float(amount.get())))
                    master.switch_frame(IncomeAdd)
                except ValueError:
                    lbl = Label(text='Please enter your Income', font='24', fg='red', bg='light cyan')
                    lbl.place(relx=0.54, rely=0.45, anchor=W)
                    lbl.after(4000, lbl.place_forget)
            except ValueError:
                lbl = Label(text='Please enter a Valid Date', font='24', bg='light cyan', fg='red')
                lbl.place(relx=0.54, rely=0.25, anchor=W)
                lbl.after(4000, lbl.place_forget)

        Button(text='Add income', command=add_inc, height=1, width=12, fg='blue',
               bg='#ffff14', font=('Calibri', '20', 'bold')).place(anchor=CENTER, rely=0.8, relx=0.5)
        back_btn(self, master, IncomeFront)


class ShowIncome(Frame):
    def __init__(self, master):
        master.title('All Income')
        global var_show_all
        var_show_all = 'a'
        Frame.__init__(self, master, bg='light cyan')
        Label(self, text="My Income", bg='light cyan', fg='orange',
              font='Calibri 40 bold').place(rely=0.08, relx=0.5, anchor=CENTER)
        back_btn(self, master, IncomeFront)
        show_all(self, master, IncomeAdd, 'income', 16, 16, 20, 10, ShowIncome)


class ExpenseFront(Frame):
    def __init__(self, master):
        master.title('Expenses')
        exp_amt_ttl = get_total("select sum(amount) from expense")
        if exp_amt_ttl is None:
            exp_amt_ttl = '0.00'

        Frame.__init__(self, master, bg='light cyan')
        back_btn(self, master, StartPage)
        balance_label(self, 0.9, 0.1)
        Label(self, text='Total Expense : Rs. {0}'.format(exp_amt_ttl),
              font='Arial 35 bold', bg='light cyan', fg='red').place(relx=0.5, rely=0.22, anchor='center')
        Button(self, text='+ Add', height=1, width=8, font=('Arial Rounded MT Bold', 14, 'bold'),
               cursor="hand2", bg='white', fg='#4287f5', relief=RAISED,
               command=lambda: master.switch_frame(ExpenseAdd)).place(relx=0.9, rely=0.34, anchor='e')
        Button(self, text='Show Transaction', height=1, width=20, font=('Helvetica', 20, 'bold'),
               cursor="hand2", bg='white', fg='Brown', relief=RAISED,
               command=lambda: master.switch_frame(ShowExpense)).place(relx=0.5, rely=0.8, anchor=CENTER)
        Button(self, text='Pie Chart', height=4, width=9, font=('Helvetica', 20, 'bold'), command=pie_exp,
               cursor="hand2", bg='white', fg='Green', relief=RAISED).place(relx=0.35, rely=0.55, anchor=CENTER)
        Button(self, text='Bar Graph', height=4, width=9, font=('Helvetica', 20, 'bold'), command=exp_bar,
               cursor="hand2", bg='white', fg='Green', relief=RAISED).place(relx=0.65, rely=0.55, anchor=CENTER)


class ExpenseAdd(Frame):
    def __init__(self, master):
        master.title('Add Expense')
        Frame.__init__(self, master, bg='light cyan')
        back_btn(self, master, ExpenseFront)
        date2 = Entry(width=20, font=('Arial', 16))
        valid_date(date2, 0.12)
        amount2 = Entry(width=20, font=('Arial', 16))
        valid_amt(master, amount2, 0.2, 0.45, 'Amount :', 40)

        def limit_size_day(*_arg):
            value = dayValue.get()
            if len(value) > 20:
                dayValue.set(value[:20])

        dayValue = StringVar()
        dayValue.trace('w', limit_size_day)
        desc2 = Entry(width=20, font=('Arial', 16), textvariable=dayValue)
        valid_desc(master, desc2, 0.12, 0.63, '(Optional)', 'Description :', 0.12)

        Label(text='Category :', font='Calibri 40', bg='light cyan').place(relx=0.17, rely=0.28, anchor=W)
        combo = ttk.Combobox(width=19, font=('Arial', 16))
        combo['values'] = ('Food', 'Travel', 'Entertainment', 'Fuel', 'Health', 'Misc', "Select Category")
        combo.current(6)
        combo.place(anchor=W, rely=0.28, relx=0.54)

        def add_exp():
            try:
                try:
                    day, month, year = (date2.get()).split('-')
                except ValueError:
                    day, month, year = (date2.get()).split('/')
                datetime.datetime(int(year), int(month), int(day))
                date_inc = "{0}-{1}-{2}".format(day, month, year)
                if combo.get() == 'Select Category':
                    lbl = Label(text='Please select a Category', font='24', bg='light cyan', fg='red')
                    lbl.place(relx=0.54, rely=0.35, anchor=W)
                    lbl.after(4000, lbl.place_forget)
                else:
                    if desc2.get() == '(Optional)':
                        desc2.delete(0, "end")
                    try:
                        start("insert into expense values('{0}',{1},'{2}','{3}')".
                              format(date_inc, float(amount2.get()), combo.get(), desc2.get()))
                        showinfo('Transaction added', 'Your transaction of Rs.{0} has been added successfully'.
                                 format(float(amount2.get())))
                        master.switch_frame(ExpenseAdd)

                    except ValueError:
                        lbl = Label(text='Please enter your Amount', font='24', fg='red', bg='light cyan')
                        lbl.place(relx=0.54, rely=0.5, anchor=W)
                        lbl.after(4000, lbl.place_forget)
            except ValueError:
                lbl = Label(text='Please enter a Valid Date', font='24', bg='light cyan', fg='red')
                lbl.place(relx=0.54, rely=0.18, anchor=W)
                lbl.after(4000, lbl.place_forget)

        Button(text='Add Transaction', command=add_exp, height=1, width=14, fg='blue',
               bg='#ffff14', font=('Calibri', '20', 'bold')).place(anchor=CENTER, rely=0.8, relx=0.5)


class ShowExpense(Frame):
    def __init__(self, master):
        master.title('All Expense')
        global var_show_all
        var_show_all = 'b'
        Frame.__init__(self, master, bg='light cyan')
        Label(self, text="My Expenses", bg='light cyan', fg='orange',
              font='Calibri 40 bold').place(rely=0.08, relx=0.5, anchor=CENTER)
        back_btn(self, master, ExpenseFront)
        show_all(self, master, ExpenseAdd, 'expense', 10, 10, 13, 10, ShowExpense)


class SavingFront(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg='light cyan')
        back_btn(self, master, StartPage)
        balance_label(self, 0.9, 0.1)
        Button(self, text='+ Add/ Delete', height=2, width=12, font=('Arial Rounded MT Bold', 20, 'bold'),
               cursor="hand2", bg='white', fg='red', relief=RAISED,
               command=lambda: master.switch_frame(SavingAdd)).place(relx=0.8, rely=0.3, anchor='e')
        Button(self, text='Create', height=2, width=12, font=('Arial Rounded MT Bold', 20, 'bold'),
               cursor="hand2", bg='white', fg='red', relief=RAISED,
               command=lambda: master.switch_frame(SavingCreate)).place(relx=0.4, rely=0.3, anchor='e')
        Label(self, text="Active Savings :", bg='light cyan', fg='dark green',
              font=('Calibri', '26', 'bold')).place(relx=0.2, rely=0.5, anchor="w")
        frame2 = Frame(bg='light cyan')
        frame2.place(relx=0.5, rely=0.76, anchor=CENTER)

        try:
            show_table('select * from saving', frame2)
            table(frame2, 'Title', 'black', ('Arial', 17, 'bold')).grid(row=0, column=0, pady=1, padx=1)
            table(frame2, 'Amount', 'black', ('Arial', 17, 'bold')).grid(row=0, column=1, pady=1, padx=1)
            table(frame2, 'Current Amount', 'black', ('Arial', 17, 'bold')).grid(row=0, column=2, pady=1, padx=1)
        except IndexError:
            Label(frame2, text='No Savings Created Yet.', fg='red',
                  bg='light cyan', font=('Arial', 18)).grid()


class SavingCreate(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg='light cyan')
        back_btn(self, master, SavingFront)
        balance_label(self, 0.9, 0.1)
        amount = Entry(width=20, font=('Arial', 16))
        valid_amt(master, amount, 0.13, 0.45, 'Target Amount :', 30)
        c_amount = Entry(width=20, font=('Arial', 16))
        valid_amt(master, c_amount, 0.06, 0.6, 'Initial Investment (if any) :', 23)

        def limit_size_day(*_arg):
            value = dayValue.get()
            if len(value) > 20:
                dayValue.set(value[:20])

        dayValue = StringVar()
        dayValue.trace('w', limit_size_day)
        desc3 = Entry(width=20, font=('Arial', 16), textvariable=dayValue)
        valid_desc(master, desc3, 0.12, 0.3, 'Enter Title', 'Title :', 0.3)

        def add_sav():
            lst = show_table('select * from saving')
            if len(lst) < 5:
                if desc3.get() not in ('Enter Title' or ''):
                    try:
                        if c_amount.get() in ('In Rs.' or ''):
                            a = 0.00
                        else:
                            a = float(c_amount.get())
                        start("insert into saving values('{0}', {1}, {2})"
                              .format(desc3.get(), float(amount.get()), a))
                        showinfo('Saving Created', 'Your saving of Rs. {0} for {1} has been created successfully'.
                                 format(float(amount.get()), desc3.get()))
                        master.switch_frame(SavingCreate)
                    except ValueError:
                        lbl = Label(text='Please enter a valid Target Amount.', font='24', fg='red', bg='light cyan')
                        lbl.place(relx=0.54, rely=0.51, anchor=W)
                        lbl.after(4000, lbl.place_forget)
                else:
                    lbl = Label(text='Please enter a Title.', font='24', fg='red', bg='light cyan')
                    lbl.place(relx=0.54, rely=0.36, anchor=W)
                    lbl.after(4000, lbl.place_forget)
            else:
                showinfo('Saving Limit Reached', "Sorry! You can't create more than 5 active savings")

        Button(text='Create Saving', command=add_sav, height=1, width=14, fg='blue', cursor='hand2',
               bg='#ffff14', font=('Calibri', '20', 'bold')).place(anchor=CENTER, rely=0.8, relx=0.5)


class SavingAdd(Frame):
    def __init__(self, master):
        master.title('Add Savings')
        global var_show_all
        var_show_all = 'c'
        Frame.__init__(self, master, bg='light cyan')
        back_btn(self, master, SavingFront)
        balance_label(self, 0.9, 0.1)
        Label(self, text="Savings", bg='light cyan', fg='green',
              font='Calibri 40 bold').place(rely=0.2, relx=0.5, anchor=CENTER)
        show_all(self, master, ExpenseAdd, 'saving', 16, 16, 20, 5, SavingAdd)


if __name__ == '__main__':
    App().mainloop()
