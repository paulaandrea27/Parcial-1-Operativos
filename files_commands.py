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
