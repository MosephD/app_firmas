import customtkinter as ctk
from PIL import Image,  ImageDraw, ImageFont
from pathlib import Path
import subprocess
import shutil
import os

# --------------------------------------------


# --------------------------------------------

# THEME
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


# --------------------------------------------
# Loading firma images
# --------------------------------------------
user_homefolder = str(Path.home())
# Loading firma Image File - FRONT
firma_image = Image.open(
    r'assets/Frente.png')

firma_image.save('preview.png')  # Reseting Preview

# Loading firma Font File Location
fonts_folder = r'assets/Fonts/'


#  Selecting firma Font File & Font Size------------------------------------


def changing_font(font_size):
    name_font = ImageFont.truetype(os.path.join(
        fonts_folder, "msjhbd.ttc"), font_size)
    return name_font


# Select the front side image of firma
draw_name = ImageDraw.Draw(firma_image)

# Get front side image Width and Height values
W, H = firma_image.size
# -------------------------------------------------------------


def textbox(current_draw, size):  # Creating textboxes
    _, _, w, h = draw_name.textbbox(
        (0, 0), current_draw, font=changing_font(size))  # aqui esta el pedo
    return w, h


# -------------------------------------------------------------

# Creating APP Window-----------------------------------------------

root = ctk.CTk()
root.geometry("954x686")  # WidthxHeight
root.maxsize(954, 686)
root.title("firmas")

previews_frame = ctk.CTkFrame(
    root, width=954, height=292, fg_color="white")
previews_frame.place(x=0, y=0,)

frame = ctk.CTkFrame(root, width=954, height=394, fg_color="white")
frame.place(x=0, y=292)

root.iconbitmap(r'assets/icon.ico')

# ----------------------------------------------------------------------------------------------------------------Displaying firma preview
# -------------------------------

raw_preview = Image.open(
    'preview.png')

width, height = 954, 266
resized_preview = raw_preview.resize((width, height))

# Convert the resized image to PhotoImage
converted_preview = ctk.CTkImage(resized_preview, size=(954, 266))

# Create a CTkLabel widget to display the image
firma_preview = ctk.CTkLabel(root, image=converted_preview, text=None, )

firma_preview.place(x=0, y=0)

# -------------------------------------------------------------------------
# Exit Button #--------------------


def close_app(event):
    root.destroy()


raw_exit_icon = Image.open(
    r'assets/logout.png')

exit_width, exit_height = 40, 40
resized_exit_icon = raw_exit_icon.resize((exit_width, exit_height))
converted_exit_icon = ctk.CTkImage(resized_exit_icon, size=(40, 40))

exit_icon = ctk.CTkLabel(root, image=converted_exit_icon,
                         text=None, fg_color="white")
exit_icon.place(x=516, y=649)
exit_icon.bind("<Button-1>", close_app)

# Save Button #--------------------


def save_result(event):
    first_name_text = first_name_field.get()
    export_firma_folder = (user_homefolder +
                           '/Downloads/' + first_name_text)
    export_file_name = first_name_text + ".png"
    if os.path.exists(export_firma_folder):
        shutil.rmtree(export_firma_folder)
    os.makedirs(export_firma_folder)
    export_front = (export_firma_folder + '/' +
                    'Frente_' + export_file_name)

    firma_image.save(export_front)

    formatted_path = os.path.normpath(export_firma_folder)
    subprocess.Popen(r'explorer /open,"{}"'.format(formatted_path))


raw_save_icon = Image.open(
    r'assets/save.png')

save_width, save_height = 40, 40
resized_save_icon = raw_save_icon.resize((save_width, save_height))
converted_save_icon = ctk.CTkImage(resized_save_icon,  size=(36, 36))

save_icon = ctk.CTkLabel(root, image=converted_save_icon,
                         text=None, fg_color="white")
save_icon.place(x=455, y=650)
save_icon.bind("<Button-1>", save_result)


# --------------------------------------------------------------------------------------

# Validating user inputs


def validate_name_input(value_if_allowed):
    if len(value_if_allowed) <= 26 and all(c.isalpha() or c.isspace() or c == '.' for c in value_if_allowed):
        return True
    else:
        return False


def validate_position_input(value_if_allowed):
    if len(value_if_allowed) <= 29 and all(c.isalpha() or c.isspace() for c in value_if_allowed):

        return True
    else:
        return False
