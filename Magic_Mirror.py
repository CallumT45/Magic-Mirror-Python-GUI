import tkinter as tk
import time
from cogs import googleCalendar as gC
from cogs import weather
from cogs import news
from cogs import reddit
import datetime
from cogs import Spotify
from cogs import bus

from tkinter import scrolledtext as st
from tkinter import constants as const
from datetime import date
from PIL.ImageTk import PhotoImage
from PIL import Image
from random import choice


def listTostr(lst):
	"""Takes a list as input and outputs as a single string with two newlines between each index"""
	string = ''
	for i in lst:
		string += str(i) + '\n\n'
	return string

#The time with seconds is taken from https://github.com/Avuo/Magic-Mirror-Python
def clock1(time1=''):
	time2 = time.strftime("%H")
	if time2 != time1:
		time1 = time2
		clock_frame.config(text=time2)
	clock_frame.after(200, clock1)

def clock2(time3=''):
	time4 = time.strftime(":%M:%S")
	if time4 != time3:
		time3 = time4
		clock_frame2.config(text=time4)
	clock_frame2.after(200, clock2)



def scroll_textbox(elem):#needs fix
    """Function is responsable to the scrolling headlines, and is an adaption of code from 
    https://python-forum.io/Thread-Tkinter-scrolling-text-in-tkinter?pid=2972"""
    # get the current index
    current = float(elem.index(const.CURRENT))
    new = current
    # keep incrementing the index until it's not visible
    while elem.bbox(new):
        new += 1
    # make sure the new index is visible
    elem.see(new)
    # move the index again in 1250ms
    elem.after(2000, lambda: scroll_textbox(elem))
    if elem.bbox(new) == None:#When the scroll box reaches the bottom return to the top
    	elem.see(1.0)

def welMessage(hour):
	"""Given the hour this function will randomly choose from the lists of predetermined messages"""
	morningMessages = ["Rise and Shine Callum", "G'day Mate!", "Okay first of all, \nbrush your teeth.", "Good Morning Cute Face", "Wake Up Panda", "Good Morning Callum", "Callum Stop Snoring \nand Wake Up", "Good Morning Handsome"]
	nightMessages = ["Goodnight Callum", "Nighty-night", "Buenas Noches", "Bon Nuit", "Sweet Dreams", "Sleep snug as a bug in a rug"]
	afternoonMessages = ["Good Afternoon Callum","There is my pumkin", "Howdy, Partner!", "Hello Honey Bunch", "What's Up Handsome", "Welcome to the Club", "Nice Smile", "You slayer, What's Up?" ]
	insults = ["You have a face for radio", "Jaysus the face on you", "I envy everyone you \nhave never met", "Your mother was a hamster and \nyour father smelled of elderberries!", "I do desire we may \nbe better strangers", "You consistently meet \nmy expectations","Is your Family Tree a circle?", "Your grades say marry rich, \nbut your face says study harder.", "You're so ugly, \nyou couldn't even arouse suspicion" ]

	if 4 <= hour < 12:
	    message = choice(morningMessages+insults)
	elif 12 <= hour < 17:
	    message = choice(afternoonMessages+insults)
	elif 17 <= hour < 20:
	    message = 'Good Evening Callum!'
	elif 20 <= hour < 24:
		message = choice(nightMessages+insults)
	elif 0 <= hour < 4:
	    message = 'Time to ride the rainbow to dreamland!'
	else:
		message = "What's Up Callum"
	return message

def refresh():
	"""Updates the scrolling widget with reddit and newsheadlines, this function is run every 3 hours"""
	redditFeed = reddit.main()
	newsHead = news.main()
		
	headStr = listTostr(newsHead)
	RedditStr = listTostr(redditFeed)
	TotalStr = headStr + RedditStr
	#=======================================
		
	stext.delete('1.0', const.END)
	stext.insert(const.END,TotalStr) 
	root.after(10800000, refresh)

def shortRefresh():
	"""Updates the date, welcome message and current temperature every 20 mins"""
	my_date = date.today()
	currentTime = datetime.datetime.now()
	hour = currentTime.hour
	message = welMessage(hour)
	currentTemp = weather.currentTemp()
	currentTempStr = str(currentTemp) + str(u"\u2103")

	dateframe.config(text=my_date.strftime("%A %d, %B %Y"))#converts format to weekday, day, month and year
	WelcomeMessage.config(text=message)
	WeatherTemp.config(text=currentTempStr)
	root.after(1200000, shortRefresh)


def updateWeatherEvents():
	"""Function which updates every 61 mins. The token for spotify expires after an hour, until it refreshes, the Spot
	refresh idles. Weather and events are also updated"""
	global token
	# weatherRefresh()
	eventRefresh()
	token = Spotify.getToken()
	root.after(3660000, updateWeatherEvents)

