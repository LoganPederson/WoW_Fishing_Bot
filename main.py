from tkinter import *
from wow_fishing_agent import FishingAgent
from time import *
import multiprocessing as mp
import logging
import queue

def custom_print(message, msg_queue=None):
    if msg_queue:
        # Send message to the queue
        msg_queue.put(message)
    else:
        # Directly update the text widget and print to console
        text_widget.configure(state=NORMAL)
        text_widget.insert(END, message + '\n')
        text_widget.see(END)
        text_widget.configure(state=DISABLED)
        print(message)

def runFishingBot(msg_queue):
    fishingAgent = FishingAgent(msg_queue)
    fishingAgent.exitPlease = False
    fishingAgent.main()

def stopRaftFishingBot():
    if fishing_process.is_alive():
        fishing_process.terminate()
    custom_print('Fishing bot stopped.')

def runFishingBot_background():
    global fishing_process
    fishing_process = mp.Process(target=runFishingBot, args=(msg_queue,))
    fishing_process.start()
def process_queue():
    try:
        while True:
            # Non-blocking check of message queue
            message = msg_queue.get_nowait()
            custom_print(message)
    except queue.Empty:
        # No messages in queue
        pass
    root.after(100, process_queue)  # Check the queue again after 100 ms

def start_gui():
    global text_widget, root, msg_queue
    root = Tk()
    root.title("WowFishing_Bot")
    root.geometry("700x300+1400+850")
    root.attributes('-topmost', True)

    myLabel1 = Label(root, text="Start Fishing")
    myLabel2 = Button(root, command=runFishingBot_background, text="Click Me!")
    myLabel3 = Button(root, command=stopRaftFishingBot, text="Exit")
    myLabel1.grid(row=0, column=0)
    myLabel2.grid(row=0, column=1)
    myLabel3.grid(row=0, column=2)

    text_widget = Text(root, height=10, state=DISABLED)
    text_widget.grid(row=1, columnspan=3)

    root.after(100, process_queue)  # Start checking the queue
    root.mainloop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')
    mp.freeze_support()
    msg_queue = mp.Queue()  # Create a multiprocessing queue
    start_gui()