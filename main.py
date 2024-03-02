import matplotlib.pyplot as plt

labels = ['Soja', 'Milho', 'Café', 'Algodão']
sizes = [15, 30, 45, 10]

plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.axis('equal')

plt.savefig('grafico_teste.png')


# Mostrar gráfico
#plt.show()

