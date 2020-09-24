from tkinter import *
from tkinter import filedialog
import time
import pygame
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk() #instance is created of TKinter
root.title("My MP3 Player")
root.geometry("600x450")


#initialize pygame
pygame.mixer.init()

def play_time():
	if stopped:
		return
	current_time = pygame.mixer.music.get_pos()/1000
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
	#status_bar.config(text=f'Time Elapsed: {converted_current_time}')
	#check time every second
	
	song = playlist_box.get(ACTIVE)
	song = f'D:/mp3/audio/{song}.mp3'
    #find current song length
	song_mut = MP3(song)
	global song_length
	song_length = song_mut.info.length
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

	if int(song_slider.get()) == int(song_length):
		stop()

	elif paused:
		song_slider.config(value=current_time)
	else:
		next_time = int(song_slider.get()) + 1
		song_slider.config(to=song_length, value=next_time)

		converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')
	

	


	if current_time > 0:
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')
	status_bar.after(1000, play_time)




def add_song():
	song = filedialog.askopenfilename(initialdir='audio/', title='Choose a song', filetypes=(("mp3 Files", "*.mp3" ), ))
	#strip directory from song name
	song = song.replace("D:/mp3/audio/","")
	song = song.replace(".mp3","")
	playlist_box.insert(END, song)


def add_multiple_songs():
	songs = filedialog.askopenfilenames(initialdir='audio/', title='Choose a song', filetypes=(("mp3 Files", "*.mp3" ), ))
	#loop through list and replace dir
	for song in songs:
		song = song.replace("D:/mp3/audio/","")
		song = song.replace(".mp3","")
		playlist_box.insert(END, song)
	
	
#function to delete songs

def delete_song():
	playlist_box.delete(ANCHOR)


def delete_all_songs():
	playlist_box.delete(0, END)


#create play function
def play():
	global stopped
	stopped = False
	#reconstust dir of song
	song = playlist_box.get(ACTIVE)
	song = f'D:/mp3/audio/{song}.mp3'

	#play song using pygame
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	play_time()

global stopped
stopped = False

	
#create stop function
def stop():
	pygame.mixer.music.stop()
	playlist_box.selection_clear(ACTIVE)
	status_bar.config(text='Song Stopped ')
	#song_slider.config(text='')
	song_slider.config(value=0)

	global stopped
	stopped = True


#pause function
global paused 
paused = False

# Create Pause Function
def pause():
	global paused
	#paused = is_paused

	if paused:
		#Unpause
		pygame.mixer.music.unpause()
		paused = False
	else:
		#Pause
		pygame.mixer.music.pause()
		paused = True


def next_song():
	#reset slider pos and status bar
	status_bar.config(text='')
	song_slider.config(value=0)
	next_one = playlist_box.curselection()
	next_one = next_one[0] + 1
	song = playlist_box.get(next_one)
	song = f'D:/mp3/audio/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	playlist_box.selection_clear(0, END)
	playlist_box.activate(next_one)
	playlist_box.selection_set(next_one, last=None)


def previous_song():

	status_bar.config(text='')
	song_slider.config(value=0)
	next_one = playlist_box.curselection()
	next_one = next_one[0] - 1
	song = playlist_box.get(next_one)
	song = f'D:/mp3/audio/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	playlist_box.selection_clear(0, END)
	playlist_box.activate(next_one)
	playlist_box.selection_set(next_one, last=None)

#create volume function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())
	
#create slide funtion for song position
def slide(y):
	song = playlist_box.get(ACTIVE)
	song = f'D:/mp3/audio/{song}.mp3'

	#play song using pygame
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start=song_slider.get())

#create main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

#create volume slider frame
volume_frame= LabelFrame(main_frame, text="Volume", padx=20)
volume_frame.grid(row=0, column=1)

#create volume slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, length=125, value=1, command=volume)
volume_slider.pack(pady=10)

#create song slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=20)

# create playlist box
playlist_box = Listbox(main_frame, bg="black", fg="yellow", width=60, selectbackground="green", selectforeground="black") # contains list of widgets
playlist_box.grid(row=0, column=0) #padding above and below

#define button controls images
back_img = PhotoImage(file='images/back.png')
forward_img = PhotoImage(file='images/forward.png')
play_img = PhotoImage(file='images/play.png')
pause_img = PhotoImage(file='images/pause.png')
stop_img = PhotoImage(file='images/stop.png')


#create buttons frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)
 
#create buttons
back = Button(control_frame, image=back_img, borderwidth=0, command=previous_song)
forward = Button(control_frame, image=forward_img, borderwidth=0, command=next_song)
play = Button(control_frame, image=play_img, borderwidth=0, command=play)
pause = Button(control_frame, image=pause_img, borderwidth=0, command=pause)
stop = Button(control_frame, image=stop_img, borderwidth=0, command=stop)

back.grid(row=0, column=0, padx=10)
forward.grid(row=0, column=1, padx=10)
play.grid(row=0, column=2, padx=10)
pause.grid(row=0, column=3, padx=10)
stop.grid(row=0, column=4, padx=10)


#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#add song menu dropdowns
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add one song", command=add_song)
add_song_menu.add_command(label="Add multiple songs", command=add_multiple_songs)

#delete song dropdowns
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)



#create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X,side=BOTTOM, ipady=2)



my_label = Label(root, text='')
my_label.pack(pady=20)

root.mainloop()  #allows the program to run