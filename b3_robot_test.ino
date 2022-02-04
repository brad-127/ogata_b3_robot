#include<Servo.h>

Servo servo1; //arm
Servo servo2;
Servo servo3;
Servo servo4;
Servo c1;      //camera
Servo c2;
Servo o_servo;

int pos1 = 0;
int pos2 = 0;
int pos3 = 0;
char inkey;       // 入力文字格納用

void setup() {
 Serial.begin( 9600 );
 servo1.attach(11);
 servo2.attach(2);
 servo3.attach(4);
 servo4.attach(3);
 c1.attach(9);
 c2.attach(10);
 o_servo=servo2;
 c1.write(110);
 c2.write(0);
}

void loop() {

    servo_move();

if( Serial.available() > 0  ) {
    //　シリアルから値の読み込み
    inkey = Serial.read();
    // シリアルポートへ出力
    Serial.print( inkey );
    switch( inkey ){
      case '1':
        o_servo=servo1;
        break;
      case '2':
        o_servo=servo2;
        break;
      case '3':
        o_servo=servo3;
        break;
      case '4':
        o_servo=servo4;
        break;
      case '5':
        o_servo=c1;
        break;
      case '6':
        o_servo=c2;
        break;
      default:
        break;
       
    }
  }
  delay( 1 );   // 1ms停止

}

void servo_move(){

for(pos1 = 60;pos1 < 90;pos1++)
{
  o_servo.write(pos1);
  delay(30);
  
  }

for(pos1 = 90;pos1 >= 60;pos1--)
{
  o_servo.write(pos1);
  delay(30);
  
  }

  
  }
