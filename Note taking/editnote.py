from tkinter import *
from tkinter import messagebox, font
from Note import Note


class EditNote:
    def __init__(self):
        pass

    def update_callback(self, note):
        msg = self.text.get("1.0", 'end-1c')
        if len(msg) <= 0:
            messagebox.showinfo("Invalid Action", "Please Enter Note...")
            return
        try:
            obj = Note(idt=note.get_idt(), msg=msg)
            self.db.update_note(obj)
            self.dash.list_all_callback()
            self.dash.root.attributes('-disabled', False)
            self.root.destroy()
            
            messagebox.showinfo("Success", "Note Updated!")

        except Exception as e:
            self.dash.root.attributes('-disabled', False)
            self.root.destroy()
            messagebox.showinfo("Error", "Failed To Update Note! Try Again")

    def cancel_callback(self):
        self.dash.root.attributes('-disabled', False)
        self.root.destroy()

    def delete_callback(self, note):
        try:
            self.db.delete_note(note)
            self.dash.list_all_callback()
            self.dash.root.attributes('-disabled', False)
            self.root.destroy()
            
            messagebox.showinfo("Success", "Note Deleted!")

        except Exception as e:
            self.dash.root.attributes('-disabled', False)
            self.root.destroy()
            
            messagebox.showinfo("Error", "Failed To Delete Note! Try Again")
    
    def initUI(self, dash, db, note):
        self.dash = dash
        self.dash.root.attributes('-disabled', True)
        self.db = db
        self.root = Tk()
        self.root.geometry("650x530")
        self.root.resizable(0, 0)
        self.root.protocol("WM_DELETE_WINDOW", self.cancel_callback)
        self.root.title("Edit Note")
        self.Font = font.Font(family='Helvetica', size=15, weight='bold')
        self.Font_search_text = font.Font(family='Helvetica', size=15)
        self.Font_search_btn = font.Font(family='Helvetica', size=10, weight='bold')
        self.Font_note = font.Font(family='Helvetica', size=12)
        self.Font_add_label = font.Font(family='Helvetica', size=25, weight='bold')
        self.add_label = Label(self.root, text="View\Edit Note", font=self.Font_add_label)
        self.add_label.place(x=250, y=15)
        self.text = Text(self.root, font=self.Font_note, width=70, height=22)
        self.text.insert('1.0', note.get_msg())
        self.text.place(x=1, y=40)
        self.scroll = Scrollbar(self.root, orient=VERTICAL, command=self.text.yview)
        self.text['yscroll'] = self.scroll.set

        # self.scroll.pack(side="right", fill="y")
        self.scroll.place(x=632, y=40, height=401)
        time = "Created At : "+str(note.get_time())
        self.time_label = Label(self.root, text=time, font=self.Font_note)
        self.time_label.place(x=190, y=448)
        self.save_button = Button(self.root, bg="#900C3F", fg="white", text="Update",
                                  command=lambda: self.update_callback(note), font=self.Font_search_btn, width=13)
        self.save_button.place(x=420, y=480)
        self.delete_button = Button(self.root, bg="#900C3F", fg="white", text="Delete",
                                    command=lambda: self.delete_callback(note), font=self.Font_search_btn, width=13)
        self.delete_button.place(x=250, y=480)
        self.cancel_button = Button(self.root, bg="#900C3Fs", fg="white", text="Cancel",
                                    command=lambda: self.cancel_callback(), font=self.Font_search_btn, width=13)
        self.cancel_button.place(x=80, y=480)
        self.root.mainloop()
