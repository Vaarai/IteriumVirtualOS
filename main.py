#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import sys, getopt
from sty import fg, bg, ef, rs

class VirtualOS:
    initTopic = "home/init"
    mainTopic = "home"
    globalTopic = "home"
    initPayload = "$INIT$"
    brokerip = "localhost"
    state = True
    argv = ''

    def strState(self):
        if(self.state):
            return "isON"
        else:
            return "isOFF"
    def bitState(self):
        if(self.state):
            return "1"
        else:
            return "0"

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(self.initTopic)
        client.subscribe(self.mainTopic)
        client.subscribe(self.globalTopic)
        client.publish(self.mainTopic, self.initPayload + self.bitState())


    def on_message(self, client, userdata, msg):
        strPayload = str(msg.payload)[2:-1]
        if(not(strPayload.startswith(self.initPayload)) and not(strPayload.startswith("is"))):
            print(fg.yellow + "============ on_message ============" + fg.rs)
            print(fg.green + "Incomming message : " + fg.rs + strPayload)
            print(fg.green + "Precedent state   : " + fg.rs + self.strState())
            shouldSendState = False
            if(strPayload == "ON"):
                self.state = True
                shouldSendState = True
            elif(strPayload == "OFF"):
                self.state = False
                shouldSendState = True
            elif(strPayload == "SWITCH"):
                self.state = not(self.state)
                shouldSendState = True
            elif(strPayload == "INIT"):
                client.publish(self.mainTopic, self.initPayload + self.bitState())
                print(fg.green + "Action            : "  + fg.rs + "SEND INIT")
            
            if(shouldSendState == True):
                client.publish(self.mainTopic, self.strState())
                print(fg.green + "Action            : "  + fg.rs + "CHANGE STATE and UPDATE")
            print(fg.green + "New state         : " + fg.rs + self.strState())

    def init(self, arguments):
        self.argv = arguments

        try:
            opts, args = getopt.getopt(self.argv,"ht:ip:",["topic=","brokerip="])
        except getopt.GetoptError:
            print(str(err))  # will print something like "option -a not recognized"
            usage()
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print("""
                => IteriumVirtualOS
                    -t  --topic    : topic string
                    -ip --brokerip : Mqtt broker ip
                """)
                sys.exit()
            elif opt in ("-t", "--topic"):
                self.mainTopic = arg
                mainParsed = self.mainTopic.split('/')
                self.globalTopic = mainParsed[0] + '/' + mainParsed[1]
            elif opt in ("-ip", "--brokerip"):
                self.brokerip = arg

        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(self.brokerip, 1883)

        client.loop_forever()


myOS = VirtualOS()
myOS.init(sys.argv[1:])
