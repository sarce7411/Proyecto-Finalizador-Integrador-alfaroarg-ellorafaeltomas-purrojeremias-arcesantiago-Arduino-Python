int estadoAnt8 = HIGH;
int estadoAnt9 = HIGH;
int estadoAnt10 = HIGH;
int estadoAnt11 = HIGH;

int potAnt = -100;
int nivelActual = 1;

void setup() {
  pinMode(5, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(6, OUTPUT);

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

  if (estadoAnt8 == HIGH && estadoAct8 == LOW) {
    Serial.println("BOTON:A");
  }
  if (estadoAct8 == LOW) {
    digitalWrite(5, HIGH);
  } else {
    digitalWrite(5, LOW);
  }

  if (estadoAnt9 == HIGH && estadoAct9 == LOW) {
    Serial.println("BOTON:B");
  }
  if (estadoAct9 == LOW) {
    digitalWrite(2, HIGH);
  } else {
    digitalWrite(2, LOW);
  }

  if (estadoAnt10 == HIGH && estadoAct10 == LOW) {
    Serial.println("BOTON:C");
  }
  if (estadoAct10 == LOW) {
    digitalWrite(3, HIGH);
  } else {
    digitalWrite(3, LOW);
  }

  if (estadoAnt11 == HIGH && estadoAct11 == LOW) {
    Serial.println("BOTON:D");
  }
  if (estadoAct11 == LOW) {
    digitalWrite(4, HIGH);
  } else {
    digitalWrite(4, LOW);
  }

  estadoAnt8 = estadoAct8;
  estadoAnt9 = estadoAct9;
  estadoAnt10 = estadoAct10;
  estadoAnt11 = estadoAct11;
}

void nivel2() {
  int lecturaCruda = analogRead(A1);

  if (abs(lecturaCruda - potAnt) >= 5) {
    Serial.println(lecturaCruda);
    potAnt = lecturaCruda;
  }
}

void nivel3() {
  int lecturaCruda = analogRead(A1);

  if (abs(lecturaCruda - potAnt) >= 5) {
    Serial.print("POT:");
    Serial.println(lecturaCruda);
    potAnt = lecturaCruda;
  }
}

void mostrarLeds(int cantidad) {
  digitalWrite(5, cantidad >= 1 ? HIGH : LOW);
  digitalWrite(2, cantidad >= 2 ? HIGH : LOW);
  digitalWrite(3, cantidad >= 3 ? HIGH : LOW);
  digitalWrite(4, cantidad >= 4 ? HIGH : LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "NIVEL1") {
      nivelActual = 1;
      tone(6, 1000, 200);
    } else if (comando == "NIVEL2") {
      nivelActual = 2;
      potAnt = -100;
      mostrarLeds(0);
      tone(6, 200, 500);
    } else if (comando == "NIVEL3") {
      nivelActual = 3;
      potAnt = -100;
      mostrarLeds(0);
      tone(6, 200, 500);
    } else if (comando == "BUZZER:OK") {
      tone(6, 1000, 200);
    } else if (comando == "BUZZER:ERROR") {
      tone(6, 200, 500);
    } else if (nivelActual == 3 && comando.startsWith("LEDS:")) {
      if (comando.length() == 6 && comando[5] >= '0' && comando[5] <= '4') {
        mostrarLeds(comando[5] - '0');
      }
    }
  }

  if (nivelActual == 1) {
    nivel1();
  } else if (nivelActual == 2) {
    nivel2();
  } else if (nivelActual == 3) {
    nivel3();
  }
}