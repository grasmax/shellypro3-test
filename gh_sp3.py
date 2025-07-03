# Mit diesem Script kann ein shellypro3-3-Kanal-Schalter geprüft werden
# Aufruf, nur Abfrage: python sp3.py [0||1||2]
# Aufruf, Kanal schalten: python sp3.py [0||1||2] [on||off]

import time, sys
import requests 


ShellyPro3Ip = '192.168.1.100'

###### HoleShellyStatus(Id) ##############################################################################
def HoleShellyStatusIntern(Id):
   try:
      sReq = f'http://{ShellyPro3Ip}/rpc/Switch.GetStatus?id={Id}'

      jStat = requests.get( sReq, headers={'Content-Type': 'application/json'}).json()
      # {'id': 1, 'source': 'HTTP_in', 'output': False, 'temperature': {'tC': 36.2, 'tF': 97.1}}

      sId = jStat['id'] if (jStat.get('id') != None) else ''
      sOutput = jStat['output'] if (jStat.get('output') != None) else ''
      sTemp = f'{jStat["temperature"]["tC"]}' if jStat["temperature"]["tC"] != None else ''

      print(f'Kanal-Id: {sId}: output: {sOutput}, temperature.tC: {sTemp}')

      jRv = {
         "Id": sId,
         "EinAus": "Aus" if sOutput == False else "Ein" if sOutput == True else "??",
         "Temp": sTemp,
         "rv": "okok"
      }

      return jRv

   except Exception as e:
      sAusn = f'Ausnahme in HoleShellyStatus(Id={Id}): {e}'
      print(sAusn)
      jRv = {
         "Id": "",
         "EinAus": "??",
         "Temp": "",
         "rv": sAusn
      }
      return jRv


###### HoleShellyStatus123() ##############################################################################
def HoleShellyStatus123():
   try:
      sOut = ''
      
      jRv = HoleShellyStatusIntern(0)
      if jRv["rv"] == "okok":
         sOut += f'Id {jRv["Id"]} (230V für MPII): {jRv["EinAus"]}, Temperatur: {jRv["Temp"]}°C'
      
      jRv = HoleShellyStatusIntern(1)
      if jRv["rv"] == "okok":
         if len(sOut) > 0:
            sOut += '\r\n'
         sOut += f'Id {jRv["Id"]} (5V für OpenDTU): {jRv["EinAus"]}, Temperatur: {jRv["Temp"]}°C'

      jRv = HoleShellyStatusIntern(2)
      if jRv["rv"] == "okok":
         if len(sOut) > 0:
            sOut += '\r\n'
         sOut += f'Id {jRv["Id"]} (Reserve): {jRv["EinAus"]}, Temperatur: {jRv["Temp"]}°C'
      
      return sOut

   except Exception as e:
      sAusn = f'Ausnahme in HoleShellyStatus(Id={Id}): {e}'
      print(sAusn)
      return sAusn



###### HoleShellyStatus(Id) ##############################################################################
def HoleShellyStatus(Id):
   try:
      jRv = HoleShellyStatusIntern(Id)
      if jRv["rv"] != "okok":
         return jRv["rv"]
      
      if jRv["EinAus"] == "Aus":
         return 'false'
      elif jRv["EinAus"] == "Ein":
         return 'true'
      else:
         return jRv["EinAus"]

   except Exception as e:
      sAusn = f'Ausnahme in HoleShellyStatus(Id={Id}): {e}'
      print(sAusn)
      return sAusn


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

      if (jStat.get('was_on') != None):
         print(f"was_on: {jStat['was_on']}")
      else:
         print(jStat)
      
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

      if iArgs == 1:
         HoleShellyStatus(0)
         HoleShellyStatus(1)
         HoleShellyStatus(2)
         
      elif iArgs == 2:

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