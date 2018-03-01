from appJar import gui
from time import strftime
import socket
import configparser
import select

#Load all variables from config file
config = configparser.ConfigParser()
config.read('config.ini')

HOST = config['SETTINGS']['HOST']
BUFSIZE = int(config['SETTINGS']['BUFSIZE'])
UDP_PORT = int(config['SETTINGS']['UDP_PORT'])

FONT_SIZE = int(config['SETTINGS']['FONT_SIZE'])
FONT_COLOR = config['SETTINGS']['FONT_COLOR']
BACKGROUND_COLOR = config['SETTINGS']['BACKGROUND_COLOR']

EXIT_KEY = config['SETTINGS']['EXIT_KEY']
SHOW_TIME = config['SETTINGS']['SHOW_TIME']

#Connect to server and bind port on local
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, UDP_PORT))


#Get timecode from UDP
def get_LTC():
    ready = select.select([sock], [], [], 1)
    if ready[0]:
        data, addr = sock.recvfrom(BUFSIZE)
        data_Decoded = data.decode("UTF-8")[0:11]  # Making sure just to take "xx:xx:xx:xx"
        return data_Decoded
    else:
        return 'xx:xx:xx:xx'
        pass


#Exit app function called by keypress
def quit(x):
    app.stop()
    sock.close()
    print("Bye!")


#Refresh clock and timecode
def update_tc():
    app.setLabel("ltc", get_LTC())
    app.after(2, update_tc)

def update_time():
    app.setLabel("time", strftime('%H:%M'))
    app.after(100, update_time)



app = gui()

app.bindKey(EXIT_KEY, quit)

app.setTitle("UDP to LTC display")
app.setGeometry("fullscreen")

#Create all labels
app.addLabel("filler", " ")
if SHOW_TIME == 'True':
    app.addLabel("currenttime", "Current time:").config(font="Helvetica 20", anchor="s")
    app.addLabel("time", "--:--")
    app.addLabel("filler2", " ")
app.addLabel("currentltc", "LTC:").config(font="Helvetica 20", anchor="s")
app.addLabel("ltc", "--:--:--:--")
app.addLabel("filler3", " ")

app.setFont(FONT_SIZE)
app.setBg(BACKGROUND_COLOR)
app.setFg(FONT_COLOR)


#Start background loop
app.thread(update_tc())
if SHOW_TIME == 'True':
    app.thread(update_time())

app.go()