import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

# Create the main application window
root = tk.Tk()
root.title('TIFF Merge Tool')

# Define the file paths for the TIFF files
tiff_files = {
    'upper_left': None,
    'upper_right': None,
    'lower_left': None,
    'lower_right': None
}

# Function to select TIFF files and store their paths
def select_file(position):
    file_path = filedialog.askopenfilename(
        title=f'Select the TIFF file for {position.replace("_", " ")}',
        filetypes=[('TIFF files', '*.tif *.tiff')]
    )
    if file_path:
        tiff_files[position] = file_path
        buttons[position]['text'] = os.path.basename(file_path)

# Function to merge the TIFF files into one JPEG
def merge_files():
    # Check if all files are selected
    if None in tiff_files.values():
        tk.messagebox.showerror('Error', 'Please select all TIFF files before merging.')
        return
    
    # Load images
    images = {pos: Image.open(path) for pos, path in tiff_files.items()}
    
    # Find the max width and height per row and column
    max_width_column = max(images['upper_left'].width + images['upper_right'].width,
                           images['lower_left'].width + images['lower_right'].width)
    max_height_row = max(images['upper_left'].height + images['lower_left'].height,
                         images['upper_right'].height + images['lower_right'].height)
    
    # Create a new blank image with the correct size
    merged_image = Image.new('RGB', (max_width_column, max_height_row))
    
    # Paste the images into the correct positions
    merged_image.paste(images['upper_left'], (0, 0))
    merged_image.paste(images['upper_right'], (images['upper_left'].width, 0))
    merged_image.paste(images['lower_left'], (0, images['upper_left'].height))
    merged_image.paste(images['lower_right'], (images['lower_left'].width, images['upper_left'].height))
    
    # Convert to JPEG and save
    jpeg_image = merged_image.convert('RGB')
    save_path = filedialog.asksaveasfilename(
        defaultextension='.jpg',
        filetypes=[('JPEG', '*.jpg'), ('All Files', '*.*')],
        title='Save the merged JPEG file'
    )
    if save_path:
        jpeg_image.save(save_path)
        tk.messagebox.showinfo('Success', f'The merged JPEG has been saved to {save_path}')

# Create buttons for selecting TIFF files
buttons = {
    'upper_left': tk.Button(root, text='Sol üst TIFF', command=lambda: select_file('upper_left')),
    'upper_right': tk.Button(root, text='Sağ üst TIFF', command=lambda: select_file('upper_right')),
    'lower_left': tk.Button(root, text='Sol alt TIFF', command=lambda: select_file('lower_left')),
    'lower_right': tk.Button(root, text='Sağ alt TIFF', command=lambda: select_file('lower_right')),
    'merge': tk.Button(root, text='JPEG oluştur', command=merge_files)
}

# Place the buttons on the window
for button in buttons.values():
    button.pack(expand=True, fill='both')

# Start the Tkinter event loop
root.mainloop()
