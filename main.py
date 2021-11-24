from PIL import Image
import PySimpleGUI as sg
import os
import math
import threading


class GUI ():
    def __init__(self):
        self.filetype = ["png", "jpg", "jpeg", "gif", "tif", "bmp"]
        sg.theme('DarkGrey1')
        self.layout = [
            [sg.Text('Choose a directory:', size=(35, 1), font=("Helvetica", 15), key="text_dir")],
            [sg.In(), sg.FolderBrowse()],
            [sg.Text('Tilemap width (amount of images, 0 = auto):', size=(35, 1), font=("Helvetica", 15), key="text_images")],
            [sg.Input(default_text="0")],
            [sg.Text('Resolution of Tiles in Px (0 = original size):', size=(35, 1), font=("Helvetica", 15), key="text_resolution")],
            [sg.Input(default_text="0")],
            [sg.Button('Set Tilemap', bind_return_key=True, key='tile')],
            [sg.ProgressBar(100, orientation='h', size=(35, 5), key='progress')],
            [sg.Text('TJ 2021 V1.0 Tiler')]]

    def start(self):
        self.window = sg.Window('Tiler - Create Tilemaps', self.layout)
        self.progress_bar = self.window.FindElement('progress')

        # Display and interact with the Window using an Event Loop
        while True:
            event, values = self.window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break
            if event == 'tile':
                self.window.FindElement('tile').Update(disabled=True)
                def_thread = threading.Thread(target=self.create, args=(values,))
                def_thread.daemon = True
                def_thread.start()
        self.window.close

    def create(self, values):
        images = []
        img_row = int(values[1])
        img_resolution = int(values[2])
        path = values[0]
        files = os.listdir(path)
        # print(files)
        for f in files:
            try:
                filename, fileextension = f.split(".")
            except:
                continue
            if fileextension.lower() in self.filetype:
                images.append(f)
        # print(images)
        im = Image.open(path + "/" + images[0])
        if img_resolution == 0:
            x, y = im.size
        else:
            x, y = img_resolution, img_resolution
        amount_images = len(images)
        if img_row == 0:
            if amount_images > 10:
                temp_width = int(math.sqrt(amount_images))
            else:
                temp_width = amount_images
        else:
            temp_width = int(img_row)
        if amount_images % temp_width > 0:
            new_tilemap_y = int((amount_images / temp_width + 1)) * y
        else:
            new_tilemap_y = int((amount_images / temp_width)) * y
        new_tilemap = Image.new("RGBA", (temp_width * x, new_tilemap_y), (0, 0, 0, 0))
        row_counter = 1
        offset = (0, 0)
        tmp_x = 0
        tmp_y = 0
        progress = 0
        progress_stepper = 99 / amount_images
        for limg in images:
            tmp_img = Image.open(path + "/" + limg)
            tmp_img_resized = tmp_img.resize((x, y), Image.ANTIALIAS)
            if row_counter > temp_width:
                row_counter = 1
                tmp_x = 0
                tmp_y = tmp_y + y

            offset = (tmp_x, tmp_y)
            new_tilemap.paste(tmp_img_resized, offset)
            row_counter = row_counter + 1
            tmp_x = tmp_x + x
            progress = progress + progress_stepper
            self.progress_bar.UpdateBar(progress)
        new_tilemap.save(path + "/tilemap.png")
        self.progress_bar.UpdateBar(0)
        self.window.FindElement('tile').Update(disabled=False)


if __name__ == '__main__':
    tile = GUI()
    tile.start()