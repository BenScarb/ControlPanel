#!/usr/bin/python3

import cherrypy
import paho.mqtt.client as mqtt
import io
import lightcontrol

class WebPanel(object):
    def __init__(self):
        self.pos_temps = dict()
        self.pos_temps['none'] = "status;No position supplied"
        self.lightsstrip = lightcontrol.Lights()
        self.lightsstrip.CreateStrip()

    @cherrypy.expose
    def index(self):
        pageContents = ''
        with open('page.html', 'r') as inFile:
            pageContents = inFile.read()

        return pageContents
    index.exposed = True

    @cherrypy.expose
    def lights(self, state='on', timespan='20'):
        self.lightsstrip.Terminate = True
        if state == 'on':
            self.lightsstrip.OnForTime(self.lightsstrip.Colours['White'], timespan)
        elif state == 'off':
            self.lightsstrip.TurnOff()
        elif state == 'towards':
            self.lightsstrip.ToShedForTime(self.lightsstrip.Colours['White'], timespan)
        elif state == 'away':
            self.lightsstrip.ToHouseForTime(self.lightsstrip.Colours['White'], timespan)
            

        return "Done - " 

    @cherrypy.expose
    def temps(self, position='none'):
        if position not in self.pos_temps.keys():
            self.pos_temps['none'] = position + ';N/A'
            position = 'none'
        return self.pos_temps[position]

class MosListener(object):
    def __init__(self, broker_address):
        self.key = 'sensors/#'
        self.panel = None

        #create new instance
        self.client = mqtt.Client("Sensors_PageListener")
        #attach function to callback
        self.client.on_message=self.on_message
        #connect to broker
        self.client.connect(broker_address)

    def Start(self):
        #start the loop
        self.client.loop_start()
        self.client.subscribe(self.key)

    def Stop(self):
        #stop the loop
        self.client.loop_stop()
        self.client.disconnect()

    def on_message(self, client, userdata, message):
        keyParts = message.topic.split('/')

        if keyParts[1] == "shed" and keyParts[2] == "temp":
            messageParts = message.payload.decode("utf-8", 'ignore').split(';')
            self.panel.pos_temps[keyParts[3].lower()] = keyParts[3].lower() + ';' + messageParts[1]


if __name__ == '__main__':
    thePage = WebPanel()
    theListener = MosListener("192.168.17.21")
    theListener.panel = thePage

    theListener.Start()
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(thePage)
    theListener.Stop()
