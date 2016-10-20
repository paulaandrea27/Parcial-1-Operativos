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
