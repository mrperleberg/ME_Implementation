# -*- coding: utf-8 -*-
# @Author: muril
# @Date:   2020-11-03 08:47:36
# @Last Modified by:   Murilo
# @Last Modified time: 2024-02-06 15:20:36

import sys

def pegaBloco(frame, i, j, parm, tamBloco):
    bloco = [[0 for i in range(0, tamBloco)] for i in range(0, tamBloco)]
    for m in range(0,tamBloco):
        for n in range(0,tamBloco):
            try:
                bloco[m][n] = frame[i+m][j+n]
            except:
                print("erro ao pegarBloco da posicao", i, j, m, n, i+m, j+n)
    return bloco

def pegaArea(frame, i, j, parm, tamBloco, rangeArea):
    areaDeBusca = [[0 for i in range(0, 2*rangeArea+tamBloco)] for i in range(0, 2*rangeArea+tamBloco)]
    for m in range(-rangeArea,rangeArea+tamBloco):
        for n in range(-rangeArea,rangeArea+tamBloco):
            if     ((0<=(i+m)) and ((i+m)<parm.h)):
                if ((0<=(j+n)) and ((j+n)<parm.w)):
                    areaDeBusca[rangeArea+m][rangeArea+n] = frame[i+m][j+n]
    return areaDeBusca

def xTZSearchHelp(blocoAtual, areaDeBusca, i, j, k, m, bestResult, parm, tamBloco, rangeArea):
    #i, j: posicao do bloco no frame
    #k, m: vetor do bloco referencia
    
    s = 0
    posX = rangeArea+k;
    posY = rangeArea+m;
    #testa se existem amostras dentro da area de busca
    if ((-rangeArea <= k) and (k <= rangeArea) and (-rangeArea <= m) and (m <= rangeArea)):
        #testa se bloco esta dentro do quadro
        if ((0 <= (i+posX)) and ((i+posX) < parm.h)):
            if ((0 <= (j+posY)) and ((j+posY) < parm.w)):
                #compara o bloco atual com o bloco referencia (k,m)
                s = fnSAD(posX, posY, blocoAtual, areaDeBusca, tamBloco)
                #testa SAD obtido
                if (s < bestResult.sad):
                    bestResult.sad = s
                    bestResult.vec_x = k
                    bestResult.vec_y = m
    return bestResult

def fnSAD(linhaBloco, colunaBloco, curr_frame, ref_frame, tamBloco):
    temp = 0
    for i in range(0, tamBloco):
        for j in range(0, tamBloco):
            #print(i, j, linhaBloco+i, colunaBloco+j, len(ref_frame))
            try:
                cur = curr_frame[i][j]
                ref = ref_frame[linhaBloco+i][colunaBloco+j]
            except:
                print(i, j, linhaBloco+i, colunaBloco+j, len(ref_frame), len(ref_frame[0]))
                sys.exit()
            temp += abs(cur - ref)
    return temp

def reconstroi(rec_frame, ref_frame, i, j, parm, bestResult, tamBloco):
    for a in range(i, i+tamBloco):
        for b in range(j, j+tamBloco):
            rec_frame[a][b] = ref_frame[a+bestResult.vec_x][b+bestResult.vec_y]

    return rec_frame

def geraResiduo(res_frame, curr_frame, ref_frame, i, j, bestResult, parm, tamBloco):
    for a in range(i, i+tamBloco):
        for b in range(j, j+tamBloco):
            difference = curr_frame[a][b] - ref_frame[a+bestResult.vec_x][b+bestResult.vec_y]
            
            if (difference < 0):
                difference = - difference

            if (255 < (difference)):
                res_frame[a][b] = 255
            else:
                res_frame[a][b] = (difference)
    return res_frame
            