import sys
import datetime
from string import ascii_letters


TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso à agenda. Um compromisso tem no mínimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração.
def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False
  else:
    novaAtividade = ''

    data = ''
    hora = ''
    prioridade =''
    contexto = ''
    projeto = ''
    descricao = descricao + " "
    
    for x in extras:    #LAÇO PARA PERCORRER A TUPLA E VALIDAR OS ITENS 
      if dataValida(x) == True:
        data = str(x + " ") 
      elif horaValida(x) == True:
        hora = str(x + " ") 
      elif prioridadeValida(x)== True:
        prioridade = str(x + " ") 
      elif contextoValido(x) == True:
        contexto = str(x + " ") 
      elif projetoValido(x) == True:
        projeto = str(x) 

  #CONCATENAÇÃO DOS ITENS DA TUPLA + DESCRIÇÃO 
  novaAtividade = data + hora + prioridade + descricao + contexto + projeto 
  


  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):
  if len(pri) != 3 or not soLetras(pri[1]):
    return False
  elif pri[0] !="(" or pri[2]!=(")"):
      return False
  else:
    return True


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    x = int(horaMin[0]+ horaMin[1])
    y = int(horaMin[2]+ horaMin[3])
    aux = False

    if x >= 0 and x < int(24):
      aux = True
    
    elif  y >= int(0) and y < 60:
      aux = True


    if aux :
      return True

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  if len(data) != 8 or not soDigitos(data):
    return False

  else:
    aux = False
    dia = int(data[0]+data[1])
    mes = int(data[2]+data[3])
    ano = int(data[4:])
    lista31 = [1,3,5,7,8,9,10,12]
    lista30 = [4,6,9,11]
    if ano >= int(2017) and mes <= int(12):
      aux = True
      if mes in lista31 and dia <= int(31):
        aux = True
      elif mes in lista30 and dia <= int(30):
        aux = True
      elif mes == int(2) and dia <= int(29):
        aux = True

    
    
  return aux

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if len(proj) >= int(2) and proj[0]== "+" :
    return True
  else:
    return False

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  if len(cont)>= int(2) and cont[0]== "@":
    return True
  else:
    return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True

def soLetras(letra):
  if type(letra)!= str:
    return False
  for x in letra:
    if letra in ascii_letters:
      aux = True
    else:
      aux = False

  return aux

# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.
lista = []
f = open("todo.txt","r")
for x in f:
  lista.append(x)
f.close()


def organizar(linhas):
  itens = []
  

  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split()# quebra o string em palavras
    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis.
    
    if horaValida(tokens[0]):  # esse é o caso se so existir hora 
      hora = tokens[0]
      tokens.remove(tokens[0])

    elif (dataValida(tokens[0])== False) and horaValida(tokens[1]):
      desc += tokens[0] + " " + tokens[1] + " "
      tokens.remove(tokens[0])
      tokens.remove(tokens[0])
      
      
    for x in tokens:
      if dataValida(x):
        data = x
        tokens.remove(x)
        

    for x in tokens:
      if horaValida(x):
        hora = x
        tokens.remove(x)

    for x in tokens:
      if prioridadeValida(x):
        pri = x
        tokens.remove(x)
    for x in tokens:
      if contextoValido(x):
        contexto = x
        tokens.remove(x)
    for x in tokens:
      if projetoValido(x):
        projeto = x
        tokens.remove(x)
    
    for x in tokens:
      desc += x + " "
      
      
      

    itens.append((desc, (data, hora, pri, contexto, projeto)))
  
  return itens



# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém.


def fazerString(x): #recebe uma tupla 
  data = x[1][0]
  if data != '':
    data = data[0:2]+"/"+data[2:4]+"/"+data[4:] + " " 

  hora = x[1][1]
  if hora != '':
    hora = hora[0:2]+"h"+ hora[2:]+"m" + " "

  prioridade = x[1][2]
  if prioridade != '':
    prioridade +=  " "

  contexto = x[1][3]
  if contexto != '':
    contexto += " "

  projeto = x[1][4] 

  descricao = x[0] + " " 
    

  #CONCATENAÇÃO DOS ITENS DA TUPLA + DESCRIÇÃO 
  return data + hora + prioridade + descricao + contexto + projeto 

