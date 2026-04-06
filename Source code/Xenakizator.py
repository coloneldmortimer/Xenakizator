"""
GUI module for entering two numeric values and an output path.
Uses only built-in tkinter - no external dependencies.

Usage:
    Run directly:   python3 ST10_interface.py
    Import:         from ST10_interface import data_input
                    val1, val2, path = data_input()
"""

import tkinter as tk
from tkinter import font as tkfont, filedialog
import os


# ── Theme ─────────────────────────────────────────────────────────────
BG         = "#1e1e2e"
FRAME_BG   = "#2a2a3e"
ACCENT     = "#4a9eff"
ACCENT_HOV = "#2176d6"
RESET_BG   = "#3a3a50"
RESET_HOV  = "#4a4a60"
TEXT       = "#e0e0f0"
SUBTLE     = "#7070a0"
ERROR      = "#ff6b6b"
ENTRY_BG   = "#13131f"
ENTRY_BD   = "#3a3a55"
ENTRY_FOC  = "#4a9eff"


def _rounded_button(parent, text, command, bg, hover, fg="#ffffff"):
    btn = tk.Label(
        parent, text=text, bg=bg, fg=fg,
        font=tkfont.Font(family="Helvetica", size=13, weight="bold"),
        cursor="hand2", padx=0, pady=10, anchor="center",
    )
    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>",    lambda e: btn.config(bg=hover))
    btn.bind("<Leave>",    lambda e: btn.config(bg=bg))
    return btn


def _entry_widget(parent, placeholder):
    var = tk.StringVar()
    e = tk.Entry(
        parent, textvariable=var,
        bg=ENTRY_BG, fg=SUBTLE, insertbackground=TEXT,
        relief="flat", bd=0,
        font=tkfont.Font(family="Helvetica", size=13),
        highlightthickness=2,
        highlightbackground=ENTRY_BD,
        highlightcolor=ENTRY_FOC,
    )

    def on_focus_in(event):
        if var.get() == placeholder:
            var.set("")
            e.config(fg=TEXT)

    def on_focus_out(event):
        if var.get() == "":
            var.set(placeholder)
            e.config(fg=SUBTLE)

    var.set(placeholder)
    e.bind("<FocusIn>",  on_focus_in)
    e.bind("<FocusOut>", on_focus_out)
    e._placeholder = placeholder
    e._var = var
    return e


def _get_value(entry):
    val = entry._var.get().strip()
    if val == entry._placeholder or val == "":
        raise ValueError("empty")
    return float(val)


def _get_text(entry):
    val = entry._var.get().strip()
    if val == entry._placeholder or val == "":
        raise ValueError("empty")
    return val


def build_hint(minv, maxv):
    if minv is not None and maxv is not None:
        return f"  [{minv} - {maxv}]"
    if minv is not None:
        return f"  [min: {minv}]"
    if maxv is not None:
        return f"  [max: {maxv}]"
    return ""


def check_range(val, minv, maxv, name):
    if minv is not None and val < minv:
        return f"⚠  {name}: minimum value is {minv}"
    if maxv is not None and val > maxv:
        return f"⚠  {name}: maximum value is {maxv}"
    return None


