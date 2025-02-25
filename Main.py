import customtkinter
import os
import pytesseract
import threading
from PIL import Image

def analyze_frames_thread():
    thread = threading.Thread(target = analyze_frames)
    thread.daemon = True  # Allows the thread to close when the program exits
    thread.start()


def write_file(output_list):
    new_file = open("AnalyzedFrames.txt", 'w')

    for i in output_list:
        new_file.write(i + ", ")

    new_file.close()


def analyze_frames():
    global input_dir
    global analyzed_frames
    path = input_dir.get()
    output_list = []

    try:
        for filename in os.listdir(path):
            # Directory Formatting
            dir = os.path.abspath(filename)
            dir = os.path.join(path, filename)

            if filename.endswith(".png") or filename.endswith(".jpeg"): # Ensures .png & .jpeg file
                
                # Opens image
                img= Image.open(dir)

                # # Crops Image
                img = img.crop((0, 1000, 360 , img.height))
                img = img.convert('L')

                # # Binarize Image
                img = img.point(lambda x: 0 if x<175 else 255, '1')

                # Tesseract Setup
                config = "--psm 8"
                tesseract = str(pytesseract.image_to_string(img, config=config)).strip()
                
                sys_dlg.configure(text="Analyzing Frames", text_color = 'green')

                # Format OCR Result
                while True:
                    if tesseract[-1] in ['0','1','2','3','4','5','6','7','8','9']:
                        break
                    tesseract = tesseract[:-1]
                
                # Appends Result to list
                output_list.append(tesseract)

        # Terminal Log
        print (output_list)

        # Format List to only contain Numbers
        for j in range (len(output_list)):
            output_list[j] = output_list[j][6:]

        # Write File
        sys_dlg.configure(text="Writing File", text_color = 'green')
        write_file(output_list)
        
        # Output
        sys_dlg.configure(text="Completed Analyzation", text_color = 'green')
        sys_dlg.after(3000, lambda: sys_dlg.configure(text=""))
            
    except:
        print("There has been an error")


def Confirm_dir():
    global input_dir
    dir = input_dir.get()
    try:
        if os.path.isdir(dir):
            button.configure(state="normal")
            input_dir.configure(state="disabled")
            input_dir.configure(text_color = "#6b6b6b")  

            sys_dlg.configure(text="Valid Directory", text_color = "green")
            sys_dlg.after(3000, lambda: sys_dlg.configure(text=""))
        else: 
            sys_dlg.configure(text="Invalid Directory", text_color = "red")
            sys_dlg.after(3000, lambda: sys_dlg.configure(text=""))
    except:
        sys_dlg.configure(text="Invalid Directory", text_color = "red")
        sys_dlg.after(3000, lambda: sys_dlg.configure(text=""))


# Creating App Object
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Frame Identifier Tool")
app.iconbitmap(r"E:\Users\Downloads\Scripting\Frame Analyzer\Display_ICO.ico")

# Set Appearence
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Create Label
title = customtkinter.CTkLabel(app, text= "Frame Identifier Tool", font=("Arial", 30))
title.pack(pady=10)

# Creating Grid
grid_frame = customtkinter.CTkFrame(app)

# Create input field
input_dir = customtkinter.CTkEntry(grid_frame, placeholder_text="Place Folder Directory", width= 300)
input_dir.grid(row=0, column = 0, padx= 10, pady=10)

# Create submit dir button
confirm_dir_button = customtkinter.CTkButton(grid_frame, text="->", width = 50, command=Confirm_dir)
confirm_dir_button.grid(row=0, column = 1, pady=10, padx=(0,10), sticky="ew")

grid_frame.pack(pady=10, padx=20)


# Create sys dialogue text
sys_dlg = customtkinter.CTkLabel(app, text="")
sys_dlg.pack(padx=10,pady=(0,10))

# Create Button
button = customtkinter.CTkButton(app, text="Analyze Frames", command=analyze_frames_thread)
button.configure(state="disabled")
button.pack(padx= 10)


app.mainloop()