def listar(): ### FALTA TERMINAR !!!!
  linhas = []
  f = open("todo.txt","r")
  for cada_linha in f:
    linhas.append(cada_linha)
  f.close()

  lista_tuplas = organizar(linhas)
  aux = ordenarPorPrioridade(ordenarPorDataHora(lista_tuplas)) #tuplas ordenadas

  for x in aux:  #para cada elemento das tuplas ja ordenadas
    i = 0        #disparo o contador que vai ser o numero da linha
    while i < len(lista_tuplas): # laço que percorre todos os elementos da lista de tuplas inicial
      y = lista_tuplas[i]    
      if x == y:                 # se um X na lista de tupla ordenada for == a um Y na tupla inicial
        if x[1][2] == "(A)":          # laços para checar qual a prioridade dos elementos e colorir de acordo
          h = (str(i)+" "+fazerString(x))
          printCores(h,BLUE + BOLD)
        elif x[1][2] == "(B)":
          h = (str(i)+" "+fazerString(x))     #NESSA PARTE DO CÓDIGO EU USO UM VARIAVEL AUXILIAR E UMA FUNÇÃO QUE TRANSFORMA E TUPLA EM UM STRING 
          printCores(h,RED)
        elif x[1][2] == "(C)":
          h = (str(i)+" "+fazerString(x))
          printCores(h,YELLOW)
        elif x[1][2] == "(D)":
          h = (str(i)+" "+fazerString(x))
          printCores(h,GREEN)
        else:
          print(i,fazerString(x))
        
      i += 1
  
  return 


def ordenarPorPrioridade(lista):
  semprioridade = [] #LISTA AUXILIAR
  comprioridade = [] #LISTA AUXILIAR
  for x in lista: #LAÇO PARA TIRAR AS TUPLAS QUE NÃO TEM PRIORIDADE 
    if x[1][2] == '' :   #SE NÃO TIVER PRIORIDADE DA APPEND NA LISTA "semprioridade".
      semprioridade.append(x)
    else:
      comprioridade.append(x)

 
  
  def bubble(lista):
    while True:
      trocado = False
      for i in range(len(lista)- 1):
        if lista[i][1][2] > lista[i + 1][1][2]:
          aux = lista[i]
          lista[i] = lista[i + 1]
          lista[i+ 1] = aux
          trocado = True

      if trocado == False:
            break
    return lista
  
  aux = bubble(comprioridade)
  aux = aux + semprioridade
  return aux


###FUNÇÃO QUE AUXILIA NA FUNÇÃO QUE ORDENA DATAHORA###
def prioridadeIgual(x,y):
  return x[2] and y[2]

###FUNÇÃO QUE AUXILIA NA FUNÇÃO QUE ORDENA DATAHORA###
def dataHoraMaior(x,y):
  data1=''
  data2=''
  if len(x)==8: 
    data1= x[4:8] + x[2:4] +x[:2] #ALTERA A ORDEM PARA (ANO/MES/DIA) 
  elif len(x)==12:
    data1= x[4:8] + x[2:4] +x[:2] +x[8:] #ALTERA A ORDEM PARA (ANO/MES/DIA) + HORA
  if len(y)==8:#se true, tem apenas data
    data2= y[4:8] + y[2:4] +y[:2]
  elif len(y)==12:# se true tem data e hora
    data2= y[4:8] + y[2:4] +y[:2] +y[8:]

  return data1 > data2 


def ordenarPorDataHora(itens): 
  semDataHora = []
  comDataHora = []
  
  for x in itens:
    if x[1][0] == '' and x[1][1] == '' : #se a data e a hora forem vazias 
      semDataHora.append(x)
    else:
      comDataHora.append(x)

  def bubble(lista):
    while True:
      trocado = False
      for i in range(len(lista)- 1):
        x = lista[i][1][0] + lista[i][1][1] 
        y = lista[i + 1][1][0] + lista[i+1][1][1]
        if dataHoraMaior(x,y) and prioridadeIgual(lista[i][1],lista[i+1][1]):
          aux = lista[i]
          lista[i] = lista[i + 1]
          lista[i+ 1] = aux
          trocado = True

      if trocado == False:
        break
    return lista
    
      
  aux = bubble(comDataHora)
  aux = aux + semDataHora
    

  return aux



