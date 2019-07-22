import random
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
import os
import pygame
import pygame.event
from mutagen.id3 import ID3
from mutagen.mp3 import MP3

root = Tk()
root.title("Player")
root.geometry("380x185+200+200")
root.configure(background='white')
# root.resizable(0, 0)

# Просто изображение для красоты
photo_bear = PhotoImage(file="./assets/buttons/png/small_bear.png")
bear = Label(image=photo_bear, background='white')
bear.grid(row=1, column=5, sticky=NE, columnspan=7, rowspan=3)

playlist = Listbox(master=root, selectmode=SINGLE)
playlist.grid(row=3, column=0, columnspan=10, sticky=NW)

pygame.mixer.init()

list_of_songs = []  # Список с названиями песен для загрузки
real_names = []  # Список реальных названий композиций для отображения в окне плеера

index = 0  # Номер трека в списке для загрузки текущего трека
loop = 0  # Количество повторов, принимает значения 0 и -1 в зависимости от состояния кнопки repeat
song_name = StringVar()  # Название трека


# Выбор папки с музыкой, вызывается кнопкой open
def manage_playlist(one_file_flag, adding=False):
    global index
    global list_of_songs
    global real_names
    global current_track_time

    playlist.delete(0, len(list_of_songs) - 1)

    if not adding:
        list_of_songs = []
        real_names = []
        index = 0
        current_track_time = 0
        time_var.set(current_track_time)

    filenames = []
    if one_file_flag:
        name = askopenfilename()
        if name.endswith("mp3"):
            filenames.append(name)
    else:
        directory = askdirectory()
        os.chdir(directory)
        for name in os.listdir(directory):
            if name.endswith("mp3"):
                filenames.append(name)

    for name in filenames:
        # Составление списка реальных названий композиций
        realdir = os.path.realpath(name)
        audio = ID3(realdir)
        real_names.insert(len(list_of_songs), audio['TIT2'].text[0])

        # Составление списка имён музыкальных файлов
        list_of_songs.append(name)

    if not adding:
        pygame.mixer.music.load(list_of_songs[index])
        pygame.mixer.music.play()
        root.after(0, update_position)
        update_label()

    add_to_playlist()


def add_to_playlist():
    real_names.reverse()

    for items in real_names:
        playlist.insert(0, items)  # Добавляются не туда!

    real_names.reverse()


def open_folder():
    manage_playlist(False, False)


def open_file():
    manage_playlist(True, False)


def add_folder():
    manage_playlist(False, True)


def add_file():
    manage_playlist(True, True)


# Кнопка открытия папки с файлами
photo_open_file = PhotoImage(file="./assets/buttons/png/open.png")
open_menu = Menubutton(master=root, image=photo_open_file, bd=0, bg="white")
open_menu.grid(row=0, column=0, sticky=NW, columnspan=2)
open_menu.menu = Menu(master=open_menu)
open_menu["menu"] = open_menu.menu  # назначаем Menu ID??
open_menu.menu.add_command(label="Open Folder", command=open_folder)
open_menu.menu.add_command(label="Open File", command=open_file)
open_menu.menu.add_command(label="Add Folder to Playlist", command=add_folder)
open_menu.menu.add_command(label="Add File to Playlist", command=add_file)


# Функция отображения названия текущей композиции, обновляет соотв. метку
def update_label():
    global index

    song_name.set(real_names[index])


# Метка с названием текущей композиции
song_label = Label(root, textvariable=song_name, width=30)
song_label.grid(row=1, column=0, sticky=NW, columnspan=6)


# Следующая композиция. Выбирается случайным образом, если флаг playing_random == True
def next_song():
    global playing_random
    global loop
    global index
    global current_track_time

    current_track_time = 0

    if playing_random:
        index = random.randint(0, len(list_of_songs) - 1)
    else:
        index += 1
        if index >= len(list_of_songs):
            index = 0

    pygame.mixer.music.load(list_of_songs[index])
    pygame.mixer.music.play(loop)

    update_label()


# Кнопка воспроизведения следующей композиции
photo_next = PhotoImage(file="./assets/buttons/png/next_song.png")  # next and peremotka vpered
next_song_button = Button(master=root, image=photo_next, bd=0, command=next_song, background='white')
next_song_button.grid(row=2, column=4, sticky=SW)
root.grid_rowconfigure(1, minsize=110)


# Предыдущая композиция. Выбирается случайным образом, если флаг playing_random == True
def previous_song():
    global playing_random
    global loop
    global index
    global current_track_time

    current_track_time = 0

    if playing_random:
        index = random.randint(0, len(list_of_songs) - 1)
    else:
        index -= 1
        if index == -1:
            index = 0

    pygame.mixer.music.load(list_of_songs[index])
    pygame.mixer.music.play(loop)

    update_label()


# Кнопка воспроизведения предыдущей композиции
photo_prev = PhotoImage(file="./assets/buttons/png/previous.png")  # prev and peremotka nazad
previous = Button(master=root, image=photo_prev, bd=0, command=previous_song, background='white')
previous.grid(row=2, column=3, sticky=SW)


