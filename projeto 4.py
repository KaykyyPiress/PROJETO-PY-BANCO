import pickle #Para controlar melhor os dados salvos nos arquivos, meio que codifica
from datetime import datetime #importa data e hora principalmente para o extrato

# Lista para armazenar os clientes
clientes = []

# Função para carregar os clientes de um arquivo
def carregar_arquivo():
    try:
        with open("arquivo_banco.txt", "rb") as file: #Abre o arquivo pedido em modo read
            clientes = pickle.load(file) #Descodifica em pickle
    except FileNotFoundError: #Caso não tenha clientes, retorne a lista clientes
        clientes = []
    return clientes

# Função para salvar os clientes em um arquivo
def salvar_dados():
    with open("arquivo_banco.txt", "wb") as file: # Abre o arquivo em modo write
        pickle.dump(clientes, file) #Codifica em pickle

# Carrega os clientes do arquivo
clientes = carregar_arquivo()

# Função para cadastrar um novo cliente
def cadastro():
    # Pede os dados do cliente
    nome = input("Qual seu nome completo? ")
    cpf = input("Qual seu CPF? Ex: 123.456.789-10 ")
    # O usuário tem que escolher alguma das opções de conta
    while True:
        conta = input("Deseja conta comum ou plus? Para enteder mais as taxas volte ao menu e aperte 10. ")
        if conta.lower() == "comum" or conta.lower() == "c":
            limite_negativo = -1000.0
            taxa_debito = 0.05
            break
        elif conta.lower() == "plus" or conta.lower() == "p":
            limite_negativo = -5000.0
            taxa_debito = 0.03
            break
        else:
            print("Tipo de conta inválido, selecione comum ou plus.")

    deposito = float(input("Qual o depósito inicial? "))
    senha = input("Crie uma senha: ")


    # Cria um dicionário com os dados do cliente
    pessoa = {
    "nome": nome,
    "cpf": cpf,
    "tipo conta": conta,
    "deposito": deposito,
    "poupanca": 0,  # Saldo da poupança inicialmente zero
    "senha": senha,
    "historico": []  # Histórico vazio para armazenar as transações
}

    # Adiciona o dicionário 'pessoa' na lista 'clientes'
    clientes.append(pessoa)
    print(pessoa)
    salvar_dados()
    print("Cadastrado com sucesso!")

    senha = input("Digite sua senha: ")
    for cliente in clientes:
        if cliente["cpf"] == cpf and cliente["senha"] == senha: # Se dentro da biblioteca que tiver aquele CPF tiver aquela senha, autoriza
            return cliente
    print("Senha ou CPF inválido, tente novamente") # Se não tiver retorna
    return None

def autenticar_usuarios(cpf, senha): # Pega a variável cpf e senha que a pessoa digitar e procura nas bibliotecas
    for cliente in clientes:
        if cliente["cpf"] == cpf and cliente["senha"] == senha: # Procura se o CPF digitado e a senha são da mesma bilbioteca
            return cliente
    return None

# Função para exibir o extrato de um cliente
def extrato():
    cpf = input("Digite o CPF: ") # CPF e senha para autenticar
    senha = input("Digite a senha: ")
    cliente = autenticar_usuarios(cpf, senha) # Autentica
    if cliente is None:
        print("CPF ou senha inválidos.")
        return
    print(f"Extrato de {cliente['nome']}:")
    print(f"Saldo atual na conta: R${cliente['deposito']:.2f}")
    print(f"Saldo atual na poupança: R${cliente['poupanca']:.2f}")
    for acontecimento in cliente['historico']:
        tipo = acontecimento['tipo'] # Pega o tipo de informação na bilbioteca
        valor = acontecimento['valor']
        horario = acontecimento['horario']
        if tipo == 'DEPOSITO':
            print(f"Depósito de R${valor:.2f} em {horario}") # Mostra informação de valor e o horário do depósito
        elif tipo == 'DEBITO':
            print(f"Débito de R${valor:.2f} em {horario}") # Mostra informação de valor e o horário do débito
        elif tipo == 'TRANSFERENCIA':
            destino = acontecimento['destino']
            print(f"Transferência para {destino} no valor de R${valor:.2f} em {horario}") # Mostra informação de valor e o horário de transferência
    rendimento = cauculo_do_rendimento(cliente)
    print(f"Rendimento da poupança neste mês: R${rendimento:.2f}") # Mostra informação de valor e o horário do rendimento da poupança

# Função para realizar operações livres
def cauculo_do_rendimento(cliente):
    taxa_rendimento = 0.01  # Taxa de rendimento da poupança (1% ao mês)
    rendimento = cliente["poupanca"] * taxa_rendimento #multiplica o valor que pessoa selecionou pela taxa de rendimento
    cliente["poupanca"] += rendimento # Depois soma
    return rendimento

