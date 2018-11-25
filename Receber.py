import re
import os
from socket import *
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process
import pickle

# imprime linhas do gráfico
def my_lines(ax, pos, *args, **kwargs):
    if ax == 'x':
        for p in pos:
            plt.axvline(p, *args, **kwargs)
    else:
        for p in pos:
            plt.axhline(p, *args, **kwargs)

def plot_graph():
	plt.show()

host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

print("Esperando receber a mensagem...")
(cod, addr) = UDPSock.recvfrom(buf)
print("Mensagem recebida: " + cod)

data = pickle.loads(cod)

while(True):
	opcao = input("Escolha a codificação:\n1 = AMI\n2 = Pseudoternário\n")
	if opcao == "1":
		codfic = "AMI"
		mensagem = []
		i = 0
		while i != len(data):
			if data[i] == 0:
				mensagem.append(0)
			if data[i] == 0.5 or data[i] == -0.5:
				mensagem.append(1)
			i += 1
	elif opcao == "2":
		codfic = "Pseudoternário"
		mensagem = []
		i = 0
		while i != len(data):
			if data[i] == 0:
				mensagem.append(1)
			if data[i] == 0.5 or data[i] == -0.5:
				mensagem.append(0)
			i += 1
	else:
		print("Valor incorreto!!!")
		continue

data1 = np.repeat(mensagem, 2)
data2 = np.repeat(data, 2)
t = 0.5 * np.arange(len(data1))

my_lines('y', [0, 2, 4], color='.5', linewidth = 1)
plt.step(t, data1 + 4, 'r', linewidth = 1, where='post')
plt.step(t, data2 + 2, 'r', linewidth = 1, where='post')
plt.ylim([-1,6])

for tbit, bit in enumerate(mensagem):
	plt.text(tbit + 0.5, 5.5, str(bit))

mensagem = bytes(int(b, 2) for b in re.split('(........)', mensagem) if b).decode('latin_1')

plt.text(0.1, 6.1, "Mensagem: " + mensagem)
plt.text(0.1, 3, codfic)

plt.gca().axis('off')

p = Process(target=plot_graph)
p.start()

UDPSock.close()
os._exit(0)