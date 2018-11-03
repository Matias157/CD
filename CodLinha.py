import matplotlib.pyplot as plt
import numpy as np

def my_lines(ax, pos, *args, **kwargs):
    if ax == 'x':
        for p in pos:
            plt.axvline(p, *args, **kwargs)
    else:
        for p in pos:
            plt.axhline(p, *args, **kwargs)

menssagem = "oi"
bits = ''.join(['%08d'%int(bin(ord(i))[2:]) for i in menssagem])
print bits

intbits = []
j = 0
while j != len(bits):
	if bits[j] == "0":
		intbits.append(0)
	else:
		intbits.append(1)
	j += 1

AMI = []
i = 0
onepos = 0
while i != len(intbits):
	if intbits[i] == 0:
		AMI.append(0)
	if intbits[i] == 1 and i != onepos:
		if AMI[onepos] == 0.5:
			AMI.append(-0.5)
		else:
			AMI.append(0.5)
		onepos = i
	i += 1

pseudoternario = []
i = 0
zeropos = 0
while i != len(intbits):
	if i == 0:
		pseudoternario.append(0.5)
	if intbits[i] == 1:
		pseudoternario.append(0)
	if intbits[i] == 0 and i != zeropos:
		if pseudoternario[zeropos] == 0.5:
			pseudoternario.append(-0.5)
		else:
			pseudoternario.append(0.5)
		zeropos = i
	i += 1

print intbits
print AMI
print pseudoternario

data1 = np.repeat(intbits, 2)
data2 = np.repeat(AMI, 2)
data3 = np.repeat(pseudoternario, 2)
t = 0.5 * np.arange(len(data1))

plt.hold(True)
my_lines('y', [0, 2, 4], color='.5', linewidth = 1)
plt.step(t, data1 + 4, 'r', linewidth = 1, where='post')
plt.step(t, data2 + 2, 'r', linewidth = 1, where='post')
plt.step(t, data3, 'r', linewidth = 1, where='post')
plt.ylim([-1,6])

for tbit, bit in enumerate(bits):
	plt.text(tbit + 0.5, 5.5, str(bit))

plt.text(0.1, 6.1, "Menssagem")
plt.text(0.1, 3, "AMI")
plt.text(0.1, 1, "Pseudoternario")

plt.gca().axis('off')
plt.show()
