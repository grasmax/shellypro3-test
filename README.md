# shellypro3-test
Python test script for use with ShellyPro3.

Der 3-Kanal-Schalter ShellyPro3 ersetzt ein RaspberryPi-Relaisboard und Stromstoßschalter mit KM12-Rückmeldemodulen.

## Warum?
Nicht behebbare Abstürze beim Schalten von Relais auf dem [Raspi-Relay-Board](https://github.com/grasmax/AcOnOff/blob/main/doc/Inbetriebnahme%20eines%20Steuerrechners%20f%C3%BCr%20eine%20Photovoltaikinsel.pdf) (Siehe Seite 22).

Aktuell werden 2 Schalter benötigt: 48VDC für Schaltschütz und 5VDC für OpenDTU-Funkeinheit.

### Warum Shelly?
Gute Erfahrung mit Shelly-Energiezählern.

Shelly mit 3 Schaltern benötigt so viel Platz wie 2 Stromstoßschalter mit angedockten KM12-Modulen.

Dritter Schalter in Reserve.

## Vorarbeiten:
  1.Update von 1.3.0 auf 1.3.3
  
  2.Update von 1.3.3 auf 1.6.2
  
  WLAN aus
  
  Accesspoint aus
  
  Bluetooth aus
  
  Im Router feste IP eingestellt
  

## Tests mit gh_sp3.py
![image](https://github.com/user-attachments/assets/7ff42f43-6115-4a35-b754-6514234c93c2)
 

## Test mit Multimeter: alle drei Kanäle schalten richtig
 Id 0 - Out 1/rechts (von vorn gesehen)
 
 Id 1 - Out 2/Mitte
 
 Id 2 - Out 3/links
 
![image](https://github.com/user-attachments/assets/3bdda053-11eb-4021-8993-5614f5edf50b)

## Reboot-Test: eingeschaltete Relais bleiben eingeschaltet
