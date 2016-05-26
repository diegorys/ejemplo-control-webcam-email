/* 
  Firmware for MicOS.
  by Diego de los Reyes Rodríguez <http://diegorys.es> 

  created on 9 Dec 2014
  modified on 9 Dec 2014
  by Diego de los Reyes Rodríguez.
  http://diegorys.es
*/

#include <Servo.h> 

Servo servoCam;    // create servo object to control the webcam
int posCam = 0;

void setup() 
{ 
  Serial.begin(9600);         // initialize serial communication at 9600 bits per second.
  servoCam.attach(9);          // attaches the servo on pin 9 to the servo obj
  moveCenter();
} 
 
void loop() 
{
  int command = -1;
  
  if (Serial.available() > 0) {
    // read the incoming byte:
    command = Serial.read();
    
    switch(command){
      case 'a':
        moveRight();
        break;
      case 'd':
        moveLeft();
        break;
      case 'x':
        moveCenter();
        break;
      default:
        Serial.println("Unknown command");
    }
  }
  delay(100);
}

void moveRight(){
  posCam -= 30;
  if(posCam < 0) posCam = 0;
  servoCam.write(posCam);
  Serial.println("Moved right");
}

void moveLeft(){
  posCam += 30;
  if(posCam > 179) posCam = 179;
  servoCam.write(posCam);
  Serial.println("Moved left");
}

void moveCenter(){
  posCam = 90;
  servoCam.write(posCam);
  Serial.println("Moved center");
}
