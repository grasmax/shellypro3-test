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
      # {'id': 1, 'source': 'HTTP_in', 'output': False, 'temperature': {'tC': 36.2, 'tF': 97.1}}

      sId = jStat['id'] if (jStat.get('id') != None) else ''
      sOutput = jStat['output'] if (jStat.get('output') != None) else ''
      sTemp = f'{jStat["temperature"]["tC"]}°C' if jStat["temperature"]["tC"] != None else ''
      
      print(f'Kanal-Id: {sId}: output: {sOutput}, temperature.tC: {sTemp}')
      
      if sOutput == False:
         return 'false'
      elif sOutput == True:
         return 'true'
      else:
         return ''

   except Exception as e:
      print( f'Ausnahme in HoleShellyStatus(Id={Id}): {e}')
      return -1

###### ShellySendeSchaltimpuls( Id=[0||1||2], sEinAus=[true||false]) ##############################################################################
# Id 0 - Out 1/rechts (von vorn gesehen)
# Id 1 - Out 2/Mitte
# Id 2 - Out 3/links
# Beispiele: 
# http://192.168.1.100/rpc/Switch.Set?id=1&on=true 
# http://192.168.1.100/rpc/Switch.Set?id=1&on=false 

def ShellySendeSchaltimpuls( Id, TrueFalse):

   try:
      sOutput = HoleShellyStatus(Id)
      if TrueFalse == sOutput:
         print(f'Schalten nicht nötig: {TrueFalse} == {sOutput}') 
         return
        
      sReq = f"http://{ShellyPro3Ip}/rpc/Switch.Set?id={Id}&on={TrueFalse}"

      jStat = requests.get( sReq, headers={'Content-Type': 'application/json'}).json()

      print(f'was_on: {jStat["was_on"]}')
      
      time.sleep(0.5) # warten, bis das Relais umgeschaltet hat
            
      sStat = HoleShellyStatus( Id)
      if TrueFalse == sStat:
         print(f'Gewünschter Schaltimpuls {TrueFalse} ausgeführt')
      else:
         print(f'Schaltimpuls {TrueFalse} konnte nicht ausgeführt werden. Ergebnis: {sStat}')
            

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