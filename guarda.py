import sys
import os
import getopt
import hmac
import hashlib
import base64

def gerarHmac(arquivo, key):# Gera o Hmac de um arquivo
    text = arquivo.read()
    b = str.encode(key)
    h = hmac.new( b, text, hashlib.sha256)
    return h.hexdigest()

def gerarHash(arquivo): # Gera a Hash de um arquivo
    sha256 = hashlib.sha256()
    while True:
        data = arquivo.read(65534)
        if not data:
            break
        sha256.update(data)
    return sha256.hexdigest()

def verificarPasta(pasta): # Função que verifica se a string passada é um diretório ou não
    if os.path.isdir(pasta):
        return 0
    return -1

def Dir(pasta): #Gera os diretórios que estão dentro do diretório passado
    files = []
    for r, d, f in os.walk(pasta):
        for file in d:
            files.append(os.path.join(r, file))
    return files

def Arq(pasta): #Gera os arquivos que estão dentro do diretório passado
    files = []
    for r, d, f in os.walk(pasta):
        for file in f:
            files.append(os.path.join(r, file)) 
    return files

def dicioAntigo(pasta): # Monta um dicionário 'arquivo':'hash' a partir do arquivo ".guarda"
    dicio = {}
    dados = open(pasta+"/"+".guarda","r")
    l = dados.readlines()
    for linha in l: # Montando o dicionário
        data = linha.split(" > ") # Símbolo que separa o nome do arquivo da sua hash"
        dicio[data[0]] = data[1][:len(data[1])-2] 
    return dicio

def dicioAtual(pasta,metodo,key): #Função que cria o dicionário da pasta atual com todas as alterações
    dicio = {}
    dr = Dir(pasta)
    for x in dr:
        files = Arq(x)
        for f in files:
            arq_aberto = open(f,"rb")
            if metodo == "hash":
                hash_arq = gerarHash(arq_aberto)
            if metodo == "hmac":
                hash_arq = gerarHmac(arq_aberto,key)
            arq_aberto.close()
            dicio[f] = hash_arq #Salvando no dicionário o nome do arquivo como a chave (f), e seu hash correspondente
    files = Arq(pasta)
    for f in files:
        arq_aberto = open(f,"rb")
        if metodo == "hash":
            hash_arq = gerarHash(arq_aberto)
        if metodo == "hmac":
            hash_arq = gerarHmac(arq_aberto,key)
        arq_aberto.close()
        dicio[f] = hash_arq[:len(hash_arq)-1]

    return dicio

def i(pasta,saida, metodo, key): #inicia a guarda da pasta
    if saida != "Default":
        arq_saida = open(saida, "w")
    dr = Dir(pasta)
    cond = 0
    for x in dr:
        files = Arq(x)
        for j in files:
            if j == x+"/"+".guarda":
                cond = 1
                print("já estava guardado->  " + x)
        if cond == 0:
            arq_oculto = open(x+"/"+".guarda", "w")
            for f in files:
                arq_aberto = open(f,"rb")
                if metodo == "hash":
                    hash_arq = gerarHash(arq_aberto)
                if metodo == "hmac":
                    hash_arq = gerarHmac(arq_aberto,key)
                arq_aberto.close()
                arq_oculto.write(f+" > "+hash_arq+"\n")
            arq_oculto.close()
        cond = 0
    files = Arq(pasta)
    cond = 0
    for j in files:
            if j == pasta+"/"+".guarda":
                cond = 1
                print("já estava guardado->  " + pasta)
    if cond == 0:
        arq_oculto = open(pasta+"/"+".guarda", "w")
        for f in files:
            arq_aberto = open(f,"rb")
            if metodo == "hash":
                hash_arq = gerarHash(arq_aberto)
            if metodo == "hmac":
                hash_arq = gerarHmac(arq_aberto,key)
            arq_aberto.close()
            if saida != "Default":
                arq_saida.write(f+" > "+hash_arq+"\n")
            arq_oculto.write(f+" > "+hash_arq+"\n")
        if saida != "Default":
            arq_saida.close()
        arq_oculto.close()

