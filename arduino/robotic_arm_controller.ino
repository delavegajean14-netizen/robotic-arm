#include <Servo.h>

// --- CONFIGURACIÓN DE PINES ---
const int PIN_BASE   = 8;  // Servo Q0 (Giro Base)
const int PIN_HOMBRO = 9;  // Servo Q1 (Hombro)
const int PIN_CODO   = 10; // Servo Q2 (Codo)
const int PIN_MUNECA = 11; // Servo Q3 (Muñeca)

Servo servoBase;
Servo servoHombro;
Servo servoCodo;
Servo servoMuneca;

// Variables para almacenar los ángulos a recibir
int anguloBase = 90;
int anguloHombro = 90;
int anguloCodo = 90;
int anguloMuneca = 90;

void setup() {
  // Iniciar comunicación serie a 115200 baudios (más rápido y estable)
  Serial.begin(115200);
  
  // Conectar servos a los pines
  servoBase.attach(PIN_BASE);
  servoHombro.attach(PIN_HOMBRO);
  servoCodo.attach(PIN_CODO);
  servoMuneca.attach(PIN_MUNECA);

  // Posición inicial de reposo (Todos en 90 grados)
  moverServos(90, 90, 90, 90);
  
  Serial.println("Arduino listo. Esperando comandos: q0,q1,q2,q3");
}

void loop() {
  // Comprobar si hay datos disponibles en el puerto serie
  if (Serial.available() > 0) {
    // Leer los enteros separados por comas
    anguloBase   = Serial.parseInt();
    anguloHombro = Serial.parseInt();
    anguloCodo   = Serial.parseInt();
    anguloMuneca = Serial.parseInt();

    // Leer el salto de línea (\n) que marca el final del comando
    if (Serial.read() == '\n') {
      // Limitar los ángulos por seguridad mecánica (0 a 180)
      anguloBase   = constrain(anguloBase, 0, 180);
      anguloHombro = constrain(anguloHombro, 0, 180);
      anguloCodo   = constrain(anguloCodo, 0, 180);
      anguloMuneca = constrain(anguloMuneca, 0, 180);

      // Ejecutar el movimiento
      moverServos(anguloBase, anguloHombro, anguloCodo, anguloMuneca);
      
      // Confirmar a Python que el movimiento se realizó
      Serial.println("OK");
    }
  }
}

void moverServos(int b, int h, int c, int m) {
  servoBase.write(b);
  servoHombro.write(h);
  servoCodo.write(c);
  servoMuneca.write(m);
}