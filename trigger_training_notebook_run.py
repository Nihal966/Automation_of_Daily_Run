import os, sys, datetime, subprocess, tkinter as tk, tkinter.messagebox as mb

# === CONFIG ===
# NOTEBOOK_NEW = r"C:\YourFolder\new_model.ipynb"
# NOTEBOOK_PREV = r"C:\YourFolder\best_model.ipynb"
# OUTPUT = r"C:\YourFolder\output.ipynb"
# LAST_RUN = r"C:\YourFolder\.last_run.txt"
# MODE_FILE = r"C:\YourFolder\run_mode.txt"

NOTEBOOK_NEW = r"D:\Nihal\Codes\Automatic Notebook Run\ADNI_new_train.ipynb"
NOTEBOOK_PREV = r"D:\Nihal\Codes\Automatic Notebook Run\ADNI_train_notebook.ipynb"
OUTPUT_dir = r"D:\Nihal\Codes\Output Notebooks"
LAST_RUN = r"D:\Nihal\Codes\Automation\.last_run.txt"
MODE_FILE = r"D:\Nihal\Codes\Automation\Command_of_next_run.txt"
BAT_FILE = r"D:\Nihal\Codes\Automation\run_notebook.bat"  # 🟨 Your .bat file path

OUTPUT = rf"{OUTPUT_dir}\\output_{datetime.date.today().isoformat().replace('-', '_')}.ipynb"

def has_run_today():
    if not os.path.exists(LAST_RUN):
        return False
    try:
        last = open(LAST_RUN).read().strip()
        return last == datetime.date.today().isoformat()
    except:
        return False

def mark_run():
    with open(LAST_RUN, "w") as f:
        f.write(datetime.date.today().isoformat())

def get_run_mode():
    if not os.path.exists(MODE_FILE):
        return None
    
    modified_date = datetime.date.fromtimestamp(os.path.getmtime(MODE_FILE))
    today = datetime.date.today()
    if modified_date not in (today, today - datetime.timedelta(days=1)):
        return None

    with open(MODE_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line in ("1", "Run new model"):
                return "new"
            elif line in ("2", "Run previous model"):
                return "previous"
            elif line in ("3", "Do not run"):
                return "none"
    return None

def run_notebook_with_conda(notebook_path):
    subprocess.Popen(
        ["cmd.exe", "/c", BAT_FILE, OUTPUT, notebook_path],
    #    creationflags=subprocess.CREATE_NEW_CONSOLE
    )

# === MAIN ===
if __name__ == "__main__":
    if has_run_today():
        sys.exit("Notebook has already been run today.")

    mode = get_run_mode()
    if mode == "none" or mode is None:
        sys.exit("No valid run mode specified or 'Do not run' selected.")

    root = tk.Tk()
    root.withdraw()

    if mb.askyesno("Run Notebook?", f"Run the {'NEW' if mode == 'new' else 'PREVIOUS'} model notebook?"):
        run_notebook_with_conda(NOTEBOOK_NEW if mode == "new" else NOTEBOOK_PREV)
        mark_run()

    root.destroy()
