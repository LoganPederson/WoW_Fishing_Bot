from tkinter import *
from wow_fishing_agent import FishingAgent
from time import *
import multiprocessing as mp

fishingAgent = FishingAgent()


def runFishingBot():
    fishingAgent.exitPlease = False
    fishingAgent.main()

# Function to stop the fishing bot
def stopRaftFishingBot():
    # Signal the process to terminate
    if fishing_process.is_alive():
        fishing_process.terminate()
    print('Fishing bot stopped.')

# Function to start the fishing bot i(n a separate process
def runFishingBot_background():
    global fishing_process
    fishing_process = mp.Process(target=runFishingBot)
    fishing_process.start()


def start_gui():
    # Create the main Tkinter window
    root = Tk()
    root.title("WowFishing_Bot")
    root.geometry("500x1500+1400+850")
    root.attributes('-topmost', True)

    # Create widgets
    myLabel1 = Label(root, text="Start Fishing")
    myLabel2 = Button(root, command=runFishingBot_background, text="Click Me!")
    myLabel3 = Button(root, command=stopRaftFishingBot, text="Exit")

    # Position widgets
    myLabel1.grid(row=0, column=0)
    myLabel2.grid(row=0, column=1)
    myLabel3.grid(row=0, column=2)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == '__main__':
    mp.freeze_support()
    start_gui()