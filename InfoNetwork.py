# Create by Github.com/Kurama250
# pip install psutil pyperclip tk

import psutil
import tkinter as tk
from tkinter import ttk
import pyperclip
import threading

def format_bytes(byte_size):
    if byte_size < 1024:
        return f"{byte_size} B"
    elif byte_size < 1048576:
        return f"{byte_size / 1024:.2f} KB"
    elif byte_size < 1073741824:
        return f"{byte_size / 1048576:.2f} MB"
    else:
        return f"{byte_size / 1073741824:.2f} GB"

def get_network_usage():
    network_usage = {}
    for conn in psutil.net_connections(kind='inet'):
        try:
            pid = conn.pid
            if pid:
                process = psutil.Process(pid)
                name = process.name()
                bytes_sent, bytes_recv = process.io_counters()[:2]
                
                if name not in network_usage:
                    network_usage[name] = {'sent': 0, 'recv': 0}
                
                network_usage[name]['sent'] += bytes_sent
                network_usage[name]['recv'] += bytes_recv
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return network_usage

def calculate_per_second_usage(prev, current):
    usage_per_second = {}
    for name, data in current.items():
        if name in prev:
            sent_per_sec = max(0, data['sent'] - prev[name]['sent'])
            recv_per_sec = max(0, data['recv'] - prev[name]['recv'])
            usage_per_second[name] = {'sent': sent_per_sec, 'recv': recv_per_sec}
    return usage_per_second

def copy_to_clipboard(event=None):
    selected_item = tree.selection()
    if selected_item:
        selected_item = selected_item[0]
        name, sent, recv = tree.item(selected_item, "values")
        copy_text = f"Program: {name}\nSent: {sent}\nReceived: {recv}"
        pyperclip.copy(copy_text)

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

def update_ui():
    global previous_usage
    if update_ui.is_updating:
        return

    update_ui.is_updating = True
    current_usage = get_network_usage()
    per_second_usage = calculate_per_second_usage(previous_usage, current_usage)

    for row in tree.get_children():
        tree.delete(row)

    total_sent = 0
    total_recv = 0

    active_usage = []
    inactive_usage = []

    sorted_usage = sorted(per_second_usage.items(), key=lambda x: x[1]['recv'], reverse=True)

    for name, usage in sorted_usage:
        if usage['sent'] == 0 and usage['recv'] == 0:
            inactive_usage.append((name, usage))
        else:
            active_usage.append((name, usage))
            total_sent += usage['sent']
            total_recv += usage['recv']

    for name, usage in active_usage:
        name_color = "blue"
        sent_color = "blue"
        recv_color = "blue"
        tree.insert("", "end", values=(name, format_bytes(usage['sent']), format_bytes(usage['recv'])),
                    tags=(name_color, sent_color, recv_color))

    for name, usage in inactive_usage:
        name_color = "red"
        sent_color = "red"
        recv_color = "red"
        tree.insert("", "end", values=(name, format_bytes(usage['sent']), format_bytes(usage['recv'])),
                    tags=(name_color, sent_color, recv_color))

    total_bandwidth = total_sent + total_recv
    total_sent_label.config(text=f"Total Bandwidth Usage: {format_bytes(total_bandwidth)}", fg="white", font=("Arial", 16, "bold"))

    previous_usage = current_usage
    root.after(2000, update_ui)
    update_ui.is_updating = False

update_ui.is_updating = False

root = tk.Tk()

root.title("InfoNetwork | Alpha 1.1")
root.geometry("700x500")
root.configure(bg="#333333")

title_label = tk.Label(root, text="Real-Time Network Usage by Program (Updated Every 2 Seconds)",
                       font=("Arial", 16, "bold"), fg="white", bg="#333333")
title_label.pack(pady=10)

columns = ("Program", "Sent", "Received")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Program", text="Program")
tree.heading("Sent", text="Sent")
tree.heading("Received", text="Received")

tree.column("Program", width=300, anchor="center")
tree.column("Sent", width=150, anchor="center")
tree.column("Received", width=150, anchor="center")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="white", background="#444444")
style.configure("Treeview", background="#EEEEEE", fieldbackground="#EEEEEE", foreground="black", font=("Arial", 10))
style.map("Treeview", background=[('selected', '#A5D6A7')])

tree.tag_configure("blue", foreground="blue")
tree.tag_configure("red", foreground="red")
tree.tag_configure("green", foreground="green")
tree.tag_configure("white", foreground="black")

tree.pack(expand=True, fill="both", padx=20, pady=10)

total_sent_label = tk.Label(root, text="Total Bandwidth Usage: 0 B/s", font=("Arial", 16), fg="white", bg="#555555", relief="solid", padx=10, pady=5)
total_sent_label.pack(pady=(20, 5))

previous_usage = get_network_usage()

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Copy", command=copy_to_clipboard)

tree.bind("<Button-3>", show_context_menu)

credits_label = tk.Label(root, text="InfoNetwork by Github.com/Kurama250 | Alpha 1.1", font=("Arial", 8), fg="white", bg="#333333")
credits_label.pack(side="left", padx=10, pady=5)

root.after(2000, update_ui)

root.mainloop()
