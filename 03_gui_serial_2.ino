#include<Servo.h>

Servo servo1; //arm
Servo servo2;
Servo servo3;
Servo servo4;
Servo c1;      //camera
Servo c2;
Servo o_servo;
int move_time = 50;
int ENA = 5;
int ENB = 6;
int IN1 = 8;
int IN2 = 7;
int IN3 = 12;
int IN4 = 13;
int IR_R_num = A14;
int IR_L_num = A13;
int IR_R = HIGH;
int IR_L = HIGH;
#define GO_FORWARD {digitalWrite(IN1,LOW);digitalWrite(IN2,HIGH);digitalWrite(IN3,LOW);digitalWrite(IN4,HIGH);}
#define GO_BACK {digitalWrite(IN1,HIGH);digitalWrite(IN2,LOW);digitalWrite(IN3,HIGH);digitalWrite(IN4,LOW);}
#define GO_RIGHT {digitalWrite(IN1,LOW);digitalWrite(IN2,HIGH);digitalWrite(IN3,HIGH);digitalWrite(IN4,LOW);}
#define GO_LEFT {digitalWrite(IN1,HIGH);digitalWrite(IN2,LOW);digitalWrite(IN3,LOW);digitalWrite(IN4,HIGH);}
#define GO_STOP {digitalWrite(IN1,LOW);digitalWrite(IN2,LOW);digitalWrite(IN3,LOW);digitalWrite(IN4,LOW);}

int pos[] = {90, 90, 90, 90, 120, 0}; //それぞれの関節の角度、最初の4つがarm、後がcamera
char inkey;       // 入力文字格納用
int sub = 2;    //subject 対象の関節
int count = 0;
void setup() {
  Serial.begin( 9600 );
  servo1.attach(11);
  servo2.attach(2);
  servo3.attach(4);
  servo4.attach(3);
  c1.attach(9);
  c2.attach(10);
  o_servo = servo3;
  servo1.write(90);
  servo2.write(90);
  servo3.write(90);
  servo4.write(90);
  c1.write(120);
  c2.write(0);

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  GO_STOP;
  
  pinMode(IR_R_num, INPUT);
  pinMode(IR_L_num, INPUT);
}

void loop() {
  if (digitalRead(ENA == HIGH) or digitalRead(ENB == HIGH)) {
    digitalWrite(ENA, LOW);
    digitalWrite(ENB, LOW);
  }
  if ( Serial.available() > 0 ) {
    //　シリアルから値の読み込み
    inkey = Serial.read();
    switch ( inkey ) {
      case 'a':
        sub = 0;
        o_servo = servo1;
        pos[0]++;
        servo_move();
        break;
      case 'b':
        sub = 0;
        o_servo = servo1;
        pos[0]--;
        servo_move();
        break;
      case 'c':
        sub = 1;
        o_servo = servo2;
        pos[1]++;
        servo_move();
        break;
      case 'd':
        sub = 1;
        o_servo = servo2;
        pos[1]--;
        servo_move();
        break;
      case 'e':
        sub = 2;
        o_servo = servo3;
        pos[2]++;
        servo_move();
        break;
      case 'f':
        sub = 2;
        o_servo = servo3;
        pos[2]--;
        servo_move();
        break;
      case 'g':
        sub = 3;
        o_servo = servo4;
        pos[3]++;
        servo_move();
        break;
      case 'h':
        sub = 3;
        o_servo = servo4;
        pos[3]--;
        servo_move();
        break;
      case 'i':
        digitalWrite(ENA, HIGH);
        digitalWrite(ENB, HIGH);
        GO_FORWARD;
        delay(move_time);
        break;
      case 'j':
        digitalWrite(ENA, HIGH);
        digitalWrite(ENB, HIGH);
        GO_RIGHT;
        delay(move_time);
        break;
      case 'k':
        digitalWrite(ENA, HIGH);
        digitalWrite(ENB, HIGH);
        GO_LEFT;
        delay(move_time);
        break;
      case 'l':
        digitalWrite(ENA, HIGH);
        digitalWrite(ENB, HIGH);
        GO_BACK;
        delay(move_time);
        break;
    }
    inkey = -1;
    delay(1);
  }
}

void servo_move() {
  pos[0] = constrain(pos[0], 0, 180);
  pos[1] = constrain(pos[1], 0, 180);
  pos[2] = constrain(pos[2], 0, 180);
  pos[3] = constrain(pos[3], 20, 90);
  pos[4] = constrain(pos[4], 0, 180);
  pos[5] = constrain(pos[5], 0, 90);
  o_servo.write(pos[sub]);

}
