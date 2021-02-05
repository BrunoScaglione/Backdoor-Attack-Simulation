# Backdoor-Attack-Simulation
Three sub-projects of different backdoor attack configurations scaling in complexity, with server and client implementations.

<h1 align="center">
Backdoor-Attack-Simulation
</h1>

<p align="center">
    This project is part of the Industrial Networks Course from the department of Mechatronics of the University of São Paulo (USP).
    It contains three sub-projects of different configurations for a backdoor attack. The main goal of the project was to learn to work with sockets, real-time applications, select
    library for managing multiple clients with  I/O multiplexing, and to understand the fundamentals of backdoor attacks, in Python.
</p>

<p align="center">
    Each of the sub-projects has a <strong>server.py</strong> and <strong>client.py</strong> file, correspondig to the programs running in the attacker's machine and 
    victim's machine respectively. In the first project, "Ex 1.1", the server always sends the same command to be run on the client's terminal and get the output. In the second project, "Ex 1.2", the attacker chooses the command. In the third project, "Ex 1.3",  the server program keeps track of each victim's situation, and allows the attacker to choose not only the command, but also which victim he wants to attack.
</p>

## Features
[//]: # (Add the features of your project here:)

- **socket** — a module that allows low-level networking , providing access to the BSD socket interface;
- **select** —  a module that allows I/O multiplexing;
- **subprocess** — a module that allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes;
- **threading** — a module that allows thread-based parallelism.

## Getting started

1. Pick a sub-project and go to it's directory (example below for the first project):
```bash
cd Ex 1.1
```
2. Run the server:
```bash
python server.py
```

3. Run the client(s):
```bash
python client.py
```


## Project details

You can check [my report](https://github.com/BrunoScaglione/Backdoor-Attack-Simulation/blob/main/Relatorio_Redes___Entrega_2.pdf) (in Portuguese) for more details on the project.
