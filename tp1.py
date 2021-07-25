import re
import os
from prettytable import PrettyTable


def parse_file():

    f = open("inscritos-form.json", encoding="utf-8")

    atleta = {}
    
    for line in f:

        if e := re.search(r'"nome":"(.*)"', line):
            atleta["nome"] = e.group(1)

        elif e := re.search(r'"dataNasc":"(.*)"', line):
            atleta["dataNasc"] = e.group(1)

        elif e := re.search(r'"morada":"(.*)"', line):
            atleta["morada"] = e.group(1)

        elif e := re.search(r'"email":"(.*)"', line):
            atleta["email"] = e.group(1)

        elif e := re.search(r'"prova":"(.*)"', line):
            atleta["prova"] = e.group(1)

        elif e := re.search(r'"escalao":"(.*)"', line):
            atleta["escalao"] = e.group(1)

        elif e := re.search(r'"equipa":"(.*)"', line):
            equipa = e.group(1)

            if re.search(r'(?i:ind)|^,$|s/ clube|^n/d$|^na$', equipa) :
                equipa = 'Individual'
            
            elif re.search(r'(?i:cães)', equipa) :
                equipa = 'Cães da Avenida'

            elif re.search(r'(?i:ponte de lima)', equipa) :
                equipa = 'Clube Náutico de Ponte de Lima'
            
            elif re.search(r'(?i:caga tacos)', equipa) :
                equipa = 'Os Caga Tacos Running Team'

            elif re.search(r'(?i:turb)', equipa) :
                equipa = 'Os Turbulentos'
            
            elif re.search(r'(?i:edv)', equipa) :
                equipa = 'EDV - Viana Trail'

            atleta["equipa"] = equipa

        elif re.search(r'}[^{]', line):
            if atleta not in inscritos:
                inscritos.append(atleta.copy())

    f.close()

def a():

    print("Atletas individuais de Valongo:\n")

    for atleta in inscritos:

        equipa = atleta.get("equipa") #apanhar os indivudual
        morada = atleta.get("morada")

        individual = re.search(r'Individual', equipa)
        valongo = re.search(r'(?i:Valongo)', morada)

        if individual and valongo:
            print(atleta.get("nome").upper())

def b():
    table = PrettyTable()
    table.field_names = ["Nome", "Email", "Prova"]

    for atleta in inscritos:

        nome = atleta.get("nome")
        email = atleta.get("email")

        nome1 = re.search(r'(?i:Paulo)|(?i:Ricardo)', nome)
        gmail = re.search(r'gmail', email) 

        if(nome1 and gmail):
            table.add_row([nome, email, atleta.get("prova")])
    
    print(table)

def c():

    table = PrettyTable()
    table.field_names = ["Nome", "Nascimento", "Morada", "Email", "Prova", "Escalão"]

    for atleta in inscritos:

        equipa = atleta.get("equipa")
        
        turbulentos = re.search(r'Os Turbulentos', equipa)

        if turbulentos:
            table.add_row([atleta.get("nome"), atleta.get("dataNasc"), atleta.get("morada"), atleta.get("email"), atleta.get("prova"), atleta.get("escalao")])

    print("Equipa TURBULENTOS:")
    print(table)

def d():

    escaloes = {} 

    for atleta in inscritos:

        escalao = atleta.get("escalao")

        if escalao == '':
            escalao = 'Indefinido'

        if escalao in escaloes.keys():
            escaloes[escalao] += 1
        else:
            escaloes[escalao] = 1 

    escaloes = dict(sorted(escaloes.items(), key=lambda p: p[0]))

    print('ESCALÕES')

    for escalao in escaloes.keys():

        print(escalao + ': ' + str(escaloes[escalao]) + ' atletas inscritos')

def e():

    equipas = {} 
    path = 'webfiles\\'

    if not os.path.exists(path):
        os.makedirs(path)

    for atleta in inscritos:
        eq = atleta.get("equipa").upper()

        if eq in equipas.keys():
            equipas[eq] += 1
        else:
            equipas[eq] = 1 


    equipas = dict(sorted(equipas.items(),key=lambda p: (p[1],p[0]), reverse=True))

    html_file = os.path.join(path, 'equipas.html')
    html = open(html_file,"w")

    html.write("<!DOCTYPE html><br><html>")
    html.write("\n		<h2> Lista de equipas </h2><hr>")
    html.write("\n			<body>")
    html.write("\n				<ul>")

    for equipa in equipas: #adicionar as equipas, criar links de cada equipa
        #chave = equipa.key() #nome da equipa
        equipaParsed = re.sub(r'[^(\w\d)]', r'_', equipa)

        valor = equipas.get(equipa) #num de elementos da equipa
        html.write("\n				<li>" + equipa + ": " + str(valor) + " atletas </li>")
        html.write("\n					<a href=" + "./" + equipaParsed + ".html" +">" + equipa + "<a>")

        #criar html da equipa
               
        link_file = os.path.join(path, equipaParsed + ".html")
        link = open(link_file, "w")

        link.write("<!DOCTYPE html><br><html>")
        link.write("\n		<h2> Atletas da equipa " + equipa + " </h2><hr>")
        link.write("\n			<body>")
        link.write("\n				<ul>")
        link.write('<table style="width:70%" border=1 frame=hsides rules=rows>\n')
        link.write('    <tr>\n      <th>Nome</th>\n     <th>Data Nascimento</th>\n     <th>Morada</th>\n     <th>Email</th>\n       <th>Prova</th>\n        <th>Escalão</th>\n        </tr>')
        
        for atleta in inscritos: #percorrer todos os atletas
            
            nome = atleta.get("nome")
            dataNasc = atleta.get("dataNasc")
            morada = atleta.get("morada")
            email = atleta.get("email")
            prova = atleta.get("prova")
            escalao = atleta.get("escalao")
            eq = atleta.get("equipa").upper()

            if (eq== equipa): #se o atleta pertencer à equipa, adicionar ao html
                            
                link.write('    <tr>\n')
                link.write("<td>" + nome + '</td>')
                link.write("<td>" + dataNasc + '</td>')
                link.write("<td>" + morada + '</td>') 
                link.write("<td>" + email + '</td>')
                link.write("<td>" + prova + '</td>')
                link.write("<td>" + escalao + '</td>')
                link.write('    </tr>\n')
                

        link.write('</table>\n')
        link.write('</ul>\n')
        link.write("\n   </body>")
        link.write("\n</html>")
        link.close()

    html.write("\n         </ul>")
    html.write("\n   </body>")
    html.write("\n</html>")

    html.close()

    print("Ficheiros gerados!")

