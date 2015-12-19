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
