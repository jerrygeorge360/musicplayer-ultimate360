import os, time
from mutagen.mp3 import MP3
import tkinter as window
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from pygame import mixer
from PIL import Image, ImageTk
import stagger
import io

mixer.init()
from tkinter import PhotoImage


def picturechecker():
    from PIL import Image, ImageTk
    import stagger
    import io
    mp3 = stagger.read_tag()
    by_data = mp3[stagger.id3.APIC][0].data
    im = io.BytesIO(by_data)
    imageFile = Image.open(im)
    photo = ImageTk.PhotoImage(imageFile)


class musicplayer(window.Tk):

    def __init__(self):
        super().__init__()

        self.count = -1
        self.title('ULTIMATE360')
        self.resizable(width=False, height=False)
        self.iconphoto(False, PhotoImage(file='icon image.png'))
        self.geometry('700x500')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.popup = Menu(self, tearoff=0)
        self.bigimage = PhotoImage(file='big.png')
        self.image0 = PhotoImage(file='back.png')
        self.image1 = PhotoImage(file='replay.png')
        self.image2 = PhotoImage(file='play.png')
        self.image3 = PhotoImage(file='pause.png')
        self.image4 = PhotoImage(file='next.png')
        self.image5 = PhotoImage(file='folder.png')



        # self.defaultpath = os.listdir(r'.\musicfolder')

        self.header = Frame(self, width=700, height=100, bg='grey')
        self.header.grid(row=0, column=0)

        self.body = Frame(self, width=700, height=300, bg='blue')
        self.body.grid(row=1, column=0, sticky='nwse')
        self.body.rowconfigure(0, weight=1)
        self.body.columnconfigure(0, weight=1)
        self.body.columnconfigure(1, weight=1)
        self.body.rowconfigure(1, weight=1)

        self.leftbody = Frame(self.body, width=350, height=300, bg='black')
        self.leftbody.grid(row=0, column=0, sticky='nwse')
        self.leftbody1 = Frame(self.leftbody, width=350, height=200, bg='black')
        self.leftbody1.grid(row=0, column=0)

        self.bigimagecenter = Frame(self.leftbody1, bg='black', width=200, height=200)
        self.bigimagecenter.place(anchor='center', relx=0.5, rely=0.5)
        self.imageLabel = Label(self.bigimagecenter, image=self.bigimage)
        self.imageLabel.place(anchor='center', relx=0.5, rely=0.5)
        self.status = Label(self.leftbody1, text='length', bd=1, bg='black', relief=GROOVE, anchor=E)
        self.status.place(x=280, y=180)
        self.leftbody2 = Frame(self.leftbody, width=350, height=100, bg='white')
        self.leftbody2.grid(row=1, column=0, sticky='nwse')

        self.rightbody = Frame(self.body, width=350, height=300, bg='yellow')
        self.rightbody.grid(row=0, column=1, sticky='nwse')
        self.rightinner = Frame(self.rightbody, width=350, height=300, bg='orange')
        self.rightinner.pack(expand=True)

        self.scrollbar = Scrollbar(self.rightinner)

        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.list = Listbox(self.rightinner, bg='black', fg='purple', cursor='dot', width=58, height=30,
                            yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.list.yview)
        self.list.pack(expand=True)

        self.bottom = Frame(self, width=700, height=100, bg='grey')
        self.bottom.grid(row=2, column=0)

        self.Button0 = Button(self.leftbody2, width=40, height=40, image=self.image0, bg='black',
                              command=self.previousmusic)
        self.Button0.place(x=4, y=20)

        self.Button1 = Button(self.leftbody2, width=40, height=40, image=self.image1, bg='black', command=self.rewind)
        self.Button1.place(x=65, y=20)

        self.Button2 = Button(self.leftbody2, width=40, height=40, image=self.image2, bg='black', command=self.play)
        self.Button2.place(x=126, y=20)

        self.Button3 = Button(self.leftbody2, width=40, height=40, image=self.image3, bg='black',
                              command=self.pauseunpause)
        self.Button3.place(x=182, y=20)

        self.Butoton4 = Button(self.leftbody2, width=40, height=40, image=self.image4, bg='black',
                               command=self.nextmusic)
        self.Butoton4.place(x=240, y=20)

        self.Button5 = Button(self.leftbody2, width=40, height=40, image=self.image5, bg='black', command=self.folder)
        self.Button5.place(x=300, y=20)

        self.slide = Scale(self.leftbody2, length=330, from_=0, to=100, orient=HORIZONTAL, width=5,
                           highlightcolor='red', sliderrelief='ridge', bg='purple', border=0, showvalue=False,
                           troughcolor='#432690', command=self.slider)
        self.slide.place(x=3, y=74)

        self.volume = Scale(self.leftbody2, length=330, from_=0, to=100, orient=HORIZONTAL, width=5,
                            highlightcolor='red', sliderrelief='ridge', bg='white', border=0, showvalue=False,
                            troughcolor='black', command=self.volume1)
        self.volume.place(x=3, y=90)
        self.bind("<Button-3>", self.menu_popup)
        self.popup.add_command(label='delete', command=self.delete)

        # self.my_slider = ttk.Scale(self.leftbody1,from_=0, to = 100, orient = HORIZONTAL, value=0,length=120)
        # self.my_slider.grid(row=2,column=2)
        # self.default()
        self.mainloop()
    def delete(self):
        print('deleted')

        self.list.delete(self.list.curselection())

    def menu_popup(self, event):
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup.grab_release()

    def folder(self):

        self.path = filedialog.askdirectory(title='choose folder where your music is located.')
        for i in os.listdir(self.path):
            counter = 1
            self.list.insert(counter, i)
            self.contain = os.listdir(self.path)

    def playtime(self):
        self.current_time = int(mixer.music.get_pos() / 1000)
        convert = time.strftime('%M:%S', time.gmtime(self.current_time))

        currnt_one = self.list.curselection()
        song = self.list.get(currnt_one)
        song = self.path + '\\' + song
        song_mut = MP3(song)
        self.song_lenght = song_mut.info.length
        convert_lenght = time.strftime("%M:%S", time.gmtime(self.song_lenght))

        if int(self.slide.get()) == int(self.current_time):

            self.slidepos = self.song_lenght
            self.slide.config(to=int(self.slidepos))
            self.slide.set(value=(self.current_time))




        else:
            mixer.music.play(start=self.slide.get())
            self.slidepos = self.song_lenght
            self.slide.config(to=int(self.slidepos))
            self.slide.set(value=int(self.slide.get()))
            convert = time.strftime('%M:%S', time.gmtime(int(self.slide.get())))
            # self.value = self.list.get(ACTIVE)
            # mixer.music.load(filename=self.path + '\\' + self.value)

            self.status.config(text=f'{convert}/{convert_lenght}', bg='black', fg='white')
            next_time = int(self.slide.get()) + 1
            self.slide.set(value=next_time)
        # print(self.current_time)
        # print(self.slide.get())
        # self.status.config(text=f'{convert}/{convert_lenght}',bg='black',fg='white')

        self.status.after(1000, self.playtime)

    pcounter = 0

    def play(self):

        self.boxlist = [i for i in self.list.curselection()]

        self.value = self.list.get(self.boxlist[0])

        # music_image = ID3(thefile)
        # pict=music_image.get("APIC:")
        # print(pict)
        # print(type(music_image))
        mixer.music.load(filename=self.path + '\\' + self.value)
        mixer.music.play()
        if self.pcounter == 0:

            try:
                mixer.music.load(filename=self.path + '\\' + self.value)
                mp3 = stagger.read_tag(filename=self.path + '\\' + self.value)
                by_data = mp3[stagger.id3.APIC][0].data
                im = io.BytesIO(by_data)
                image_file = Image.open(im)
                photo = ImageTk.PhotoImage(image_file)
            except:
                self.imagecheck()
                self.bigimage = PhotoImage(file='big.png')

            mixer.music.play()

        self.playtime()
        self.volume1(int(self.volume.get()) / 100)

    def nextmusic(self):
        self.slide.set(value=0)
        next_one = self.list.curselection()
        next_one = next_one[0] + 1
        song = self.list.get(next_one)
        mixer.music.load(filename=self.path + '\\' + song)
        mixer.music.play()
        print(song)
        self.list.selection_clear(0, END)
        self.list.activate(next_one)
        self.list.selection_set(next_one, last=None)
        self.volume1(int(self.volume.get()) / 100)

    def previousmusic(self):
        self.slide.set(value=0)
        next_one = self.list.curselection()
        next_one = next_one[0] - 1
        song = self.list.get(next_one)
        mixer.music.load(filename=self.path + '\\' + song)
        mixer.music.play()
        print(song)
        self.list.selection_clear(0, END)
        self.list.activate(next_one)
        self.list.selection_set(next_one, last=None)
        self.volume1(int(self.volume.get()) / 100)

    def rewind(self):

        self.slide.set(value=0)
        self.volume1(int(self.volume.get()) / 100)

    def slider(self, x):

        # self.value = self.list.get(ACTIVE)
        # mixer.music.load(filename=self.path + '\\' + self.value)
        # mixer.music.play(start=self.slide.get())
        pass

    def volume1(self, x):
        mixer.music.set_volume(int(self.volume.get()) / 100)

    def pauseunpause(self):

        if self.count % 2 == 0:

            # self.slide.set(value=self.slide.get())
            mixer.music.pause()
        elif self.count % 2 != 1:
            mixer.music.unpause()
        self.count += 1
        print(self.count)


musicplayer()
