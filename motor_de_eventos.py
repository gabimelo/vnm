# -*- coding: utf-8 -*-

class MotorDeEventos():
	def __init__(self, rastro, lista_inicial_eventos, mvn, programa):
		self.agora = 0
		self.count = 0
		self.rastro = rastro
		self.lista_eventos = lista_inicial_eventos
		self.log = ""
		self.mvn = mvn
		self.programa = programa
								
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

		if tipo_evento == "LOAD":
			self.mvn.load(self.programa)
			self.log += "instante " + str(self.agora) + " chegada de evento LOAD\n"
			# print('load')

		elif tipo_evento == "START":
			self.mvn.start(self.programa)
			self.log += "instante " + str(self.agora) + " chegada de evento START\n"
			# print('start')

		elif tipo_evento == "FETCH":
			self.mvn.fetch()
			self.adiciona_evento_no_topo('DECODE')
			self.log += "instante " + str(self.agora) + " chegada de evento FETCH\n"
			# print('fetch')

		elif tipo_evento == "DECODE":
			prox_evento = self.mvn.decode()
			self.adiciona_evento_no_topo(prox_evento)
			self.log += "instante " + str(self.agora) + " chegada de evento DECODE\n"
			# print('decode')

		elif tipo_evento == "JP":
			self.mvn.JP()
			self.adiciona_evento_no_topo('FETCH')
			self.log += "instante " + str(self.agora) + " chegada de evento JP\n"
			# print('jp')

		elif tipo_evento == "JZ":
			self.mvn.JZ()
			self.adiciona_evento_no_topo('FETCH')
			self.log += "instante " + str(self.agora) + " chegada de evento JZ\n"
			# print('jz')
		
		elif tipo_evento == "JN":
			self.mvn.JN()
			self.adiciona_evento_no_topo('FETCH')
			self.log += "instante " + str(self.agora) + " chegada de evento JN\n"
			# print('jn')
		
		elif tipo_evento == "LV":
			self.mvn.LV()
			self.adiciona_evento_no_topo('FETCH')
			self.log += "instante " + str(self.agora) + " chegada de evento LV\n"	
			# print('lv')

		elif tipo_evento == "+":
			self.mvn.add()
			self.adiciona_evento_no_topo('FETCH')
			self.log += "instante " + str(self.agora) + " chegada de evento +\n"
			# print('+')

		elif tipo_evento == "-":
			self.mvn.sub()
			self.adiciona_evento_no_topo('FETCH')
			self.log += "instante " + str(self.agora) + " chegada de evento -\n"
			# print('-')

		elif tipo_evento == "*":
			self.mvn.mult()
			self.adiciona_evento_no_topo('FETCH')
			self.log += "instante " + str(self.agora) + " chegada de evento *\n"
			# print('*')

		elif tipo_evento == "/":
			self.mvn.div()
			self.adiciona_evento_no_topo('FETCH')
			self.log += "instante " + str(self.agora) + " chegada de evento /\n"
			# print('/')

		elif tipo_evento == "LD":
			self.mvn.LD()
			self.adiciona_evento_no_topo('FETCH')
			self.log += "instante " + str(self.agora) + " chegada de evento LD\n"
			# print('ld')

		elif tipo_evento == "MM":
			self.mvn.MM()
			self.adiciona_evento_no_topo('FETCH')
			self.log += "instante " + str(self.agora) + " chegada de evento MM\n"
			# print('mm')

		elif tipo_evento == "SC":
			self.mvn.SC()
			self.adiciona_evento_no_topo('FETCH')
			self.log += "instante " + str(self.agora) + " chegada de evento SC\n"
			# print('sc')

		elif tipo_evento == "RS":
			self.mvn.RS()
			self.adiciona_evento_no_topo('FETCH')			
			self.log += "instante " + str(self.agora) + " chegada de evento RS\n"
			# print('rs')

		elif tipo_evento == "HM":
			self.mvn.HM()
			self.adiciona_evento_no_topo('FIM_SIMULACAO')
			self.log += "instante " + str(self.agora) + " chegada de evento HM\n"
			# print('hm')

		elif tipo_evento == "GD":
			self.mvn.GD()
			self.adiciona_evento_no_topo('FETCH')	
			self.log += "instante " + str(self.agora) + " chegada de evento GD\n"
			# print('gd')

		elif tipo_evento == "PD":
			self.mvn.PD()
			self.adiciona_evento_no_topo('FETCH')	
			self.log += "instante " + str(self.agora) + " chegada de evento PD\n"
			# print('pd')

		elif tipo_evento == "OS":
			self.mvn.OS()
			self.adiciona_evento_no_topo('FETCH')	
			self.log += "instante " + str(self.agora) + " chegada de evento OS\n"
			# print('os')

		elif tipo_evento == "FIM_SIMULACAO":
			self.mvn.imprime_memoria()
			self.mvn.imprime_registradores()
			self.gera_relatorio()
			self.gera_log()
			fim = True

		else:
			self.gera_relatorio()
			self.gera_log()
			raise TypeError("Tipo inválido de evento, simulação foi forçada a terminar")
		
		return fim
	
	def gera_log(self):
		if self.rastro:
			print(self.log)

	def gera_relatorio(self):
		print("Foram processados " + str(self.count) + " eventos, em " + str(self.agora) + " unidades de tempo.")