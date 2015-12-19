/*
 * LED CUBE, Joakim Andersson 2015
 *
 * Built with 8 TPICB595 shift registers, a 74hc238 demultiplexer for layer select,
 * paired with 8 NPN transistors driving 8 PNP driver transistor for each layer.
 * Driven by an Arduino Nano.
 *
 */

//shift registers
#define latchPinne 8 //RCK, green wire
#define clockPinne 12 //SRCK, blue wire
#define dataPinne 11 //SER IN, yellow wire

//demultiplexer
#define pwmPin 3 // E3
#define a0Pin 4 // A0
#define a1Pin 5 // A1
#define a2Pin 6 // A2

uint8_t pixelData[8][8]; //total 512 bits of data

#define frameDelay 15

#define START_BYTE 0xAA

int pos = 0;

bool startByteFound = false;

void setup() {

  //Serial com setup
  Serial.begin(115200);
  Serial.println("Setup");

  //Select used pins as outputs
  pinMode(latchPinne, OUTPUT);
  pinMode(clockPinne, OUTPUT);
  pinMode(dataPinne, OUTPUT);
  pinMode(pwmPin, OUTPUT);
  pinMode(a0Pin, OUTPUT);
  pinMode(a1Pin, OUTPUT);
  pinMode(a2Pin, OUTPUT);

  digitalWrite(pwmPin, HIGH); //no PWM just yet

  clearData();
  fillCube();
  testSequence();
}

void loop() {
  testSequence();
  //drawCube();
}


void parseSerial()
{
  if (Serial.available() > 0)
  {
    byte inByte = Serial.read();
    if (startByteFound) 
    {
      pixelData[pos / 8][pos % 8] = inByte;
      pos++;
      if (64 == pos)
      {
        startByteFound = false;
        pos = 0;
      }
    }
    else if (inByte == START_BYTE)
    {
      startByteFound = true;
    }
  }
}

void testSequence()
{
  rain();
  //fillCube();
  //swipeUp();
  //swipeSide();
  //randomPixel();
  //sinWave();
}

// "renders" cube
void drawCube()
{
  //z - up, y - in, x - right
  for (int zLayer = 0; zLayer < 8; ++zLayer)
  {
    //parseSerial();
    // drive latch low while transmitting
    //digitalWrite(latchPinne, LOW);
    PORTB = 0 | (PORTB & B11111110); // faster way to drive latch pin low

    for (int yLayer = 0; yLayer < 8; ++yLayer)
    {
      parseSerial(); // had to do this more often
      shiftOut(dataPinne, clockPinne, MSBFIRST, pixelData[zLayer][yLayer]); // shift out x
    }
    PORTB = 1 | (PORTB & B11111110); // latch pin pin

    //select layer to show
    //PORTD = 0 | (PORTD & B11110111); // pwm pin
    PORTD = (zLayer << 4) | (PORTD & B10001111); //select what layer to show, outputs are matched to demultiplexer.
    //PORTD = (1 << pwmPin) | (PORTD & B11110111); // pwm pin
  }
  
  //clear
  for (int yLayer = 0; yLayer < 8; ++yLayer)
  {
    shiftOut(dataPinne, clockPinne, MSBFIRST, 0);
  }
  PORTB = 0 | (PORTB & B11111110); // latch pin pin
  PORTB = 1 | (PORTB & B11111110); // latch pin pin

}

//crude wait function, displays current data
void wait(int t)
{
  for (int i = 0; i < t; ++i)
  {
    drawCube();
  }
}

//clears pixel data array
void clearData()
{
  for (int i = 0; i < 8; ++i)
  {
    clearLayer(i);
  }
}

//clears pixel data layer in array
void clearLayer(int layer)
{
  for (int i = 0; i < 8; ++i)
  {
    pixelData[layer][i] = 0;
  }
}

