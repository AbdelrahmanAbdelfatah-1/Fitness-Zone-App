import tkinter as tk

Dark_Gray = "#111827"
Charcoal_Gray = "#1F2937"
Dark_Blue = "#004477"


def info_row(parent, left_text, right_text, is_first=False):
    f = tk.Frame(parent, bg="#1F2937", relief='raised', bd=2)
    f.pack(fill="x", pady=5)

    l = tk.Label(f, text=left_text, font=("Arial", 15), bg="#1F2937", fg="white")
    l.pack(side="left", padx=16, pady=8)

    if is_first:
        right_frame = tk.Frame(f, bg="#1F2937")
        right_frame.pack(side="right", padx=16, pady=8)

        entry = tk.Entry(right_frame, font=("Arial", 15), bg="#111827", fg="white",
                         insertbackground="white", width=10)
        entry.insert(0, right_text)
        entry.pack(side="left", padx=(0, 8))

        r = entry
    else:
        r = tk.Label(f, text=right_text, font=("Arial", 15, "bold"),
                     fg="#1e88e5", bg="#1F2937")
        r.pack(side="right", padx=16, pady=8)

    sep = tk.Frame(parent, height=10, bg="#111827")
    sep.pack(fill="x")

    return r


def nut_col(parent, pct, grams, label):
    c = tk.Frame(parent, bg=Dark_Gray)
    c.pack(side="left", padx=20)

    pct_lbl = tk.Label(c, text=f"{round(pct, 1)}%", font=("Arial", 15, "bold"),
                       bg=Dark_Gray, fg="#34BDAC" if label == "Carbs" else ("#9966cc" if label == "Fat" else "#d9902f"))
    pct_lbl.pack()

    g_lbl = tk.Label(c, text=f"{grams}g", font=("Arial", 12), bg=Dark_Gray, fg="white")
    g_lbl.pack()

    lbl = tk.Label(c, text=label, font=("Arial", 12), bg=Dark_Gray, fg="white")
    lbl.pack()

    return {"pct_label": pct_lbl, "grams_label": g_lbl, "name_label": lbl}