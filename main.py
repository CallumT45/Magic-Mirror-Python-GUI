import datetime
import random
import time
from tkinter import Button, Entry, Frame, Label, Tk, scrolledtext, constants

from cogs import Spotify, bus
from cogs import googleCalendar as gC
from cogs import news, reddit, weather

from PIL.ImageTk import PhotoImage
from PIL import Image


class MagicMirror:
    def __init__(self, master):
        self.master = master
        self.draw_funcs()
        self.refresh_funcs()
        self.master.title('Magic Mirror')
        self.master.attributes("-fullscreen", True)
        self.master.configure(background='black')
        self.master.bind("<Escape>", lambda event:self.master.destroy())


    def draw_funcs(self):
        self.grid()
        self.clock_set_up()
        self.general_set_up()
        self.drawSpot()
        self.drawBus()
        self.drawWeather()
    
    def refresh_funcs(self):
        self.clock1()
        self.clock2()
        self.shortRefresh()
        self.refresh()
        self.drawEvents()
        self.updateWeatherEvents()


    def clock_set_up(self):
        self.clock_frame = Label(self.master, font = ('caviar dreams', 130), bg='black', fg='white')
        self.clock_frame.grid(in_=self.TL, row=1, column=0, rowspan = 2)

        self.clock_frame2 = Label(self.master, font = ('caviar dreams', 50), bg='black', fg='white')
        self.clock_frame2.grid(in_=self.TL, row=1, column=1, columnspan = 2)

        self.dateframe = Label(self.master, font = ('caviar dreams', 25), bg='black', fg='white')
        self.dateframe.grid(in_=self.TL, row=0, column=0, columnspan = 3)


        
        my_image = PhotoImage(Image.open('images/Thermometer.png'))
        self.Temp = Label(image=my_image, borderwidth = 0)
        self.Temp.image = my_image
        self.Temp.grid(in_=self.TL, row =2, column = 1, sticky="NE")
        self.WeatherTemp = Label(self.master, font = ('caviar dreams', 15, 'bold'), bg='black', fg='white')
        self.WeatherTemp.grid(in_=self.TL, row =2, column = 2, sticky="NW")

    def general_set_up(self):
        self.WelcomeMessage = Label(self.master, font = ('caviar dreams', 25), bg='black', fg='white')
        self.WelcomeMessage.grid(in_=self.TM, pady=15)

        self.stext = scrolledtext.ScrolledText(font = ('caviar dreams', 12), bg='black', fg='white', height =10, borderwidth = 0)
        self.stext.after(1000, lambda: self.scroll_textbox(self.stext))
        self.stext.grid(in_=self.BM, sticky = "ESW", padx = 25)

    def drawEvents(self):
        self.eventTitle = Label(root, font = ('caviar dreams', 15, 'bold'), bg='black', fg='white')
        self.eventTitle.grid(in_=self.ML, row = 0, column = 0, columnspan = 2)
        self.eventTitle.config(text="Upcoming Events")

        events = gC.main()
        self.eventCells = {}
        if events:
            for i in range(8): #Rows
                for j in range(2): #Columns
                    table = Label(root, text=events[i][j], font = ('caviar dreams', 12), bg='black', fg='white')
                    table.grid(in_= self.ML, row = i+1, column = j, padx=15, sticky = "E")
                    self.eventCells[(i,j)] = table
        else:
            No_Events = Label(root, text="No upcoming events", font = ('caviar dreams', 10), bg='black', fg='white')
            No_Events.grid(in_= self.ML, row = 1, column = 1, padx=15)

    def drawWeather(self):
        weatherForecast = weather.weatherFor()
        self.weatherCells={}
        for i in range(8): #Rows
            weather_table = Label(self.master, text=weatherForecast[i][0], font = ('caviar dreams', 12, 'bold'), bg='black', fg='white')
            weather_table.grid(in_= self.MR, row=i, column=0, padx = 10)
            self.weatherCells[(i,0)] = weather_table
            try:
                first_step = Image.open('images/' + weatherForecast[i][1]  +'.png')
                img = first_step.resize((50,50), resample=0)
                my_image = PhotoImage(img)
                weather_table = Label(image=my_image, borderwidth = 0)
                weather_table.image = my_image
                weather_table.grid(in_= self.MR, row=i, column=1, padx=10)
            except:
                weather_table = Label(self.master, text=weatherForecast[i][1], font = ('caviar dreams', 10), bg='black', fg='white')
                weather_table.grid(in_= self.MR, row=i, column=1, padx = 10)
            self.weatherCells[(i,1)] = weather_table

    def drawBus(self):
        """need to test at night with no buses"""
        headers = ["Bus", "Destination", "Time"]
        self.busCells = {}
        for i in range(4): #Rows, limiting it to four buses
            for j in range(3): #Columns
                if i == 0:#the headers
                    busTable = Label(self.master, text=headers[j], font = ('caviar dreams', 12, 'bold'), bg='black', fg='white')
                    busTable.grid(in_= self.TR, row = i+1, column = j, padx=15)
                else:
                    busTable = Label(self.master, font = ('caviar dreams', 12), bg='black', fg='white')
                    busTable.grid(in_= self.TR, row = i+1, column = j, padx=15)
                self.busCells[(i,j)] = busTable
        self.busRefresh()

    def drawSpot(self):
        """Function to be called on inital startup, it defines the table representing spotify information.
        If saves the labels created to a dictionary based on their i and j coords.""" 
        self.spotCells = {}	
        for i in range(3): #Rows
            for j in range(2): #Columns
                spotLabel = Label(root, font = ('caviar dreams', 15), bg='black', fg='white')
                spotLabel.grid(in_= self.BL, row = i+1, column = j, padx=25)		

                self.spotCells[(i,j)] = spotLabel
        self.spotRefresh()


    def clock1(self, time1=''):
       	time2 = time.strftime("%H")
        if time2 != time1:
            time1 = time2
            self.clock_frame.config(text=time2)
        self.clock_frame.after(200, self.clock1)

    def clock2(self, time3=''):
        time4 = time.strftime(":%M:%S")
        if time4 != time3:
            time3 = time4
            self.clock_frame2.config(text=time4)
        self.clock_frame2.after(200, self.clock2)

    def scroll_textbox(self, elem):
        """Function is responsable to the scrolling headlines, and is an adaption of code from 
        https://python-forum.io/Thread-Tkinter-scrolling-text-in-tkinter?pid=2972"""
        # get the current index
        current = float(elem.index(constants.CURRENT))
        new = current
        # keep incrementing the index until it's not visible
        while elem.bbox(new):
            new += 1
        # make sure the new index is visible
        elem.see(new)
        # move the index again in 1250ms
        elem.after(2000, lambda: self.scroll_textbox(elem))
        if elem.bbox(new) == None:#When the scroll box reaches the bottom return to the top
            elem.see(1.0)

    def refresh(self):
        """Updates the scrolling widget with reddit and newsheadlines, this function is run every 3 hours"""

        def listTostr(lst):
            """Takes a list as input and outputs as a single string with two newlines between each index"""
            string = ''
            for i in lst:
                string += str(i) + '\n\n'
            return string

        redditFeed = reddit.main()
        newsHead = news.main()
            
        headStr = listTostr(newsHead)
        RedditStr = listTostr(redditFeed)
        TotalStr = headStr + RedditStr
          
        self.stext.delete('1.0', constants.END)
        self.stext.insert(constants.END,TotalStr) 
        self.master.after(10800000, self.refresh)


    def weatherRefresh(self):
        """Gets the weather forecast for the next 24 hours, if this is not none then, update the 5th column(time) and try to 
        update the 6th column(weather). If no image exists with the name, then print the text version of the weather."""
        weatherForecast = weather.weatherFor()

        if weatherForecast:
            for i in range(8):
                self.weatherCells[(i,0)].configure(text=weatherForecast[i][0])
                try:
                    first_step = Image.open('images/' + weatherForecast[i][1]  +'.png')
                    img = first_step.resize((50,50), resample=0)
                    my_image = PhotoImage(img)
                    self.weatherCells[(i,1)].configure(image=my_image)
                    self.weatherCells[(i,1)].image = my_image
                except:
                    self.weatherCells[(i,1)].configure(text=weatherForecast[i][1], font = ('caviar dreams', 10), bg='black', fg='white')
        else:
            for i in range(8):
                for j in range(2):
                    self.weatherCells[(i,j)].configure(text="")	


    def eventRefresh(self):
        events = gC.main()

        if events:
            for i in range(8):
                for j in range(2):
                    self.eventCells[(i,j)].configure(text=events[i][j])
        else:
            for i in range(8):
                for j in range(2):
                    self.eventCells[(i,j)].configure(text="")


    def busRefresh(self):
        """Funnction calls the main method in bus.py for given stop. If there are more than 4 buses, only the first 4 will be printed.
        As this is refresh there is no need to re place the headings, so i starts at 1. Refreshes every minute"""
        try:
            busTimes = bus.main(876)
            for i in range(1,4):#clearing the table
                for j in range(3):
                    self.busCells[(i,j)].configure(text="")
            if busTimes:
                for i in range(1,min(4,len(busTimes))):
                    for j in range(3): #Columns
                        self.busCells[(i,j)].configure(text=busTimes[i][j])

        except:
            pass
        self.master.after(60000, self.busRefresh)

    def updateWeatherEvents(self):
        """Function which updates every 61 mins. The token for spotify expires after an hour, until it refreshes, the Spot
        refresh idles. Weather and events are also updated"""

        self.weatherRefresh()
        self.eventRefresh()
        self.token = Spotify.getToken()
        self.master.after(3660000, self.updateWeatherEvents)


    def spotRefresh(self):
        """In column 0, place the symbols which represent song, artist, a song playback details, unless no song available.
        In column 1, place the song details. Refresh every second"""
        try:
            spotDetails = Spotify.main(self.token)
            icons = ("music note", "person", "pause")

            if spotDetails:

                for i in range(3):
                    first_step = Image.open('images/' + icons[i]  +'.png')
                    img = first_step.resize((50,50), resample=0)
                    my_image = PhotoImage(img)
                    self.spotCells[(i,0)].configure(image=my_image)
                    self.spotCells[(i,0)].image = my_image


                self.spotCells[(0,1)].configure(text=spotDetails[0][:45])#limiting name length
                self.spotCells[(1,1)].configure(text=spotDetails[1][:55])
                self.spotCells[(2,1)].configure(text=spotDetails[2] + " / " + spotDetails[3])

            else:
                self.spotCells[(0,0)].configure(image="")
                self.spotCells[(1,0)].configure(image="")
                self.spotCells[(2,0)].configure(image="")

                self.spotCells[(0,1)].configure(text="")
                self.spotCells[(1,1)].configure(text="")
                self.spotCells[(2,1)].configure(text="")		
        except:
            pass
        self.master.after(1000, self.spotRefresh)


    def grid(self):
        self.BL = Label(self.master, bg='black', width=30)
        self.BL.grid(row=2,column=0, sticky='W')

        self.BM = Label(self.master, bg='black', width=30)
        self.BM.grid(row=2,column=1,sticky = "EW")

        self.BR = Label(self.master, bg='black', width=30)
        self.BR.grid(row=2,column=2)

        self.ML = Label(self.master, bg='black', width=30)
        self.ML.grid(row=1,column=0,sticky = "W")

        self.MM = Label(self.master, bg='black', width=30)
        self.MM.grid(row=1,column=1)

        self.MR = Label(self.master, bg='black', width=30)
        self.MR.grid(row=1,column=2, sticky="NE")

        self.TL = Label(self.master, bg='black', width=30)
        self.TL.grid(row=0,column=0,sticky = "NW")

        self.TM = Label(self.master, bg='black', width=30)
        self.TM.grid(row=0,column=1, sticky="N")

        self.TR = Label(self.master, bg='black', width=30)
        self.TR.grid(row=0,column=2)

        self.master.grid_columnconfigure(0, weight=2)
        self.master.grid_columnconfigure(1, weight=5)
        self.master.grid_columnconfigure(2, weight=2)  

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=2)
        self.master.grid_rowconfigure(2, weight=2)

        # self.BM.grid_columnconfigure(0, weight=1)
        # self.BM.grid_rowconfigure(0, weight=1)

        self.TL.grid_propagate(False)
        self.TM.grid_propagate(False)
        self.TR.grid_propagate(False)

        self.ML.grid_propagate(False)
        self.MM.grid_propagate(False)
        self.MR.grid_propagate(False)

        self.BL.grid_propagate(False)
        self.BM.grid_propagate(False)
        self.BR.grid_propagate(False)

    def welMessage(self):
        """Given the hour this function will randomly choose from the lists of predetermined messages"""
        morningMessages = ["Rise and Shine\n Callum", "G'day Mate!", "Okay first of all, \nbrush your teeth.", "Good Morning Cute Face", "Wake Up Panda", "Good Morning Callum", "Callum Stop Snoring \nand Wake Up", "Good Morning Handsome"]
        nightMessages = ["Goodnight Callum", "Nighty-night", "Buenas Noches", "Bon Nuit", "Sweet Dreams", "Sleep snug\n as a bug\n in a rug"]
        afternoonMessages = ["Good Afternoon\nCallum","There is my pumkin", "Howdy, Partner!", "Hello Honey \nBunch", "What's Up Handsome", "Welcome to the Club", "Nice Smile", "You slayer, What's Up?" ]
        
        if 4 <= self.hour < 12:
            self.message = random.choice(morningMessages)
        elif 12 <= self.hour < 17:
            self.message = random.choice(afternoonMessages)
        elif 17 <= self.hour < 20:
            self.message = 'Good Evening Callum!'
        elif 20 <= self.hour < 24:
            self.message = random.choice(nightMessages)
        elif 0 <= self.hour < 4:
            self.message = 'Time to ride the rainbow to dreamland!'
        else:
            self.message = "What's Up Callum"

    def shortRefresh(self):
        """Updates the date, welcome message and current temperature every 20 mins"""
        my_date = datetime.date.today()
        currentTime = datetime.datetime.now()
        self.hour = currentTime.hour
        self.welMessage()
        currentTemp = weather.currentTemp()
        currentTempStr = str(currentTemp) + str(u"\u2103")

        self.dateframe.config(text=my_date.strftime("%A %d, %B %Y"))#converts format to weekday, day, month and year
        self.WelcomeMessage.config(text=self.message)
        self.WeatherTemp.config(text=currentTempStr)
        self.master.after(1200000, self.shortRefresh)



root = Tk()
my_gui = MagicMirror(root)
root.mainloop()
