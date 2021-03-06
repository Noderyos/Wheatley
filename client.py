import requests
import base64

HOST = "http://noderyos.dev:5000"
def handleMsgs(s):
    if "E_PNE_" in s:
        return f'Error : Program with id {s[-13:]} does not exist'
    elif "E_PAE_" in s:
        return f'Error : Program with id {s[-13:]} already exist'
    elif "E_NID" in s:
        return f'Error : No ID Provided'
    elif "E_IID" in s:
        return f'Error : Invalid ID provided ({s[-13:]})'
    elif "E_AR_" in s:
        return f'Error : Program with id {s[-13:]} already running'
    elif "E_AS_" in s:
        return f'Error : Program with id {s[-13:]} already stopped'
    elif "E_LNE_" in s:
        return f'Error : Library with name {s.split("_")[-1]} doesn\'t exist'
    elif "S_DL_" in s:
        return f'Info : Program with id {s[-13:]} deleted'
    elif "S_ST_" in s:
        return f'Info : Program with id {s[-13:]} started'
    elif "S_SP_" in s:
        return f'Info : Program with id {s[-13:]} stopped'
    elif "S_CR_" in s:
        return f'Info : Program with id {s[-13:]} created'

banner = """
             .,-:;//;:=,
         . :H@@@MM@M#H/.,+%;,
      ,/X+ +M@@M@MM%=,-%HMMM@X/,
     -+@MM; $M@@MH+-,;XMMMM@MMMM@+-
    ;@M@@M- XM@X;. -+XXXXXHHH@M@M#@/.
  ,%MM@@MH ,@%=            .---=-=:=,.
  -@#@@@MX .,              -%HX$$%%%+;
 =-./@M@M$                  .;@MMMM@MM:
 X@/ -$MM/                    .+MM@@@M$
,@M@H: :@:                    . -X#@@@@-
,@@@MMX, .                    /H- ;@M@M=
.H@@@@M@+,                    %MM+..%#$.
 /MMMM@MMH/.                  XM@MH; -;
  /%+%$XHH@$=              , .H@@@@MX,
   .=--------.           -%H.,@@@@@MX,
   .%MM@@@HHHXX$$$%+- .:$MMX -M@@MM%.
     =XMMM@MM@MM#H;,-+HMM@M+ /MMMX=
       =%@M@M#@$-.=$@MM@@@M; %M%=
         ,:+$+-,/H#MMMMMMM@- -,
               =++%%%%+/:-.
"""
print(banner)
id = input("Enter you ID -> ")
print("\n[1] Send program\n[2] Start program\n[3] Stop program\n[4] Delete program")
choice = int(input("-> "))
if choice == 1:
    file = open(input("File to upload -> ").replace("'",""),"r")
    libs = input("Libraries used (separated by a comma): ")
    code = base64.b64encode(bytes(file.read().encode('utf-8'))).decode('utf-8')
    print("Please Wait ...")
    msg = requests.post(HOST + "/submit", json={'id': id,'libs': libs,'code': code}).text
    print(handleMsgs(msg))
elif choice == 2:
    print("Please Wait ...")
    msg = requests.post(HOST + "/start", json={'id': id}).text
    print(handleMsgs(msg))
elif choice == 3:
    print("Please Wait ...")
    msg = requests.post(HOST + "/stop", json={'id': id}).text
    print(handleMsgs(msg))
elif choice == 4:
    print("Please Wait ...")
    msg = requests.post(HOST + "/delete",json={'id':id}).text
    print(handleMsgs(msg))
