import re
import ply.lex as lex
import ply.yacc as yacc

tokens = [
    'INT',
    'LETRA',
    'MOD',
    'EQUAL',
    'DIFF',
    'GREATER',
    'LESSER',
    'GEQ',
    'LEQ',
    'IF',
    'ELSE',
    'REPEAT',
    'UNTIL',
    'WHILE',
    'DO',
    'WRITE',
    'READ',
    'STRING',
    'COMMENT'
]

literals = [
    '+',
    '-',
    '*',
    '/',
    ',',
    '=',
    '@',
    '&',
    '|',
    '$',
    ':',
    '(',
    ')',
    '{',
    '}',
    '%',
    ';',
    '#',
    '.',
    '[',
    ']'
]

t_LETRA = r'\w+[\w\d_]*'
t_STRING = r'".[^"]*"'
t_EQUAL = r'=='
t_DIFF = r'!='
t_GREATER = r'\>'
t_LESSER = r'\<'
t_GEQ = r'\>='
t_LEQ = r'\<='

def t_INT(t):
    r'[-]?\d+'
    return t

def t_MOD(t):
    r'mod'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_REPEAT(t):
    r'repeat'
    return t

def t_UNTIL(t):
    r'until'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_DO(t):
    r'do'
    return t

def t_COMMENT(t):
    r'\#.[^\#]*\#'
    pass

def t_WRITE(t):
    r'write'
    return t

def t_READ(t):
    r'read'
    return t

t_ignore = ' \n\t'

