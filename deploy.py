import tkinter
import customtkinter
from PIL import ImageTk, Image

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # creating cutstom tkinter window
app.geometry("400x340")
app.title('AI VIRTUAL MOUSE')

img1 = ImageTk.PhotoImage(Image.open("bg.jpg"))
l1 = customtkinter.CTkLabel(master=app, image=img1)
l1.pack()


app.mainloop()