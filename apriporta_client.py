import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import socket
import time
import logging
import logging.handlers
import RPi.GPIO as GPIO
import time


#logging, max 2M a file e ne tengo solo 5
LOG_FILENAME = 'client.log'
logger = logging.getLogger('client')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s (%(threadName)-10s) %(levelname)s %(message)s')
handler = logging.handlers.RotatingFileHandler(
			  LOG_FILENAME, maxBytes=2097152, backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

def apriporta(rele):
	pinList = [2,3]
	for x in range(0,1):
		GPIO.setmode(GPIO.BCM)

		for i in pinList: 
			GPIO.setup(i, GPIO.OUT) 
			GPIO.output(i, GPIO.HIGH)

		SleepTimeL = 2

	# main loop

		rele = int(rele)
		try:
			GPIO.output(rele, GPIO.LOW)
			logger.info ("Attivo rele " + str(rele))
			time.sleep(SleepTimeL);
			logger.info('cleanup dei gpio')
			GPIO.cleanup()
			#ret=publish.single("test", str(rele), hostname="www.romito.net")
			#logger.info('msg mandato')

	# End program cleanly with keyboard
		except:
			pass
			#logger.error('Qualcosa non ha funzionato!')


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("VIASACCHI/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	porta = ""
	logger.info(msg.topic + " " + msg.payload)

	if msg.payload == 'apri':
		if str(msg.topic[-1:]) == "1":
			porta = "2" #corrisponde a pin GPIO
		elif str(msg.topic[-1:]) == "2":
			porta = "3" #corrisponde a pin GPIO
		logger.info("porta selezionata " + str(porta))
		apriporta(porta)

	#apriporta(str(msg.payload))
	#print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("www.romito.net", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()