#include <EEPROM.h>
// functionality to wipe out eeprom.
void setup()
{
  for (int i = 0; i < 255; i++) {
    // this performs as EEPROM.write(i, i)
    EEPROM.update(i, 0);
  }
  
}

void loop()
{
}
