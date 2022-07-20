#include <Arduino.h>
#include "sensirion_common.h"
#include "sgp30.h"
#include <Wire.h>
#include "rgb_lcd.h"
 
rgb_lcd lcd;
 
const int colorR = 255;
const int colorG = 0;
const int colorB = 0;


void setup() {
    s16 err;
    u32 ah = 0;
    u16 scaled_ethanol_signal, scaled_h2_signal;
    Serial.begin(115200);
    Serial.println("serial start!!");

    /*For wio link!*/
    #if defined(ESP8266)
    pinMode(15, OUTPUT);
    digitalWrite(15, 1);
    Serial.println("Set wio link power!");
    delay(500);
    #endif
    /*  Init module,Reset all baseline,The initialization takes up to around 15 seconds, during which
        all APIs measuring IAQ(Indoor air quality ) output will not change.Default value is 400(ppm) for co2,0(ppb) for tvoc*/
    while (sgp_probe() != STATUS_OK) {
        Serial.println("SGP failed");
        while (1);
    }
    /*Read H2 and Ethanol signal in the way of blocking*/
    err = sgp_measure_signals_blocking_read(&scaled_ethanol_signal,
                                            &scaled_h2_signal);
    if (err == STATUS_OK) {
        Serial.println("get ram signal!");
    } else {
        Serial.println("error reading signals");
    }

    //ah=get_relative_humidity();
    /*
        The function sgp_set_absolute_humidity() need your own implementation
    */
    //sgp_set_absolute_humidity(ah);

    // Set absolute humidity to 13.000 g/m^3
    //It's just a test value
    sgp_set_absolute_humidity(13000);
    err = sgp_iaq_init();
    //

    lcd.begin(16, 2);
 
    lcd.setRGB(colorR, colorG, colorB);
}

void loop() {
    s16 err = 0;
    u16 tvoc_ppb, co2_eq_ppm;
    err = sgp_measure_iaq_blocking_read(&tvoc_ppb, &co2_eq_ppm);
    if (err == STATUS_OK) {
        Serial.print("tVOC  Concentration:");
        Serial.print(tvoc_ppb);
        Serial.println("ppb");

        Serial.print("CO2eq Concentration:");
        Serial.print(co2_eq_ppm);
        Serial.println("ppm");
    } else {
        Serial.println("error reading IAQ values\n");
    }
    lcd.setCursor(0, 0);
    lcd.print("tVOC: ");
    lcd.print(tvoc_ppb);

    lcd.setCursor(0,1);
    lcd.print("CO2eq: ");
    lcd.print(co2_eq_ppm);
    delay(1000);
}
