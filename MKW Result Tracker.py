import tkinter as tk
import json
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def start():
    global mode, lounge, ModeButton, LoungeButton, SF, TF, PF, LF, MF, AF
    
    app.title(f"MKW Result Tracker {app.version} - WHOni")
    app.geometry("1585x880+100+100")
    
    load_images()
    
    White = Label(app, bg = "#FFFFFF")
    White.put(0, 0, 1585, 880)
    
    SF = Frame(app, bg = "#000000") #Settings Frame
    SF.put(0, 0, 1585, 40)
    mode = "12P"
    ModeButton = Button(SF, 16, text = mode, bg = "#000000", fg = "#FFFFFF", command = lambda: switch_mode())
    ModeButton.put(740, 5, 105, 30)
    
    lounge = False
    LoungeButton = Button(SF, 16, text = f"Start {mode} Lounge", bg = "#000000", fg = "#FFFFFF", command = lambda: start_lounge())
    LoungeButton.put(10, 5, 200, 30)
    
    TF = Frame(app, bg = "#000000") #Track Frame
    TF.put(0, 45, 670, 560)
    
    for i, t in enumerate(tracks):
        TrackButton = Button(TF, image = trackimages[t], bg = "#000000", command = lambda t=t: select_track(t))
        TrackButton.put(10 + (i % 6) * 110, 10 + (i // 6) * 110, 100, 100)
        TrackButton.bind("<Button-3>", lambda event, t=t: delete_placement(t))
    
    PF = Frame(app, bg = "#000000") #Placement Frame
    PF.put(0, 610, 670, 270)
    
    LF = Frame(app, bg = "#000000") #Last Races Frame
    LF.put(675, 45, 300, 835)
    last_races(0)
    
    MF = Frame(app, bg = "#000000") #Most Played Frame
    MF.put(980, 45, 300, 835)
    most_played()
    
    AF = Frame(app, bg = "#000000") #Averages Frame
    AF.put(1285, 45, 300, 835)
    averages()
        
def load_images():
    global trackimages
    
    trackimages = {}
    for t in tracks:
        try:
            PNG = Image.open(f"Images/{t}.png")
            trackimages[t] = ImageTk.PhotoImage(PNG.resize((100, 100)))
        except:
            trackimages[t] = None

def switch_mode():
    global mode
    
    if lounge: return
    mode = "12P" if mode == "24P" else "24P"
    most_played()
    averages()
    PF.clear()
    
    ModeButton.config(text = mode)
    LoungeButton.config(text = f"Start {mode} Lounge")
    
def start_lounge():
    global lounge, l
    
    lounge = True
    l = Lounge()

def select_track(t):
    def cancel():
        PF.clear()
        
    def confirm(p):
        r[mode][t].append(p)
        r.save()
        PF.clear()
        
        session.append([mode, t, p])
        
        Confirmation = Label(PF, 16, text = f"{mode} Placement registered for {t}:\n{p}", bg = "#000000", fg = "#00FF00")
        Confirmation.put(0, 0, 670, 270)
        
        if lounge: 
            l.results.append((t, p))
            l.finish_race()
        
        last_races(0)
        most_played()
        averages()
    
    PF.clear()
    
    if lounge and l.races == 12:
        LoungeOver = Label(PF, 16, text = "Your Lounge is over.\nFinish it first before registering another race.", bg = "#000000", fg = "#FFAAAA")
        LoungeOver.put(0, 0, 670, 270)
        return
    
    Title = Label(PF, 16, text = f"{mode} - {t}", bg = "#000000", fg = "#FFFFFF")
    Title.put(0, 0, 670, 25)
    
    if mode == "24P":
        for p in range(24):
            Place = Button(PF, 16, text = p + 1, bg = "#000000", fg = "#FFFFFF", command = lambda p=p: confirm(p + 1))
            Place.put(8 + (p % 12) * 55, 70 + (p // 12) * 55, 50, 50)
    else:
        for p in range(12):
            Place = Button(PF, 32, text = p + 1, bg = "#000000", fg = "#FFFFFF", command = lambda p=p: confirm(p + 1))
            Place.put(10 + (p % 6) * 110, 30 + (p // 6) * 100, 100, 90)
            
    CancelButton = Button(PF, 16, text = "Cancel", bg = "#000000", fg = "#FF0000", command = lambda: cancel())
    CancelButton.put(285, 230, 100, 30)

def delete_placement(t):
    def cancel():
        PF.clear()
        
    def confirm():
        r[mode][t].pop(len(r[mode][t]) - 1)
        r.save()
        PF.clear()
        
        Confirmation = Label(PF, 16, text = f"Last {mode} Placement for {t} deleted.", bg = "#000000", fg = "#FFFF00")
        Confirmation.put(0, 0, 670, 270)
        
        most_played()
        averages()
    
    if len(r[mode][t]) == 0:
        NoPlacements = Label(PF, 16, text = f"No {mode} Placements registered yet on\n{t}.", bg = "#000000", fg = "#FFAAAA")
        NoPlacements.put(0, 0, 670, 270)
    else:
        DeleteInfo = Label(PF, 16, text = f"Delete last registered {mode} Placement on {t}?\n({r[mode][t][len(r[mode][t]) - 1]})", bg = "#000000", fg = "#FF0000")
        DeleteInfo.put(0, 0, 670, 210)
        CancelButton = Button(PF, 16, text = "Cancel", bg = "#000000", fg = "#FFFFFF", command = lambda: cancel())
        CancelButton.put(225, 220, 100, 40)
        ConfirmButton = Button(PF, 16, text = "Delete", bg = "#000000", fg = "#FF0000", command = lambda: confirm())
        ConfirmButton.put(345, 220, 100, 40)

def last_races(sc):
    if sc < 0 or len(session) <= sc or lounge: return
    
    LF.clear()
    
    Title = Label(LF, 16, text = "Current Session", bg = "#000000", fg = "#FFFFFF")
    Title.put(0, 0, 300, 25)
    
    for i in range(30):
        x = i + sc
        if x < len(session):
            Mode = Label(LF, 12, text = session[x][0], bg = "#222222", fg = "#FFFFFF")
            Mode.put(5, 30 + i * 26, 50, 22)
            Track = Label(LF, 12, text = session[x][1], bg = "#222222", fg = "#FFFFFF")
            Track.put(60, 30 + i * 26, 180, 22)
            Place = Label(LF, 12, text = session[x][2], bg = "#222222", fg = "#FFFFFF")
            Place.put(245, 30 + i * 26, 50, 22)
    
    ScrollUp = Button(LF, 12, text = "\u2191", bg = "#000000", fg = "#FFFFFF", command = lambda: last_races(sc - 30))
    ScrollUp.put(110, 810, 30, 22)
    ScrollDown = Button(LF, 12, text = "\u2193", bg = "#000000", fg = "#FFFFFF", command = lambda: last_races(sc + 30))
    ScrollDown.put(160, 810, 30, 22)

def most_played():
    MF.clear()
    
    Ranking = [[t, len(r[mode][t])] for t in tracks]
    Ranking.sort(key = lambda x: -x[1])
    
    Title = Label(MF, 16, text = f"Most Played - {mode}", bg = "#000000", fg = "#FFFFFF")
    Title.put(0, 0, 300, 25)
    
    for i in range(30):
        Rank = Label(MF, 12, text = f"{i + 1})", bg = "#222222", fg = "#FFFFFF")
        Rank.put(5, 30 + i * 26, 50, 22)
        Track = Label(MF, 12, text = Ranking[i][0], bg = "#222222", fg = "#FFFFFF")
        Track.put(60, 30 + i * 26, 180, 22)
        Place = Label(MF, 12, text = Ranking[i][1], bg = "#222222", fg = "#FFFFFF")
        Place.put(245, 30 + i * 26, 50, 22)
        
def averages():
    AF.clear()
    
    Ranking = [[t, sum(r[mode][t]) / len(r[mode][t])] for t in tracks if len(r[mode][t]) != 0]
    Ranking.sort(key = lambda x: x[1])
    
    Title = Label(AF, 16, text = f"Average Places - {mode}", bg = "#000000", fg = "#FFFFFF")
    Title.put(0, 0, 300, 25)
    
    for i in range(30):
        if i < len(Ranking):
            Rank = Label(AF, 12, text = f"{i + 1})", bg = "#222222", fg = "#FFFFFF")
            Rank.put(5, 30 + i * 26, 50, 22)
            Track = Label(AF, 12, text = Ranking[i][0], bg = "#222222", fg = "#FFFFFF")
            Track.put(60, 30 + i * 26, 180, 22)
            Place = Label(AF, 12, text = round(Ranking[i][1], 2), bg = "#222222", fg = "#FFFFFF")
            Place.put(245, 30 + i * 26, 50, 22)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.version = "v1.1.0"
        self.font = "Calibri"
        
class Toplevel(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        
class Frame(tk.Frame):
    def __init__(self, master, bg = "#000000", **kwargs):
        super().__init__(master, bg = bg, **kwargs)
        
        self.w = {}
        self.var = {}
        self.visible = False
        self.pos = ()
        
    def put(self, x, y, width, height):
        self.place(x = x, y = y, width = width, height = height)
        self.visible = True
        self.pos = (x, y, width, height)
        
    def clear(self):
        for l in self.winfo_children():
            l.destroy()
            
    def hide(self):
        if not self.visible: return
        self.place_forget()
        self.visible = False
        
    def show(self):
        if not self.pos or self.visible: return
        self.place(x = self.pos[0], y = self.pos[1], width = self.pos[2], height = self.pos[3])
        self.visible = True
      
class Label(tk.Label):
    def __init__(self, master, fs = 12, **kwargs):
        self.fs = fs
        
        super().__init__(master, font = (app.font, fs, "bold"), **kwargs)
        
    def put(self, x, y, width, height):
        self.place(x = x, y = y, width = width, height = height)
        
class Button(tk.Button):
    def __init__(self, master, fs = 12, **kwargs):
        self.fs = fs
        
        super().__init__(master, font = (app.font, fs, "bold"), **kwargs)
        
    def put(self, x, y, width, height):
        self.place(x = x, y = y, width = width, height = height)
    
class ResultDict(dict):
    def __init__(self):
        try:
            with open("Results.json", "r") as file:
                data = json.load(file)
        except Exception:
            data = {"12P": {track: [] for track in tracks},
                     "24P": {track: [] for track in tracks}}
        
        super().__init__(data)
        
    def save(self):
        with open("Results.json", "w") as file:
            json.dump(self, file)
    
class Lounge():
    def __init__(self):
        self.frame = Frame(SF, bg = "#000000")
        self.frame.put(0, 0, 1585, 40)
        self.mode = mode
        self.races = 0
        self.progress = Label(self.frame, 16, text = f"{mode} Lounge in progress: {self.races} / 12 Races", bg = "#000000", fg = "#00FF00")
        self.progress.put(0, 0, 1585, 40)
        
        self.ov = Frame(LF, bg = "#000000")
        self.ov.put(0, 0, 300, 835)
        Title = Label(self.ov, 16, bg = "#000000", fg = "#FFFFFF", text = "Lounge Results")
        Title.put(0, 0, 300, 25)
        WhiteBG = Label(self.ov, bg = "#FFFFFF")
        WhiteBG.put(0, 685, 300, 150)
        PointsTitle = Label(self.ov, 32, bg = "#000000", fg = "#FFFFFF", text = "Points:")
        PointsTitle.put(0, 690, 180, 100)
        self.results = []
        self.points = 0
        self.pointlabel = Label(self.ov, 32, bg = "#000000", fg = "#FFFFFF", text = self.points)
        self.pointlabel.put(185, 690, 115, 100)
        self.avg = Label(self.ov, 16, bg = "#000000", fg = "#FFFFFF", text = "Current Average: 0")
        self.avg.put(0, 795, 300, 35)
        
        UndoLast = Button(self.ov, 16, bg = "#000000", fg = "#FFAAAA", text = "Delete last race", command = lambda: self.clear_race())
        UndoLast.put(10, 605, 280, 30)
        self.finish = Button(self.ov, 16, bg = "#000000", fg = "#FFAAAA", text = "Finish Lounge", command = lambda: self.finish_lounge())
        self.finish.put(10, 645, 280, 30)
        
        self.raceframes = []
        for rc in range(12):
            RaceFrame = Frame(self.ov, bg = "#000000")
            RaceFrame.put(0, 35 + rc * 30, 300, 25)
            self.raceframes.append(RaceFrame)
            
        self.fig = Figure(figsize = (10, 8), dpi = 100, facecolor = "#000000")
        self.fig.subplots_adjust(left = 0.15, right = 0.95, top = 0.95, bottom = 0.15)
        self.plot = self.fig.add_subplot(1, 1, 1)
        self.plot.set_facecolor("#111111")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.ov)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x = 5, y = 395, width = 290, height = 200)
        
        self.graph()
        
    def finish_race(self):
        self.enter_race(self.races)
        
        self.races += 1
        self.progress.config(text = f"{mode} Lounge in progress: {self.races} / 12 Races")
        
        self.update()
    
    def clear_race(self):
        if self.races == 0: return
        
        self.races -= 1
        rm = self.races
        self.raceframes[rm].clear()
        r[mode][self.results[rm][0]].pop(len(r[mode][self.results[rm][0]]) - 1)
        r.save()
        self.results.pop(len(self.results) - 1)
        
        self.progress.config(text = f"{mode} Lounge in progress: {self.races} / 12 Races")
        
        self.update()
        
    def update(self):
        avg = round(self.races * (82 if mode == '12P' else 72) / 12, 1)
        self.avg.config(text = f"Current Average: {avg}")
        
        self.points = sum([points[mode][x[1] - 1] for x in self.results])
        
        self.pointlabel.config(text = self.points, fg = "#FF0000" if self.points < avg else "#00FF00" if self.points > avg else "#FFFF00")
        
        if self.races == 12:
            self.finish.config(fg = "#AAFFAA")
        else:
            self.finish.config(fg = "#FFAAAA")
            
        self.graph()
        
        most_played()
        averages()
        
    def enter_race(self, rc):
        self.raceframes[rc].clear()
        RaceNumber = Label(self.raceframes[rc], 12, bg = "#220022", fg = "#FFFFFF", text = f"{rc + 1})")
        RaceNumber.put(5, 0, 30, 25)
        Track = Label(self.raceframes[rc], 12, bg = "#220022", fg = "#FFFFFF", text = self.results[rc][0])
        Track.put(40, 0, 160, 25)
        Place = Label(self.raceframes[rc], 12, bg = "#220022", fg = "#FFFFFF", text = self.results[rc][1])
        Place.put(205, 0, 40, 25)
        Points = Label(self.raceframes[rc], 12, bg = "#220022", fg = "#FFFFFF", text = f"{points[mode][self.results[rc][1] - 1]} P.")
        Points.put(250, 0, 45, 25)
        
    def graph(self):
        self.plot.clear()
        self.plot.set_xlim(0, 12)
        self.plot.set_xticks([x for x in range(13)])
        self.plot.set_xticklabels([x for x in range(13)], color = "#FFFFFF")
        
        maxi = max([82 if mode == "12P" else 72, self.points])
        self.plot.set_ylim(0, maxi)
        self.plot.set_yticks([x * 10 for x in range(maxi // 10 + 1)])
        self.plot.set_yticklabels([x * 10 for x in range(maxi // 10 + 1)], color = "#FFFFFF")
        self.plot.grid(True, which = "both", linestyle = "--", linewidth = 0.2, alpha = 0.8)
        
        self.plot.tick_params(axis = "both", colors = "#FFFFFF")
        
        self.plot.plot([x for x in range(13)], [x * (82 if mode == "12P" else 72) / 12 for x in range(13)], color = "#666666", linewidth = 1)
        point_history = [0]
        for x in self.results:
            point_history.append(point_history[len(point_history) - 1] + points[mode][x[1] - 1])
        self.plot.plot(range(len(point_history)), point_history, color = "#00FFFF", linewidth = 1)
        self.canvas.draw()
        
    def finish_lounge(self):
        global lounge
        
        self.frame.destroy()
        self.ov.destroy()
        lounge = False
        last_races(0)
    
tracks = ["Acorn Heights", "Airship Fortress", "Boo Cinema", "Bowsers Castle", "Cheep Cheep Falls", "Choco Mountain", "Crown City", "DK Pass", "DK Spaceport",
          "Dandelion Depths", "Desert Hills", "Dino Dino Jungle", "Dry Bones Burnout", "Faraway Oasis", "Great Q. Block Ruins", "Koopa Troopa Beach",
          "Mario Bros. Circuit", "Mario Circuit", "Moo Moo Meadows", "Peach Beach", "Peach Stadium", "Rainbow Road", "Salty Salty Speedway", "Shy Guy Bazaar",
          "Sky-High Sundae", "Starview Peak", "Toads Factory", "Wario Shipyard", "Wario Stadium", "Whistlestop Summit"]
points = {"12P": [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
          "24P": [15, 12, 10, 9, 9, 8, 8, 7, 7, 6, 6, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 1]}

r = ResultDict()
session = []

app = App()
start()
app.mainloop()