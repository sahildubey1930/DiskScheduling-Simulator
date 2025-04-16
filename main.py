import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


# ----------- Disk Scheduling Algorithms -----------

def fcfs(requests, head):
    sequence = [head] + requests
    total_seek = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, total_seek

def sstf(requests, head):
    sequence = [head]
    total_seek = 0
    pending = requests.copy()

    while pending:
        next_request = min(pending, key=lambda r: abs(r - sequence[-1]))
        total_seek += abs(next_request - sequence[-1])
        sequence.append(next_request)
        pending.remove(next_request)
    return sequence, total_seek

def scan(requests, head, direction="up"):
    sequence = [head]
    requests.sort()
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    if direction == "up":
        sequence += right + left[::-1]
    else:
        sequence += left[::-1] + right

    total_seek = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, total_seek

def cscan(requests, head):
    sequence = [head]
    requests.sort()
    max_cyl = max(requests + [head])
    min_cyl = min(requests + [head])
    right = [r for r in requests if r >= head]
    left = [r for r in requests if r < head]

    sequence += right + [max_cyl, min_cyl] + left
    total_seek = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, total_seek

def look(requests, head, direction="up"):
    sequence = [head]
    requests.sort()
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    if direction == "up":
        sequence += right + left[::-1]
    else:
        sequence += left[::-1] + right

    total_seek = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, total_seek


# ----------- Visualization -----------

def plot_sequence(sequence, title):
    plt.figure()
    plt.plot(range(len(sequence)), sequence, marker='o')
    plt.title(title)
    plt.xlabel("Step")
    plt.ylabel("Cylinder Number")
    plt.grid(True)
    plt.show()


# ----------- GUI -----------

def run_simulation():
    try:
        request_list = list(map(int, entry_requests.get().split(',')))
        head = int(entry_head.get())
        algo = combo_algo.get()

        if not request_list:
            raise ValueError("Empty request list.")

        if algo == "FCFS":
            seq, seek = fcfs(request_list, head)
        elif algo == "SSTF":
            seq, seek = sstf(request_list, head)
        elif algo == "SCAN":
            seq, seek = scan(request_list, head)
        elif algo == "C-SCAN":
            seq, seek = cscan(request_list, head)
        elif algo == "LOOK":
            seq, seek = look(request_list, head)
        else:
            messagebox.showerror("Error", "Please select an algorithm.")
            return

        output_text.set(f"Sequence: {seq}\nTotal Seek Time: {seek}")
        plot_sequence(seq, f"{algo} Algorithm")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid Input: {e}")


# Main Window
root = tk.Tk()
root.title("Disk Scheduling Simulator")
root.geometry("500x400")

# Labels and Inputs
tk.Label(root, text="Request Queue (comma-separated):").pack(pady=5)
entry_requests = tk.Entry(root, width=50)
entry_requests.pack()

tk.Label(root, text="Initial Head Position:").pack(pady=5)
entry_head = tk.Entry(root, width=20)
entry_head.pack()

tk.Label(root, text="Select Algorithm:").pack(pady=5)
combo_algo = ttk.Combobox(root, values=["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK"], state="readonly")
combo_algo.pack()

# Run Button
tk.Button(root, text="Simulate", command=run_simulation, bg="lightblue").pack(pady=10)

# Output
output_text = tk.StringVar()
tk.Label(root, textvariable=output_text, wraplength=450, justify="left").pack(pady=10)

# Run GUI Loop
root.mainloop()
