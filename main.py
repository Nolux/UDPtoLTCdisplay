from appJar import gui
from time import strftime
import socket
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

HOST = config['SETTINGS']['HOST']
BUFSIZE = int(config['SETTINGS']['BUFSIZE'])
UDP_PORT = int(config['SETTINGS']['UDP_PORT'])

FONT_SIZE = int(config['SETTINGS']['FONT_SIZE'])
FONT_COLOR = config['SETTINGS']['FONT_COLOR']
BACKGROUND_COLOR = config['SETTINGS']['BACKGROUND_COLOR']

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, UDP_PORT))

#get timecode from UDP
def get_LTC():
    data, addr = sock.recvfrom(BUFSIZE)
    if data is None:
        return '--:--:--:--'
    data_Decoded = data.decode("UTF-8")[0:11] #Making sure just to take "xx:xx:xx:xx"
    return data_Decoded

def quit(x):
    app.stop()
    sock.close()
    print("Bye!")

#refresh clock and timecode
def set_text():
    app.setLabel("ltc", get_LTC())
    app.setLabel("time", strftime('%H:%M'))
    app.after(20, set_text)


app = gui()

app.bindKey("x", quit)
app.bindKey("<Escape>", quit)

app.setTitle("UDP to LTC display")
app.setGeometry("fullscreen")

app.addLabel("filler", " ")
app.addLabel("time", "--:--")
app.addLabel("ltc", "--:--:--:--")
app.addLabel("filler2", " ")

app.setFont(FONT_SIZE)
app.setBg(BACKGROUND_COLOR)
app.setFg(FONT_COLOR)

app.thread(set_text())

app.go()