import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

from parsers.parser_manager import extract_text
from processing.cleaner import clean_text
from processing.normalizer import normalize_text


# ---------------- GUI WINDOW ----------------
root = tk.Tk()
root.title("ZecPath AI Resume Analyzer")
root.geometry("700x500")

# Title
title = tk.Label(root, text="ZecPath AI Resume Analyzer",
                 font=("Arial", 16, "bold"))
title.pack(pady=10)

# Text Area
output_area = ScrolledText(root, width=80, height=25)
output_area.pack(pady=10)


# Upload Function
def upload_resume():
    file_path = filedialog.askopenfilename(
        filetypes=[("Resume Files", "*.pdf *.docx")]
    )

    if file_path:
        raw_text = extract_text(file_path)
        cleaned = clean_text(raw_text)
        final_text = normalize_text(cleaned)

        output_area.delete(1.0, tk.END)
        output_area.insert(tk.END, final_text)


# Upload Button
upload_btn = tk.Button(root,
                       text="Upload Resume",
                       command=upload_resume,
                       font=("Arial", 12))

upload_btn.pack(pady=5)

# Run App
root.mainloop()