# Função para listar os clientes cadastrados
def mostrar_clientes():
    login = input("SOMENTE ADMINISTRADOR\nLogin:") #Pede senha e login do adiministrador. Senha e login padrão: admin
    senha = input("Senha:")
    if login.lower() == "admin" and senha.lower() == "admin": # Senha e login padrão: admin
        print("Clientes cadastrados:")
        for x in clientes: #Dentro da lista clientes, vai aparecer todas as bibliotecas (usuários)
            print(f"Nome: {x['nome']}, CPF: {x['cpf']}, Tipo de conta: {x['tipo conta']}, Saldo: R${x['deposito']:.2f}")
    else:
        print("Administrador não autorizado!")
        return menu()

def poupanca():
    cpf = input("Digite o CPF: ") # CPF e senha para autenticar
    senha = input("Digite a senha: ")
    cliente = autenticar_usuarios(cpf, senha) # Autentica
    if cliente is None:
        print("CPF ou senha inválidos.")
        return
    print("A poupança rende 1%% ao mês")
    continuar = input("Deseja prosseguir? Sim/Não\n") # Se o cliente não querer contunuar ele aperta não
    if continuar.lower() == "sim" or "s":
        for cliente in clientes:
            if cliente["cpf"] == cpf: #Vai selecionar o CPF citado na autenticação
                valor_deposito = float(input("Qual o valor a ser depositado na poupança? "))
                cliente["poupanca"] += valor_deposito #O valor colocado vai ser adicionado o que já tem na poupança que originalment é 0 (valor que tinha = valor que tinha + valor do deposito)
                print(f"Depósito de R${valor_deposito:.2f} realizado com sucesso na poupança de {cliente['nome']}.")
                return
        print("Cliente não encontrado.")
    else:
        return

def debito():
    cpf = input("Digite o CPF do cliente: ") 
    senha = input("Digite a senha do cliente: ")
    cliente = autenticar_usuarios(cpf, senha) # cCOnfere senha e dados digitados
    if cliente is None:
        print("CPF ou senha inválidas")
        return
    for cliente in clientes:
        if cliente["cpf"] == cpf:
            valor_debito = float(input("Qual o valor a ser debitado? "))
            if cliente["tipo conta"].lower() == "comum":
                valor_debito += valor_debito * 0.05 #Valor que a pessoa digitou + o valor que ela digitou vezes a taxa
            elif cliente["tipo conta"].lower() == "plus":
                valor_debito += valor_debito * 0.03 #Valor que a pessoa digitou + o valor que ela digitou * a taxa
            if cliente["deposito"] - valor_debito >= -1000.0: #Confere o valor negativado
                cliente["deposito"] -= valor_debito
                registro = {
                    "tipo": "DEBITO",
                    "valor": valor_debito,
                    "horario": datetime.now() #Coloca o horário que ocorreu
                }
                cliente["historico"].append(registro)
                print(f"Débito de R${valor_debito:.2f} realizado com sucesso na conta de {cliente['nome']}.")
            else:
                print("Saldo insuficiente. Limite de saldo negativo excedido.")
            return
    print("Cliente não encontrado.")

def deleta_cliente():
    login = input("SOMENTE ADMINISTRADOR\nLogin:") #Senha e login do administrador
    senha = input("Senha:")
    if login.lower() == "admin" and senha.lower() == "admin": #Senha e login padrão: admin
        cpf = input("Digite o CPF do cliente que deseja apagar: ")
        for cliente in clientes: #Dentro da lista clientes
            if cliente["cpf"] == cpf:
                nome = cliente["nome"] #Para aparecer o nome da pessa na mensagem
                confirmacao = input(f"Tem certeza que deseja apagar o cliente {nome}? Sim ou Não? ")
                if confirmacao.lower() == "sim" or "s":
                    clientes.remove(cliente)  # Remove o cliente da lista de clientes
                    print("Cliente removido com sucesso!")
                    return
                else:
                    print("Operação cancelada.")
                    return
        print("Cliente não encontrado.")
    else:
        print("ADMINISTRADOR INVÁLIDO!")
        return menu()

