// C++ code

int estadoAnt8 = HIGH;
int estadoAnt9 = HIGH;
int estadoAnt10 = HIGH;
int estadoAnt11 = HIGH;

void setup() {
  pinMode(5, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(6, OUTPUT); // Pin del Buzzer
  
  pinMode(8, INPUT_PULLUP);
  pinMode(9, INPUT_PULLUP);
  pinMode(10, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);
  
  Serial.begin(9600);
}

void loop() {
  int estadoAct8 = digitalRead(8);
  int estadoAct9 = digitalRead(9);
  int estadoAct10 = digitalRead(10);
  int estadoAct11 = digitalRead(11);
  
  // --- BOTÓN A (Pin 8) -> Encender LED (Pin 5) ---
  if (estadoAnt8 == HIGH && estadoAct8 == LOW) {
    Serial.println("BOTON:A");
  }
  if (estadoAct8 == LOW) {
    digitalWrite(5, HIGH);
  } else {
    digitalWrite(5, LOW);
  }
  
  // --- BOTÓN B (Pin 9) -> Encender LED (Pin 2) ---
  if (estadoAnt9 == HIGH && estadoAct9 == LOW) {
    Serial.println("BOTON:B");
  }
  if (estadoAct9 == LOW) {
    digitalWrite(2, HIGH);
  } else {
    digitalWrite(2, LOW);
  }
  
  // --- BOTÓN C (Pin 10) -> Encender LED (Pin 3) ---
  if (estadoAnt10 == HIGH && estadoAct10 == LOW) {
    Serial.println("BOTON:C");
  }
  if (estadoAct10 == LOW) {
    digitalWrite(3, HIGH);
  } else {
    digitalWrite(3, LOW);
  }
  
  // --- BOTÓN D (Pin 11) -> Encender LED (Pin 4) ---
  if (estadoAnt11 == HIGH && estadoAct11 == LOW) {
    Serial.println("BOTON:D");
  }
  if (estadoAct11 == LOW) {
    digitalWrite(4, HIGH);
  } else {
    digitalWrite(4, LOW);
  }
  
  // Actualización de estados
  estadoAnt8 = estadoAct8;
  estadoAnt9 = estadoAct9;
  estadoAnt10 = estadoAct10;
  estadoAnt11 = estadoAct11;
  
  

  // --- ESCUCHAR ÓRDENES DE PYTHON PARA EL BUZZER ---
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "BUZZER:OK") {
      tone(6, 1000, 200); // Tono agudo (Acierto)
    }
    else if (comando == "BUZZER:ERROR") {
      tone(6, 200, 500);  // Tono grave (Error)
    }
  }
}