# Пауза
def pause_song():
    pygame.mixer.music.pause()


# Кнопка паузы
photo_pause = PhotoImage(file="./assets/buttons/png/pause.png")
pause = Button(master=root, image=photo_pause, bd=0, command=pause_song, background='white')
pause.grid(row=2, column=1, sticky=SW)


# Воспроизведение
def play_song():
    global loop
    global playback_stopped

    playback_stopped = False

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(loop)
    else:
        pygame.mixer.music.unpause()

    update_label()


# Кнопка воспроизведения
photo_play = PhotoImage(file="./assets/buttons/png/play.png")
play = Button(master=root, image=photo_play, bd=0, command=play_song, background='white')
play.grid(row=2, column=0, sticky=SW)

playback_stopped = False


# Остановка воспроизведения
def stop_song():
    global playback_stopped
    global current_track_time

    playback_stopped = True
    pygame.mixer.music.stop()
    current_track_time = 0
    scale_pos.set(0)

    song_name.set("")
    time_var.set(0)


# Кнопка остановки воспроиздведения
photo_stop = PhotoImage(file="./assets/buttons/png/stop.png")
stop = Button(master=root, image=photo_stop, bd=0, command=stop_song, background='white')
stop.grid(row=2, column=2, sticky=SW)


# Настройка громкости по шкале
def set_volume(self):
    volume = scale.get()
    if type(volume) == int:
        volume = float(volume / 100)
    pygame.mixer.music.set_volume(float(volume))


# Шкала громкости
scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=120, command=set_volume, background='white', bd=0,
              highlightbackground='white', sliderlength=20)
scale.grid(row=2, column=7, sticky=NE, columnspan=5)
scale.set(100)

# Метка с изображением к шкале громкости для красоты
photo_sound_label = PhotoImage(file="./assets/buttons/png/sound.png")
sound_label = Label(image=photo_sound_label, background='white')
sound_label.grid(row=2, column=6, sticky=SE)
root.grid_columnconfigure(5, minsize=50)

# Шкала времени. current_track_time служит для отсчета времени текущей композиции
current_track_time = 0  # in seconds
time_var = IntVar()
time_var.set(current_track_time)

time_label = Label(master=root, textvariable=time_var)
time_label.grid(row=1, column=0, sticky=SW)


# Обновление шкалы времени
def update_position():
    global index
    global current_track_time

    if len(list_of_songs) != 0:
        song = MP3(list_of_songs[index])
        current_song_length = song.info.length

        if pygame.mixer.music.get_busy():
            scale_pos.set(current_track_time / current_song_length * 100)
            current_track_time += 1
            time_var.set(int(current_track_time))

    if not pygame.mixer.music.get_busy() and not playback_stopped:
        index += 1
        pygame.mixer.music.load(list_of_songs[index])
        pygame.mixer.music.play()
        scale_pos.set(0)
        current_track_time = 0
        time_var.set(current_track_time)

    root.after(1000, update_position)


# Перемотка композиции при помощи шкалы времени
def change_time(self):
    global index
    global current_track_time

    song = MP3(list_of_songs[index])
    current_song_length = song.info.length

    pygame.mixer.music.rewind()
    pygame.mixer.music.set_pos(current_song_length / 100 * scale_pos.get())
    current_track_time = current_song_length / 100 * scale_pos.get()


# Шкала времени
scale_pos = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=150, background='white',
                  bd=0, highlightbackground='white', sliderlength=20, showvalue=0)
scale_pos.grid(row=1, column=1, sticky=SW, columnspan=5)
scale_pos.bind("<ButtonRelease-1>", change_time)


# Повторение трека
def repeat_track():
    global current_track_time
    global index
    global loop

    if not loop == -1:
        loop = -1
        repeat_track.configure(relief=SUNKEN, bd=1, bg="blue")
    else:
        loop = 0
        repeat_track.configure(relief=RAISED, bd=0, bg="white")

    pygame.mixer.music.stop()
    pygame.mixer.music.play(loop)
    pygame.mixer.music.set_pos(current_track_time)


# Кнопка повторения трека
photo_repeat_track = PhotoImage(file="./assets/buttons/png/repeat.png")
repeat_track = Button(master=root, image=photo_repeat_track, bd=0, bg="white",
                      command=repeat_track)
repeat_track.grid(row=0, column=1, sticky=NW, columnspan=2)

# Воспроизведение случайного трека (флаг playing_random изменяет работу методов next_song и previous_song
playing_random = False


# Проигрывание случайного трека
def random_track():
    global playing_random

    if not playing_random:
        playing_random = True
        random_track.configure(relief=SUNKEN, bd=1, bg="blue")
    else:
        playing_random = False
        random_track.configure(relief=RAISED, bd=0, bg="white")


# Кнопка воспроизведения случайного трека из списка
photo_random_track = PhotoImage(file="./assets/buttons/png/shuffle.png")
random_track = Button(master=root, image=photo_random_track, bd=0, bg="white",
                      command=random_track, relief=RAISED)
random_track.grid(row=0, column=2, sticky=NW, columnspan=2)

root.mainloop()
