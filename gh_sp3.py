# Mit diesem Script kann ein shellypro3-3-Kanal-Schalter geprüft werden
# Aufruf, nur Abfrage: python sp3.py [0||1||2]
# Aufruf, Kanal schalten: python sp3.py [0||1||2] [on||off]


import time, sys
import requests 


ShellyPro3Ip = '192.168.1.100'

###### HoleShellyStatus(Id) ##############################################################################
def HoleShellyStatus(Id):
   try:
      sReq = f'http://{ShellyPro3Ip}/rpc/Switch.GetStatus?id={Id}'

      jStat = requests.get( sReq, headers={'Content-Type': 'application/json'}).json()

      print(f'Kanal-Id: {Id}: output: {jStat["output"]}, temperature.tC: {jStat["temperature"]["tC"]}°C')

   except Exception as e:
      sErr = f'Fehler in HoleShellyStatus(Id={Id}): {e}'

###### ShellySendeSchaltimpuls( Id=[0||1||2], sEinAus=[true||false]) ##############################################################################
# Id 0 - Out 1/rechts (von vorn gesehen)
# Id 1 - Out 2/Mitte
# Id 2 - Out 3/links
# Beispiele: 
# http://192.168.1.100/rpc/Switch.Set?id=1&on=true 
# http://192.168.1.100/rpc/Switch.Set?id=1&on=false 
def ShellySendeSchaltimpuls( Id, TrueFalse):

   try:
        
      sReq = f"http://{ShellyPro3Ip}/rpc/Switch.Set?id={Id}&on={TrueFalse}"

      jStat = requests.get( sReq, headers={'Content-Type': 'application/json'}).json()

      print(f'was_on: {jStat["was_on"]}')
      
      time.sleep(0.5) # warten, bis das Relais umgeschaltet hat
            
      HoleShellyStatus( Id)

   except Exception as e:
      print(f'Ausnahme in ShellySendeSchaltimpuls({Id}):  {e}')

def main(argv):

   try:

      iArgs = len(argv)

      if iArgs == 2:

         id = int(argv[1])
         HoleShellyStatus(id)
         
      elif iArgs == 3:
         id = int(argv[1])
         onoff = argv[2].lower()

         if onoff == 'on':
            ShellySendeSchaltimpuls( Id=id, TrueFalse='true')
         elif onoff == 'off':
            ShellySendeSchaltimpuls( Id=id, TrueFalse='false')


   except Exception as e:
           sErr = f'Ausnahme : {e}'
           print(sErr)
           

if __name__ == "__main__":
    main(sys.argv)