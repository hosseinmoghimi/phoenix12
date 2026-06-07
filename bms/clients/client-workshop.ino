#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
//DOIT ESP-Mx Devkit (ESP8266)
//const char *ssid = "leo";
//const char *password = "OmranRamzBedam!@#";
const char *ssid = "WORKSHOP";
const char *password = "09155323633";

const String FEEDER_SN = "32476500065398";
const String FEEDER_PIN = "09155323633@";

const int DELAY_FOR_RECURSIVE_COMMAND = 500;   
const int HTTP_PORT = 80;
const String BASE_URL = "/";
const String handleExecuteCommand_url = "execute_command/";
const String handleGetStatus_url = "status/";

const String requestAddLog_url = "http://192.168.30.80/bms/add_log_from_client/";

// 0 for all registers
const int RELAY_1 = 1;  //tx
const int RELAY_2 = 4;  //d4
const int RELAY_3 = 3;  //rx
const int RELAY_4 = 2;  //d2

const String RELAY_1_PIN = "09155323633#";
const String RELAY_2_PIN = "09155323633#";
const String RELAY_3_PIN = "09155323633#";
const String RELAY_4_PIN = "09155323633#";

const int led = LED_BUILTIN;
ESP8266WebServer server(HTTP_PORT);
void handleRoot() {
  digitalWrite(led, 1);
  server.send(200, "text/plain", "hello from esp8266!");
  digitalWrite(led, 0);
}

void handleNotFound() {
  digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  digitalWrite(led, 0);
}

String current_registers_status() {
  String reg1 = digitalRead(RELAY_1) ? "1" : "0";
  String reg2 = digitalRead(RELAY_2) ? "1" : "0";
  String reg3 = digitalRead(RELAY_3) ? "1" : "0";
  String reg4 = digitalRead(RELAY_4) ? "1" : "0";
  String data = "{\"registers\":[{\"register\":\"1\",\"state\":\"" + reg1 + "\"},{\"register\":\"2\",\"state\":\"" + reg2 + "\"},{\"register\":\"3\",\"state\":\"" + reg3 + "\"},{\"register\":\"4\",\"state\":\"" + reg4 + "\"}]}";
  return data;
}

void add_log(int my_register, String command) {
  // Your Domain name with URL path or IP address with path
  //    HTTPClient http;
  //
  //    http.begin(requestAddLog_url.c_str());
  //
  //    // Send HTTP POST request
  //    String post_data = "{\"feeder_sn\":\"" + FEEDER_SN + "\",\"feeder_pin\":\"" + FEEDER_PIN + "\",\"register\":\"" + my_register + "\",\"command\":\"" + command + "\"}";
  //
  //    http.addHeader("Content-Type", "application/json");
  //    int httpResponseCode = http.POST(post_data);
  //    if (httpResponseCode > 0)
  //    {
  //
  //        String payload = http.getString();
  //    }
  //    http.end();

  return;
}

void execute_command(int my_register, String command) {
  if (command == "+") {
    digitalWrite(my_register, true);
  }
  if (command == "-") {
    digitalWrite(my_register, false);
  }
  if (command == "!") {
    digitalWrite(my_register, !digitalRead(my_register));
  }
  if (command == "^") {
    digitalWrite(my_register, true);
    delay(DELAY_FOR_RECURSIVE_COMMAND);
    digitalWrite(my_register, false);
  }
  if (command == "v") {
    digitalWrite(my_register, false);
    delay(DELAY_FOR_RECURSIVE_COMMAND);
    digitalWrite(my_register, true);
  }
  
  add_log(my_register, command);
}





void handleExecuteCommand() {

  if (!server.hasArg("register") || server.arg("register") == NULL || !server.hasArg("command") || server.arg("command") == NULL || !server.hasArg("pin") || server.arg("pin") == NULL

  ) {  // If the POST request doesn't have username and password data
    server.send(400, "text/plain", "400: Invalid Request");
    return;
  }
  int my_register = server.arg("register").toInt();

  String command = server.arg("command");
  String pin = server.arg("pin");

  if (my_register == 0) {
    execute_command(RELAY_1, command);
    execute_command(RELAY_2, command);
    execute_command(RELAY_3, command);
    execute_command(RELAY_4, command);
  } else if (my_register == 1) {
    my_register = RELAY_1;
  } else if (my_register == 2) {
    my_register = RELAY_2;
  } else if (my_register == 3) {
    my_register = RELAY_3;
  } else if (my_register == 4) {
    my_register = RELAY_4;
  }

  execute_command(my_register, command);


  server.send(200, "text/json", current_registers_status());
  return;
}



 


void handleGetStatus() {
  server.send(200, "text/json", current_registers_status());
  return;
}


void setup_outputs() {

  pinMode(led, OUTPUT);
  digitalWrite(led, 0);

  pinMode(RELAY_1, OUTPUT);
  pinMode(RELAY_2, OUTPUT);
  pinMode(RELAY_3, OUTPUT);
  pinMode(RELAY_4, OUTPUT);

  digitalWrite(RELAY_1, 0);
  digitalWrite(RELAY_2, 0);
  digitalWrite(RELAY_3, 0);
  digitalWrite(RELAY_4, 0);


}
void setup(void) {
  setup_outputs();
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  if (MDNS.begin("esp8266")) { 
  }
  server.on(BASE_URL, handleRoot);
  server.on(BASE_URL + handleExecuteCommand_url, HTTP_POST, handleExecuteCommand);
  server.on(BASE_URL + handleGetStatus_url, HTTP_GET, handleGetStatus);

  server.begin();
  server.onNotFound(handleNotFound);
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}