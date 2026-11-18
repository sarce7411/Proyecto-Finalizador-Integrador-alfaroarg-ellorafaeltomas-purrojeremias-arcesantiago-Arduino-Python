// C++ code

int estadoAnt8 = HIGH;
int estadoAnt9 = HIGH;
int estadoAnt10 = HIGH;
int estadoAnt11 = HIGH;

int potAnt = -100;     // 1. Variable agregada para que compile nivel3()  

void setup() {
  pinMode(5, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(6, OUTPUT); // pin buzzer
  
  pinMode(8, INPUT_PULLUP);
  pinMode(9, INPUT_PULLUP);
  pinMode(10, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);
  
  Serial.begin(9600);
}


void nivel1() {
  int estadoAct8 = digitalRead(8);
  int estadoAct9 = digitalRead(9);
  int estadoAct10 = digitalRead(10);
  int estadoAct11 = digitalRead(11);
  
  // pulsador 8 -> led 5
  if (estadoAnt8 == HIGH && estadoAct8 == LOW) {
    Serial.println("BOTON:A");
  }
  if (estadoAct8 == LOW) {
    digitalWrite(5, HIGH);
  } else {
    digitalWrite(5, LOW);
  }
  
  // pulsador 9 -> led 2
  if (estadoAnt9 == HIGH && estadoAct9 == LOW) {
    Serial.println("BOTON:B");
  }
  if (estadoAct9 == LOW) {
    digitalWrite(2, HIGH);
  } else {
    digitalWrite(2, LOW);
  }
  
  // pulsador 10 -> led 3
  if (estadoAnt10 == HIGH && estadoAct10 == LOW) {
    Serial.println("BOTON:C");
  }
  if (estadoAct10 == LOW) {
    digitalWrite(3, HIGH);
  } else {
    digitalWrite(3, LOW);
  }
  
  // pulsador 11 -> led 4
  if (estadoAnt11 == HIGH && estadoAct11 == LOW) {
    Serial.println("BOTON:D");
  }
  if (estadoAct11 == LOW) {
    digitalWrite(4, HIGH);
  } else {
    digitalWrite(4, LOW);
  }
  
  // actualizasr estados
  estadoAnt8 = estadoAct8;
  estadoAnt9 = estadoAct9;
  estadoAnt10 = estadoAct10;
  estadoAnt11 = estadoAct11;
  
  // escuchar al python
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "BUZZER:OK") {
      tone(6, 1000, 200); // buzzer:ok -> tono agudo
    }
    else if (comando == "BUZZER:ERROR") {
      tone(6, 200, 500);  // buzzer:error -> tono grave
    }
  }
}

void nivel2() {

}

void nivel3() {
  int lecturaCruda = analogRead(A0); // 0 a 1023

  // Solo enviamos si la perilla se movió al menos 5 unidades (evita ruido eléctrico)
  if (abs(lecturaCruda - potAnt) >= 5) {
    Serial.print("POT:");
    Serial.println(lecturaCruda);
    potAnt = lecturaCruda;
  }
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "NIVEL1") {
      tone(6, 1000, 200); // buzzer:ok -> tono agudo
      nivel1()
    }
    else if (comando == "NIVEL2") {
      tone(6, 200, 500);  // buzzer:error -> tono grave
      nivel2()
    }
    else if (comando == "NIVEL3") {
      tone(6, 200, 500);  // buzzer:error -> tono grave
      nivel3()
    }
  }
}
