from tkinter import *
from tkinter import messagebox
import os
from socket import *
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process
import pickle

# Define as linhas do gráfico
def my_lines(ax, pos, *args, **kwargs):
    if ax == 'x':
        for p in pos:
            plt.axvline(p, *args, **kwargs)
    else:
        for p in pos:
            plt.axhline(p, *args, **kwargs)

#Plota as linhas do gráfico
def plot_graph():
	plt.show()

def codifica_mensagem_AMI(intbits, mensagem, bits):
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

def codifica_mensagem_Pseudo(intbits, mensagem, bits):
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

def codifica_mensagem():
	# Transforma a mensagem em binário
	mensagem = txt.get()
	bits = ''.join('{:08b}'.format(b) for b in mensagem.encode('latin_1'))
	print(bits)
	
	# Tranforma a mensagem em binário de string para inteiro
	intbits = []
	j = 0
	while j != len(bits):
		if bits[j] == "0":
			intbits.append(0)
		else:
			intbits.append(1)
		j += 1
	print(intbits)

	if var.get() == 1:
		codificacao = 'AMI'
		codifica_mensagem_AMI(intbits, mensagem, bits)
	elif var.get() == 2:
		codificacao = 'Pseudoternário'
		codifica_mensagem_Pseudo(intbits, mensagem, bits)
	messagebox.showinfo('Enviada!', 'Mensagem "'+mensagem+'" enviada na codificação '+codificacao)

#Mostra mensagens de erros e codificação escolhida
def verifica():
	if txt.get() == "":
		res = messagebox.askretrycancel('Erro', 'Digite uma mensagem para ser enviada.')
		if res == False:
			window.destroy()
	else:
		if var.get() != 1 and var.get() != 2:
			res = messagebox.askretrycancel('Erro', 'Escolha uma opção de codificação.')
			if res == False:
				window.destroy()
		else:
			codifica_mensagem()

	plt.gca().axis('off')

	p = Process(target=plot_graph)
	p.start()
	
	UDPSock.close()
	os._exit(0)

# Estabelece conexão com o outro computador
host = "192.168.0.2"
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)

#Cria a janela da interface gráfica
window = Tk()
window.geometry('400x200+400+300')
window.title("AMI/Pseudoternário")

#Cria label da entrada
lbl = Label(window, text="Digite sua mensagem:")
lbl.grid(column=0, row=0)

#Cria botões de escolha entre AMI e Pseudoternário
var = IntVar()
rad1 = Radiobutton(window,text='AMI', value=1,variable=var)
rad2 = Radiobutton(window,text='Pseudoternário', value=2,variable=var)
rad1.grid(column=0, row=1)
rad2.grid(column=1, row=1)

#Cria entrada de texto
txt = Entry(window,width=10)
txt.grid(column=1, row=0)

#Cria botão para enviar mensagem
btn = Button(window, text="Enviar", command=verifica)
btn.grid(column=1, row=2)


window.mainloop()

