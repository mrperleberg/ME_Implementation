# -*- coding: utf-8 -*-
# @Author: muril
# @Date:   2020-11-03 08:47:36
# @Last Modified by:   Murilo
# @Last Modified time: 2024-02-06 15:19:47

import defs, common

def fullSearch(blocoAtual, areaDeBusca, i, j, parm, tamBloco, rangeArea):
    bestResult = defs.strsad()
    bestResult.sad = 9999999
    s = 0
    for k in range(0, (3*rangeArea)-tamBloco+1):
        for m in range(0, (3*rangeArea)-tamBloco+1):
            if ((0 <= (i-rangeArea+k)) and ((i-rangeArea+k) < parm.h+1)):
                if ((0 <= (j-rangeArea+m)) and ((j-rangeArea+m) < parm.w+1)):
                    #compara o bloco atual com o bloco referencia (k,m)
                    s = fnSAD(k, m, blocoAtual, areaDeBusca)
                        
                    if (s < bestResult.sad):
                        bestResult.sad = s
                        bestResult.vec_x = k - rangeArea
                        bestResult.vec_y = m - rangeArea

    return bestResult

def fullSearch2(blocoAtual, areaDeBusca, i, j, parm, tamBloco, rangeArea):
    bestResult = defs.strsad()
    bestResult.sad = 9999999

    #Raster
    for iStartX in range(-rangeArea, rangeArea):
        for iStartY in range(-rangeArea, rangeArea):
            bestResult = common.xTZSearchHelp(blocoAtual, areaDeBusca, i, j, iStartX, iStartY, bestResult, parm, tamBloco, rangeArea)

    return bestResult


def TZSearch(blocoAtual, areaDeBusca, i, j, parm, iRaster, tamBloco, rangeArea):
    bestResult = defs.strsad()
    bestResult.sad = 9999999

    rangeExp = []
    exp = 0
    while ((2**exp) <= rangeArea):
        rangeExp.append(2**exp)
        exp+=1

    #Predicao
    bestResult = common.xTZSearchHelp(blocoAtual, areaDeBusca, i, j, 0, 0, bestResult, parm, tamBloco, rangeArea)

    #Busca Inicial
    for iDist in rangeExp:
        bestResult = xTZ8PointDiamondSearch (blocoAtual, areaDeBusca, i, j, 0, 0, iDist, bestResult, parm, tamBloco, rangeArea)
    #   if ( bFirstSearchStop && ( cStruct.uiBestRound >= uiFirstSearchRounds ) ) // stop criterion
    #       break;

    #Raster
    bestX = bestResult.vec_x
    bestY = bestResult.vec_y
    
    if ((bestX > iRaster) or (bestY > iRaster) or (-bestX > iRaster) or (-bestY > iRaster)):
        Top = -int(rangeArea/2)
        Bottom = int(rangeArea/2)
        Left = -int(rangeArea/2)
        Right = int(rangeArea/2)
        for iStartY in range(Top, Bottom, iRaster):
            for iStartX in range(Left, Right, iRaster):
                bestResult = common.xTZSearchHelp(blocoAtual, areaDeBusca, i, j, iStartX, iStartY, bestResult, parm, tamBloco, rangeArea)

    #Refinamento    
    bestX = bestResult.vec_x
    bestY = bestResult.vec_y
    refinamentos=0
    if ((bestX != 0) or (bestY != 0)):
        while ((bestResult.vec_x == bestX) and (bestResult.vec_y == bestY)):
            for iDist in rangeExp:
                bestResult = xTZ8PointDiamondSearch (blocoAtual, areaDeBusca, i, j, bestX, bestY, iDist, bestResult, parm, tamBloco, rangeArea);

                if  (((4 <= iDist) and (bestResult.bestDist == 0)) or #(3 EXPANSOES SEM MELHOR RESULTADO:)
                    ((8 <= iDist) and (bestResult.bestDist <= 1)) or
                    ((16 <= iDist) and (bestResult.bestDist <= 2)) or
                    ((32 <= iDist) and (bestResult.bestDist <= 4))):
                    break
                    #TESTAR iDist com iDist do bestSAD atual

            if (((bestResult.vec_x == bestX) and (bestResult.vec_y == bestY)) or (refinamentos == 7)):
                break
            else:
                bestX = bestResult.vec_x;
                bestY = bestResult.vec_y;
                refinamentos += 1

    return bestResult

