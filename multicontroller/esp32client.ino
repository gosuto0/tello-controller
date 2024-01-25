#include <WiFi.h>

const char *tello_ssid="TELLO-ID";
const char *tello_password="";

const char *pc_ssid="PCMOBILEHOTSPOT";
const char *pc_password="PASS";

const char *TELLO_IP="192.168.10.1";
const char *PC_IP="192.168.137.1";

const int CLIENTPORT=5555;
const int TELLOPORT=8889;

boolean isPMODE=false;

const int maxSize=10;
String programList[maxSize];

int listSize=0;

WiFiUDP Udp;
char packetBuffer[255];

WiFiClient client;

void setup() {
  Serial.begin(250000);
  server_connect();
}

void server_connect() {
  WiFi.begin(pc_ssid, pc_password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("[WIFI] Wifi Connecting");
  }
  Serial.println("[WIFI] Wifi Connected");
  while (!client.connect(PC_IP, CLIENTPORT)){
    delay(1000);
    Serial.println("[Client] Server Connecting");
  }
  client.write("c0");
  Serial.println("[Client] Server Connected");
}

void server_receive(char* command) {
  if(!isPMODE){
    if(String(command)=="s0"){
      Serial.println("[Client] Test Succesfully");
    }else if(String(command)=="s1"){
      isPMODE=true;
      listSize = 0;
      Serial.println("[Write] Now Program Mode");
    } else{
      Serial.println(String(command) + " is unknow command.");
    }
  }else if(isPMODE){
    if(String(command)=="allclear"){
      Serial.println("[Write] Program clear.");
      listSize = 0;
      for (int i = 0; i < maxSize; ++i) {
        programList[i] = '\0';
      }
      Serial.println("[Write] Clear done.");
    }else if(String(command)=="end"){
      Serial.println("[Write] Program Finish.");
      Serial.println("[Client] Disconnecting server.");
      client.write("c1");
      client.stop();
      wifi_disconnect();
      Serial.println("[Client] Disconnected.");
      Serial.println("[TELLO] Start Tello Sequence");
      tello_sequence();
    }else if(maxSize>listSize){
      programList[listSize] = command;
      listSize++;
      Serial.println("[Write] Line: "+String(listSize)+" Command: "+String(command));
    }
  }
}

void loop() {
  static char buffer[30];
  static int index = 0;
  while (client.available()) {
    char c = client.read();
    if (c == '!') {
      server_receive(buffer);
      index = 0;
      for (int i = 0; i < 30; ++i) {
        buffer[i] = '\0';
      }
    } else {
      buffer[index] = c;
      index++;
    }
  }
}

void tello_sequence(){
  WiFi.begin(tello_ssid, tello_password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("[TELLO] Connecting Tello");
  }
  Serial.println("[TELLO] Connected");
  Udp.begin(TELLOPORT);
  telloSendMessage("command");
  for (int i = 0; i < maxSize; ++i) {
    if(programList[i]!=""){
      if(programList[i].indexOf("delay")!=-1){
        int delaynum = String(programList[i]).substring(5).toInt();
        delay(int(delaynum));
      }
      char buffer[50];
      programList[i].toCharArray(buffer, sizeof(buffer));
      telloSendMessage(buffer);
      Serial.println("[TELLO] "+String(programList[i]));
    }
  }
  Serial.println("[TELLO] Program Finished, Wait 5 seconds.");
  delay(5000);
  telloSendMessage("land");
  Serial.println("[Write] Program clear.");
  listSize = 0;
  for (int i = 0; i < maxSize; ++i) {
    programList[i] = '\0';
  }
  isPMODE = false;
  Serial.println("[Write] Clear done.");
  Serial.println("[TELLO] Disconnecting Tello.");
  wifi_disconnect();
  Serial.println("[TELLO] Disconncted.");
  delay(1000);
  server_connect();
}

void telloSendMessage(char* ReplyBuffer) {
  Udp.beginPacket(TELLO_IP, TELLOPORT);
  Udp.printf(ReplyBuffer);
  Udp.endPacket();
}

void wifi_disconnect(){ while(WiFi.status() == WL_CONNECTED ){ WiFi.disconnect(); delay(2000); } }