# ----------------------------------------------


def custom_title(s):
    return ' '.join(word.capitalize() if not word.startswith('.') else word.upper() for word in s.split(' '))

# ----------------------------------------------


# FIRTS NAME INPUT FIELD-------------------------------------------------
first_name_CTkLabel = ctk.CTkLabel(
    root, text="Nombre:", font=("NotoSans-Bold", 20, "bold"),  fg_color="#ffffff", text_color="#595959")

# --------------------------------------------------------------------------------------

first_name_CTkLabel.place(x=256, y=272,)

first_name_field = ctk.CTkEntry(
    root, fg_color="white", corner_radius=7,  width=170, font=("Amiko", 15))
first_name_field.place(x=350, y=273,)
first_name_field.configure(validate="key",
                           validatecommand=(root.register(validate_name_input), '%P'))

# --------------------------------------------

# -------------------------------------------
# Storing First Name Input entry-------------------------------------------


def draw_first_name_text():
    global changing_font, converted_preview, firma_image
    name_rectangle = Image.open(
        r'assets/name-rectangle.png')
    firma_image.paste(name_rectangle, (705, 26))
    empleado_firstname = ''
    name_font = changing_font(18)
    w, h = textbox(empleado_firstname, 18)
    first_name_text = first_name_field.get()  # get the text from the input field
    first_name_input = first_name_text
    empleado_firstname = custom_title(first_name_input)
    draw_name.text(((W-w)/2+240, ((H-h)/2-112)), empleado_firstname.title(),
                   font=name_font, fill='white',)


def save_text():
    firma_image.save('preview.png')
    raw_preview = Image.open(
        'preview.png')
    resized_preview = raw_preview.resize((width, height))
    converted_preview = ctk.CTkImage(resized_preview, size=(954, 266))
    firma_preview.configure(root, image=converted_preview, text=None)


def store_firstname_text(event):  # store first name
    global empleado_firstname
    draw_first_name_text()
    save_text()


# Store field user input with a button
add_firstname_button = ctk.CTkButton(
    root, text="+", width=24, height=24,   font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff")
add_firstname_button.place(x=530, y=274,)
# Bind the field user input storing to keys and click
add_firstname_button.bind("<Button-1>",  store_firstname_text)
first_name_field.bind("<Return>", store_firstname_text)
first_name_field.bind("<Tab>", store_firstname_text)

# -----------------------------------------------

# POSITION-----------------------------------------------------------------------


# POSITION INPUT FIELD-------------------------------------------------
position_CTkLabel = ctk.CTkLabel(
    root, text="Puesto:", font=("NotoSans-Bold", 20, "bold"),  fg_color="#ffffff", text_color="#595959")
# --------------------------------------------------------------------------------------


position_CTkLabel.place(x=256, y=312,)
position_field = ctk.CTkEntry(
    root, fg_color="white", corner_radius=7,  width=170, font=("Amiko", 15))
position_field.place(x=350, y=313,)
position_field.configure(validate="key",
                         validatecommand=(root.register(validate_name_input), '%P'))

# --------------------------------------------

# -------------------------------------------
# Storing First Name Input entry-------------------------------------------


def draw_position_text():
    global changing_font, converted_preview, firma_image
    position_rectangle = Image.open(
        r'assets/position-rectangle.png')
    firma_image.paste(position_rectangle, (672, 48))
    empleado_position = ''
    name_font = changing_font(17)
    w, h = textbox(empleado_position, 17)
    position_text = position_field.get()  # get the text from the input field
    position_input = position_text
    empleado_position = custom_title(position_input)
    draw_name.text(((W-w)/2+212, ((H-h)/2-91)), empleado_position.title(),
                   font=name_font, fill='white',)


def store_position_text(event):  # store first name
    global empleado_position
    draw_position_text()
    save_text()


# Store field user input with a button
add_position_button = ctk.CTkButton(
    root, text="+", width=24, height=24,   font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff")

add_position_button.place(x=530, y=314,)
# Bind the field user input storing to keys and click
add_position_button.bind("<Button-1>",  store_position_text)
position_field.bind("<Return>", store_position_text)
position_field.bind("<Tab>", store_position_text)

# ----------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------


root.mainloop()
