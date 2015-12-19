void rain()
{
    //rand nr of drops each layer
    int drops = random(3);
    for (int i = 0; i < drops; ++i)
    {
      int rand_pos = random(64);
      pixelData[7][rand_pos >> 3] |= (0x01 << (rand_pos & 0x07));
    }
   
  for (int layer = 0; layer < 8; ++layer)
  {
    for (int row = 0; row < 8; ++row)
    {
      for (int col = 0; col < 8; ++col)
      {
        if ((pixelData[layer][row] >> col) & 0x01)
        {
          pixelData[layer][row] = pixelData[layer][row] & ~(0x01 << col);
          if (0 < layer)
          {
            pixelData[layer - 1][row] |= 0x01 << col;
          }
        }
      }
    }
    wait(2);
  }
}
