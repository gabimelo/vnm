# -*- coding: utf-8 -*-

class Ligador():
	def __init__(self, base_relocacao, referencias_cruzadas):
		self.modulo_corrente = ''
		self.dados = []
		self.base_relocacao = base_relocacao
		self.bases_relocacao = {}
		self.referencias_cruzadas = referencias_cruzadas
		self.endereco_inicio = None

	def soma_hex(numero_hex, numero_int):
		return hex(int(numero_hex, 16) + numero_int)

	def interpreta_bloco_nome(self, bloco):
		itens = bloco.split(' ')
		if itens[1] == '':
			raise ValueError('Ocorreu um erro tentando realizar as ligações, um módulo não possuia nome definido')
		self.modulo_corrente = itens[1]
		self.bases_relocacao[self.modulo_corrente] = self.base_relocacao
		self.base_relocacao = self.soma_hex(self.base_relocacao, itens[3])

	def interpreta_bloco_ent_ext(self, bloco):
		for i in range(len(bloco)-2):
			self.referencias_cruzadas[bloco[i]].posicao = self.soma_hex(self.referencias_cruzadas[bloco[i]].posicao, self.bases_relocacao[self.modulo_corrente])

	def interpreta_bloco_dados(self, bloco):
		self.dados.append([self.modulo_corrente, bloco])

	def interpreta_bloco_fim(self, bloco):
		if not self.endereco_inicio:
			self.endereco_inicio = self.soma_hex('0x' + str(bloco.split(' ')[1][1:4]), self.bases_relocacao[self.modulo_corrente])

	def reloca_enderecos(self):
		for bloco in self.dados:
			self.modulo_corrente = bloco[0]
			self.base_relocacao = self.bases_relocacao[self.modulo_corrente]
			for linha in bloco[1]:
				if linha[1:4].isdigit():
					self.arquivo_saida.write(linha[0] + linha[1:4] + self.base_relocacao)
				else:
					simbolo = linha[2:-2]
					self.arquivo_saida.write(linha[0] + self.referencias_cruzadas[simbolo].posicao