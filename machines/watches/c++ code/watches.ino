#include "config.h"

TTGOClass *ttgo;

const char * watch_qr = 
"000000011101010000000"
"011111011111010111110"
"010001010101110100010"
"010001011111010100010"
"010001011010010100010"
"011111011000110111110"
"000000010101010000000"
"111111110101111111111"
"000100000101000111011"
"110100100010100000110"
"010001011100110001010"
"000001110110001101101"
"110110010000110100010"
"111111110001110001010"
"000000010111011000110"
"011111010101110011101"
"010001010101010000111"
"010001011010101101101"
"010001010100100000110"
"011111010100001111101"
"000000010000100101100";
void sleep_(double n){
  delay(int(n*1000));
}
class State{
public:
  int cur_state = 0;
  const char* qr = watch_qr;
  State(){}
  void operator=(const State& _) {}
  
  void act(){
    show_qr_while_idle();
    show_data();
  }
  void show_qr_while_idle(){
    int ind = 0;
    int x = 15, y = 15;
    int dx = 10, dy = 10;
    unsigned int color;
    for (int i = 0; i < 21; i += 1){
      for (int j = 0; j < 21; j += 1){
        color = qr[ind] == '0'? TFT_BLACK : TFT_WHITE;
        ttgo->tft->fillRect (x, y, dx, dy, color);
        x += dx;
        ind += 1;
      }
      x = 15;
      y += dy;
    }
    Serial.println("Done QR!");
  }
  void show_data(){
    while(true){
      if (Serial.available()){
        ttgo->tft->setTextColor(TFT_GREEN, TFT_BLACK);
        ttgo->tft->setCursor(0, 0);
        ttgo->tft->print(Serial.parseFloat());
      }
      sleep(.2);
    }
  }
};

State* state = new State;
void setup(){
  Serial.begin(115200);
  pinMode(12, OUTPUT);
  ttgo = TTGOClass::getWatch();
  ttgo->begin();
  ttgo->openBL();
  ttgo->tft->fillRect (0, 0, 240, 240, TFT_WHITE);
  ttgo->setBrightness(50);
}

void loop(){
  state->act();
}
