  
int m13_cw=2;
int m13_ccw=3;
int m24_cw=4;
int m24_ccw=5;
int pwm_13 = 9;
int pwm_24= 10;


char x = 0;

void setup() {
  pinMode(m13_cw,OUTPUT);
  pinMode(m13_ccw,OUTPUT);
  pinMode(m24_cw,OUTPUT);
  pinMode(m24_ccw,OUTPUT);
  pinMode(pwm_13,OUTPUT);
  pinMode(pwm_24,OUTPUT);

  Serial.begin(230400);
}

void loop() {
  
if(Serial.available()>0){
        x = Serial.read();
        Serial.println(x);
        if(x=='0')
             stop();
        else if(x=='1')
             forward();
        else if(x=='2')
             backward();
        else if(x=='3')
               left();
        else if(x=='4')
               right();
        else if(x=='5')
               not_in_frame_r();
        else if(x=='6')
               nw();
        else if(x=='7')
             ne();
        else if(x=='8')
              sf();
        else if(x=='9')
             not_in_frame_l();

  
}
}

void forward(){
  digitalWrite(pwm_13,HIGH);
  digitalWrite(pwm_24,HIGH);
  
  digitalWrite(m13_cw,HIGH);
  digitalWrite(m24_cw,HIGH);

  digitalWrite(m13_ccw,LOW);
  digitalWrite(m24_ccw,LOW);


}

void backward(){
  digitalWrite(m13_ccw,HIGH);
  digitalWrite(m24_ccw,HIGH);
  
  analogWrite(pwm_13,255);
  analogWrite(pwm_24,255);

  digitalWrite(m13_cw,LOW);
  digitalWrite(m24_cw,LOW);

}

void left(){
  digitalWrite(m13_ccw,HIGH);
  digitalWrite(m24_cw,HIGH);
 
  digitalWrite(pwm_13,HIGH);
  digitalWrite(pwm_24,HIGH);
  
  digitalWrite(m13_ccw,HIGH);
  digitalWrite(m24_cw,HIGH);

  digitalWrite(m13_cw,LOW);
  digitalWrite(m24_ccw,LOW);


}

void right(){
  digitalWrite(pwm_13,HIGH);
  digitalWrite(pwm_24,HIGH);
  
  digitalWrite(m13_cw,HIGH);
  digitalWrite(m24_ccw,HIGH);

  digitalWrite(m13_ccw,LOW);
  digitalWrite(m24_cw,LOW);
}

void not_in_frame_r(){
  digitalWrite(pwm_13,HIGH);  
  digitalWrite(pwm_24,HIGH);      

  digitalWrite(m13_cw,HIGH);
  digitalWrite(m24_ccw,HIGH);

  digitalWrite(m13_ccw,LOW);
  digitalWrite(m24_cw,LOW);
}

void stop(){
  digitalWrite(pwm_13,HIGH);
  digitalWrite(pwm_24,HIGH);
 
  digitalWrite(m13_cw,LOW);
  digitalWrite(m24_ccw,LOW);

  digitalWrite(m13_ccw,LOW);
  digitalWrite(m24_cw,LOW); 
}

void nw(){
  
  digitalWrite(pwm_24,HIGH);
  analogWrite(pwm_13,70);
  
  digitalWrite(m13_cw,HIGH);
  digitalWrite(m24_cw,HIGH);

  digitalWrite(m13_ccw,LOW);
  digitalWrite(m24_ccw,LOW);
}

void ne(){
  digitalWrite(pwm_13,HIGH);
  analogWrite(pwm_24,70);
  
  digitalWrite(m13_cw,HIGH);
  digitalWrite(m24_cw,HIGH);

  digitalWrite(m13_ccw,LOW);
  digitalWrite(m24_ccw,LOW);
}

void sf(){
  analogWrite(pwm_13,150);
  analogWrite(pwm_24,150);
 
  digitalWrite(m13_cw,HIGH);
  digitalWrite(m24_cw,HIGH);

  digitalWrite(m13_ccw,LOW);
  digitalWrite(m24_ccw,LOW);
}

void not_in_frame_l(){
  analogWrite(pwm_13,255);
  analogWrite(pwm_24,255);
  
  digitalWrite(m13_ccw,HIGH);
  digitalWrite(m24_cw,HIGH);

  digitalWrite(m13_cw,LOW);
  digitalWrite(m24_ccw,LOW);
}
