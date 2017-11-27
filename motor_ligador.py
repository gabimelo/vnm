# -*- coding: utf-8 -*-

class MotorDeEventosLigador():
	def __init__(self, rastro, ligador, lista_inicial_eventos, codigo_final, codigo_montado, referencias_cruzadas, base_relocacao):
		self.agora = 0
		self.count = 0
		self.rastro = rastro
		self.lista_eventos = lista_inicial_eventos
		self.log = ""
		self.codigo_montado = codigo_montado
		self.codigo_final = codigo_final
		self.ligador.referencias_cruzadas = referencias_cruzadas
		self.ligador.base_relocacao_geral = base_relocacao_geral
								
	def inicia(self):
		fim = False
		while not fim:
			if self.lista_eventos.is_empty():
				fim = True
			else:
				fim = self.processa_evento(self.lista_eventos.serve())
				return self.referencias_cruzadas

	def adiciona_evento_no_topo(self, tipo):
		if self.lista_eventos.is_empty():
			proximo_instante = self.agora + 1
		else:
			proximo_instante = self.agora
		self.lista_eventos.append([proximo_instante, tipo])

	def processa_evento(self, evento):
		self.count += 1
		self.agora = evento[0]
		tipo_evento = evento[1]

		fim = False

		if tipo_evento == "PASSO_UM":
			self.arquivo_entrada = open(self.codigo_montado)
			self.ligador.arquivo_saida = open(self.codigo_final)
			self.adiciona_evento_no_topo("LE_BLOCO_NOME")
			self.log += "instante " + str(self.agora) + " chegada de evento PASSO_UM\n"

		if tipo_evento == "LE_BLOCO_NOME":
			linha = self.arquivo_entrada.readline()
			if linha != '':
				self.adiciona_evento_no_topo('LE_BLOCOS_ENT_EXT')
				self.ligador.interpreta_bloco_nome(linha)

		if tipo_evento == "LE_BLOCOS_ENT_EXT":
			linhas = [self.arquivo_entrada.readline()]
			while linha[0][:3] == 'ENT':
				linha = self.arquivo_entrada.readline()
				linhas.append(linha)
			self.adiciona_evento_no_topo('LE_BLOCO_DADOS')
			self.ligador.interpreta_bloco_ent_ext(linhas)
		
		if tipo_evento == "LE_BLOCO_DADOS":
			self.adiciona_evento_no_topo('LE_BLOCO_FIM')
			linhas = [self.arquivo_entrada.readline()]
			while linha[0][:3] == 'ENT':
				linha = self.arquivo_entrada.readline()
				linhas.append(linha)
			self.ligador.interpreta_bloco_dados(linhas)
		
		if tipo_evento == "LE_BLOCO_FIM":
			self.adiciona_evento_no_topo('LE_BLOCO_NOME')
			self.ligador.interpreta_bloco_fim(self.arquivo_entrada.readline())

		elif tipo_evento == "PASSO_DOIS":
			self.ligador.reloca_enderecos()
			self.log += "instante " + str(self.agora) + " chegada de evento PASSO_DOIS\n"

		elif tipo_evento == "FIM_SIMULACAO":
			self.arquivo_entrada.close()
			self.ligador.arquivo_saida.close()
			self.gera_relatorio()
			self.gera_log()
			fim = True

		else:
			self.arquivo_entrada.close()
			self.ligador.arquivo_saida.close()
			self.gera_relatorio()
			self.gera_log()
			raise TypeError("Tipo inválido de evento, simulação foi forçada a terminar")
		
		return fim
	
	def gera_log(self):
		if self.rastro:
			print(self.log)

	def gera_relatorio(self):
		print("Foram processados " + str(self.count) + " eventos, em " + str(self.agora) + " unidades de tempo.")