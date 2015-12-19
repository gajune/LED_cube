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
