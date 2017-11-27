# -*- coding: utf-8 -*-

from motor_montador import *
from montador import *
from motor_ligador import *
from ligador import *
from minHeap import *
	
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

def agenda_eventos_montador():
	lista_eventos = MinHeap()
	horario = 0
	lista_eventos.append([horario, "PASSO_UM"])
	horario += 1
	lista_eventos.append([horario, "DETECCAO_ERROS"])
	horario += 1
	lista_eventos.append([horario, "GERACAO_REFERENCIAS_CRUZADAS"])
	horario += 1
	lista_eventos.append([horario, "PASSO_DOIS"])
	return lista_eventos

def agenda_eventos_ligador():
	lista_eventos = MinHeap()
	horario = 0
	lista_eventos.append([horario, "PASSO_UM"])
	horario += 1
	lista_eventos.append([horario, "PASSO_DOIS"])
	return lista_eventos

def main():
	codigo_montado = "montado.txt"
	referencias_cruzadas = []
	montador = Montador()

	mais_modulos = true
	while mais_modulos:
		lista_eventos = agenda_eventos_montador()
		# codigo_mnemonico = "mnemonico.txt"
		codigo_mnemonico = input("Digite o nome do arquivo que contém o programa em linguagem mnemônica: ")
		motor = MotorDeEventosMontador(aciona_rastro(), lista_eventos, codigo_montado, codigo_mnemonico) # TODO arrumar parametros
		# motor = MotorDeEventosMontador(False, montador, lista_eventos, codigo_montado, codigo_mnemonico) # TODO arrumar parametros
		motor.inicia()

	ok = montador.verifica_referencias_cruzadas()
	if !ok:
		print("Houve erro nas referências cruzadas, e código não pode ser gerado")
		return
	
	ligador = Ligador('0x0100', montador.referencias_cruzadas)
	lista_eventos = agenda_eventos_ligador()
	# codigo_final = "final.txt"
	codigo_final = input("Digite o nome do arquivo no qual deseja que o código final seja colocado: ")
	motor = MotorDeEventosLigador(aciona_rastro(), lista_eventos, codigo_final, codigo_montado, referencias_cruzadas, base_relocacao) # TODO arrumar parametros
	# motor = MotorDeEventosLigador(False, ligador, lista_eventos, codigo_final, codigo_montado, referencias_cruzadas, base_relocacao) # TODO arrumar parametros
	motor.inicia()

if __name__ == "__main__":
	main()