def t(pasta,saida,metodo,key): #verifica alterações da pasta
    if saida != "Default":
        arq_saida = open(saida, "w")
    files = Arq(pasta)
    cond = 0
    for j in files:
        if j == pasta+"/"+".guarda":
            cond = 1
    if cond == 1:
        d1 = dicioAntigo(pasta)
        d2 = dicioAtual(pasta,metodo,key)
        alterado = []
        excluido = []
        inalterado = []
        adicionado = []
        for d in d1:
            if d not in d2:     # Foi excluido
                excluido.append(d)
            if d in d2 and d2[d] != d1[d] and d != pasta+"/"+".guarda":     #Foi alterado
                alterado.append(d)
            elif d in d2 and d2[d] == d1[d]:      #Continua o mesmo
                inalterado.append(d)
        for d in d2:
            if d not in d1 and d != pasta+"/"+".guarda":
                adicionado.append(d)
        if(saida != "Default"):
            arq_saida.write("Excluídos: \n")
            for x in excluido:
                arq_saida.write(x)
            arq_saida.write("\nAlterados: \n")
            for x in alterado:
                arq_saida.write(x)
            arq_saida.write("\nInalterados: \n")
            for x in inalterado:
                arq_saida.write(x)
            arq_saida.write("\nAdicionados: \n")
            for x in adicionado:
                arq_saida.write(x)
        else:
            print("Excluídos: \n")
            print(excluido)
            print("\nAlterados: \n")
            print(alterado)
            print("\nInalterados: \n")
            print(inalterado)
            print("\nAdicionados: \n")
            print(adicionado)
    else:
        print("A pasta não é guardada")


def x(pasta): #retira a guarda, ou seja exclui o arquivo .guarda
    dr = Dir(pasta)
    cond = 0
    for x in dr:
        files = Arq(x)
        for j in files:
            if j == x+"/"+".guarda":
                cond = 1
                os.remove(j)
                print("removido a guarda->  " + x)
        if cond == 0:
            print("A pasta já não estava sendo guardada->   " + x)
        cond = 0
    files = Arq(pasta)
    cond = 0
    for j in files:
        if j == pasta+"/"+".guarda":
            cond = 1
            os.remove(j)
            print("removido a guarda->  " + x)
    if cond == 0:
        print("A pasta já não estava sendo guardada->   " + x)

args = sys.argv[1:]
try:
    optlist,arguments= getopt.gnu_getopt(args,'i:t:x:o:',['hash','hmac='])
except:
    print("Erro de parâmetros!")
    print("Exit")
saida = ""
metodo = ""
pasta = ""
opcao = ""
senha = ""

for j in optlist:
    if (j[0]=="--hmac"):
        metodo = "hmac"
        senha = j[1]
    if (j[0]=="--hash"):
        metodo = "hash"
    if (j[0]=="-t"):
        opcao = "t"
        pasta = j[1]
    if (j[0]=="-i"):
        pasta = j[1]
        opcao = "i"
    if (j[0]=="-x"):
        opcao = "x"
        pasta = j[1]
    if (j[0]== "-o"):
        saida = j[1]
    elif saida == "":
        saida = "Default"
    elif senha == "":
        senha = "Default"

# Verificando as entradas dos usuários
if verificarPasta(pasta):
    print("Parâmetro <pasta> inválido!")
    print("Exit")
    sys.exit(-1)

print("********** Tabela de Configuração **********")
print("Método: " +  metodo)
if metodo == "hmac":
    print("Senha: " + senha)
print("Opção: " + opcao)
print("Pasta: " + pasta)
print("Arquivo de saída: " + saida)
print("********************************************")
if opcao == "i":
    i(pasta, saida, metodo, senha)
if opcao == "t":
    t(pasta, saida, metodo, senha)
if opcao == "x":
    x(pasta)