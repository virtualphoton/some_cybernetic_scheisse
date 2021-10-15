#include "config.h"

TTGOClass* ttgo;

const char* watch_aruco =
"0000"
"1111"
"1001"
"1010";
void sleep_(double n) {
    delay(int(n * 1000));
}

void change_brightness_by_touch(void *args){
    float b;
    int16_t x, y;
    while (true){
      if (ttgo->getTouch(x, y)) {
          b = x/240.*256 + y/240.*16;
          ttgo->setBrightness(int(b));
      }
    }
}

class SerialResult {
public:
    byte BUF_SIZE = 64;
    byte * body;
    byte code;
    SerialResult() {
        body = new byte[BUF_SIZE];
    }
    void wait_for_transmission() {
        size_t size_;
        while (true)
            if (Serial.available() and Serial.read() == '<') {
                size_ = Serial.readBytesUntil('>', body, 64);
                Serial.println(size_);
                Serial.println(body[size_]);
                break;
            }
        code = body[0];
    }
    ~SerialResult(){
      delete[] body;
    }
};

class State {
public:
    int cur_state = 0;
    float joints_speeds[6] = { 2.9,2.4,2.6,2.1,2.5,3 }; // how much radians per second
    float joints_states[6] = { 0,0,0,0,0,0 };
    float constraints[6][2] = { {-3.15, 3.15}, {-3.15, 3.15}, {-2.82, 2.82}, {-3.15, 3.15},  {-3.15, 3.15},  {-3.15, 3.15} };
    const char* aruco = watch_aruco;
    State() {}
    void operator=(const State& _) {}

    void act() {
        int t;
        SerialResult ser;
        show_aruco();
        while (true) {
            ser.wait_for_transmission();
            if (ser.code == 2)
                show_aruco();
            else if (ser.code == 1 or ser.code == 3)
                show_data(ser.body, ser.code);
        }
    }
    void show_aruco() {
      int aruco_size = 4;
      ttgo->tft->fillRect(0, 0, 240, 240, TFT_WHITE);
      ttgo->tft->fillRect(30, 30, 180, 180, TFT_BLACK);
      int ind = 0;
      int x = 60, y = 60;
      int dx = 30, dy = 30;
      unsigned int color;
      for (int i = 0; i < aruco_size; i += 1) {
          for (int j = 0; j < aruco_size; j += 1) {
              color = aruco[ind] == '0' ? TFT_BLACK : TFT_WHITE;
              ttgo->tft->fillRect(x, y, dx, dy, color);
              x += dx;
              ind += 1;
          }
          x = 60;
          y += dy;
      }
    }

    void show_data(byte* body, byte code) {
      body += 1;
      ttgo->tft->fillRect(0, 0, 240, 240, TFT_BLACK);
      int dmillis = 100;
      ttgo->tft->setTextColor(TFT_GREEN, TFT_BLACK);
      float targets[6];
      float deltas[6];
      int x, y;
      int dx;
      for (int i = 0; i < 6; i += 1) {
          targets[i] = (constraints[i][1] - constraints[i][0]) / 256 * body[i] + constraints[i][0];
          deltas[i] = joints_speeds[i] * (dmillis / 1000.) * (targets[i] > joints_states[i] ? 1 : -1);
          x = i < 3? 10:130;
          y = 24 + (i%3)*72;
          dx = ttgo->tft->drawNumber(i+1,x,y,4);
          dx += ttgo->tft->drawChar(':',x+dx,y,4);
          x += dx;
          ttgo->tft->drawFloat(joints_states[i], 2, x, y, 4);
      }
      if (code == 1)
          return;
      bool has_changed = false;
      while (not has_changed) {
          has_changed = true;
          for (int i = 0; i < 6; i += 1) {
              if ((joints_states[i] < targets[i]) == (deltas[i] > 0)) {
                  joints_states[i] += deltas[i];
                  has_changed = false;
                  x = dx + (i < 3? 10:130);
                  y = 24 + (i%3)*72;
                  ttgo->tft->fillRect(x, y, 120-dx, 26, TFT_BLACK);
                  ttgo->tft->drawFloat(joints_states[i], 2, x, y, 4);
              }
          }
          delay(dmillis);
      }
      Serial.println("done");
    }
};

State* state = new State;
void setup() {
    Serial.begin(115200);
    pinMode(12, OUTPUT);
    ttgo = TTGOClass::getWatch();
    ttgo->begin();
    ttgo->openBL();
    ttgo->setBrightness(25);
    //xTaskCreate(change_brightness_by_touch, "touch", 2048, NULL, 2, NULL);
}

void loop() {
    state->act();
}