# def weatherRefresh():
# 	"""Gets the weather forecast for the next 24 hours, if this is not none then, update the 5th column(time) and try to 
# 	update the 6th column(weather). If no image exists with the name, then print the text version of the weather."""
# 	global weatherCells
# 	weatherForecast = weather.weatherFor()

# 	if weatherForecast:
# 		for i in range(8):
# 			weatherCells[(i,5)].configure(text=weatherForecast[i][5])
# 			try:
# 				path= 'images/' + weatherForecast[i][6]  +'.png'
# 				first_step = Image.open(path)
# 				img = first_step.resize((50,50), resample=0)
# 				my_image = PhotoImage(img)
# 				weatherCells[(i,6)].configure(image=my_image)
# 				weatherCells[(i,6)].image = my_image
# 			except:
# 				weatherCells[(i,6)].configure(text=weatherForecast[i][6], font = ('caviar dreams', 10), bg='black', fg='white')
# 	else:
# 		for i in range(8):
# 			for j in range(5,7):
# 				weatherCells[(i,j)].configure(text="")	

# def drawWeather():
# 	global weatherCells
# 	weatherForecast = weather.weatherFor()
# 	weatherCells={}
# 	for i in range(8): #Rows
# 		for j in range(7): #Columns
# 			if j<5:
# 				weathertable = tk.Label(root, text=weatherForecast[i][j], font = ('caviar dreams', 12, 'bold'), bg='black', fg='white')
# 				weathertable.grid(in_=MR, row=i, column=j, padx = 10)				
# 			elif j == 5:
# 				weathertable = tk.Label(root, text=weatherForecast[i][j], font = ('caviar dreams', 12, 'bold'), bg='black', fg='white')
# 				weathertable.grid(in_=MR, row=i, column=j, padx = 10)
# 			elif j ==6:
# 				try:
# 					path= 'images/' + weatherForecast[i][j]  +'.png'
# 					first_step = Image.open(path)
# 					img = first_step.resize((50,50), resample=0)
# 					my_image = PhotoImage(img)
# 					weathertable = tk.Label(image=my_image, borderwidth = 0)
# 					weathertable.image = my_image
# 					weathertable.grid(in_=MR, row=i, column=j, padx=10)
# 				except:
# 					weathertable = tk.Label(root, text=weatherForecast[i][j], font = ('caviar dreams', 10), bg='black', fg='white')
# 					weathertable.grid(in_=MR, row=i, column=j, padx = 10)
# 			weatherCells[(i,j)] = weathertable


def eventRefresh():
	global eventCells
	events = gC.main()

	if events:
		for i in range(8):
			for j in range(2):
				eventCells[(i,j)].configure(text=events[i][j])
	else:
		for i in range(8):
			for j in range(2):
				eventCells[(i,j)].configure(text="")


def busRefresh():
	"""Funnction calls the main method in bus.py for given stop. If there are more than 4 buses, only the first 4 will be printed.
	As this is refresh there is no need to re place the headings, so i starts at 1. Refreshes every minute"""
	global busCells
	try:
		busTimes = bus.main(876)
		for i in range(1,4):#clearing the table
			for j in range(3):
				busCells[(i,j)].configure(text="")
		if busTimes:
			for i in range(1,min(4,len(busTimes))):
				for j in range(3): #Columns
					busCells[(i,j)].configure(text=busTimes[i][j])

	except:
		pass
	root.after(60000, busRefresh)

def drawBus():
	"""need to test at night with no buses"""
	global busCells
	headers = ["Bus", "Destination", "Time"]
	busCells = {}
	for i in range(4): #Rows, limiting it to four buses
		for j in range(3): #Columns
			if i == 0:#the headers
				busTable = tk.Label(root, text=headers[j], font = ('caviar dreams', 12, 'bold'), bg='black', fg='white')
				busTable.grid(in_=TR, row = i+1, column = j, padx=15)
			else:
				busTable = tk.Label(root, font = ('caviar dreams', 12), bg='black', fg='white')
				busTable.grid(in_=TR, row = i+1, column = j, padx=15)
			busCells[(i,j)] = busTable
	busRefresh()
					
def drawEvents():
	global eventCells
	events = gC.main()
	eventCells = {}
	if events:
		for i in range(8): #Rows
		    for j in range(2): #Columns
		        table = tk.Label(root, text=events[i][j], font = ('caviar dreams', 12), bg='black', fg='white')
		        table.grid(in_=ML, row = i+1, column = j, padx=15, sticky = "E")
		        eventCells[(i,j)] = table
	else:
		No_Events = tk.Label(root, text="No upcoming events", font = ('caviar dreams', 10), bg='black', fg='white')
		No_Events.grid(in_=ML, row = 1, column = 1, padx=15)

