import re
import os
from socket import *
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process
import pickle
from tkinter import *
from tkinter import messagebox
import time

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

def conecta():
	lbl.config(text = "Esperando receber mensagem...")
	(cod, addr) = UDPSock.recvfrom(buf)

	data = pickle.loads(cod)

	if(data[0] == 'A'):
		data.pop(0)
		codfic = "AMI"
		mensagem = []
		i = 0
		while i != len(data):
			if data[i] == 0:
				mensagem.append(0)
			if data[i] == 0.5 or data[i] == -0.5:
				mensagem.append(1)
			i += 1
	else:
		data.pop(0)
		codfic = "Pseudoternário"
		mensagem = []
		i = 0
		while i != len(data):
			if data[i] == 0:
				mensagem.append(1)
			if data[i] == 0.5 or data[i] == -0.5:
				mensagem.append(0)
			i += 1

	print(mensagem)

	data1 = np.repeat(mensagem, 2)
	data2 = np.repeat(data, 2)
	t = 0.5 * np.arange(len(data1))

	my_lines('y', [0, 4], color='.5', linewidth = 1)
	plt.step(t, data1 + 4, 'r', linewidth = 1, where='post')
	plt.step(t, data2, 'r', linewidth = 1, where='post')
	plt.ylim([-1,6])

	for tbit, bit in enumerate(mensagem):
		plt.text(tbit + 0.5, 5.5, str(bit))


	strbits = ''
	for bit in mensagem:
		if bit == 0:
			strbits = strbits + '0' 
		else:
			strbits = strbits + '1'

	texto = bytes(int(b, 2) for b in re.split('(........)', strbits) if b).decode('latin_1')

	lbl.config(text = 'Mensagem recebida: "'+texto+'"' )
	lbl2.config(text = 'Estabelecer conexão novamente? ')

	plt.text(0.1, 6.1, "Mensagem: "+texto)
	plt.text(0.1, 1, codfic)

	plt.gca().axis('off')

	p = Process(target=plot_graph)
	p.start()

	# UDPSock.close()
	os._exit(0)


host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

window = Tk()
window.geometry('400x200+500+300')
window.title("AMI/Pseudoternário")
lbl = Label(window, text="Estabelecer conexão?")
lbl.grid(column=0, row=0)
lbl2 = Label(window, text="")
lbl2.grid(column=0, row=1)
#Cria botão para estabelecer conexão
btn = Button(window, text="Sim", command=conecta)
btn.grid(column=2, row=2)

window.mainloop()