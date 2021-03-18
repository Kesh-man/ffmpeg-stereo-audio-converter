# -*- coding: utf-8 -*-

'''-------------------------------

----ffmpeg-stereo-audio-encoder-beta-version-0.0.5----

->functions:
    -str_rename
    -str_fix
    -str_cmp
    -file_remove
    -find_file
    -while "for encoder of the files"

-------------------------------'''

import os
import glob
import re

'''
criação do arquivo "feitos.txt" onde será salvo todos os arquivos
já concluidos pelo ffmpeg
'''
arquivo = open("feitos.txt", 'a+')
arquivo.close()

'''
a função str_rename() vai renomear os arquivos feitos pelo ffmpeg.
todos arquivos de saída recebem a extensão "-new" para se diferenciar,
a função rename vai remover esse termo para que permaneça com o mesmo
nome do arquivo de origem
'''
def str_rename():
    path = "."
    dir = os.listdir(path)
    for file in dir:
        if re.search('\\bnew\\b', file, re.IGNORECASE):
            oldname = file
            new_name = file.replace("-new.mp4","")
            new_name = new_name+".mp4"
            os.rename('./'+oldname, './'+new_name)

'''
a função str_fix(aux) serve para remover o parâmetro de quebra de linha "\n"
das strings que serão lidas do arquivo "feitos.txt" para extrair somente
o nome dos arquivos e nada mais
'''
def str_fix(aux):
    new = []
    for aux in aux:
        aux = aux.rstrip(' \n')
        new.append(aux)

    return new

'''
a função str_cmp(name) vai verificar se o nome do arquvio que
é passado como parâmetro contém a extensão "new" e retorn 1 caso contenha
ou 0 caso não contenha
'''
def str_cmp(name):
    if re.search('\\bnew\\b', name, re.IGNORECASE):
        return 1
    else:    
        return 0

'''
a função file_remove(fil2) é responsável por remover o arquivo 
já convertido do diretório
'''
def file_remove(fil2):
    path = "."
    fil2 = fil2+".mp4"
    dir = os.listdir(path)
    for file in dir:
        if file == fil2:
            os.remove(fil2)

'''
a função find_file(file) vai fazer uma busca no arquivo "feitos.txt" 
pelo parâmetro passado, caso contenha será retornado 1 caso naõ contenha
será retornado 0
'''
def find_file(file):
    dados = open("feitos.txt", 'r')
    aux = dados.readlines()
    aux = str_fix(aux)
    for lines in aux:
        if lines == file:
            return 1
            dados.close()
        else:
            continue

    dados.close()
    return 0

#definição do loop da quantidade de arquivos que serão trabalhados


#lista com arquivos presentes no diretório
files = []
'''
FOR responsável por listar todso os arquivos com extensão ".mp4" 
e adicionar eles a lista "files" removendo a extensão, ficando
somente o nome do arquivo
'''
for f in glob.glob("*.mp4*"):
    files.append((f.replace(".mp4","")))

loop = len(files)

#while responsável por efetuar o processo principal do script
i = 0
while i<loop :

    #coletar para a varíavel aux o nome do arquivo a ser trabalhado
    aux = files[i]

    #verificação se o arquvo já foi utilizado ou não
    if find_file(aux) == 1:
        loop+=1
        i+=1
    else:
        
        '''
        OS.SYSTEM vai executar a linha de código responsável pelo 
        processo dos arquivos        
        '''
        os.system("ffmpeg -n -i {}.mp4 -c:v copy -ac 2 -af \"pan=stereo|FL=FC+0.70*FL+0.70*BL|FR=FC+0.70*FR+0.70*BR\" {}-new.mp4".format(files[i],files[i]))
        
        '''
        if responsável por remover o arquivo de origem e renomear
        o novo que foi gerado, logo após guardar essa informação
        no arquvio "feitos.txt" para que seja passado como parâmetro
        de "ARQUIVO JÀ FEITO"
        '''
        if str_cmp(aux) == 0:
            file_remove(aux)
            str_rename()
            dados = open("feitos.txt", 'a')
            dados.write(aux+" \n")
            dados.close()
            i+=1
        else:
            continue