def transferencia():
    cpf_origem = input("Digite o CPF do cliente que irá transferir: ")
    senha_origem = input("Digite a senha do cliente que irá transferir: ")
    cliente_origem = autenticar_usuarios(cpf_origem, senha_origem) #confere senha e cpf da pessoa que vai enviar
    if cliente_origem is None:
        print("Cliente de origem não autenticado.")
        return
    for cliente_destino in clientes:
        if cliente_destino["cpf"] == cpf_origem: # confirma o cliente de origem
            cpf_destino = input("Digite o CPF do destinatário: ")
            for cliente_destino in clientes: # Procura cpf do destinatário
                if cliente_destino["cpf"] == cpf_destino: # confirma cpf do destinatário
                    valor_transferencia = float(input("Qual o valor a ser transferido? "))
                    if valor_transferencia > cliente_origem["deposito"]: #Se o o valor da transferencia for maior do que o valor que ele tem, aparece inválid
                        print("Saldo insuficiente.") 
                    else:
                        cliente_origem["deposito"] -= valor_transferencia #Tira depoisto do remente (origem)
                        cliente_destino["deposito"] += valor_transferencia  # Coloca o deposito no destinatário
                        registro_origem = {
                            "tipo": "TRANSFERENCIA",
                            "valor": valor_transferencia,
                            "destino": cliente_destino["nome"],
                            "horario": datetime.now()  # Armazena o horário, nome da pesoa da transação no rementente para extrato
                        }
                        registro_destino = {
                            "tipo": "TRANSFERENCIA",
                            "valor": valor_transferencia,
                            "destino": cliente_origem["nome"],
                            "horario": datetime.now()  # Armazena o horário, nome da pessoa da transação no destinatario para extrato
                        }
                        cliente_origem["historico"].append(registro_origem)  # Registra a transação no histórico do cliente de origem
                        cliente_destino["historico"].append(registro_destino)  # Registra a transação no histórico do cliente de destino
                        print(f"Transferência de R${valor_transferencia:.2f} realizada com sucesso da conta de {cliente_origem['nome']} para a conta de {cliente_destino['nome']}.")
                    return
            print("Destinatário não encontrado.")
            return
    print("Cliente de origem não encontrado.")

def deposito():
    cpf = input("Digite o CPF do cliente: ")
    senha = input("Digite a senha do cliente: ")
    cliente = autenticar_usuarios(cpf, senha) # Confirma dados da pessoa 
    if cliente is None:
        print("CPF ou senha inválidas")
        return
    for cliente in clientes: # procura CPF digitado
        if cliente["cpf"] == cpf: # achou
            valor_deposito = float(input("Qual o valor a ser depositado? "))
            cliente["deposito"] += valor_deposito # o valor que a pessoa digitou acima é adivionada no deposito (saldo total)
            registro = { #Salva dados para o extrato
                "tipo": "DEPOSITO",
                "valor": valor_deposito,
                "horario": datetime.now()
            }
            cliente["historico"].append(registro)
            print(f"Depósito de R${valor_deposito:.2f} realizado com sucesso na conta de {cliente['nome']}.")
            return
    print("Cliente não encontrado.")

#Mostra as taxas do banco
def instrução():
    print("BEM VINDO AO BANCO ECONÔMICO:\nNossas taxas da conta comum e plus são respectivamente:\nLimite negativo: 1000.00 e 5000.00\nTaxa de débito:0.5 e 0.3\nA poupança é 100%% segura e rende 1%%a.m\nSEMPRE SELECIONE 9 PARA SAIR E SALVAR SEUS DADOS\nAgradecemos sua escolha ;)")
    return

#FUNÇÃO MENU PRINCIPAL
def menu():
    clientes = carregar_arquivo() #Carrega o arquivo primeiro
    while True:
        print("BEM VINDO AO BANCO ECONÔMICO: ")
        opcao = int(input("1. Registrar Cliente\n2. Apagar Cliente\n3. Mostrar Clientes\n4. Débito\n5. Depósito\n6. Extrato\n7. Transferência\n8. Poupança\n9. Salvar/Sair\n10. Taxas\nSalve antes de sair (aperte 9)\nOPÇÃO = "))
        # Verifica a opção selecionada
        if opcao == 1:
            cadastro()
            fim = input("Deseja voltar o menu inicial?\nSim ou Não\n")
            if fim.upper() == "NÃO" or fim.upper() == "N" or fim.upper() == "NAO":
                print(clientes)
                print("Obrigado por usar nosso banco")
                break

        elif opcao == 2:
            deleta_cliente()
            salvar_dados()

        elif opcao == 3:
            mostrar_clientes()

        elif opcao == 4:
            debito()
            salvar_dados()

        elif opcao == 5:
            deposito()
            salvar_dados()

        elif opcao == 6:
            extrato()
            salvar_dados()

        elif opcao == 7:
            transferencia()
            salvar_dados()

        elif opcao == 8:
            poupanca()
            salvar_dados()

        elif opcao == 9:
            salvar_dados()
            print("Obrigado por usar nosso banco")
            break
        elif opcao == 10:
            instrução()
        else:
            print("Opção inválida. Tente novamente.")
            
menu()