def data_input(
    title="Xenakizator 1.0 - ST10",
    label1="Mean length of a section",
    label2="Number of sections",
    placeholder1="e.g. 20",
    placeholder2="e.g. 10",
    min1=0.01, max1=500,
    min2=1, max2=80,
):
    """
    Opens the input window and returns (val1, val2, output_path) as (float, float, str).
    Returns (None, None, None) if the user closes the window without confirming.
    """
    result = [None, None, None]

    # ── Window ────────────────────────────────────────────────────────
    root = tk.Tk()
    root.title(title)
    root.geometry("420x540")
    root.resizable(False, False)
    root.configure(bg=BG)

    card = tk.Frame(root, bg=FRAME_BG, padx=30, pady=24)
    card.place(relx=0.5, rely=0.5, anchor="center", width=370, height=490)

    # ── Title ─────────────────────────────────────────────────────────
    tk.Label(card, text=title, bg=FRAME_BG, fg=TEXT,
             font=tkfont.Font(family="Georgia", size=20, weight="bold")
             ).pack(anchor="w")

    tk.Label(card, text="Enter values and output path", bg=FRAME_BG, fg=SUBTLE,
             font=tkfont.Font(family="Helvetica", size=11)
             ).pack(anchor="w", pady=(2, 16))

    # ── Field builder ─────────────────────────────────────────────────
    def build_field(lbl, ph, minv=None, maxv=None):
        tk.Label(card, text=lbl, bg=FRAME_BG, fg=TEXT,
                 font=tkfont.Font(family="Helvetica", size=12, weight="bold")
                 ).pack(anchor="w")
        hint = build_hint(minv, maxv)
        e = _entry_widget(card, ph + hint)
        e.pack(fill="x", ipady=7, pady=(3, 12))
        return e

    entry1    = build_field(label1, placeholder1, min1, max1)
    entry2    = build_field(label2, placeholder2, min2, max2)

    # ── Separator ─────────────────────────────────────────────────────
    tk.Frame(card, bg=ENTRY_BD, height=1).pack(fill="x", pady=(0, 12))

    # ── Output path field ─────────────────────────────────────────────
    tk.Label(card, text="Output path", bg=FRAME_BG, fg=TEXT,
             font=tkfont.Font(family="Helvetica", size=12, weight="bold")
             ).pack(anchor="w")

    documents_dir = os.path.join(os.path.expanduser("~"), "Documents")
    path_var = tk.StringVar(value=os.path.join(documents_dir, "ST10.pdf"))

    path_row = tk.Frame(card, bg=FRAME_BG)
    path_row.pack(fill="x", pady=(4, 14))

    browse_btn = tk.Label(
        path_row, text="Browse", bg=ACCENT, fg="white",
        font=tkfont.Font(family="Helvetica", size=11, weight="bold"),
        cursor="hand2", pady=10, anchor="center",
)
    browse_btn.pack(side="right", padx=(6, 0))
    browse_btn.bind("<Button-1>", lambda e: on_browse())
    browse_btn.bind("<Enter>",    lambda e: browse_btn.config(bg=ACCENT_HOV))
    browse_btn.bind("<Leave>",    lambda e: browse_btn.config(bg=ACCENT))

    path_display = tk.Label(
        path_row, textvariable=path_var,
        bg=ENTRY_BG, fg=TEXT, anchor="w",
        font=tkfont.Font(family="Helvetica", size=11),
        relief="flat", padx=8, pady=8,
        highlightthickness=2, highlightbackground=ENTRY_BD,
        cursor="arrow", wraplength=280,
    )
    path_display.pack(fill="x", ipady=2)

    def on_browse():
        chosen = filedialog.asksaveasfilename(
            title="Save PDF as",
            initialdir=documents_dir,
            initialfile="ST10.pdf",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if chosen:
            path_var.set(chosen)

    # ── Message label ─────────────────────────────────────────────────
    msg_var = tk.StringVar()
    tk.Label(card, textvariable=msg_var, bg=FRAME_BG, fg=ERROR,
             font=tkfont.Font(family="Helvetica", size=11),
             wraplength=310, justify="left"
             ).pack(anchor="w", pady=(0, 10))

    # ── Actions ───────────────────────────────────────────────────────
    def on_confirm():
        try:
            v1 = _get_value(entry1)
            v2 = _get_value(entry2)
        except ValueError:
            msg_var.set("⚠  Please enter valid numeric values")
            return

        err = check_range(v1, min1, max1, label1) or check_range(v2, min2, max2, label2)
        if err:
            msg_var.set(err)
            return

        path = path_var.get().strip()
        if not path:
            msg_var.set("⚠  Please select an output path")
            return
        if not path.lower().endswith(".pdf"):
            path += ".pdf"
        directory = os.path.dirname(path)
        if directory and not os.path.isdir(directory):
            msg_var.set(f"⚠  Directory not found: {directory}")
            return

        result[0], result[1], result[2] = v1, v2, path
        root.destroy()

    def on_reset():
        for e in (entry1, entry2):
            e._var.set(e._placeholder)
            e.config(fg=SUBTLE)
        path_var.set(os.path.join(documents_dir, "ST10.pdf"))
        msg_var.set("")
        entry1.focus()

    btn_row = tk.Frame(card, bg=FRAME_BG)
    btn_row.pack(fill="x")

    _rounded_button(btn_row, "Confirm", on_confirm, ACCENT, ACCENT_HOV
                    ).pack(side="left", expand=True, fill="x", padx=(0, 6))
    _rounded_button(btn_row, "Reset", on_reset, RESET_BG, RESET_HOV
                    ).pack(side="left", expand=True, fill="x", padx=(6, 0))

    root.bind("<Return>", lambda e: on_confirm())
    entry1.focus()
    root.mainloop()

    return tuple(result)


# ── Entry point ───────────────────────────────────────────────────────
if __name__ == "__main__":
    import importlib.util, sys

    val1, val2, output_path = data_input()

    if val1 is None:
        print("Cancelled.")
        sys.exit(0)

    print(f"Values: {val1}, {val2}  →  {output_path}")

    # Load and run ST10.py from the same directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    st10_path  = os.path.join(script_dir, "ST10.py")

    spec   = importlib.util.spec_from_file_location("ST10", st10_path)
    st10   = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(st10)

    # ST10.py must expose a run(val1, val2, output_path) function
    st10.run(val1, val2, output_path)