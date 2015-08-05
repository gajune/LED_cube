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

uint8_t pixelData[8][8] ; //total 512 bits of data

#define frameDelay 15

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
}

void loop() {
  drawCube();
  testSequence();

}


void testSequence()
{
  //fillCube();
  //swipeUp();
  //swipeSide();
  //randomPixel();
  sinWave();
}

// "renders" cube
void drawCube()
{
  //z - up, y - in, x - right
  for (int zLayer = 0; zLayer < 8; ++zLayer)
  {
    // drive latch low while transmitting
    //digitalWrite(latchPinne, LOW);
    PORTB = 0 | (PORTB & B11111110); // faster way to drive latch pin low

    for (int yLayer = 0; yLayer < 8; ++yLayer)
    {
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

// fills whole cube
void fillCube()
{
  for (int layer = 0; layer < 8; ++layer)
  {
    for (int i = 0; i < 8; ++i)
    {
      pixelData[layer][i] = 255;
    }
  }
  wait(150);
  clearData();
}

//plane swiping up
void swipeUp()
{
  for (int layer = 0; layer < 8; ++layer)
  {
    for (int i = 0; i < 8; ++i)
    {
      pixelData[layer][i] = 255;
      pixelData[(layer - 1) % 8][i] = 0;

    }
    wait(frameDelay);
  }
  clearLayer(7);
}

//plane swiping right
void swipeSide()
{
  for (int outer = 0; outer < 8; ++outer)
  {
    for (int layer = 0; layer < 8; ++layer)
    {
      for (int i = 0; i < 8; ++i)
      {
        pixelData[layer][i] = 1 << outer;
      }
    }
    wait(frameDelay);
  }
  clearData();
}

//displays random pixels
void randomPixel()
{
  for (int i = 0; i < 50; ++i)
  {
    pixelData[random(8)][random(8)] = 1 << random(8);
    wait(frameDelay);
  }
  clearData();
}

//wave
void sinWave()
{
  for (int outer = 0; outer < 2880; outer += 60)
  {
    for (int layer = 0; layer < 8; ++layer)
    {
      for (int i = 0; i < 8; ++i)
      {
        float rad = (i * 45 + outer) / 360.0f * PI;
        int sVal = sin(rad) * 4;
        pixelData[4 + sVal][i] = 255;

      }
      drawCube();
    }
    
    clearData();
  }
  clearData();
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

