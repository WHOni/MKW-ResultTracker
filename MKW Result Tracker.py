import tkinter as tk
import json
from PIL import ImageTk, Image

def start():
    global mode, ModeButton, SF, TF, PF, LF, MF, AF
    
    app.title(f"MKW Result Tracker {app.version} - WHOni")
    app.geometry("1585x880+100+100")
    
    load_images()
    
    SF = Frame(app, bg = "#000000") #Settings Frame
    SF.put(0, 0, 1585, 40)
    mode = "12P"
    ModeButton = Button(SF, 16, text = mode, bg = "#000000", fg = "#FFFFFF", command = lambda: switch_mode())
    ModeButton.put(740, 5, 105, 30)
    
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
    
    mode = "12P" if mode == "24P" else "24P"
    most_played()
    averages()
    PF.clear()
    
    ModeButton.config(text = mode)

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
        
        last_races(0)
        most_played()
        averages()
    
    PF.clear()
    
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
    if sc < 0 or len(session) <= sc: return
    
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
        
        self.version = "v1.0.1"
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
        with open("Results.json", "r") as file:
            data = json.load(file)
        
        super().__init__(data)
        
    def save(self):
        with open("Results.json", "w") as file:
            json.dump(self, file)
    
tracks = ["Mario Bros. Circuit", "Crown City", "Whistlestop Summit", "DK Spaceport", "Desert Hills", "Shy Guy Bazaar", "Wario Stadium", "Airship Fortress",
          "DK Pass", "Starview Peak", "Sky-High Sundae", "Wario Shipyard", "Koopa Troopa Beach", "Faraway Oasis", "Peach Beach",
          "Salty Salty Speedway", "Dino Dino Jungle", "Great Q. Block Ruins", "Cheep Cheep Falls", "Dandelion Depths", "Boo Cinema", "Dry Bones Burnout",
          "Moo Moo Meadows", "Choco Mountain", "Toads Factory", "Bowsers Castle", "Acorn Heights", "Mario Circuit", "Peach Stadium", "Rainbow Road"]

r = ResultDict()
session = []

app = App()
start()
app.mainloop()