import Tkinter as tk
import subprocess

class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.button = tk.Button(self)
        self.entry = tk.Entry(self, show='*')
        self.entry.bind("<KeyRelease-Return>", self.StorePassEvent)
        self.entry.pack()
        self.button = tk.Button(self)
        self.button["text"] = "Open"
        self.button["command"] = self.StorePass
        self.button.pack()

    def StorePassEvent(self, event):
        self.StorePass()

    def StorePass(self):
        self.password = self.entry.get()
        self.destroy()
        self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    appz = MainApplication(root)
    appz.pack(side="top", fill="both", expand=True)
    root.mainloop()
   
    proc = subprocess.Popen(
                            ['su','-c','ls'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    proc.stdin.write(appz.password+'\n')
    proc.stdin.close()
    proc.wait()
    print proc.stdout.read()