#!/usr/bin/env python3

import rtmidi, sys, threading, time
import tkinter as tk

#midiin = rtmidi.RtMidiIn()
#ports = range(midiin.getPortCount())

notes=[]

#def dsmmText(delay, text):
#    dsmmMain.update_idletasks()
#    dsmmMain.after(delay,dsmmMain.pictureString.set(text))


logo="""
###   ### #   # #   #
#  # #    ## ## ## ##
#  #  ##  # # # # # #
#  #    # #   # #   #
###  ###  #   # #   #
"""

mainHelpText = """
Main
=====
This software shows hashes
on place each Matrix.
The picture has a
resolution 16x8
because of resolution
the single MIDI channel
to 128 notes.
Table below illustrates,
how this software runs.

+-----+-----------+
|     | Midi note |
| Row |   number  |
+-----+-----------+
|  0  |   0-15    |
|  1  |  16-31    |
|  2  |  32-47    |
|  3  |  48-63    |
|  4  |  64-79    |
|  5  |  80-95    |
|  6  |  96-111   |
|  7  | 112-127   |
+-----------------+

"""

aboutText = """
\n\n
Damn Simple MIDI Matrix \n
by Ar2Di2 \n
\n\n
If do You have any suggestions,\n
please write me on
artur.wrona91 (at) gmail (dot) com
\n\n

"""






def initPort():
    messageText=""
    dsmmMain.text(10, " ")
    for i in ports:
        device = rtmidi.RtMidiIn()
        messageText+='OPENING '
        messageText+=dev.getPortName(i)
        messageText+="\n"
        dsmmMain.text(10, messageText)
        collector = Collector(device, i)
        collector.start()
        collectors.append(collector)      
    messageText="\n"
    dsmmMain.text(1000, " ")
    global running
    running=True
    
def quitPorts():
    for c in collectors:
        c.quit = True    
    
def scanning():    
    if running:
        #print(ports)
        dsmmMain.text(0, drawMatrix(notes))
        dsmmMain.after(0, scanning)
       

def destroyPort():
    for c in collectors:
        c.quit = True    


def print_message(midi):
    if midi.isNoteOn():
        noteNumber=midi.getNoteNumber()
        notes.append(noteNumber)
        return noteNumber
    elif midi.isNoteOff():
        #print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
        notes.clear()
        #print("OFF")
        return 0
    elif midi.isController():
        pass

def tuiDrawMatrix(fps):
    time.sleep(1/fps)
    print("\033c")
    print(drawMatrix(notes))
    return 0

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

