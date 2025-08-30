import os
import tkinter as tk
from tkinter import filedialog, messagebox

class FolderParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Structure Generator")
        self.root.geometry("600x400")
        
        # Variables
        self.selected_folder_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.ignore_folders = tk.StringVar()
        self.ignore_contents = tk.StringVar()

        # UI Layout
        self.create_widgets()

    def create_widgets(self):
        # Frame for UI elements
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Folder Selection
        tk.Label(main_frame, text="Select Parent Folder:").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(main_frame, textvariable=self.selected_folder_path, state='readonly', width=50).grid(row=0, column=1, padx=5, sticky="ew")
        tk.Button(main_frame, text="Browse", command=self.select_folder).grid(row=0, column=2, padx=5)

        # Output File Selection
        tk.Label(main_frame, text="Output File Path:").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(main_frame, textvariable=self.output_file_path, state='readonly', width=50).grid(row=1, column=1, padx=5, sticky="ew")
        tk.Button(main_frame, text="Save As", command=self.select_output_file).grid(row=1, column=2, padx=5)

        # Ignore Folders
        tk.Label(main_frame, text="Folders to Ignore (comma-separated):").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(main_frame, textvariable=self.ignore_folders, width=50).grid(row=2, column=1, columnspan=2, padx=5, sticky="ew")

        # Ignore Contents
        tk.Label(main_frame, text="Folders to Ignore Contents of (comma-separated):").grid(row=3, column=0, sticky="w", pady=5)
        tk.Entry(main_frame, textvariable=self.ignore_contents, width=50).grid(row=3, column=1, columnspan=2, padx=5, sticky="ew")

        # Generate Button
        tk.Button(main_frame, text="Generate Structure", command=self.generate_structure, font=("TkDefaultFont", 12, "bold")).grid(row=4, column=0, columnspan=3, pady=20)
        
        # Make columns resizeable
        main_frame.grid_columnconfigure(1, weight=1)

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Select a folder")
        if folder_path:
            self.selected_folder_path.set(folder_path)
            self.autofill_output_path(folder_path)

    def select_output_file(self):
        initial_dir = os.path.dirname(self.selected_folder_path.get()) if self.selected_folder_path.get() else os.getcwd()
        output_path = filedialog.asksaveasfilename(
            title="Save Output File",
            initialdir=initial_dir,
            initialfile=os.path.basename(self.selected_folder_path.get()) + "_structure.txt" if self.selected_folder_path.get() else "folder_structure.txt",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if output_path:
            self.output_file_path.set(output_path)

    def autofill_output_path(self, folder_path):
        folder_name = os.path.basename(folder_path)
        desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        output_file_name = f"{folder_name}_structure.txt"
        self.output_file_path.set(os.path.join(desktop_path, output_file_name))

    def generate_structure(self):
        parent_folder = self.selected_folder_path.get()
        output_file = self.output_file_path.get()
        
        if not parent_folder or not output_file:
            messagebox.showerror("Error", "Please select a parent folder and an output file path.")
            return

        ignore_folders_list = [f.strip() for f in self.ignore_folders.get().split(',') if f.strip()]
        ignore_contents_list = [f.strip() for f in self.ignore_contents.get().split(',') if f.strip()]
        
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(os.path.basename(parent_folder) + "/\n")
                
                for root, dirs, files in os.walk(parent_folder):
                    # Sort files and directories for consistent output
                    dirs.sort()
                    files.sort()

                    # Calculate depth
                    level = root.replace(parent_folder, '').count(os.sep)
                    indent = '    ' * level
                    
                    # Apply ignore logic
                    # Filter dirs in place to control recursion
                    dirs[:] = [d for d in dirs if d not in ignore_folders_list]

                    # Write the current directory if it's not being ignored entirely
                    if level > 0: # Do not write the parent directory again
                        dir_name = os.path.basename(root)
                        # Check if the folder's contents should be ignored
                        if dir_name not in ignore_contents_list and dir_name not in ignore_folders_list:
                             f.write(f"{indent[:-4]}├── {dir_name}/\n")
                        else:
                             f.write(f"{indent[:-4]}└── {dir_name}/\n")
                             continue # Skip the rest of the loop for this folder

                    # Print files in the current directory
                    for i, file in enumerate(files):
                        prefix = "├── "
                        if i == len(files) - 1 and (not dirs or all(d in ignore_folders_list or d in ignore_contents_list for d in dirs)):
                            prefix = "└── "
                        f.write(f"{indent}{prefix}{file}\n")
                        
                    # Print sub-directories
                    for i, d in enumerate(dirs):
                        prefix = "├── "
                        if i == len(dirs) - 1:
                            prefix = "└── "
                        f.write(f"{indent}{prefix}{d}/\n")

            messagebox.showinfo("Success", f"Folder structure has been saved to:\n{output_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderParserApp(root)
    root.mainloop()