def f():

    por_idade = {}
    table = PrettyTable()
    table.field_names = ['Idade', 'Nome']

    for atleta in inscritos:

        dataNasc = atleta.get("dataNasc")
        ano = re.split(r'/|-', dataNasc)
        
        if (ano[0] != '') :
            anoNasc = '19' + ano[2]
            idade = 2021 - int(anoNasc)

            if idade not in por_idade:
                por_idade[idade] = list()

            por_idade[idade].append(atleta.get('nome'))
        
    por_idade = dict(sorted(por_idade.items(), key = lambda p: (p[0], p[1])))

    for idade in por_idade:
        persons = ''
        for person in por_idade[idade]:
            persons = persons + person + '\n'

        table.add_row([idade, persons])

    print(table)

def g():
    provas = {}
    table = PrettyTable()
    table.field_names = ['Prova', 'Nome']

    for atleta in inscritos:

        prova = atleta.get("prova")
        nome = atleta.get("nome")
        apelido = re.search(r'(?i:silva)', nome)

        if (apelido):
            if prova not in provas:
                provas[prova] = list()

            provas[prova].append(nome)
        
    provas = dict(sorted(provas.items(), key = lambda p: (p[0], p[1])))

    for prova in provas:
        persons = ''

        for person in provas[prova]:
            persons = persons + '\n' + person

        table.add_row([prova, persons])

    print(table)

def h():

    table = PrettyTable()
    table.field_names = ["Prova", "Equipas"]

    nr_equipas = 0

    provas = {}
    letra = input("Insira a inicial da equipa: ").upper()

    for atleta in inscritos:

        prova = atleta.get("prova")
        equipa = atleta.get("equipa")
        y = re.search(rf'^{letra}', equipa)

        if y :
            if prova not in provas:
                provas[prova] = list()
            if equipa not in provas[prova]:
                provas[prova].append(equipa)
            nr_equipas += 1

    provas = dict(sorted(provas.items(), key = lambda p: (p[0], p[1])))

    for prova in provas.keys():
        equipas = ''
        for equipa in provas[prova]:
            equipas += equipa + '\n'
        
        table.add_row([prova, equipas])

    if nr_equipas > 0:
        print(table)
    else:
        print('Não existem equipas com a inicial ' + letra)

def i():

    por_mes = {}
  
    table = PrettyTable()
    table.field_names = ['Mês', 'Atletas e idade']

    for atleta in inscritos:

        nomeAtleta = atleta.get("nome")
        nome = re.split(r' ', nomeAtleta) 
        #verificamos quantos white spaces existem no nome para proceder a sua contagem

        dataNasc = atleta.get("dataNasc")
        data = re.split(r'/|-', dataNasc)

        morada = atleta.get('morada')
        de_braga = re.search(r'(?i:braga)', morada)

        if data[0] != '' : # if it has bithday date

            mesNasc = data[1]
            anoNasc = '19' + data[2]
            idade = 2021 - int(anoNasc)

            if mesNasc not in por_mes:
                por_mes[mesNasc] = list()

            if len(nome) == 2 and de_braga:
                nome_string = nome[0] + ' ' + nome[1] 
                person = nome_string + ' (' + str(idade) + ')'
                por_mes[mesNasc].append(person)

    por_mes = dict(sorted(por_mes.items(), key = lambda p: (p[0], p[1])))

    for mes in por_mes:
        persons = ''
        for person in por_mes[mes]:
            persons += person + '\n'

        table.add_row([mes, persons])

    print(table)


# ------------------- MENU ------------------- #

inscritos = []

parse_file()

print("MENU")
print('A. Concorrentes individuais de Valongo')
print('B. Concorrentes ''Paulo'' ou ''Ricardo'' com Gmail')
print('C. Atletas da equipa Turbulentos')
print('D. Atletas inscritos por escalão')
print('E. Gerar html com equipas')
print('F. Atletas por idade')
print('G. Atletas com apelido ''Silva'' em cada prova')
print('H. Equipas por prova por inicial')
print('I. Atletas de Braga com 2 nomes, divididos por mês de aniversário')
print('S. Sair')

inp = input('\n--Opção ').lower()

while inp != 's':
    
    if inp == 'a':
        a()
    elif inp == 'b':
        b()
    elif inp == 'c':
        c()
    elif inp == 'd':
        d()
    elif inp == 'e':
        e()
    elif inp == 'f':
        f()
    elif inp == 'g':
        g()
    elif inp == 'h':
        h()
    elif inp == 'i':
        i() 
    else:
        print('Opção inválida')

    inp = input('\n--Opção ').lower()

# ----------------- FIM MENU ----------------- #
