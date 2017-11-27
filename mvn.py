# -*- coding: utf-8 -*-

from minHeap import *
from random import randint
import math

class MVN():
	def __init__(self):
		self.registradores = {}
		self.registradores["AC"] = '0x0'
		self.registradores["CI"] = '0x0'
		self.registradores["OP"] = '0x0'
		self.registradores["CO"] = '0x0'
		self.tabela_de_operandos = [
			"JP", "JZ", "JN", "LV", "+", "-", 
			"*","/", "LD", "MM", "SC", "RS", 
			"HM", "GD", "PD", "OS"];
		self.memoria = [hex(randint(0,255)) for i in range(int("0xFFFF", 16) + 1)]
		self.discos = []
		self.impressoras = []

	def imprime_registradores(self):
		print('Registradores: ')
		print('AC: ' + str(self.registradores["AC"]))
		print('CI: ' + str(self.registradores["CI"]))
		print('OP: ' + str(self.registradores["OP"]))
		print('CO: ' + str(self.registradores["CO"]))

	def imprime_memoria(self, endereco_inicio = "0x0000", endereco_fim = "0x01F0"):
		rangeBeginning = int(endereco_inicio, 16) // 16 
		rangeEnd = math.ceil(int(endereco_fim, 16) / 16) - rangeBeginning
		for i in range(rangeBeginning, rangeEnd):
			print('\n' + hex(i).upper() + ':', end=" ")
			
			for j in range(16):
				hexStr = str(self.memoria[(i*16)+j].upper()[2:])
				if len(hexStr) == 1:
					hexStr = '0' + hexStr
				print(hexStr, end=" ")
		print('\n')

	def get_hi_nibble(self, byte):
		high, low = divmod(int(byte, 16), 0x10)
		return hex(high)

	def get_lo_nibble(self, byte):
		high, low = divmod(int(byte, 16), 0x10)
		return hex(low)

	def get_hi_byte(self, byte):
		high, low = divmod(int(byte, 16), 0x100)
		return hex(high)

	def get_lo_byte(self, byte):
		high, low = divmod(int(byte, 16), 0x100)
		return hex(low)

	def incrementaCI(self):
		self.registradores["CI"] = hex(int(self.registradores["CI"], 16) + 2)

	def load(self, programa):
		arquivo = open(programa)

		for linha in arquivo:
			endereco = '0x' + linha.rstrip('\n').split(" ")[0]
			valor = '0x' + linha.rstrip('\n').split(" ")[1]
			if len(valor) == 6:
				self.memoria[int(endereco, 16)] = self.get_hi_byte(valor)
				self.memoria[int(endereco, 16) + 1] = self.get_lo_byte(valor)
			else:
				self.memoria[int(endereco, 16)] = valor

		arquivo.close()
		self.imprime_memoria()

	def loader_manual(self, endereco, valor):
		if len(valor) == 6:
			self.memoria[int(endereco, 16)] = self.get_hi_byte(valor)
			self.memoria[int(endereco, 16) + 1] = self.get_lo_byte(valor)
			return hex(int(endereco, 16) + 2)
		else:
			self.memoria[int(endereco, 16)] = valor
			return hex(int(endereco, 16) + 1)

	def start(self, programa):
		arquivo = open(programa)
		self.registradores["CI"] = '0x' + arquivo.readline().rstrip('\n').split(" ")[0]
		arquivo.close()

		self.impressoras = ['impressora0.txt']
		impressora0 = open(self.impressoras[0], 'w')
		impressora0.write('')
		impressora0.close()

		self.discos = []
		disco0 = open('disco0.txt')
		conteudo_disco0 = disco0.read()
		conteudo_disco0 = conteudo_disco0.rstrip(' ')
		n = 4
		self.discos.append({'conteudo': [('0x' + str(conteudo_disco0[i:i+n])) for i in range(0, len(conteudo_disco0), n)], 'posicao_de_leitura': 0})

	def fetch(self):
		aux = self.memoria[int(self.registradores["CI"], 16) + 1][2:]
		if len(aux) == 1:
			aux = "0" + aux
		self.registradores["OP"] = self.get_lo_nibble(self.memoria[int(self.registradores["CI"], 16)]) + aux
		self.registradores["CO"] = self.get_hi_nibble(self.memoria[int(self.registradores["CI"], 16)])
		self.imprime_registradores()

	def decode(self):
		return self.tabela_de_operandos[int(self.registradores["CO"], 16)]

	def JP(self):
		self.registradores["CI"] = self.registradores["OP"]

	def JZ(self):
		if int(self.registradores["AC"], 16) == 0:
			self.registradores["CI"] = self.registradores["OP"]
		else:
			self.incrementaCI()

	def JN(self):
		if int(self.registradores["AC"], 16) < 0:
			self.registradores["CI"] = self.registradores["OP"]
		else:
			self.incrementaCI()

	def LV(self):
		aux = self.registradores["OP"]
		while len(aux) < 6:
			aux = aux[:2] + "0" + aux[2:]
		self.registradores["AC"] = aux
		self.incrementaCI()

	def prepara_segundo_termo(self, a, b):
		if len(a) == 3:
			a = a[0:2] + "0" + a[2:]		
		if len(b) == 1:
			b = "0" + b
		res = a + b
		return int(res, 16)

	def add(self):
		self.registradores["AC"] = hex(int(self.registradores["AC"], 16) + self.prepara_segundo_termo(self.memoria[int(self.registradores["OP"], 16)], self.memoria[int(self.registradores["OP"], 16) + 1][2:]))
		while len(self.registradores["AC"]) > 6:
			self.registradores["AC"] = self.registradores["AC"][0:2] + self.registradores["AC"][3:]
		self.incrementaCI()

	def sub(self):
		self.registradores["AC"] =  hex(int(self.registradores["AC"], 16) - self.prepara_segundo_termo(self.memoria[int(self.registradores["OP"], 16)], self.memoria[int(self.registradores["OP"], 16) + 1][2:]))
		while len(self.registradores["AC"]) > 6:
			self.registradores["AC"] = self.registradores["AC"][0:2] + self.registradores["AC"][3:]
		self.incrementaCI()

	def mult(self):
		self.registradores["AC"] = hex(int(self.registradores["AC"], 16) * self.prepara_segundo_termo(self.memoria[int(self.registradores["OP"], 16)], self.memoria[int(self.registradores["OP"], 16) + 1][2:]))
		while len(self.registradores["AC"]) > 6:
			self.registradores["AC"] = self.registradores["AC"][0:2] + self.registradores["AC"][3:]
		self.incrementaCI()

	def div(self):
		self.registradores["AC"] = hex(int(self.registradores["AC"], 16) // self.prepara_segundo_termo(self.memoria[int(self.registradores["OP"], 16)], self.memoria[int(self.registradores["OP"], 16) + 1][2:]))
		while len(self.registradores["AC"]) > 6:
			self.registradores["AC"] = self.registradores["AC"][0:2] + self.registradores["AC"][3:]
		self.incrementaCI()

	def LD(self):
		primeira_parte = self.memoria[int(self.registradores["OP"], 16)]
		if len(primeira_parte) == 3:
			primeira_parte = primeira_parte[0:2] + "0" + primeira_parte[2:]		
		segunda_parte = self.memoria[int(self.registradores["OP"], 16) + 1][2:]
		if len(segunda_parte) == 1:
			segunda_parte = "0" + segunda_parte
		self.registradores["AC"] =  primeira_parte + segunda_parte
		self.incrementaCI()

	def MM(self):
		aux = self.get_hi_byte(self.registradores["AC"])
		if len(aux) == 3:
			aux = aux[0:2] + "0" + aux[2:]
		self.memoria[int(self.registradores["OP"], 16)] = aux
		aux = self.get_lo_byte(self.registradores["AC"])
		if len(aux) == 3:
			aux = aux[0:2] + "0" + aux[2:]
		self.memoria[int(self.registradores["OP"], 16) + 1] = aux
		self.incrementaCI()

	def SC(self):
		self.memoria[int(self.registradores["OP"], 16)] = self.get_hi_byte(hex(int(self.registradores["CI"], 16) + 2))
		self.memoria[int(self.registradores["OP"], 16) + 1] = self.get_lo_byte(hex(int(self.registradores["CI"], 16) + 2))
		self.registradores["CI"] = hex(int(self.registradores["OP"], 16) + 2)

	def RS(self):
		self.registradores["CI"] = self.registradores["OP"]

	def HM(self):
		self.registradores["CI"] = self.registradores["OP"]

	def GD(self):
		if self.registradores["OP"][2] == "0":
			self.registradores["AC"] = input('Entre com o dado (formato 0x0000): ')
		if self.registradores["OP"][2] == "3":
			num_do_disco = int(self.registradores["OP"][-1])
			self.registradores["AC"] = self.discos[num_do_disco]["conteudo"][self.discos[num_do_disco]["posicao_de_leitura"]]
			self.discos[num_do_disco]["posicao_de_leitura"] += 1
		self.incrementaCI()

	def PD(self):
		if self.registradores["OP"][-2] == "1":
			if self.registradores["OP"][2] == "1":
				print(self.registradores["AC"][-1])
			else: 
				print(self.registradores["AC"][2:])
		else:
			num_da_impressora = int(self.registradores["OP"][-1])
			impressora = open(self.impressoras[num_da_impressora], 'a')
			if self.registradores["OP"][2] == "1":
				impressora.write(self.registradores["AC"][-1])
			elif self.registradores["OP"][2] == "2":
				impressora.write(self.registradores["AC"][2:4] + " " + self.registradores["AC"][4:] + " ") 
			else:
				impressora.write(self.registradores["AC"][2:])
			self.incrementaCI()

	def OS(self):
		# OS call
		self.incrementaCI()