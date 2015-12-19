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
