# -*- coding: utf-8 -*-
# @Author: muril
# @Date:   2020-11-03 08:47:36
# @Last Modified by:   muril
# @Last Modified time: 2021-11-10 15:11:51

import sys

class strsad:
    def __init__(self):
        self.sad = 0
        self.bestDist = 0
        self.vec_x = 0
        self.vec_y = 0

class parameters:
    def __init__(self):
        #char stats_path[100]; #*< path do arquivo de resultados */
        #char video_path[100]; #*< path do video de entrada */
        video_name = ""  #*< nome do video de entrada */
        #framenum; #*< numero de quadros a codificar */
        #videonum;
        w = 0  #*< largura do video */
        h = 0;  #*< altura do video */

def getLumaFrame(yuv_file, parm):
    tempFrame = [[0 for i in range(0, parm.w)] for i in range(0, parm.h)]

    try:
        for i in range(0,parm.h):
            for j in range(0,parm.w):
                tempFrame[i][j] = ord(yuv_file.read(1))
    except:
        print("Nao foi possivel ler corretamente o video! Verifique a resolucao\n")
        sys.exit(2)
    
    yuv_file.seek(int((parm.w * parm.h) / 2), 1)
    return tempFrame
    
def setLumaFrame(luma_frame, yuv_file, parm):
    for i in range(0,parm.h):
        for j in range(0,parm.w):
            yuv_file.write(luma_frame[i][j].to_bytes(1, byteorder='big', signed=False))
