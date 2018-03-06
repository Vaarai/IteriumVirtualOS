import paho.mqtt.client as mqtt
import sys, getopt

class VirtualOS:

    mainTopic = "home"
    globalTopic = "home"
    initPayload = "$INIT$"
    brokerip = "localhost"
    state = 1
    argv = ''

    def __init__(self):
        self.data = []

    def strState(self):
        if(state):
            return "isON"
        else:
            return "isOFF"

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(self.mainTopic)
        client.subscribe(self.globalTopic)
        client.publish(self.mainTopic, self.initPayload + str(self.state))


    def on_message(self, client, userdata, msg):
        strPayload = str(msg.payload)[2:-1]
        print("==== on_massage ====")
        print("Incomming message : " + strPayload)
        print("Precedent state   : " + str(self.state))
        shouldSendState = 0
        if(strPayload == "ON"):
            self.state = 1
            shouldSendState = 1
        elif(strPayload == "OFF"):
            self.state = 0
            shouldSendState = 1
        elif(strPayload == "SWITCH"):
            self.state = not(self.state)
            shouldSendState = 1
        
        if(shouldSendState):
            client.publish(self.mainTopic, strState())
        print("New state         : " + strPayload)

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