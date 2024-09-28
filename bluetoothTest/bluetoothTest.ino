#include <SoftwareSerial.h>

SoftwareSerial bluetoothSerial(2, 3); // RX, TX 핀을 지정

void setup() {
  // 시리얼 통신을 시작하고, 통신 속도를 9600bps로 설정합니다.
  Serial.begin(9600);
  bluetoothSerial.begin(9600); 
}

void loop() {
  // 시리얼 통신을 통해 데이터가 도착했는지 확인합니다.
  if (bluetoothSerial.available() > 0) {
    // 도착한 데이터를 읽어와서 출력합니다.
    String message = bluetoothSerial.readString();
    Serial.println(message);
  }
}