def t_error(t):
    print('Illegal character! Where? ' + t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()


def p_comandos_comandos(p):
    "comandos : comandos comando "
    p[0] = p[1] + p[2]

def p_comandos_comando(p):
    "comandos : comando"
    p[0] = p[1]

def p_comandos_empty(p):
    "comandos : "
    p[0] = ''

def p_comando_dec(p):
    "comando : '@' declaracoes ';' "
    p[0] = p[2]

def p_comando_atr(p):
    "comando : atribuicao ';'"
    p[0] = p[1]

def p_comando_write(p):
    "comando : WRITE '(' text ')' ';' "
    if p[3].find('pushs',0,10) != -1 :
        p[0] = p[3] + 'writes\n'
    elif p[3].find('pushg',0,10) != -1:
        p[0] = p[3] + 'writei\n'    

def p_comando_read_atr(p):
    "comando : variavel '=' READ '(' ')' ';' " # with text ?
    p[0] =  'read\n'
    p[0] += 'atoi\n'
    p[0] += 'storeg ' + str(p.parser.enderecos.get(p[1])) + '\n'

def p_comando_read(p):
    "comando : READ '(' ')' ';' " # with text ?
    p[0] =  p[3] + 'read\n'

def p_comando_if(p):
    "comando : IF '(' condicoes ')' '{' comandos '}' "
    label = 'if' + str(p.parser.ciclos)  # if0, if1, etc
    label_fim = 'ifEnd'+ str(p.parser.ciclos)

    p[0] = label + ':\n'
    p[0] += p[3]  # escreve condicoes
    p[0] += 'jz ' + label_fim  + '\n' # breaks if doesnt meet condicoes
    p[0] += p[6]  # escreve coisas a fazer
    p[0] += label_fim + ':\n'

    p.parser.ciclos += 1

def p_comando_if_else(p):
    "comando : IF '(' condicoes ')' '{' comandos '}' ELSE '{' comandos '}' "
    label = 'if' + str(p.parser.ciclos)  # if0, if1, etc
    label_else = 'ifElse' + str(p.parser.ciclos)
    label_fim = 'ifEnd' + str(p.parser.ciclos)

    p[0] = label + ':\n'
    p[0] += p[3]  # escreve condicoes
    p[0] += 'jz ' + label_else + '\n' # elses if doesnt meet condicoes
    p[0] += p[6]  # escreve coisas a fazer
    p[0] += 'jump ' + label_fim + '\n'
    p[0] += label_else + ':\n'
    p[0] += p[10]
    p[0] += label_fim + ':\n'

    p.parser.ciclos += 1

def p_comando_repeat(p):
    "comando : REPEAT '{' comandos '}' UNTIL '(' condicoes ')' "
    label = 'repeat' + str(p.parser.ciclos)
    label_until = 'repeatUntil' + str(p.parser.ciclos)
    label_fim = 'repeatEnd' + str(p.parser.ciclos)

    p[0] = label + ':\n'
    p[0] += p[3] # comandos
    p[0] += label_until + ':\n'
    p[0] += p[7]  # condicoes
    p[0] += 'jz ' + label + '\n'
    #p[0] += 'jump ' + label_fim
    p[0] += label_fim + ':\n'

    p.parser.ciclos += 1

def p_comando_while(p):
    "comando : WHILE '(' condicoes ')' '{' comandos '}' "
    label = 'while' + str(p.parser.ciclos)
    label_fim = 'whileEnd' + str(p.parser.ciclos)

    p[0] = label + ':\n'
    p[0] += p[3]  # escreve condicoes
    p[0] += 'jz ' + label_fim + '\n' # ends if doesnt meet condicoes
    p[0] += p[6]  # escreve coisas a fazer
    p[0] += 'jump ' + label + '\n'
    p[0] += label_fim + ':\n'
    
    p.parser.ciclos += 1

def p_comando_do_while(p):
    "comando : DO '{' comandos '}' WHILE '(' condicoes ')'"
    label = 'do' + str(p.parser.ciclos)
    label_do = 'while' + str(p.parser.ciclos)
    label_fim = 'whileEnd' + str(p.parser.ciclos)

    p[0] = label + ':\n'
    p[0] += p[3]  # escreve comandos
    p[0] += label_do + ':\n'
    p[0] += p[7]  # escreve condicoes
    p[0] += 'jz ' + label_fim + '\n' # ends if doesnt meet condicoes
    p[0] += 'jump ' + label + '\n'
    p[0] += label_fim + ':\n'
    
    p.parser.ciclos += 1

def p_declaracoes_declaracoes(p):
    "declaracoes : declaracoes ',' declaracao"
    p[0] = p[1] + p[3]
    
def p_declaracoes_declaracao(p):
    "declaracoes : declaracao"
    p[0] = p[1]

def p_declaracao_value(p):
    "declaracao : variavel '=' INT"
    if p[1] not in p.parser.enderecos:
        p.parser.enderecos.update({p[1]: p.parser.i})
        p[0] = 'pushi ' + p[3] + '\n'
        p.parser.i += 1

def p_declaracao_empty(p):
    "declaracao : variavel"
    if p[1] not in p.parser.enderecos:
        p.parser.enderecos.update({p[1]: p.parser.i})
        p[0] = 'pushi 0\n'
        p.parser.i += 1

def p_declaracao_array(p):
    "declaracao : variavel '[' INT ']' "
    p[0] = 'pushn ' + p[3] + '\n'
    p.parser.enderecos[p[1]] = list()
    while int(p[3]) != 0:
        p.parser.enderecos[p[1]].append(p.parser.i)
        p.parser.i += 1
        p[3] = int(p[3]) - 1
  
def p_declaracao_array_valores(p):
    "declaracao : variavel '[' INT ']' '=' '{' inteiros '}'"
    p[0] = p[7]

    p[3] = int(p[3])
    p.parser.enderecos[p[1]] = list()

    ints = re.findall(r'pushi', p[7])

    if ints < p[3]:
        print('Não inicializou todas as posições do array!')
        print('Restantes posições serão inicializadas a 0')
        while ints < p[3]:
            p[0] += 'pushi 0\n'
            ints += 1
    elif ints > p[3]:
        print('Error! Array inicializado com demasiados valores')
        print('Aborting...')
        exit(1)

    while p[3] !=  0: 
            p.parser.enderecos[p[1]].append(p.parser.i)
            p.parser.i += 1
            p[3] = p[3] - 1

def p_atribuicao(p):
    "atribuicao : variavel '=' expressao"
    if p[1] in p.parser.enderecos:
        p[0] = p[3]
        p[0] += 'storeg ' + str(p.parser.enderecos.get(p[1])) + '\n'

    else: print('A variável ' + p[1] + ' não foi declarada')

def p_atribuicao_array(p):
    "atribuicao : variavel '[' INT ']' '=' expressao"
    if p[1] in p.parser.enderecos:
        p[0] = 'pushgp\n'
        p[0] += 'pushi ' + str(p.parser.enderecos[p[1]][0]) + '\n'
        p[0] += 'padd\n'
        p[0] += 'pushi ' + p[3] + '\n'
        p[0] += p[6]
        p[0] += 'storen\n'

def p_expressao_mais(p):
    "expressao : expressao '+' termo"
    p[0] = p[1] + p[3]
    p[0] += 'add\n'

def p_expressao_menos(p):
    "expressao : expressao '-' termo"
    p[0] = p[1] + p[3]
    p[0] += 'sub\n'

def p_expressao_termo(p):
    "expressao : termo"
    p[0] = p[1]

def p_termo_mult_var(p):
    "termo : termo '*' variavel"
    p[0] = p[1]
    p[0] += 'pushg ' + str(p.parser.enderecos.get(p[3])) + '\n'
    #p[0] += 'pushi ' + str(p[3]) + '\n'
    p[0] += 'mul\n'

def p_termo_div_var(p):
    "termo : termo '/' variavel"
    p[0] = p[1] 
    p[0] += 'pushg ' + str(p.parser.enderecos.get(p[3])) + '\n'
    #p[0] += 'pushi ' + str(p[3]) + '\n'
    p[0] += 'div\n'

def p_termo_mult_array(p):  ## VER
    "termo : termo '*' variavel '[' INT ']' "
    p[0] = p[1]
    p[0] += 'pushgp\n'
    p[0] += 'pushi ' + str(p.parser.enderecos[p[1]][0]) + '\n'
    p[0] += 'padd\n'
    p[0] += 'pushi ' + p[3] + '\n'
    #p[0] += 'pushg ' + str(p.parser.enderecos.get(p[3])) + '\n'
    #p[0] += 'pushi ' + str(p[3]) + '\n'
    p[0] += 'mul\n'

def p_termo_div_array(p):     ## VER
    "termo : termo '/' variavel '[' INT ']' "
    p[0] = p[1]
    p[0] += 'pushgp\n'
    p[0] += 'pushi ' + str(p.parser.enderecos[p[1]][0]) + '\n'
    p[0] += 'padd\n'
    p[0] += 'pushi ' + p[3] + '\n'
    #p[0] += 'pushg ' + str(p.parser.enderecos.get(p[3])) + '\n'
    #p[0] += 'pushi ' + str(p[3]) + '\n'
    p[0] += 'div\n'

def p_termo_mult_int(p):
    "termo : termo '*' INT"
    p[0] = p[1]
    p[0] += 'pushi ' + str(p[3]) + '\n'
    p[0] += 'mul\n'

def p_termo_div_int(p):
    "termo : termo '/' INT"
    p[0] = p[1] 
    p[0] += 'pushi ' + str(p[3]) + '\n'
    p[0] += 'div\n'

def p_termo_mod_var(p):
    "termo : termo MOD variavel"
    p[0] = p[1] 
    p[0] += 'pushg ' + str(p.parser.enderecos.get(p[3])) + '\n'
    #p[0] += 'pushi ' + str(p[3]) + '\n'
    p[0] += 'mod\n'

def p_termo_mod_array(p): ## VER
    "termo : termo MOD variavel '[' INT ']' "
    p[0] = p[1] 
    p[0] += 'pushgp\n'
    p[0] += 'pushi ' + str(p.parser.enderecos[p[1]][0]) + '\n'
    p[0] += 'padd\n'
    p[0] += 'pushi ' + p[3] + '\n'
    #p[0] += 'pushg ' + str(p.parser.enderecos.get(p[3])) + '\n'
    #p[0] += 'pushi ' + str(p[3]) + '\n'
    p[0] += 'mod\n'

def p_termo_mod_int(p):
    "termo : termo MOD INT"
    p[0] = p[1]
    p[0] += 'pushi ' + str(p[3]) + '\n'
    p[0] += 'mod\n'

def p_termo_fator(p):
    "termo : fator"
    p[0] = p[1]

def p_fator_num(p):
    "fator : INT"
    p[0] = 'pushi ' + str(p[1]) + '\n'

def p_fator_exp(p):
    "fator : '(' expressao ')' "
    p[0] = p[2]

def p_fator_letra(p):
    "fator : variavel"
    p[0] = 'pushg ' + str(p.parser.enderecos.get(p[1])) + '\n'

def p_fator_array(p):
    "fator : variavel '[' INT ']' "
    p[0] = 'pushg ' + str(p.parser.enderecos.get(p[1])) + '\n'

def p_fator_string(p):
    "fator : STRING"
    p[0] = 'pushs ' + p[1] + '\n'

def p_text_comando(p):
    "text : comando " # because of write(read) 
    p[0] = p[1]

def p_text_variavel(p):
    "text : variavel "
    p[0] = 'pushg ' + str(p.parser.enderecos.get(p[1])) + '\n'

def p_text_string(p):
    "text : STRING "
    p[0] = 'pushs ' + p[1] + '\n'

def p_text_empty(p):
    "text : "
    p[0] = ''

def p_condicoes_and(p):
    "condicoes : condicoes '&' condicao"
    p[0] = p[1] # primeira condicao
    p[0] += p[3] # outras
    p[0] += 'mul\n'

def p_condicoes_or(p):
    "condicoes : condicoes '|' condicao"
    p[0] = p[1] # primeira condicao
    p[0] += p[3]
    p[0] += 'add\n' # soma resultados

def p_condicoes_condicao(p):
    "condicoes : condicao"
    p[0] = p[1]

def p_condicao(p):
    "condicao : variavel simbolo expressao"
    p[0] = 'pushg ' + str(p.parser.enderecos.get(p[1])) + '\n'
    p[0] += p[3]
    p[0] += p[2]

def p_condicao_array(p): ## VER
    "condicao : variavel '[' INT ']' simbolo expressao"
    #p[0] = 'pushg ' + str(p.parser.enderecos.get(p[1])) + '\n'
    p[0] = 'pushgp\n'
    p[0] += 'pushi ' + str(p.parser.enderecos[p[1]][0]) + '\n'
    p[0] += 'padd\n'
    p[0] += 'pushi ' + p[3] + '\n'
    p[0] += p[3]
    p[0] += p[2]

def p_condicao_exp(p):
    "condicao : expressao simbolo expressao"
    p[0] =  p[1]
    p[0] += p[3]
    p[0] += p[2]

def p_simbolo_geq(p):
    "simbolo : GEQ"
    p[0] = 'supeq\n'

def p_simbolo_leq(p):
    "simbolo : LEQ"
    p[0] = 'infeq\n'

def p_simbolo_greater(p):
    "simbolo : GREATER"
    p[0] = 'sup\n'

def p_simbolo_lesser(p):
    "simbolo : LESSER"
    p[0] = 'inf\n'

def p_simbolo_equal(p):
    "simbolo : EQUAL"
    p[0] = 'equal\n'

def p_simbolo_diff(p):
    "simbolo : DIFF"
    p[0] = 'equal\n'
    p[0] += 'not\n'

def p_variavel(p):
    "variavel : LETRA"
    p[0] = p[1]

def p_inteiros_inteiros(p):
    "inteiros : inteiros ',' INT "
    p[0] = p[1]
    p[0] += 'pushi ' + p[3] + '\n'

def p_inteiros_inteiro(p):
    "inteiros : INT "
    p[0] = 'pushi ' + p[1] + '\n'

def p_error(p):
    print('Syntax error! Where? ', p)


parser = yacc.yacc()

parser.enderecos = {}
parser.i = 0
parser.ciclos = 1

file = input('Insira o nome do ficheiro .txt de código: ')

try:
    code = open(file,'r')
    code = code.read().replace('\n',' ')
    output = open('assembly.txt','w')

    p = str(parser.parse(code))

    print(parser.enderecos)

    output.write(p)
    output.flush()
    output.close()

except FileNotFoundError:
    print('O ficheiro que inseriu não existe')