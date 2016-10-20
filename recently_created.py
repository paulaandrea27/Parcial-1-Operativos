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

