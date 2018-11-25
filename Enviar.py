import os
from socket import *
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process
import pickle

def my_lines(ax, pos, *args, **kwargs):
    if ax == 'x':
        for p in pos:
            plt.axvline(p, *args, **kwargs)
    else:
        for p in pos:
            plt.axhline(p, *args, **kwargs)

host = "192.168.0.2"
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
mensagem = input("Entre a mensagem: ")

def plot_graph():
	plt.show()

bits = ''.join('{:08b}'.format(b) for b in mensagem.encode('latin_1'))
print(bits)

intbits = []
j = 0
while j != len(bits):
	if bits[j] == "0":
		intbits.append(0)
	else:
		intbits.append(1)
	j += 1

print(intbits)

while(True):
	opcao = input("Escolha a codificação:\n1 = AMI\n2 = Pseudoternário\n")
	if opcao == "1":
		AMI = []
		i = 0
		onepos = 0
		while i != len(intbits):
			if intbits[i] == 0 and i == 0:
				AMI.append(0)
			if intbits[i] == 1 and i == 0:
				AMI.append(0.5)
				onepos = i
			if intbits[i] == 0 and i != 0:
				AMI.append(0)
			if intbits[i] == 1 and i != 0:
				if AMI[onepos] == 0.5:
					AMI.append(-0.5)
				else:
					AMI.append(0.5)
				onepos = i
			i += 1
		enviar = ["A"] + AMI[:]
		print(enviar)

		data = pickle.dumps(enviar)

		UDPSock.sendto(data, addr)

		data1 = np.repeat(intbits, 2)
		data2 = np.repeat(AMI, 2)
		t = 0.5 * np.arange(len(data1))

		my_lines('y', [0, 4], color='.5', linewidth = 1)
		plt.step(t, data1 + 4, 'r', linewidth = 1, where='post')
		plt.step(t, data2, 'r', linewidth = 1, where='post')
		plt.ylim([-1,6])

		for tbit, bit in enumerate(bits):
			plt.text(tbit + 0.5, 5.5, str(bit))

		plt.text(0.1, 6.1, "Mensagem: " + mensagem)
		plt.text(0.1, 1, "AMI")
		break
	elif opcao == "2":
		pseudoternario = []
		i = 0
		zeropos = 0
		while i != len(intbits):
			if intbits[i] == 0 and i == 0:
				pseudoternario.append(0.5)
				zeropos = i
			if intbits[i] == 1 and i == 0:
				pseudoternario.append(0)
			if intbits[i] == 1 and i != 0:
				pseudoternario.append(0)
			if intbits[i] == 0 and i != 0:
				if pseudoternario[zeropos] == 0.5:
					pseudoternario.append(-0.5)
				else:
					pseudoternario.append(0.5)
				zeropos = i
			i += 1
		enviar = ["P"] + pseudoternario[:]
		print(enviar)

		data = pickle.dumps(enviar)

		UDPSock.sendto(data, addr)

		data1 = np.repeat(intbits, 2)
		data3 = np.repeat(pseudoternario, 2)
		t = 0.5 * np.arange(len(data1))

		my_lines('y', [0, 4], color='.5', linewidth = 1)
		plt.step(t, data1 + 4, 'r', linewidth = 1, where='post')
		plt.step(t, data3, 'r', linewidth = 1, where='post')
		plt.ylim([-1,6])

		for tbit, bit in enumerate(bits):
			plt.text(tbit + 0.5, 5.5, str(bit))

		plt.text(0.1, 6.1, "Mensagem: " + mensagem)
		plt.text(0.1, 1, "Pseudoternario")
		break
	else:
		print("Valor incorreto!!!")
		continue

plt.gca().axis('off')

p = Process(target=plot_graph)
p.start()

UDPSock.close()
os._exit(0)