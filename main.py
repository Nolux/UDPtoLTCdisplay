from appJar import gui
from time import strftime
import socket

HOST = ''
BUFSIZE = 20
UDP_PORT = 53001

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
    print("Bye!")

#refresh clock and timecode
def set_text():
    app.setLabel("ltc", get_LTC())
    app.setLabel("time", strftime('%H:%M'))
    app.after(20, set_text)


app = gui()

app.bindKey("x", quit)

app.setTitle("UDP to LTC display")
app.setGeometry("fullscreen")

app.addLabel("filler", " ")
app.addLabel("time", "--:--")
app.addLabel("ltc", "--:--:--:--")
app.addLabel("filler2", " ")

app.setFont(100)
app.setBg("black")
app.setFg("white")

app.thread(set_text())

app.go()