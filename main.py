import subprocess
import platform
import torch
from gtts import gTTS
import tempfile
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

# Initialize the transformer model and components
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Create the main window
root = tk.Tk()
root.title("Image Caption Generator")

# Create a function for switching between login and main pages
def show_login_page():
    main_frame.pack_forget()
    login_frame.pack()

def show_main_page():
    login_frame.pack_forget()
    main_frame.pack()
    
# Function to show the registration page
def show_registration_page():
    login_frame.pack_forget()
    registration_frame.pack()
    
# Function to hide the registration page
def hide_registration_page():
    registration_frame.pack_forget()


# Function to open image files and display them
def open_images():
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        image_paths_listbox.delete(0, tk.END)
        for file_path in file_paths:
            image_paths_listbox.insert(tk.END, file_path)
            display_selected_image(file_path)

def display_selected_image(image_path):
    img = Image.open(image_path)
    img.thumbnail((300, 300), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    selected_image_label.config(image=img)
    selected_image_label.image = img
    
def text_to_speech(text):
    tts = gTTS(text, lang='en')  # Create a gTTS object with the text and language ('en' for English)
    temp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")  # Create a temporary MP3 file
    tts.save(temp_mp3.name)  # Save the audio to the temporary file
    
    # Determine the appropriate audio player command based on the operating system
    if platform.system() == "Darwin":  # macOS
        audio_player_cmd = f"afplay {temp_mp3.name}"
    elif platform.system() == "Linux":  # Linux
        audio_player_cmd = f"aplay {temp_mp3.name}"
    else:
        raise Exception("Unsupported operating system")
    
    subprocess.call(audio_player_cmd, shell=True)  # Play the audio using the selected command
    os.remove(temp_mp3.name)  # Remove the temporary file




# Function to generate captions for the selected images
def generate_captions():
    image_paths = image_paths_listbox.get(0, tk.END)
    preds = predict_step(image_paths)
    captions_listbox.delete(0, tk.END)
    for pred in preds:
        captions_listbox.insert(tk.END, pred)
        text_to_speech(pred)

def predict_step(image_paths):
    images = []
    for image_path in image_paths:
        i_image = Image.open(image_path)
        if i_image.mode != "RGB":
            i_image = i_image.convert(mode="RGB")

        images.append(i_image)

    pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    output_ids = model.generate(pixel_values, **gen_kwargs)

    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return preds

# Login Frame
login_frame = tk.Frame(root, bg="orange")
login_frame.pack(expand=True, fill='both')
login_frame.configure(bg="orange")
login_label = tk.Label(login_frame, text="Login",bg='grey',fg='white', font=("Helvetica", 24))
login_label.pack(pady=20)
login_label.configure(bg="grey")
username_label = tk.Label(login_frame, text="Username:",bg='grey')
username_label.pack()
username_entry = tk.Entry(login_frame)
username_entry.pack(pady=10)
password_label = tk.Label(login_frame, text="Password:",bg='grey')
password_label.pack()
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack(pady=10)

# Login button
def login():
    username = username_entry.get()
    password = password_entry.get()
    # Add your authentication logic here
    if reg == 1:
        if username==new_usr and password==new_pas:
            show_main_page()
        else:
             messagebox.showerror("Login Failed", "Invalid username or password")
    else :
        if username == "chad" and password == "369":
            show_main_page()  # Switch to the main page
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

login_button = tk.Button(login_frame, text="Login", bg="grey", fg="black", command=login)
login_button.pack(pady=20)

# Registration Frame
registration_frame = tk.Frame(root, bg="orange")
registration_frame.configure(bg="orange")

# Function to handle user registration
def register():
    global reg
    reg = 1
    
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()
    
    global new_usr 
    global new_pas 
    new_usr = new_username
    new_pas = new_password  
    
    print(f"Registered username: {new_username}, password: {new_password}")
    messagebox.showinfo("Registration Successful", "You have successfully registered!")
    
    hide_registration_page()
    # After registration, you can switch back to the login page
    show_login_page()

# Registration page components
registration_label = tk.Label(registration_frame, text="Registration", bg='grey', fg='white', font=("Helvetica", 24))
new_username_label = tk.Label(registration_frame, text="New Username:", bg='grey')
new_username_entry = tk.Entry(registration_frame)
new_password_label = tk.Label(registration_frame, text="New Password:", bg='grey')
new_password_entry = tk.Entry(registration_frame, show="*")
register_button = tk.Button(registration_frame, text="Register", bg="grey", fg="black", command=register)

# Place registration page components
registration_label.pack(pady=20)
new_username_label.pack()
new_username_entry.pack(pady=10)
new_password_label.pack()
new_password_entry.pack(pady=10)
register_button.pack(pady=20)


# Add a "Register" button on the login page to switch to the registration page
register_page_button = tk.Button(login_frame, text="Register", bg="grey", fg="black", command=show_registration_page)
register_page_button.pack(pady=10)

# Main Frame
main_frame = tk.Frame(root, bg="orange")
main_frame.pack(expand=True, fill='both')
main_frame.configure(bg="orange")

# Create and configure GUI elements for the main frame
open_images_btn = tk.Button(main_frame, text="Open Images",bg="grey", fg="black", command=open_images)
generate_captions_btn = tk.Button(main_frame, text="Generate Captions", bg="grey", fg="black", command=generate_captions)
image_paths_label = tk.Label(main_frame, text="Selected Image Paths:",bg='grey',fg='white')
captions_label = tk.Label(main_frame, text="Generated Captions:",bg='grey',fg='white')
image_paths_listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, selectbackground="red", height=5, width=40)
captions_listbox = tk.Listbox(main_frame, height=10, width=40)

# Place GUI elements on the main frame
open_images_btn.pack()
image_paths_label.pack()
image_paths_listbox.pack()
generate_captions_btn.pack()
captions_label.pack()
captions_listbox.pack()

# Create a frame to hold the selected image
selected_image_frame = tk.Frame(main_frame, bg='grey')
selected_image_frame.pack()
selected_image_label = tk.Label(selected_image_frame, text="Selected Image")
selected_image_label.pack()

# Exit button
exit_button = tk.Button(main_frame, text="Exit", bg="red", fg="black", command=root.destroy)
exit_button.pack(pady=20)

# Initially, show the login page
show_login_page()

# Start the main loop
gen_kwargs = {"max_length": 16, "num_beams": 4}
root.mainloop()
