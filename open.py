import Tkinter as tk

class PasswordDialog(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self)
        self.parent = parent
        self.entry = tk.Entry(self, show='*')
        self.entry.bind("<KeyRelease-Return>", self.StorePassEvent)
        self.entry.pack()
        self.button = tk.Button(self)
        self.button["text"] = "Submit"
        self.button["command"] = self.StorePass
        self.button.pack()

    def StorePassEvent(self, event):
        self.StorePass()

    def StorePass(self):
        self.parent.password = self.entry.get()
        self.destroy()
        print '1: Password was', self.parent.password

class MainApplication(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.password = None
        self.button = tk.Button(self)
        self.button["text"] = "Password"
        self.button["command"] = self.GetPassword
        self.button.pack()

    def GetPassword(self):
        self.wait_window(PasswordDialog(self))
        print '2: Password was', self.password

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
    
# import subprocess
# 
# password = 'asdf'
# #proc = subprocess.Popen(
# #  ['sudo','-p','','-S','/etc/init.d/test','restart'],
# #   stdin=subprocess.PIPE)
# proc = subprocess.Popen(
# #    ['sudo','-p','','-S','echo','restart'],
#     ['su','-c','ls'],
#     stdin=subprocess.PIPE)
# 
# proc.stdin.write(password+'\n')
# proc.stdin.close()
# proc.wait()
