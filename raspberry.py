import imaplib
import email
import time
import serial
import RPi.GPIO as GPIO
import signal
import sys
import os

from subprocess import call

MAIL_CHECK_FREQ = 2      # check mail every X seconds

#Commands
COMMAND_TAKE_PICTURE 	= "Comando foto"
COMMAND_MOVE_RIGHT 	= "Comando derecha"
COMMAND_MOVE_LEFT 	= "Comando izquierda"
COMMAND_MOVE_CENTER	= "Comando centrar"
COMMAND_EXIT		= "Comando salir"

#Mail to alert & credentials
USERNAME = "xxxxx@gmail.com"
PASSWORD = "xxxxx"

#Attributes
ser = serial.Serial('/dev/ttyACM0', 9600) # send serial data to Arduino

#Block Actions

def takePicture():
	call(["fswebcam", "-r 640x480", "foto.jpg"])

def moveRight():
	ser.write('a')

def moveLeft():
	ser.write('d')

def moveCenter():
	ser.write('x')

def exit():
	GPIO.cleanup()
	print "Hasta luego"
	os._exit(1)

actions = {COMMAND_MOVE_RIGHT: 	 moveRight,
	   COMMAND_MOVE_CENTER:  moveCenter,
	   COMMAND_MOVE_LEFT: 	 moveLeft,
	   COMMAND_TAKE_PICTURE: takePicture,
	   COMMAND_EXIT: 	 exit}

#End block Actions

#Block Utils

def exitHandler(signal, frame):
	alertOk()
	exit()

def alertOk():
	GPIO.output(7, True)
	time.sleep(1)
	GPIO.output(7, False)

def alertKo():
	GPIO.output(7, True)
	time.sleep(0.2)
	GPIO.output(7, False)
	time.sleep(0.2)
	GPIO.output(7, True)
	time.sleep(0.2)
	GPIO.output(7, False)

#End block

#Main:
def main():
	moveCenter()
	#Capture signal Ctrl+C
	signal.signal(signal.SIGINT, exitHandler)

	#Init GPIO
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT)
	GPIO.output(7, False)
	
	print "Hello!"
	print "Press Ctrl+C to exit"
	print "Waiting command..."

	# Connect
	imapClient = imaplib.IMAP4_SSL("imap.gmail.com")
	# Login
	imapClient.login(USERNAME, PASSWORD)

	command = ""

	while True:
		print "Checking..."
		# Choose folder inbox
		imapClient.select("INBOX")
		# Fetch unseen messages
		_, message_ids = imapClient.search(None, "UNSEEN")
		for msg_id in message_ids[0].split():
	        	# Download the message
			_, data = imapClient.fetch(msg_id, "(RFC822)")
		        # Parse data using email module
	        	msg = email.message_from_string(data[0][1])
			command = msg["subject"]
			print "Recibido: ",command

			try:
				alertOk()
				res = actions[command]()
				print "OK"
			except:
				print "Error ",command,": ",sys.exc_info()[0]
				alertKo()

		time.sleep(MAIL_CHECK_FREQ)

main()