def fazer(num):
  num = int(num)
  linhas = []
  f = open("todo.txt",'r')    # pega todas as linhas do arquivo e coloca numa lista "linhas"
  for cada_linha in f:
    linhas.append(cada_linha)
  f.close

  if num > len(linhas):   # se a atividade não existir mostra msg de erro 
    raise ValueError("ESSA LINHA É INEXISTENTE NO ARQUIVO.")
  else:
    
    done = []  #lista auxiliar para guardar a atividade feita
    done.append(linhas[num]) # append da atividade feita à lista done
    linhas.remove(linhas[num]) # apaga a atividade feita da lista "linhas" 

    f = open("todo.txt",'w') # REESCREVE NO ARQUIVO TODO A LISTA SEM O ELEMENTO JA FEITO 
    for x in linhas:
      f.write(x)
    f.close

    d = open("done.txt",'a+') #ESCREVE NO ARQUIVO DONE.TXT  
    for y in done:
      d.write(y)
    d.close
  

  return True

def remover(num):
  num = int(num)
  linhas = []
  f = open("todo.txt",'r')  # abre o arquivo e escreve e coloca cada linha dentro de uma lista
  for cada_linha in f:
    linhas.append(cada_linha)
  f.close()

  if num > len(linhas):            # se a atividade for inexistente printa mensagem de erro 
    raise ValueError("ESSA LINHA É INEXISTENTE NO ARQUIVO.")
  else:
    linhas.remove(linhas[num])     #remove a linha da lista

  f = open("todo.txt",'w')  #ESSE TRECHO REESCREVE NO ARQUIVO  A LISTA COM A ATIVIDADE JA REMOVIDA !
  for x in linhas:
    f.write(x)
  f.close()
  

  return True

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 

def priorizar(num, prioridade):
  num = int(num)
  linhas = []
  f = open("todo.txt",'r')
  for cada_linha in f:
    linhas.append(cada_linha)
  f.close()

  if num > len(linhas):             #caso a atividade não exista 
    raise ValueError("ESTA LINHA É INEXISTENTE NO ARQUIVO.")
  else:

    atividade = organizar(linhas)                                         #TRANSFORMA A AS LINHAS EM TUPLAS , POIS FICA MAIS FACIL DE ALTERAR JA QUE TEM POSIÇÃO FIXA
    x = atividade[num]                                                    # PEGA A TUPLA QUE VAI SER REFEITA 
    novatupla = (x[0],(x[1][0],x[1][1],prioridade,x[1][3],x[1][4]))       # UMA NOVA TUPLA COM A NOVA PRIORIDADE 
                 

    data = novatupla[1][0]   ### código para gerar um novo string através da nova tupla 
    if data != '':
      data += " " 

    hora = novatupla[1][1]   ###
    if hora != '':
      hora += " "

    prioridade = novatupla[1][2]  ###
    if prioridade != '':
      prioridade +=  " "

    contexto = novatupla[1][3]  ###
    if contexto != '':
      contexto += " "

    projeto = novatupla[1][4] ###

    descricao = novatupla[0] + " "  ###
    

   
    novoString = data + hora + prioridade + descricao + contexto + projeto   # novo string feito apartir da novatupla

    linhas.remove(linhas[num])  #remove o string desejado da lista de strings
    linhas.insert(num,novoString) # coloca o novo string na lista 

    
    f = open("todo.txt","w")  ## essa parte do código reescreve no arquivo as linhas que estão na lista ja alterada
    for x in linhas:
      f.write(x)
    f.close()


  
  return True



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, prioridade, (data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade

  elif comandos[1] == LISTAR:
    listar()
    return 
    

  elif comandos[1] == REMOVER:
    remover(comandos[2])  
    return   

       

  elif comandos[1] == FAZER:
    fazer(comandos[2])
    
    return    

    #########

  elif comandos[1] == PRIORIZAR:
    priorizar(comandos[2],comandos[3])
    return 

    ########

  else :
    print("Comando inválido.")
    


# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)

