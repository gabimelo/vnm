# -*- coding: utf-8 -*-

from motor_de_eventos import *
from minHeap import *
from mvn import *
	
def aciona_rastro(): 
	rastro = "?"
	while rastro == "?": 
		rastro = input("Deseja acionar a função de rastro? (s/n) ")
		if rastro == "s":
			rastro = True
		elif rastro == "n":
			rastro = False
		else:
			print("Opções para rastro: s ou n")
	return rastro

def agenda_eventos():
	lista_eventos = MinHeap()
	horario = 0
	lista_eventos.append([horario, "LOAD"])
	horario += 1
	lista_eventos.append([horario, "START"])
	horario += 1
	lista_eventos.append([horario, "FETCH"])
	return lista_eventos

def main():
	sair = False
	mvn = MVN()
	while not sair:
		comandos = [0, 1, 11, 12, 2, 3, 4, 5, 6, 71, 72, 8, 9, 10]
		print('''
	---Menu de Comandos---
	1 	execução de programa pela MVN a partir de arquivo texto 
	11  execução do programa n^2 pela MVN a partir de arquivo texto já fornecido
	12  execução do programa sqrt(n) pela MVN a partir de arquivo texto já fornecido
	2 	micro pré loader
	3 	dumper binário
	4 	pré loader binário
	5 	loader completo
	6 	dumper binário completo
	71 	loader hexadecimal
	72 	dumper hexadecimal
	8 	loader manual de memória
	9 	visualizador de mapa de memória
	10 	loader manual e visualizador de memória
	100 sair do modo loader manual e visualizador de memória
	0 	sair
	''')

		comando = input('Digite um comando: ')
		try:
			comando = int(comando)
			assert comando in comandos
		except (ValueError, AssertionError):
			print('Comando desconhecido, tente novamente')
		else:
			if comando == 1:
				lista_eventos = agenda_eventos()
				programa = input("Digite o nome do arquivo que contém o programa a ser executado pela MVN: ")
				# motor = MotorDeEventos(aciona_rastro(), lista_eventos, mvn, programa)
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()
			elif comando == 11:
				lista_eventos = agenda_eventos()
				# motor = MotorDeEventos(aciona_rastro(), lista_eventos, mvn, programa)
				programa = "n2.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()
			elif comando == 12:
				lista_eventos = agenda_eventos()
				# motor = MotorDeEventos(aciona_rastro(), lista_eventos, mvn, programa)
				programa = "sqrt_n.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()
			elif comando == 2:
				lista_eventos = agenda_eventos()
				# motor = MotorDeEventos(aciona_rastro(), lista_eventos, mvn, programa)
				programa = "micro_pre_loader.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()
			elif comando == 3:
				lista_eventos = MinHeap()
				horario = 0
				lista_eventos.append([horario, "LOAD"])
				programa = "dig_hex_to_bin.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()

				lista_eventos = MinHeap()
				horario = 0
				lista_eventos.append([horario, "LOAD"])
				programa = "hex_to_bin.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()

				lista_eventos = agenda_eventos()
				# motor = MotorDeEventos(aciona_rastro(), lista_eventos, mvn, programa)
				programa = "dumper_bin.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()
			elif comando == 4:
				lista_eventos = agenda_eventos()
				# motor = MotorDeEventos(aciona_rastro(), lista_eventos, mvn, programa)
				programa = "pre_loader_binario.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()
			elif comando == 5:
				lista_eventos = agenda_eventos()
				# motor = MotorDeEventos(aciona_rastro(), lista_eventos, mvn, programa)
				programa = "loader_blocos.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()
			elif comando == 6:
				lista_eventos = agenda_eventos()
				# motor = MotorDeEventos(aciona_rastro(), lista_eventos, mvn, programa)
				programa = "dumper_bin_comp.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()
			elif comando == 71:
				lista_eventos = agenda_eventos()
				# motor = MotorDeEventos(aciona_rastro(), lista_eventos, mvn, programa)
				programa = "loader_blocos_hex.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()
			elif comando == 72:
				lista_eventos = agenda_eventos()
				# motor = MotorDeEventos(aciona_rastro(), lista_eventos, mvn, programa)
				programa = "dumper_hexa.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()
			elif comando == 8:
				lista_eventos = agenda_eventos()
				# motor = MotorDeEventos(aciona_rastro(), lista_eventos, mvn, programa)
				programa = "loader_hexa.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()
			elif comando == 9:
				# endereco_inicio = input("Digite endereco de inicio (e.g. 0x1234): ")
				# endereco_fim = input("Digite endereco de termino (e.g. 0x1234): ")
				# mvn.imprime_memoria(endereco_inicio, endereco_fim)
				lista_eventos = agenda_eventos()
				# motor = MotorDeEventos(aciona_rastro(), lista_eventos, mvn, programa)
				programa = "visualizador_memoria.txt"
				motor = MotorDeEventos(False, lista_eventos, mvn, programa)
				motor.inicia()
			elif comando == 10:
				comandos = [8, 9]
			elif comando == 100:
				comandos = [0, 1, 11, 12, 2, 3, 4, 5, 6, 71, 72, 8, 9, 10]
			elif comando == 0:
				sair = True

if __name__ == "__main__":
	main()