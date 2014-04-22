import Tkinter as tk
import tkMessageBox
import subprocess

class PasswordGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.button = tk.Button(self,text="Open",command=self.Open)
        self.button2 = tk.Button(self,text="Close",command=self.Close)
        self.entry = tk.Entry(self, show='*')
        self.entry.pack()
        self.button.pack()
        self.button2.pack()
        
        
    def runAsRoot(self,command,close):
        p = subprocess.Popen(
                            ['su','-c',command],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p.stdin.write(self.password+'\n')
        if close:
            p.stdin.close()
            p.wait()
        return p


    def Open(self):
        '''
        open ssh access and open firewall
        '''
        self.Authenticate()
        
        # open ssh access
        self.runAsRoot('/sbin/service sshd start', True)
        
        # open ssh-service in firewall
        self.runAsRoot('firewall-cmd --zone=public --add-service=ssh', True)
        
        # DESTROY window etc.
        self.Destroy() 
        
        
    def Close(self):
        '''
        close ssh access and close firewall
        '''
        self.Authenticate()
        
        # close ssh access
        self.runAsRoot('/sbin/service sshd stop', True)
        
        # close ssh-service in firewall
        self.runAsRoot('firewall-cmd --zone=public --remove-service=ssh', True)
        
        # DESTROY window etc.
        self.Destroy() 
        
        
    def Authenticate(self):
        '''
        pseudo-method for checking whether su password is correct
        '''
        self.password = self.entry.get()
        proc = self.runAsRoot('ls /', False)
        proc.stderr.read(10)  # read "password prompt"
        out, err = proc.communicate(self.password+'\n')
        if (len(out) > 0) & (len(err) == 0):
            return
        elif (len(out) == 0) & (len(err) > 0):
            tkMessageBox.showinfo("Fail", "Wrong password!")
            exit()
        else:
            tkMessageBox.showinfo("Fail", "Something else is wrong!")
            exit()

        
    def Destroy(self):
        '''
        destroy windows etc.
        '''
        self.destroy()
        self.parent.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    appz = PasswordGUI(root)
    appz.pack(side="top", fill="both", expand=True)
    root.mainloop()
