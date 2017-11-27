# -*- coding: utf-8 -*-

class MotorDeEventosMontador():
	def __init__(self, rastro, montador, lista_inicial_eventos, codigo_montado, codigo_mnemonico, referencias_cruzadas):
		self.agora = 0
		self.count = 0
		self.rastro = rastro
		self.lista_eventos = lista_inicial_eventos
		self.log = ""
		self.codigo_montado = codigo_montado
		self.codigo_mnemonico = codigo_mnemonico
		self.montador = montador
		self.montador.referencias_cruzadas = referencias_cruzadas
								
	def inicia(self):
		fim = False
		while not fim:
			if self.lista_eventos.is_empty():
				fim = True
			else:
				fim = self.processa_evento(self.lista_eventos.serve())

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
			self.arquivo_entrada = open(self.codigo_mnemonico)
			self.montador.arquivo_saida = open(self.codigo_montado, a)
			self.adiciona_evento_no_topo("LE_LINHA")
			self.log += "instante " + str(self.agora) + " chegada de evento PASSO_UM\n"

		elif tipo_evento == "LE_LINHA":
			try:
				linha = self.arquivo_entrada.readline()
			except:
				raise TypeError("Evento de leitura de linha foi recebido, porém não havia arquivo de leitura aberto.")
			
			if linha != '':
				self.adiciona_evento_no_topo("LE_LINHA")
				self.montador.trata_linha(linha)

			self.log += "instante " + str(self.agora) + " chegada de evento LE_LINHA\n"

		elif tipo_evento == "DETECCAO_ERROS":
			erros = self.montador.detecta_erros()
			if erros:
				raise TypeError("Houve um erro na resolução de símbolos do arquivo de entrada, e código final não pode ser resolvido.")
			self.log += "instante " + str(self.agora) + " chegada de evento DETECCAO_ERROS\n"

		elif tipo_evento == "PASSO_DOIS":
			self.adiciona_evento_no_topo("GERA_BLOCO_NOME")
			self.log += "instante " + str(self.agora) + " chegada de evento PASSO_DOIS\n"

		elif tipo_evento == "GERA_BLOCO_NOME":
			self.montador.gera_bloco_nome()
			self.adiciona_evento_no_topo("GERA_BLOCO_ENT")
			self.log += "instante " + str(self.agora) + " chegada de evento GERA_BLOCO_NOME\n"

		elif tipo_evento == "GERA_BLOCO_ENT":
			self.montador.gera_bloco_ent()
			self.adiciona_evento_no_topo("GERA_BLOCO_EXT")
			self.log += "instante " + str(self.agora) + " chegada de evento GERA_BLOCO_ENT\n"

		elif tipo_evento == "GERA_BLOCO_EXT":
			self.montador.gera_bloco_ext()
			self.adiciona_evento_no_topo("GERA_BLOCO_DADOS")
			self.log += "instante " + str(self.agora) + " chegada de evento GERA_BLOCO_EXT\n"

		elif tipo_evento == "GERA_BLOCO_DADOS":
			self.montador.gera_bloco_dados()
			self.adiciona_evento_no_topo("GERA_BLOCO_FIM")
			self.log += "instante " + str(self.agora) + " chegada de evento GERA_BLOCO_DADOS\n"

		elif tipo_evento == "GERA_BLOCO_FIM":
			self.montador.gera_bloco_fim()
			self.log += "instante " + str(self.agora) + " chegada de evento GERA_BLOCO_FIM\n"

		elif tipo_evento == "FIM_SIMULACAO":
			self.arquivo_entrada.close()
			self.montador.arquivo_saida.close()
			self.gera_relatorio()
			self.gera_log()
			fim = True

		else:
			self.arquivo_entrada.close()
			self.montador.arquivo_saida.close()
			self.gera_relatorio()
			self.gera_log()
			raise TypeError("Tipo inválido de evento, simulação foi forçada a terminar")
		
		return fim
	
	def gera_log(self):
		if self.rastro:
			print(self.log)

	def gera_relatorio(self):
		print("Foram processados " + str(self.count) + " eventos, em " + str(self.agora) + " unidades de tempo.")