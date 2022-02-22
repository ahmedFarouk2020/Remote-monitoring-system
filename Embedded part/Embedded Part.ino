#include <dht11.h>

#define dht_pin A0 // DHT sensor is connected to A0 in arduino uno
#define IRSENSOR  3 // IR  sensor is connected to 3 in arduino uno

dht11 DHT11;

int IRSensorReading ;
void setup()
{
  Serial.begin(9600);
  pinMode (IRSENSOR, INPUT); // ir sensor pin INPUT
}

void loop() 
{
  /* Get readings of DHT */
  DHT11.read(dht_pin);
  /* Get the reading of ir sensor */
  IRSensorReading = digitalRead(IRSENSOR);
  /* print the output on serial monitor */
  /* this part can be commented while working with esp8266 */
  Serial.print("farouk.asdsad.com/get-server-order?");
  Serial.print("s1= ");
  Serial.print(IRSensorReading);
  Serial.print("&s2= ");
  Serial.print(DHT11.temperature); 
  Serial.print("&s3= ");
  Serial.print(DHT11.humidity);
  delay(5000);
}
