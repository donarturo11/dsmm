#!/usr/bin/env python3


import rtmidi, time, sys, threading
import tkinter as tk

logo="""
#####     ###   ##     ##  ##     ##
##   ##  #   #  ###   ###  ###   ###
##    #  #      ## # # ##  ## # # ##
##    #   ###   ##  #  ##  ##  #  ##
##    #      #  ##     ##  ##     ## 
##   ##  #   #  ##     ##  ##     ##
######    ###   ##     ##  ##     ##
"""

logo2="""
###   ### #   # #   #
#  # #    ## ## ## ##
#  #  ##  # # # # # #
#  #    # #   # #   #
###  ###  #   # #   #
"""

logo3=u"""

"""





midiin = rtmidi.RtMidiIn()
ports = range(midiin.getPortCount())
notes=[] ## Pressed notes

##### Detect MIDI Message
def print_message(midi):
    if midi.isNoteOn():
        noteNumber=midi.getNoteNumber()
        notes.append(noteNumber)
        return noteNumber
    elif midi.isNoteOff():
        #print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
        notes.clear()
        return "\0"
    elif midi.isController():
        print('Have a nice day :)')
        tk_Text('Have a nice day :)')
        time.sleep(1)
        quit()

def scanning():
    if ports:
        for i in ports:
            print(midiin.getPortName(i))
        tk_Text("Opening port 0!") 
        root.after(1000, tk_Text("Input MIDI Controller to EXIT"))
        midiin.openPort(0)
        root.after(1000, tk_Text(" "))
        root.after(1000)
        while running:
            root.update()
            m = midiin.getMessage(250) # some timeout in ms
            if m:
                msg=print_message(m)
                if msg!="None":
                    print("Is Message")
                else:
                    print("Not Message")
                #notes.append(m)
                tk_Matrix(notes)
            if running==False:
                tk_Text("END")
                root.after(1000, root.destroy())
            
    
            #print(drawMatrix(notes))
    else:
        tk_Text('NO MIDI INPUT PORTS!')

##########################3

###### Draw Matrix
fps=250 ## Frames per second

def cls():
    time.sleep(1/fps)
    print("\033c")

def makeHorizontalFrame(width):
    line=""
    for i in range(0,width):
        line+="#"
    line+="\n"
    return line

##### Draw Matrix ############
"""
|Row | midinotenumber  |
|----|:---------------:|
| 0  |     0-15        |
| 1  |    16-31        |
| 2  |    32-47        |
| 3  |    48-63        |
| 4  |    64-79        |
| 5  |    80-95        |
| 6  |    96-111       |
| 7  |   112-127       |

"""
##############################

def drawMatrix(notes):    
    #label.after(250)
    allNotes=range(0,128)
    count=1
    charString=""
    #charString+=makeHorizontalFrame(18)
    for i in allNotes:
        noteIn=(i in notes)
        ## Input Hash or Space if MIDI input
        if (noteIn==False):
            char=" "
        elif (noteIn==True):
            char="#"    
        #### rows divisions    
        if ((count%16==0) and (count!=0)):
            #print(char, end="#\n")
            charString+=char+"\n"
        elif (count%16==1):
            charString+=char
        else:
            charString+=char
        count+=1
    return charString

##################################3 

### GUI
def tk_Matrix(notes):
    picture = drawMatrix(notes)
    pictureString.set(picture)
    root.update_idletasks()

def tk_Text(tkString):
    pictureString.set(tkString)
    root.update_idletasks()
    

def close():
    
    root.after(500, tk_Text("Goodbye"))
    try: root.after(1000, root.destroy())
    except: 
        print("Goodbye")
        quit()
    
buttonClicked=False
running=True
####

#####

def intro():
    string=logo2
    string+="Damn Simple MIDI Matrix"
    string+="\n\n"
    string+="by Ar2Di2"
    tk_Text(string)

###############################
###############################
#### Draw Window and Matrix ###
###############################
###############################

root = tk.Tk()
root.title("Damn Simple MIDI Matrix")
#root.geometry("300x300")
pictureString = tk.StringVar()
label = tk.Label(
    root, 
    textvariable = pictureString,
    width=30,
    height=20,
    anchor="center",
    font ="Mono 20",
    fg="white", 
    bg="black")

quitButton=tk.Button(
    root,
    text="Quit (Put CC to stop)",
    command=close
    )
        

app = tk.Frame(root)
app.grid()
label.grid(row=0)
quitButton.grid(row=1)

root.protocol("WM_DELETE_WINDOW", close)
root.bind('<Escape>', close)
#root.bind("<Key>q",close_window())

############

root.after(500, intro)
root.after(2000, scanning)

root.mainloop()
