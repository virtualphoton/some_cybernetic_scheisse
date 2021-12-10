#include <LiquidCrystal.h>
//LCD pin to Arduino
const int pin_RS = 8; 
const int pin_EN = 9; 
const int pin_d4 = 4; 
const int pin_d5 = 5; 
const int pin_d6 = 6; 
const int pin_d7 = 7; 
const int pin_BL = 10; 
const int analog_button = 5;

int time_A_ms = 0;
int last_time_A_called = 0;
int time_B_ms = 0;
int last_time_B_called = 0;

LiquidCrystal lcd( pin_RS,  pin_EN,  pin_d4,  pin_d5,  pin_d6,  pin_d7);

int get_key(){
  static long last_time = millis();
  if (millis() - last_time < 500)
    return -2;
  
  int x = analogRead(0);
  if (x < 60){
   last_time = millis();
   return 0;
  }
 if (x < 200){
   last_time = millis();
   return 1;
 }
 if (x < 400){
   last_time = millis();
   return 2;
 }
 if (x < 600){
   last_time = millis();
   return 3;
 }
 if (x < 800){
   last_time = millis();
   return 4;
 }
 else
   return -1;
}

int await_key(long timeout_ms=100){
  long timer_called_time = millis();
  while (millis() - timer_called_time < timeout_ms){
    int key = get_key();
    if (key >= 0){
      return key;
    }
  }
  return -3;
}

class Timer{
public:
  int cur_player = 0;
  long move_start_time = 0;
  long player_time_at_start_of_move[2];
  Timer(long time_sec){
    player_time_at_start_of_move[0] = player_time_at_start_of_move[1] = time_sec*1000ll;
  }

  void start(){
    move_start_time = millis();
  }
  
  void change_active_player(){
    player_time_at_start_of_move[cur_player] -= millis() - move_start_time;
    cur_player = (cur_player + 1)%2;
    move_start_time = millis();
  }
  
  void show_time(){
    lcd.setCursor(0,0);
    for (int i = 0; i < 2; i+= 1){
      long time_left = player_time_at_start_of_move[i] - (millis() - move_start_time)*(i == cur_player);
      if (time_left < 0){
        lcd.print("Player ");
        lcd.print(cur_player + 1);
        lcd.print("wins");
        while (get_key() != 4)
          delay(100);
      }
      print_2_dig_int(time_left/1000/60);
      lcd.print(":");
      print_2_dig_int(time_left/1000%60);
      lcd.print("  ||  ");
    }
  }
  void print_2_dig_int(int n, int pos=-1){
      if (pos != -1)
        lcd.setCursor(pos, 0);
      lcd.print(n/10);
      lcd.print(n%10);
  }
  void operator=(const Timer & other){
    player_time_at_start_of_move[0] = other.player_time_at_start_of_move[0];
    player_time_at_start_of_move[1] = other.player_time_at_start_of_move[1];
    cur_player = other.cur_player;
    move_start_time = other.move_start_time;
  }
};

bool await_button_press(long timeout_ms=100){
  static long last_time = millis();
  if (millis() - last_time < 500)
    return false;
  
  long timer_called_time = millis();
  while (millis() - timer_called_time < timeout_ms)
    if (analogRead(analog_button) < 250){
      last_time = millis();
      return true;
    }
  return false;
}

Timer timer(0);

void setup() {
 Serial.begin(9600);
 lcd.begin(16, 2);
 int play_time = 60*15;
 timer = Timer(play_time);
 while (not await_button_press()) {}
 Serial.println(3);
 timer.start();
}

void loop() {
  timer.show_time();
  if (await_button_press())
    timer.change_active_player();
}
