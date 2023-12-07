import nmap
import tkinter as tk
from tkinter import messagebox, simpledialog
import sys
import time

def scan_ports(target_ip, ports):
    open_ports = []
    closed_ports = []

    nm = nmap.PortScanner()
    nm.scan(target_ip, ports, arguments="-sS -sV -O")
   
    for host in nm.all_hosts():
        for port in nm[host]['tcp']:
            if nm[host]['tcp'][port]['state'] == 'open':
                open_ports.append((port, nm[host]['tcp'][port]['name'], nm[host]['tcp'][port]['product']))
            else:
                closed_ports.append(port)
    detected_os = nm[host].get('osclass', [])

    return open_ports, closed_ports ,detected_os
def terminal_version():
    target_ip = input("Enter the target IP address or website URL: ")
    

    scan_type = input("Enter 'range' to scan a range of ports, or 'single' to scan a single port: ").lower()

    if scan_type == "range":
        start_port = int(input("Enter the starting port: "))
  
        end_port = int(input("Enter the ending port: "))
        ports = f"{start_port}-{end_port}"
    elif scan_type == "single":
        port = int(input("Enter the port to scan: "))
        ports = str(port)
    else:
        print("Invalid input. Please enter 'range' or 'single'.")
        exit()
    sys.stdout.write("Scanning")
    sys.stdout.flush()

    for _ in range(7):  
        time.sleep(1)
        sys.stdout.write(".")
        sys.stdout.flush()

    print("\nScan in progress...")
    open_ports, closed_ports ,detected_os = scan_ports(target_ip, ports)
    print(f"Open ports: {len(open_ports)}")
    for port, service_name, product in open_ports:
        print(f"Port {port} is open - Service: {service_name} ({product})")
    print(f"Closed ports: {len(closed_ports)}")
    
    if detected_os:
     print("Detected OS Information:")   
     for os_info in detected_os:
        print(f"OS: {os_info['osfamily']} ({os_info['osgen']})")
    else:
        print("No OS details found")    


def gui_version():

 def scan_button_clicked():
    target_ip= target_entry.get()
    
    
    if not target_ip:
        messagebox.showerror("Error", "Invalid target address.")
        return
    
    scan_type = scan_type_var.get()
    
    if scan_type == "range":
        start_port = int(simpledialog.askstring("Port Range", "Enter the starting port: "))
        end_port = int(simpledialog.askstring("Port Range", "Enter the ending port: "))
        ports = f"{start_port}-{end_port}"
    elif scan_type == "single":
        port = int(simpledialog.askstring("Port", "Enter the port to scan: "))
        ports = str(port)
    else:
        messagebox.showerror("Error", "Invalid scan type.")
        return
    
    open_ports, closed_ports ,detected_os = scan_ports(target_ip, ports)
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Open ports: {len(open_ports)}\n")
    for port, service_name, product in open_ports:
        result_text.insert(tk.END, f"Port {port} is open - Service: {service_name} ({product})\n")
    result_text.insert(tk.END, f"Closed ports: {len(closed_ports)}\n")
    result_text.config(state=tk.DISABLED)
    
    os_text.config(state=tk.NORMAL)
    os_text.delete("1.0", tk.END)
    for os_info in detected_os:
        os_text.insert(tk.END, f"OS: {os_info['osfamily']} ({os_info['osgen']})\n")
    os_text.config(state=tk.DISABLED)

 root = tk.Tk()
 root.title("Network Scanner")
 target_label = tk.Label(root, text="Enter the target IP address :")
 target_label.pack()

 target_entry = tk.Entry(root)
 target_entry.pack()

 scan_type_var = tk.StringVar()
 scan_type_var.set("range")

 scan_type_frame = tk.Frame(root)
 scan_type_label = tk.Label(scan_type_frame, text="Select scan type:")
 scan_type_label.pack()

 range_radio = tk.Radiobutton(scan_type_frame, text="Port Range", variable=scan_type_var, value="range")
 range_radio.pack()

 single_radio = tk.Radiobutton(scan_type_frame, text="Single Port", variable=scan_type_var, value="single")
 single_radio.pack()

 scan_type_frame.pack()

 scan_button = tk.Button(root, text="Start Scan", command=scan_button_clicked)
 scan_button.pack()

 result_text = tk.Text(root, height=10, width=40)
 result_text.pack()

 os_text = tk.Text(root, height=3, width=40) 
 os_text.pack()

 root.mainloop()

if __name__ == "__main__":
    use_gui = input("which version you want to use? (gui/cli): ").lower()

    if use_gui == "gui":
        print("openining gui version")
        gui_version()
    elif use_gui == "cli":
        terminal_version()
    else:
        print("Invalid input. Please enter 'gui' or 'cli'.")