####### GUI
class dsmmApp(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('DSMM')
        self.bind('<Escape>', self.escapeHandle)
        self.bind('m', self.chooseMidiHandle)
        self.bind('<F1>', self.helpHandle)
        self.pictureString=tk.StringVar()
        self.grid()
        self.createWidgets()
        self.intro(10)
        self.text(1000, "")
        self.dsmmStart()
        
    def intro(self, delay):
        string=logo
        string+="Damn Simple MIDI Matrix"
        string+="\n\n"
        string+="by Ar2Di2"
        self.text(delay,string)
        
    def escapeHandle(self, event=None):
        self.close()
    
    def chooseMidiHandle(self, event=None):
        self.chooseMidi()
        
    def helpHandle(self, event=None):
        self.help()
    
    def dsmmStart(self):
        self.after(500, initPort)
        self.after(1000, scanning)
    
    def text(self, delay, text):
        self.update_idletasks()
        self.after(delay, self.pictureString.set(text))
    
    def close(self):
        self.update_idletasks()
        global running
        running=False
        self.text(100, "Bye, bye!!!")
        self.after(1000, self.master.destroy)
    
    def chooseMidi(self):
        self.update_idletasks()
        global running
        running=False
        self.text(100, "Choose MIDI Devices")
        dsmmChooseMidi=dsmmMidi()
        dsmmChooseMidi.focus_set()
        dsmmChooseMidi.mainloop()
        
    def help(self):
        self.update_idletasks()
        global running
        running=False
        #self.text(1000, "Help")
        dsmmHelpWindow=dsmmHelp()
        dsmmHelpWindow.focus_set()
        dsmmHelpWindow.mainloop()
    
    def createWidgets(self):
        self.matrixFrame = tk.Label(
               self,
               textvariable=self.pictureString,
               bg='black',
               fg='white',
               width=30,
               height=20,
               anchor="center",
               font ="Mono 20"
               )        
        
        
        self.quitButton = tk.Button(
               self,
               text='Quit (Esc)', 
               command=self.close
               )
        
               
        self.midiButton = tk.Button(
               self,
               text='MIDI (M)', 
               command=self.chooseMidi
               )
               
        self.helpButton = tk.Button(
               self,
               text='Help (F1)', 
               command=self.help
               )               
               
        self.matrixFrame.grid(row=0, columnspan=3)
        self.quitButton.grid(row=1, column=0)
        self.midiButton.grid(row=1, column=1)
        self.helpButton.grid(row=1, column=2)
        

class dsmmMidi(tk.Toplevel):
    def __init__(self, parent=None):
        tk.Toplevel.__init__(self, parent)
        self.title('MIDI')
        self.geometry('+0+0')
        self.bind('<Escape>', self.escapeHandle)
        self.bind('<Return>', self.enterHandle)
        self.grid()
        self.createWidgets()
    
    def listPorts(self):
        
        for each_item in allPorts:
            self.port = dev.getPortName(each_item)
            self.midiDevices.insert(tk.END, self.port)
        #for each_item in range(len(ports)):
        #    self.midiDevices.insert(tk.END, ports[each_item])
    
    def escapeHandle(self, event=None):
        self.cancel()
        
    def enterHandle(self, event=None):
        self.applyAndExit()
            
    def apply(self):
        global ports
        ports=[]
        self.selected=self.midiDevices.curselection()
        stringText=""
        for i in self.selected:
            ports.append(i)
        ports=self.selected
        
    def cancel(self):
        self.destroy()
        quitPorts()
        dsmmMain.dsmmStart()
        
    def applyAndExit(self):
        self.apply()
        self.cancel()
        #self.after(200, self.cancel())
    
    def text(self, delay, text):
        self.update_idletasks()
        self.after(delay, self.pictureString.set(text))
        
        
    def createWidgets(self):
        self.midiDevices = tk.Listbox(
               self,
               selectmode = "multiple",
               exportselection = 0
                )
                
        self.applyAndExitButton = tk.Button(
               self,
               text="OK" ,
               command=self.applyAndExit
                )
                
        self.applyButton = tk.Button(
               self,
               text="Apply" ,
               command=self.apply
                )
                
        self.cancelButton = tk.Button(
                self,
                text="Cancel",
                command=self.cancel
                )
        
        self.listPorts()
        
        self.midiDevices.grid(row=0, column=0, columnspan=3)
        self.applyButton.grid(row=1, column=1)
        self.applyAndExitButton.grid(row=1, column=0)
        self.cancelButton.grid(row=1, column=2)
        
class dsmmHelp(tk.Toplevel):
    def __init__(self, parent=None):
        tk.Toplevel.__init__(self, parent)
        self.geometry('+0+0')
        self.title("Help")
        self.pictureString=tk.StringVar()
        self.bind('<Escape>', self.escapeHandle)
        self.bind('<F1>', self.mainHelpHandle)
        self.bind('<F2>', self.aboutHandle)
        self.grid()
        self.createWidgets()
    
    def text(self, delay, text):
        self.update_idletasks()
        self.after(delay, self.pictureString.set(text))
    
    def escapeHandle(self, event=None):
        self.cancel()
    
    def aboutHandle(self, event=None):
        self.about()
    
    def mainHelpHandle(self, event=None):
        self.mainHelp()
    
    def about(self):
        self.text(500, aboutText)    
    
    def mainHelp(self):
        self.text(500, mainHelpText)
                    
    def cancel(self):
        self.destroy()
        dsmmMain.dsmmStart()
        
        
        
    def createWidgets(self):
        self.helpText = tk.Label(
               self,
               textvariable=self.pictureString,
               bg='black',
               fg='white',
               width=30,
               height=30,
               wraplength=300,
               anchor="center",
               font ="Mono 12"
               )        
        
        self.mainHelpButton = tk.Button(
               self,
               text="Main (<F1>)" ,
               command=self.mainHelp
                )
        
                        
        self.aboutButton = tk.Button(
               self,
               text="About (<F2>)" ,
               command=self.about
                )
                
        self.cancelButton = tk.Button(
                self,
                text="Cancel (Esc)",
                command=self.cancel
                )
        
        
        
        self.helpText.grid(row=0, column=0, columnspan=3)
        self.mainHelpButton.grid(row=1, column=0)
        self.aboutButton.grid(row=1, column=1)
        self.cancelButton.grid(row=1, column=2)
        self.mainHelp()

####### End GUI

class Collector(threading.Thread):
    def __init__(self, device, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.port = port
        self.portName = device.getPortName(port)
        self.device = device
        self.quit = False

    def run(self):
        self.device.openPort(self.port)
        self.device.ignoreTypes(True, False, True)
        while True:
            if self.quit:
                return
            msg = self.device.getMessage(250)
            #print(msg)
            if msg:
                print_message(msg)
                #for i in notes:
                #    print(i, end=" ")
                #print("")
                
            
                
                



                

dev = rtmidi.RtMidiIn()
collectors = []


allPorts=range(dev.getPortCount())

#ports = [0]
ports = allPorts

if __name__ == '__main__':
    dsmmMain = dsmmApp()
    dsmmMain.focus_set()
    dsmmMain.mainloop()