def xTZ8PointDiamondSearch(blocoAtual, areaDeBusca, i, j, centroX, centroY, iDist, bestResult, parm, tamBloco, rangeArea):
    bestInterno = defs.strsad()
    bestInterno.sad = bestResult.sad
    bestInterno.bestDist = iDist
    #print(iDist)
    if ( iDist == 1 ):
        #bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, centroX-iDist, centroY-iDist, bestInterno, parm, tamBloco, rangeArea)
        bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, centroX-iDist, centroY      , bestInterno, parm, tamBloco, rangeArea)
        #bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, centroX-iDist, centroY+iDist, bestInterno, parm, tamBloco, rangeArea)
        bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, centroX      , centroY-iDist, bestInterno, parm, tamBloco, rangeArea)
        bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, centroX      , centroY+iDist, bestInterno, parm, tamBloco, rangeArea)
        #bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, centroX+iDist, centroY-iDist, bestInterno, parm, tamBloco, rangeArea)
        bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, centroX+iDist, centroY      , bestInterno, parm, tamBloco, rangeArea)
        #bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, centroX+iDist, centroY+iDist, bestInterno, parm, tamBloco, rangeArea)
    else:
        iTop        = centroY - iDist
        iBottom     = centroY + iDist
        iLeft       = centroX - iDist
        iRight      = centroX + iDist
        if ( iDist <= 8 ):
            iTop_2     = centroY - (iDist>>1)
            iBottom_2  = centroY + (iDist>>1)
            iLeft_2    = centroX - (iDist>>1)
            iRight_2   = centroX + (iDist>>1)
            bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, centroX,  iTop,      bestInterno, parm, tamBloco, rangeArea)
            bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, iLeft,    centroY,   bestInterno, parm, tamBloco, rangeArea)
            bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, iRight,   centroY,   bestInterno, parm, tamBloco, rangeArea)
            bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, centroX,  iBottom,   bestInterno, parm, tamBloco, rangeArea)
            #if (iDist > 2):
            bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, iLeft_2,  iTop_2,    bestInterno, parm, tamBloco, rangeArea)
            bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, iRight_2, iTop_2,    bestInterno, parm, tamBloco, rangeArea)
            bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, iLeft_2,  iBottom_2, bestInterno, parm, tamBloco, rangeArea)
            bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, iRight_2, iBottom_2, bestInterno, parm, tamBloco, rangeArea)
        else: # iDist > 8
            bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, centroX, iTop,    bestInterno, parm, tamBloco, rangeArea)
            bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, iLeft,   centroY, bestInterno, parm, tamBloco, rangeArea)
            bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, iRight,  centroY, bestInterno, parm, tamBloco, rangeArea)
            bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, centroX, iBottom, bestInterno, parm, tamBloco, rangeArea)
            for index in range(1,4):
                iPosYT     = iTop    + ((iDist>>2) * index);
                iPosYB     = iBottom - ((iDist>>2) * index);
                iPosXL     = centroX - ((iDist>>2) * index);
                iPosXR     = centroX + ((iDist>>2) * index);
                bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, iPosXL, iPosYT, bestInterno, parm, tamBloco, rangeArea)
                bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, iPosXR, iPosYT, bestInterno, parm, tamBloco, rangeArea)
                bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, iPosXL, iPosYB, bestInterno, parm, tamBloco, rangeArea)
                bestInterno = common.xTZSearchHelp( blocoAtual, areaDeBusca, i, j, iPosXR, iPosYB, bestInterno, parm, tamBloco, rangeArea)

    if (bestInterno.sad < bestResult.sad):
        return bestInterno
    else:
        return bestResult
