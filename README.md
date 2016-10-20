# Informe Primer Parcial

# Universidad ICESI
# Curso: Sistemas Operativos
# Estudiante: Paula Andrea Bolaños Arias.
# Código: 13207002 – A00068008
# Correo: pauandre27@gmail.com

# Objetivos
•	Emplear comandos de linux para la realización de tareas administrativas y obtener información del sistema operativo.
•	Implementar y desplegar servicios web en un servidor.

# Introducción
En el presente informe se explicará una guía paso a paso de lo que se realizó para la implementación exitosa de los servicios web, usando comandos Linux.

# Prerrequisitos
•	Sistema operativo CentOS 6.8 versión servidor

# Instalación
Teniendo en cuenta que, para la implementación de los servicios web es necesario emplear entornos virtuales, se debe instalar lo siguiente:
#cd /tmp
#wget https://bootstrap.pypa.io/get-pip.py
#python get-pip.py
#pip install virtualenv

# Desarrollo
1. Cree un usuario llamado filesystem_user
#adduser filesystem_user
#passwd filesystem_user

2.	Dé al usuario filesystem_user los permisos de root
#nano /etc/sudoers
Añada a la línea debajo de “root  ALL=(ALL:ALL)ALL”, la línea:
“filesystem_user  ALL=(ALL:ALL)ALL”.

3.	Conozca su ip para las diferentes conexiones remotas y para las pruebas
#ifconfig

4.	Cree un ambiente virtual en el usuario filesystem_user
#su filesystem_user
$ cd ~/
$ mkdir env
$ cd env
$ virtualenv flask_env

5.	Active el ambiente virtual creado
$ cd ~/env
$ . flask_env/bin/activate

6.	Teniendo el ambiente activo, instale Flask
$ pip install Flask

7.	Cree un directorio para guardar el código de los contratos
$ cd ~/
$ mkdir codigoContratos
$ cd codigoContratos

8.	Para implementar el contrato para /files, cree un archivo de nombre files.py
$ nano files.py
Escriba en él lo siguiente:

from flask import Flask, abort, request
import json

from files_commands import get_all_files, add_file, remove_file

app = Flask(__name__)
api_url = '/v1.0'

@app.route(api_url+'/files',methods=['POST'])
def create_file():
  content = request.get_json(silent=True)
  filename = content['filename']
  content = content['content']
  if not filename or not content:
    return "empty filename or content", 400
  if filename in get_all_files():
    return "file already exist", 400
  if add_file(filename,content):
    return "CREATED", 201
  else:
    return "error while creating file", 400

@app.route(api_url+'/files',methods=['GET'])
def read_files():
  list = {}
  list["files"] = get_all_files()
  return json.dumps(list), 200

@app.route(api_url+'/files',methods=['PUT'])
def update_file():
  return "NOT FOUND", 404

@app.route(api_url+'/files',methods=['DELETE'])
def delete_files():
  error = False
  for filename in get_all_files():
    if not remove_file(filename):
        error = True

  if error:
    return 'some files were not deleted', 400
  else:
    return 'OK. FILES DELETED', 200

if __name__ == "__main__":
  app.run(host='192.168.56.101',port=8080,debug='True')

9.	Luego, para especificar los métodos llamados en el archivo files.py, cree un archivo de nombre files_commands.py
$ nano files_commands.py
Escriba el siguiente contenido en él:

from subprocess import Popen, PIPE

def get_all_files():
  grep_process = Popen(["ls","/home/filesystem_user/git/Parcial-1-Operativos/codigoContratos"], stdout=PIPE, stderr=PIPE)
  file_list = Popen(["awk",'{print $1}'], stdin=grep_process.stdout, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')  
  return filter(None,file_list)

def add_file(filename,content):
  grep_process = Popen(["touch",filename], stdout=PIPE, stderr=PIPE)
  add_process = Popen(["echo","'",content,"'",">>",filename], stdin=grep_process.stdout, stdout=PIPE, stderr=PIPE)
  add_process.wait()
  return True if filename in get_all_files() else False

def remove_file(filename):
    remove_process = Popen(["rm",filename], stdout=PIPE, stderr=PIPE)
    remove_process.wait()
    return False if filename in get_all_files() else True


10.	Ahora, para poder implementar el servicio, abra el puerto 8080, que se está especificando en el archivo files.py y que posteriormente se usará también para el archivo recently_created.py, en las iptables, como el usuario root
$ su root
$ nano /etc/sysconfig/iptables
En este archivo, añada la siguiente línea:
-A INPUT -p tcp -s 127.0.0.1 --dport 8080 -j ACCEPT

11.	Finalmente, implemente el servicio
$ (flask_env) python files.py

12.	Pruebas del servicio web /files 
Instale la extensión Postman en su navegador de Google Chrome.
Ahora podrá ver las pruebas al servicio web empleando Postman. 
Prueba de la URI para files con GET 
Prueba de la URI para files con POST y enviando un JSON
Ahora puede ver el resultado del post, al estar agregado el archivo
Prueba de la URI para files con PUT 
Prueba de la URI para files con DELETE 
Y ahora, puede ver la prueba de que se eliminaron los archivos correctamente

13.	Cancele la ejecución del servicio, presionando la combinación de teclas CTRL y la tecla C

14.	Para implementar el contrato para /files/recently_created, cree un archivo de nombre recently_created.py
$ nano recently_created.py
Escriba en él lo siguiente:

from flask import Flask, abort, request
from subprocess import Popen, PIPE
import json

app = Flask(__name__)
api_url = '/v1.0/files'

@app.route(api_url+'/recently_created',methods=['POST'])
def post_recently_created():
  return "NOT FOUND", 404

@app.route(api_url+'/recently_created',methods=['GET'])
def get_files():
  list = {}
  files = Popen(["find","-cmin","+0","-cmin","-180"], stdout=PIPE, stderr=PIPE)
  recent_files = Popen(["awk",'-F','/','{print $2}'], stdin=files.stdout, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
  list["files"] = filter(None,recent_files)
  return json.dumps(list), 200

@app.route(api_url+'/recently_created',methods=['PUT'])
def put_recently_created():
  return "NOT FOUND", 404

@app.route(api_url+'/recently_created',methods=['DELETE'])
def delete_recently_created():
    return "NOT FOUND", 404

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8080,debug='True')

15.	Implemente el servicio
$ (flask_env) python recently_created.py

16.	Pruebas del servicio web /files/recently_created usando Postman
Prueba de la URI para files con GET
Prueba de la URI para files con POST
Prueba de la URI para files con PUT
Prueba de la URI para files con DELETE

17.	Cancele la ejecución del servicio, presionando la combinación de teclas CTRL y la tecla C

18.	Desactive el ambiente virtual
$ deactivate

# Enlace Repositorio Github: https://github.com/paulaandrea27/Parcial-1-Operativos.git