def spotRefresh():
	"""In column 0, place the symbols which represent song, artist, a song playback details, unless no song available.
	In column 1, place the song details. Refresh every second"""
	global spotCells, token
	try:
		spotDetails = Spotify.main(token)
		icons = ("music note", "person", "pause")

		if spotDetails:

			for i in range(3):
				path= 'images/' + icons[i]  +'.png'
				first_step = Image.open(path)
				img = first_step.resize((50,50), resample=0)
				my_image = PhotoImage(img)
				spotCells[(i,0)].configure(image=my_image)
				spotCells[(i,0)].image = my_image


			spotCells[(0,1)].configure(text=spotDetails[0][:45])#limiting name length
			spotCells[(1,1)].configure(text=spotDetails[1][:55])
			spotCells[(2,1)].configure(text=spotDetails[2] + " / " + spotDetails[3])

		else:
			spotCells[(0,0)].configure(image="")
			spotCells[(1,0)].configure(image="")
			spotCells[(2,0)].configure(image="")

			spotCells[(0,1)].configure(text="")
			spotCells[(1,1)].configure(text="")
			spotCells[(2,1)].configure(text="")		
	except:
		pass
	root.after(1000, spotRefresh)

def drawSpot():
	"""Function to be called on inital startup, it defines the table representing spotify information.
	If saves the labels created to a dictionary based on their i and j coords.""" 
	global spotCells, token   
	spotCells = {}	
	for i in range(3): #Rows
		for j in range(2): #Columns
			spotLabel = tk.Label(root, font = ('caviar dreams', 15), bg='black', fg='white')
			spotLabel.grid(in_=BL, row = i+1, column = j, padx=25)		

			spotCells[(i,j)] = spotLabel
	spotRefresh()

#Init GUI Window
root = tk.Tk()


root.title('Magic Mirror')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
h = screen_height//65#weird values that must be experimented with since the dont use pixels for the height and width of labels
w = screen_width//32

def CreateLabel(row, col, bg, fg, **kwargs):
	if "sticky" in kwargs:
		sk = kwargs["sticky"]
		label = tk.Label(root, height = h, width=w, font = ('caviar dreams', 15), bg=bg, fg=fg)
		label.grid(sticky = sk, row=row, column= col)
	else:
		label = tk.Label(root, height = h, width=w, bg = bg)
		label.grid(row=row, column= col)
	return label


#setting up the grid system for placement
TL = CreateLabel(0, 0, "black", "white", sticky = "NW")#sticky doesnt always work for some reason
TM = CreateLabel(0, 1, "black", "white")
TR = CreateLabel(0, 2, "black", "white")

ML = CreateLabel(1, 0, "black", "white", sticky = "W")
MM = CreateLabel(1, 1, "black", "white")
MR = CreateLabel(1, 2, "black", "white", sticky = "N")

BL = CreateLabel(2, 0, "black", "white", sticky = "W")
BM = CreateLabel(2, 1, "black", "white", sticky = "S")
BR = CreateLabel(2, 2, "black", "white")


TL.grid_propagate(False)
TM.grid_propagate(False)
TR.grid_propagate(False)

ML.grid_propagate(False)
MM.grid_propagate(False)
MR.grid_propagate(False)


#========================================================================

clock_frame = tk.Label(root, font = ('caviar dreams', 130), bg='black', fg='white')
clock_frame.grid(in_=TL, row=1, column=0, rowspan = 2)

clock_frame2 = tk.Label(root, font = ('caviar dreams', 50), bg='black', fg='white')
clock_frame2.grid(in_=TL, row=1, column=1, columnspan = 2)

dateframe = tk.Label(root, font = ('caviar dreams', 25), bg='black', fg='white')
dateframe.grid(in_=TL, row=0, column=0, columnspan = 3)

#========================================================================

WelcomeMessage = tk.Label(root, font = ('caviar dreams', 25), bg='black', fg='white')
WelcomeMessage.grid(in_=TM)

#========================================================================

eventTitle = tk.Label(root, font = ('caviar dreams', 15, 'bold'), bg='black', fg='white')
eventTitle.grid(in_=ML, row = 0, column = 0, columnspan = 2)
eventTitle.config(text="Upcoming Events")

#========================================================================

path= 'images/Thermometer.png'
my_image = PhotoImage(Image.open(path))
Temp = tk.Label(image=my_image, borderwidth = 0)
Temp.image = my_image
Temp.grid(in_=TL, row =2, column = 1, sticky="NE")

WeatherTemp = tk.Label(root, font = ('caviar dreams', 15, 'bold'), bg='black', fg='white')
WeatherTemp.grid(in_=TL, row =2, column = 2, sticky="NW")

#========================================================================

stext = st.ScrolledText(font = ('caviar dreams', 12), bg='black', fg='white', height =10, borderwidth = 0)
stext.after(1000, lambda: scroll_textbox(stext))
stext.grid(in_=BM, sticky = "S")

#========================================================================

refresh()
drawEvents()
# drawWeather()
updateWeatherEvents()
drawSpot()
drawBus()
shortRefresh()
clock1()
clock2()

root.attributes("-fullscreen", True)
root.configure(background='black')
root.bind("<Escape>", lambda event:root.destroy())
root.mainloop()

