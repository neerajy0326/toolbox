import tkinter as tk
from tkinter import filedialog
from PIL import Image
import uuid
import threading ,time
from tkinter import ttk


def encode_image(source_img_path, message,output_img_path):
    source_img = Image.open(source_img_path)
    message += "\0"  
    

    bin_message = ''.join(format(ord(char), '08b') for char in message)
    message_length = len(bin_message)
   

    
    
    img_width, img_height = source_img.size
    max_message_size = img_width * img_height * 3 // 8  
   
    if message_length > max_message_size:
        result_label.config(text="Message is too large for the image.")
        return
    
    encoded_img = source_img.copy()
    pixels = encoded_img.load()
    

    
    message_index = 0

    start_time = time.time()
    for i in range(img_width):
        for j in range(img_height):
            pixel = list(pixels[i, j])
            for c in range(3): 
                if message_index < message_length:
                    pixel[c] &= 0xFE  
                    pixel[c] |= int(bin_message[message_index])
                    message_index += 1
            pixels[i, j] = tuple(pixel)
    
    encoded_img.save(output_img_path)
    end_time = time.time()  
    execution_time = end_time - start_time
    result_label.config(text=f"Message encoded in {execution_time:.4f} seconds.")
   

def choose_source_image():
    source_img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png"), ("Image files", "*.jpg"), ("Image files", "*.jpeg")])
    source_image_entry.delete(0, tk.END)
    source_image_entry.insert(0, source_img_path)

def encode_button_clicked():
    source_img_path = source_image_entry.get()
    unique_id = str(uuid.uuid4())
    output_img_path =  f"images/encoded_image_{unique_id}.png"  
    message = message_entry.get()
   
    
   
  
    encode_thread = threading.Thread(target=encode_image_thread, args=(source_img_path, message, output_img_path))
    encode_thread.start()

    
    
def encode_image_thread(source_img_path, message, output_img_path):
    def update_result_label(text):
        result_label.config(text=text)
    update_result_label("Encoding in progress...")
    encode_image(source_img_path, message, output_img_path)
    
    


def decode_image(encoded_img_path):    
    encoded_img = Image.open(encoded_img_path)
    pixels = encoded_img.load()
    
    message_bits = []
    for i in range(encoded_img.width):
        for j in range(encoded_img.height):
            pixel = list(pixels[i, j])
            for c in range(3):
                message_bits.append(str(pixel[c] & 1)) 
    message_bits = ''.join(message_bits)
    
    decoded_message = ""
    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i + 8]
        decoded_message+= chr(int(byte, 2))
        if byte == "00000000":
            break
    
    
         
    
    return decoded_message
    


def choose_encode_image():   
    encoded_img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png"), ("Image files", "*.jpg"), ("Image files", "*.jpeg")])
    encoded_image_entry.delete(0, tk.END)
    encoded_image_entry.insert(0, encoded_img_path)

def decode_button_clicked():
    encoded_img_path = encoded_image_entry.get()
    if encoded_img_path:
        
       
        decode_thread = threading.Thread(target=decode_image_threaded, args=(encoded_img_path,))
        decode_thread.start()
    
def decode_image_threaded(encoded_img_path):
    def update_result_label(text):
        result_label.config(text=text)
    
    update_result_label("Decoding in progress...")
    decoded_message = decode_image(encoded_img_path)
    update_result_label("Decoded Message: " + decoded_message) 


root = tk.Tk()
root.title("Steganography Tool")
root.configure(bg='lightgrey')



notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill='both', expand=True)

encode_tab = ttk.Frame(notebook)
notebook.add(encode_tab, text='Encode')



title_label = tk.Label(encode_tab, text="Hide your message inside images", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=3, pady=20)

source_image_label = tk.Label(encode_tab, text="Select Source Image:")
source_image_label.grid(row=1, column=0, padx=10, pady=10)

source_image_entry = tk.Entry(encode_tab, width=40)
source_image_entry.grid(row=1, column=1, padx=10, pady=10)

source_image_button = tk.Button(encode_tab, text="Browse", command=choose_source_image)
source_image_button.grid(row=1, column=2, padx=10, pady=10)
source_image_button.configure(bg="blue", fg="blue")

message_label = tk.Label(encode_tab, text="Enter Message:")
message_label.grid(row=2, column=0, padx=10, pady=10)

message_entry = tk.Entry(encode_tab, width=40)
message_entry.grid(row=2, column=1, padx=10, pady=10)

encode_button = tk.Button(encode_tab, text="Encode", command=encode_button_clicked)
encode_button.grid(row=3, column=1, padx=10, pady=10)
encode_button.configure(bg="blue", fg="green")

decode_tab = ttk.Frame(notebook)
notebook.add(decode_tab, text='Decode')

title_label = tk.Label(decode_tab, text="Reveal messages", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=3, pady=20)

encoded_image_entry = tk.Entry(decode_tab, width=70)
encoded_image_entry.grid(row=1, column=1, padx=10, pady=10,  columnspan=1)

encoded_image_button = tk.Button(decode_tab, text="Select encoded image", command=choose_encode_image)
encoded_image_button.grid(row=2, column=1, padx=10, pady=10,  columnspan=1)

decode_button = tk.Button(decode_tab, text="Decode", command=decode_button_clicked)
decode_button.grid(row=3, column=1, padx=10, pady=10,  columnspan=1)
decode_button.configure(bg="blue", fg="green")

quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 12, "italic"))
result_label.pack(pady=20)



root.mainloop()
