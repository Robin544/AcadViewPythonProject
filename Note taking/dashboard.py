from tkinter import *
from tkinter import font, messagebox
from editnote import EditNote
from addnewnote import AddNewNote
import datetime

class Dashboard:
    def __init__(self):
        pass

    '''def refresh_notes(self):
        notes = self.curr_notes
        temp = []
        for note in notes:
            try:
                temp_note = self.db.get_one_note(note.get_idt())
                temp.append(temp_note)
            except Exception as e:
                pass
        self.show_notes(temp)
    '''

    def show_notes(self, notes):
        i = 0
        self.curr_notes = notes
        self.listbox.delete(0, self.listbox.size())
        for note in notes:
            x = str(note.get_msg())
            y = int(note.get_idt())
            if x <= x[:20]:
                self.listbox.insert(i, x)
            else:
                self.listbox.insert(i, x[:20] + "...")
            if i % 2 == 0:
                self.listbox.itemconfig(i, bg="#d3d3d3")
            i += 1

    def search_callback(self):
        if len(self.var.get()) <= 0:
             messagebox.showinfo("Invalid Action", "Please Enter Search Entry!")
             return
        notes = self.db.search_notes(self.var.get())
        if len(notes) == 0:
              messagebox.showinfo("Info", "No match Found!")
        else:
              self.show_notes(notes)

    def list_all_callback(self):
        try:
            notes = self.db.get_all_notes()
            self.show_notes(notes)
            if len(notes) == 0:
                messagebox.showinfo("List Info", "Empty list!\nPlease add a note.")
        except Exception as e:
            print(e)
            messagebox.showinfo("Error", "Could Not Fetch Notes")

    def edit_callback(self):
        try:
            EditNote().initUI(self, self.db, self.curr_notes[self.listbox.curselection()[0]])
        except Exception as e:
            pass

    def add_callback(self):
        AddNewNote().initUI(self, self.db)

    def initUI(self, db):
        self.db = db
        self.root = Tk()
        self.root.geometry("950x630")
        self.root.resizable(0, 0)
        self.root.title("Note Taking App")
        self.Font = font.Font(family='Helvetica', size=16, weight='bold')
        self.Font_search_text = font.Font(family='Helvetica', size=17)
        self.Font_search_btn = font.Font(family='Helvetica', size=12, weight='bold')
        self.Font_note = font.Font(family='Helvetica', size=16)
        self.Font_note_label = font.Font(family='Helvetica', size=18, weight='bold')
        self.Font_name_label = font.Font(family='Helvetica', size=13, weight='bold')

        #----------------------------------CLOCK-----------------------------------------------
        def clock_time():
            time = datetime.datetime.now()
            time = (time.strftime("%H:%M:%S %p"))
            txt.set(time)
            self.root.after(1000, clock_time)

        self.root.bind("x", quit)
        txt = StringVar()
        self.root.after(1000, clock_time())

        dt = datetime.date.today().strftime('%d/%m/%Y')
        self.label_date = Label(self.root, font=('ariel', 18, 'bold'), text="Date: " + dt, fg="#900C3F", anchor=W)
        self.label_date.place(x=750, y=10)
        self.label_time = Label(self.root, font=('ariel', 18, 'bold'), text="Time: ", textvariable=txt, fg="#900C3F", anchor=W)
        self.label_time.place(x=770, y=45)

        # -----------------------------------Clock Designed---------------------------------

        self.add_button = Button(self.root, width=18, bg="red", fg="white", text="Add New Note>>",
                               font=self.Font, command=lambda: self.add_callback())
        self.add_button.place(x=105, y=90)
        self.list_all_btn = Button(self.root, width=18, bg="red", fg="white", text="List All Notes",
                                 font=self.Font, command=lambda: self.list_all_callback())
        self.list_all_btn.place(x=440, y=90)
        self.search_label = Label(self.root, text="Search Notes", font=self.Font)
        self.search_label.place(x=15, y=160)
        self.var = StringVar()
        self.search_box = Entry(self.root, width=56, textvariable=self.var, font=self.Font_search_text)
        self.search_box.place(x=15, y=195)
        self.search_button = Button(self.root, bg="red", fg="white", text="Search",
                                    font=self.Font_search_btn, width=13, command=lambda: self.search_callback())
        self.search_button.place(x=790, y=192)
        self.note_label = Label(self.root, text="-- Notes --", font=self.Font_note_label)
        self.note_label.place(x=330, y=235)

        self.listbox = Listbox(self.root, selectmode=SINGLE, width=78, font=self.Font_note, height=13)
        self.scroll = Scrollbar(self.root, orient=VERTICAL, command=self.listbox.yview)
        self.listbox['yscroll'] = self.scroll.set

        self.Font_for_label = font.Font(family='Helvetica', size=35, weight='bold')
        self.label = Label(self.root, text="<< Save Your Notes Here >>", fg="#900C3F", font=self.Font_for_label)
        self.label.place(x=80, y=6)

        # self.scroll.pack(side="right", fill="y")
        self.scroll.place(x=932, y=275, height=330)
        self.list_all_callback()

        self.listbox.bind('<<ListboxSelect>>', lambda l: self.edit_callback())
        self.listbox.place(x=5, y=275)

        self.name_label = Label(self.root, text="--By Robin Singh",  fg="#900C3F", font=self.Font_name_label)
        self.name_label.place(x=795, y=604)

        def mainconfirm():
            if messagebox.askyesno("Exit", "Do you want to exit?"):
                self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW", mainconfirm)

        self.root.mainloop()
