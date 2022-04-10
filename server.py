from flask import Flask, request
import requests
import docker
import os
import shutil
import base64

client = docker.from_env()
app = Flask(__name__)
ids = [i for i in
       ["4d445220-5844",
        "4c4f4c20-5844"]] # This ID's are not valid for my intance


@app.route('/submit', methods=['POST'])
def create():
    request_json = request.get_json(force=True)
    if not 'code' in str(request_json):
        return "E_NCD"
    if not 'id' in str(request_json):
        return "E_NID"
    else:
        if request_json['id'] in ids:
            existingimg = ''.join([str(t.tag) for t in client.images.list()])
            if not request_json['id'] in existingimg:
                libs = ""
                if request_json['libs'] != "":
                    for lib in request_json['libs'].split(","):
                        if requests.post("https://pypi.org/simple/" + lib).status_code == 200:
                            libs += f'RUN pip install {lib}\n\n'
                        else:
                            return "E_LNE_" + lib

                os.mkdir(request_json['id'])
                file = open(request_json['id'] + "/Dockerfile", "w")
                file.write(
                    "FROM python:3.10.0-slim-buster\n\nCOPY main.py .\n\n" + libs + "CMD python3 main.py")
                file.close()

                file = open(request_json['id'] + "/main.py", "wb")
                file.write(base64.b64decode(request_json['code']))
                file.close()
                client.images.build(path=request_json['id'], tag=request_json['id'])
                client.containers.run(request_json['id'], detach=True)
                return "S_CR_" + request_json['id']
            else:
                return "E_PAE_" + request_json['id']
        else:
            return "E_IID_" + request_json['id']


@app.route('/stop', methods=['POST'])
def stop():
    request_json = request.get_json(force=True)
    if not 'id' in str(request_json):
        return "E_NID"
    else:
        if request_json['id'] in ids:
            existingcont = ''.join([str(t.image) for t in client.containers.list()])
            existingimg = ''.join([str(t.tag) for t in client.images.list()])
            print(existingcont)
            if request_json['id'] in existingcont:
                if request_json['id'] in existingimg:
                    for cont in client.containers.list():
                        if request_json['id'] in str(cont.image):
                            cont.stop()
                else:
                    return "E_PNE_" + request_json['id']
            else:
                return "E_AS_" + request_json['id']
            return "S_SP_" + request_json['id']
        else:
            return "E_IID_" + request_json['id']


@app.route('/start', methods=['POST'])
def start():
    request_json = request.get_json(force=True)
    if not 'id' in str(request_json):
        return "E_NID"
    else:
        if request_json['id'] in ids:
            existingcont = ''.join([str(t.image) for t in client.containers.list()])
            existingimg = ''.join([str(t.tag) for t in client.images.list()])
            print(existingcont)
            if not request_json['id'] in existingcont:
                if request_json['id'] in existingimg:
                    for cont in client.images.list():
                        if request_json['id'] in str(cont.tag):
                            client.containers.run(image=request_json['id'], detach=True)
                else:
                    return "E_PNE_" + request_json['id']
            else:
                return "E_AR_" + request_json['id']
            return "S_ST_" + request_json['id']
        else:
            return "E_IID_" + request_json['id']


@app.route('/delete', methods=['POST'])
def delete():
    request_json = request.get_json(force=True)
    if not 'id' in str(request_json):
        return "E_NID"
    else:
        if request_json['id'] in ids:
            existingimg = ''.join([str(t.tag) for t in client.images.list()])
            if request_json['id'] in existingimg:
                for cont in client.containers.list():
                    if request_json['id'] in str(cont.image):
                        cont.stop()
                for cont in client.images.list():
                    if request_json['id'] in str(cont.tag):
                        client.images.remove(image=request_json['id'], force=True)
                shutil.rmtree(request_json['id'])
            else:
                return "E_PNE_" + request_json['id']
            return "S_DL_" + request_json['id']
        else:
            return "E_IID_" + request_json['id']


if __name__ == '__main__':
    app.run(host="0.0.0.0")

# E_PNE_<id> = Program with id <id> does not exist'
# E_PAE_<id> = Program with id <id> already exist'
# E_NID = No ID Provided
# E_IID = Invalid ID provided
# E_AR_<id> = Program with id <id> already running
# E_AS_<id> = Program with id <id> already stopped
# E_LNE_<lib> = Library with name <lib> doesn't exist
# S_DL_<id> = Program with id <id> deleted
# S_ST_<id> = Program with id <id> started
# S_SP_<id> = Program with id <id> stopped
# S_CR_<id> = Program with id <id> created
