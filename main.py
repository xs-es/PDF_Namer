import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import re
import os

class PDFRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Renamer")
        
        self.selected_files = []

        # Create UI elements
        self.label = tk.Label(root, text="Select PDF files to rename:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select PDFs", command=self.select_files)
        self.select_button.pack(pady=5)

        self.rename_button = tk.Button(root, text="Rename PDFs", command=self.rename_pdfs)
        self.rename_button.pack(pady=5)

        self.file_listbox = tk.Listbox(root, width=50, height=10)
        self.file_listbox.pack(pady=10)

    def select_files(self):
        files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])
        self.selected_files = list(files)
        self.file_listbox.delete(0, tk.END)  # Clear the listbox
        for file in self.selected_files:
            self.file_listbox.insert(tk.END, file)

    def rename_pdfs(self):
        for pdf_path in self.selected_files:
            try:
                # Open the PDF file
                doc = fitz.open(pdf_path)
                first_page = doc[0]
                
                # Extract text with font size information
                text_blocks = first_page.get_text("dict")["blocks"]
                
                largest_font_size = 0
                titles = []  # List to hold all words with the largest font size

                for block in text_blocks:
                    if "lines" in block:  # Check if the block contains text
                        for line in block["lines"]:
                            for span in line["spans"]:
                                # Check for the largest font size
                                if span["size"] > largest_font_size:
                                    largest_font_size = span["size"]
                                    titles = [span["text"].strip()]  # Start a new list with the current text
                                elif span["size"] == largest_font_size:
                                    titles.append(span["text"].strip())  # Add to the list if the size matches

                doc.close()  # Close the document

                # Debugging: Print the largest font size and corresponding titles
                print(f"Largest font size: {largest_font_size}, Titles: {titles}")

                if not titles:
                    messagebox.showerror("Error", f"No title found in '{pdf_path}'")
                    continue

                # Join all titles with underscores
                formatted_title = '_'.join(titles)
                formatted_title = re.sub(r'[^\w-]', '', formatted_title)  # Remove special characters

                new_pdf_name = f"{formatted_title}.pdf"
                new_pdf_path = os.path.join(os.path.dirname(pdf_path), new_pdf_name)

                # Rename the PDF file
                os.rename(pdf_path, new_pdf_path)

                messagebox.showinfo("Success", f"Renamed '{pdf_path}' to '{new_pdf_name}'")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename '{pdf_path}': {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFRenamerApp(root)
    root.mainloop()
