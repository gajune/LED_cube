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
