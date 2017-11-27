# -*- coding: utf-8 -*-

class Montador():
	def __init__(self):
		self.tabela_mnemonicos = {
			"JP": '0',
			"JZ": '1',
			"JN": '2',
			"LV": '3',
			"+": '4',
			"-": '5',
			"*": '6',
			"/": '7',
			"LD": '8',
			"MM": '9',
			"SC": 'A',
			"RS": 'B', 
			"HM": 'C',
			"GD": 'D',
			"PD": 'E',
			"OS": 'F'
		}
		self.nome = ''
		self.tipo = ''
		self.ents = {}
		self.exts = []
		self.org = ''
		self.dados = []
		self.end = ''
		self.arquivo_saida = None
		self.tabela_simbolos = {}
		self.contador_instrucoes = '0x0'
		self.referencias_cruzadas = []
		self.pseudo_instrucoes = ['ENT', 'EXT', 'NAME', 'ORG', 'END']

	def trata_linha(self, linha, referencias_cruzadas):
		elementos_linha = linha.split(' ')
		if elementos_linha[0] in self.pseudo_instrucoes:
			self.trata_pseudo_instrucao(elementos_linha)
		if len(elementos_linha) == 3:
			if elementos_linha[0] in self.tabela_simbolos:
				raise ValueError('Rótulo ' + elementos_linha[0] + ' definido duplamente')
			elif elementos_linha[0] in self.referencias_cruzadas:
				self.referencias_cruzadas[elementos_linha[0]] = {
					'posicao': self.contador_instrucoes,
					'referencias': []
				}
				self.ents[elementos_linha[0]]["posicao"] == self.contador_instrucoes
			else:
				self.tabela_simbolos[elementos_linha[0]] = {
					'posicao': self.contador_instrucoes
				}
		self.contador_instrucoes = hex(int(self.contador_instrucoes, 16) + 2)
	
	def trata_pseudo_instrucao(self, elementos_linha):
		if elementos_linha[0] == 'ENT':
			self.ents[elementos_linha[1]] = {}
			self.referencias_cruzadas[elementos_linha[1]] = {
				'modulo': self.nome
			}
		elif elementos_linha[0] == 'EXT':
			self.exts.append(elementos_linha[1])
			self.referencias_cruzadas[elementos_linha[1]] = {}
		elif elementos_linha[0] == 'NAME':
			self.nome == elementos_linha[1]
		elif elementos_linha[0] == 'ORG':
			self.org == elementos_linha[1]
		elif elementos_linha[0] == 'END':
			self.end == elementos_linha[1]	

	def detecta_erros(self):
		for key, value in self.tabela_simbolos.items():
	    	if !value['posicao']:
	    		return true
	    return false

	def gera_bloco_nome(self):
		self.arquivo_saida.write('NAME ' + self.nome + self.tipo + len(self.dados))

	def gera_bloco_ent(self):
		for key, value in ents:
			posicao = hex(int(value['posicao'], 16) + self.org)
			self.arquivo_saida.write('ENT ' + key + ' (' + posicao[3:] + ')X')

	def gera_bloco_ext(self):
		string = ''
		for item in exts:
			string += ' ' + item
		self.arquivo_saida.write('EXT' + string)

	def gera_bloco_dados(self):
		self.contador_instrucoes = self.org
		self.arquivo_saida.write('DADOS')
		self.arquivo_saida.write('ORG ' + self.org)
		for item in self.dados:
			operador = self.tabela_mnemonicos[item[0]]
			if item[1].isdigit():
				operando = item[1][1:]
			else:
				if item[1] in self.tabela_simbolos:
					operador = self.tabela_simbolos[item[1]]['posicao'][1:]
					tipo_endereco = 'R'
				else:
					operador = item[1]
					tipo_endereco = 'X'
					self.referencias_cruzadas[item[1]]["referencias"].append({modulo: self.nome, linha: self.contador_instrucoes})
			
			self.arquivo_saida.write(operador + '(' + operando + ')' + tipo_endereco)
			self.contador_instrucoes = hex(int(self.contador_instrucoes, 16) + 2)

	def gera_bloco_fim(self):
		self.arquivo_saida.write('END (' + self.end[3:] + ')R')

	def verifica_referencias_cruzadas(self, referencias_cruzadas):
		for key, value in self.tabela_simbolos.items():
	    	if !value['posicao'] || !value['modulo']:
	    		return true
	    return false