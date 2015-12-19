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
