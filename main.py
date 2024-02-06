# -*- coding: utf-8 -*-
# @Author: muril
# @Date:   2020-11-03 08:47:36
# @Last Modified by:   Murilo
# @Last Modified time: 2024-02-06 15:57:57

#/**
# * [video_name] = caminho para o video de entrada;
# * [w] = largura do video;
# * [h] = altura do video;
# */

import sys
from time import process_time

import defs, common, BMA

parallelProcessing = False
if parallelProcessing:
	from multiprocessing import Manager, Process

rangeArea = 64 # TAMANHO DA ÁREA DE BUSCA - A AREA SERA QUADRATICA
tamBloco = 64 # TAMANHO DO BLOCO - O BLOCO SERA QUADRATICO
iRaster = 5 # tamanho do raster

def main():
	#Le parametros
	if (len(sys.argv[1:]) != 4):
		print("-> Parametros errados!\n :: videoPath w h frames\n")
		sys.exit(1)
	parm = defs.parameters()
	parm.video_name = sys.argv[1]
	parm.w = int(sys.argv[2])
	parm.h = int(sys.argv[3])
	framesToProcess = int(sys.argv[4])

	#Aloca memoria
	try:
		video_in = open(parm.video_name, "rb")
		residue_out = open("residue.yuv", "wb")
		reconst_out = open("reconst.yuv", "wb")
	except OSError:
		print("Erro em um dos arquivos", parm.video_name)
		sys.exit()

	#pega primeiro frame
	curr_frame = defs.getLumaFrame(video_in, parm) #curr_frame contem o frame de luminancia atual
	
	if parallelProcessing:
		#variaveis pra multiprocessing
		manager = Manager()

	for frameNum in range(0, framesToProcess):
		ref_frame = curr_frame.copy()	
		curr_frame = defs.getLumaFrame(video_in, parm) #ref_frame contem o frame de luminancia da referencia

		res_frame    = [[0 for i in range(0, parm.w)] for i in range(0, parm.h)] #alocação para o quadro de residuos
		rec_frame    = [[0 for i in range(0, parm.w)] for i in range(0, parm.h)] #alocação para o quadro de residuos

	#Percorre frame, bloco a bloco, obtendo os vetores/SADs
		if parallelProcessing: ###PARALELIZA O PROCESSAMENTO DE CADA LINHA:
			return_dict = parallelMotionEstimation(manager, curr_frame, ref_frame, parm)
		else: ###EXECUTA SEQUENCIALMENTE:
			return_dict = sequentialMotionEstimation(curr_frame, ref_frame, parm)

	#reconstroi utilizando os vetores
		for rowIdx in range(0, parm.h-tamBloco+1, tamBloco):		#LINHA
			for colIdx in range(0, parm.w-tamBloco+1, tamBloco):	#COLUNA
				#Pega resultado da ME anterior
				bestResult = return_dict[int(rowIdx/tamBloco)][int(colIdx/tamBloco)]
				
				#Reconstroi o quadro atual utilizando apenas o quadro de referencia e o vetor obtido
				common.reconstroi(rec_frame, ref_frame, rowIdx, colIdx, parm, bestResult, tamBloco)
				
				#Gera o residuo
				common.geraResiduo(res_frame, curr_frame, ref_frame, rowIdx, colIdx, bestResult, parm, tamBloco)

				#Printa informacoes do vetor
				print("Frame " + str(frameNum) + " : Bloco [" + str(colIdx).rjust(4) + " , " + str(rowIdx).rjust(4) + "] = ", end="")
				print("(" + str(bestResult.vec_y).rjust(3) + "," + str(bestResult.vec_x).rjust(3) + "), SAD= ", bestResult.sad)

	#Salva frames
		defs.setLumaFrame(rec_frame, reconst_out, parm) #salva o quadro reconstruido
		defs.setLumaFrame(res_frame, residue_out, parm) #salva o quadro de residuo

def sequentialMotionEstimation(curr_frame, ref_frame, parm):
	return_dict = []
	for rowIdx in range(0, parm.h-tamBloco+1, tamBloco):
		arrayReturn = []
		for colIdx in range(0, parm.w-tamBloco+1, tamBloco):
			bestResult = motionEstimation(rowIdx, colIdx, curr_frame, ref_frame, parm)
			arrayReturn.append(bestResult)
		return_dict.append(arrayReturn)
	return return_dict

def parallelMotionEstimation(manager, curr_frame, ref_frame, parm):
	return_dict = manager.dict()
	jobs = []
	for rowIdx in range(0, parm.h-tamBloco+1, tamBloco):		#UMA LINHA POR THREAD
		p = Process(target=motionEstimationOfRow, args=(rowIdx, curr_frame, ref_frame, parm, return_dict))
		jobs.append(p)
		p.start()
	for proc in jobs:
		proc.join()
	return return_dict.values()

def motionEstimationOfRow(rowIdx, curr_frame, ref_frame, parm, return_dict):
	arrayReturn = []
	for colIdx in range(0, parm.w-tamBloco+1, tamBloco):
		bestResult = motionEstimation(rowIdx, colIdx, curr_frame, ref_frame, parm)

		arrayReturn.append(bestResult)
		return_dict[rowIdx] = arrayReturn

def motionEstimation(rowIdx, colIdx, curr_frame, ref_frame, parm):
	#cria uma copia das amostras do bloco atual e da area de busca
	blocoAtual = common.pegaBloco(curr_frame, rowIdx, colIdx, parm, tamBloco)
	areaDeBusca = common.pegaArea(ref_frame, rowIdx, colIdx, parm, tamBloco, rangeArea)

	#realiza o Full Search ou o TZS utilizando apenas as amostras retiradas anteriormente.
	#retorno é o MV e o SAD do candidato com menor SAD
	bestResult = BMA.TZSearch(blocoAtual, areaDeBusca, rowIdx, colIdx, parm, iRaster, tamBloco, rangeArea)
	#bestResult = BMA.fullSearch2(blocoAtual, areaDeBusca, rowIdx, colIdx, parm, tamBloco, rangeArea)
	
	return bestResult





if __name__ == '__main__':
	t1 = process_time()
	print("iniciando, t1=", t1)
	main()
	t2 = process_time()
	print("Fim, t2=", t2 - t1)
