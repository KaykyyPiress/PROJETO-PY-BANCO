import pickle #Para controlar melhor os dados salvos nos arquivos, meio que codifica
from datetime import datetime #importa data e hora principalmente para o extrato

# Lista para armazenar os clientes
clientes = []

# Função para carregar os clientes de um arquivo
def carregar_clientes():
    try:
        with open("arquivo_banco.txt", "rb") as file: #Abre o arquivo pedido em modo read
            clientes = pickle.load(file) #Descodifica em pickle
    except FileNotFoundError: #Caso não tenha clientes, retorne a lista clientes
        clientes = []
    return clientes

# Função para salvar os clientes em um arquivo
def salvar_clientes():
    with open("arquivo_banco.txt", "wb") as file: # Abre o arquivo em modo write
        pickle.dump(clientes, file) #Codifica em pickle

# Carrega os clientes do arquivo
clientes = carregar_clientes()

# Função para cadastrar um novo cliente
def cadastro():
    # Pede os dados do cliente
    nome = input("Qual seu nome? ")
    cpf = input("Qual seu CPF? Ex: 123.456.789-10 ")
    conta = input("Qual tipo de conta? Comum ou Plus? ")
    if conta.lower() == "comum" or "c": # Se o cliente digitar comum, vai ter um limite e uma taxa de debito só para ele
        limite_negativo = -1000.0
        taxa_debito = 0.05
    elif conta.lower() == "plus" or "p": # Se o cliente digitar plus, vai ter um limite e uma taxa de debito só para ele
        limite_negativo = -5000.0
        taxa_debito = 0.03
    else:
       return
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
    salvar_clientes()

    print("Registrado com sucesso!")

# Função para autenticar um cliente
def autenticar():
    cpf = input("Digite seu CPF: ")
    senha = input("Digite sua senha: ")
    for cliente in clientes:
        if cliente["cpf"] == cpf and cliente["senha"] == senha: #Se na bibiloteca selecionada pela CPF for igual ao da senha retorna o cliente
            return cliente
    return None

# Função para exibir o extrato de um cliente
def extrato():
    cliente = autenticar()
    if cliente is None:
        print("CPF ou senha inválidos. Tente novamente.")
        return
    print(f"Extrato de {cliente['nome']}:")
    print(f"Saldo atual na conta: R${cliente['deposito']:.2f}")
    print(f"Saldo atual na poupança: R${cliente['poupanca']:.2f}")
    for acontecimento in cliente['historico']:
        tipo = acontecimento['tipo']
        valor = acontecimento['valor']
        horario = acontecimento['horario']
        if tipo == 'DEPOSITO':
            print(f"Depósito de R${valor:.2f} em {horario}")
        elif tipo == 'DEBITO':
            print(f"Débito de R${valor:.2f} em {horario}")
        elif tipo == 'TRANSFERENCIA':
            destino = acontecimento['destino']
            print(f"Transferência para {destino} no valor de R${valor:.2f} em {horario}")
    rendimento = calcular_rendimento(cliente)
    print(f"Rendimento da poupança neste mês: R${rendimento:.2f}")

# Função para realizar operações livres
def calcular_rendimento(cliente):
    taxa_rendimento = 0.01  # Taxa de rendimento da poupança (1% ao mês)
    rendimento = cliente["poupanca"] * taxa_rendimento
    cliente["poupanca"] += rendimento
    return rendimento

# Função para listar os clientes cadastrados
def listar_clientes():
    print("Lista de clientes cadastrados:")
    for x in clientes: #Dentro da lista clientes, vai aparecer todas as bibliotecas (usuários)
        print(f"Nome: {x['nome']}, CPF: {x['cpf']}, Tipo de conta: {x['tipo conta']}, Saldo: R${x['deposito']:.2f}")

def deposito_poupanca():
    cliente = autenticar() #Para o cliente conseguir fazer o deposito na poupança, tem que colocar cpf e senha
    if cliente is None: #Se a senha ou CPF não existir
        print("CPF ou senha invalidas")
        return
    print("A poupança rende 1%% ao mês")
    continuar = input("Deseja continuar? Sim/Não\n")
    if continuar.upper() == "SIM":
        cpf = input("Digite o CPF do cliente: ")
        for cliente in clientes:
            if cliente["cpf"] == cpf: #Vai selecionar o CPF citado
                valor_deposito = float(input("Qual o valor a ser depositado na poupança? "))
                cliente["poupanca"] += valor_deposito #O valor colocado vai ser adicionado o que já tem na poupança que originalment é 0 (valor que tinha = valor que tinha + valor do deposito)
                print(f"Depósito de R${valor_deposito:.2f} realizado com sucesso na poupança de {cliente['nome']}.")
                return
        print("Cliente não encontrado.")
    else:
        return

def debito():
    cpf = input("Digite o CPF do cliente: ")
    cliente = autenticar() #Confere CPF e senha antes de continuar
    if cliente is None:
        print("CPF ou senha invalidas")
        return
    for cliente in clientes:
        if cliente["cpf"] == cpf: #Procura o CPF digitado na lista clientes
            valor_debito = float(input("Qual o valor a ser debitado? "))
            # Verificar o tipo de conta e aplicar taxa de débito correspondente
            if cliente["tipo conta"].lower() == "comum":
                valor_debito += valor_debito * 0.05      #Valor que a pessoa digitou + o valor que ela digitou * a taxa
            elif cliente["tipo conta"].lower() == "plus":
                valor_debito += valor_debito * 0.03      #Valor que a pessoa digitou + o valor que ela digitou * a taxa

            # Verificar limite de saldo negativo
            if cliente["deposito"] - valor_debito >= -1000.0:
                cliente["deposito"] -= valor_debito
                registro = {
                    "tipo": "DEBITO",
                    "valor": valor_debito, #Altera o valor 
                    "horario": datetime.now() #Coloca o horário que ocorreu
                }
                cliente["historico"].append(registro)
                print(f"Débito de R${valor_debito:.2f} realizado com sucesso na conta de {cliente['nome']}.")
            else:
                print("Saldo insuficiente. Limite de saldo negativo excedido.")
            return
    print("Cliente não encontrado.")

def apaga_cliente():
    cpf = input("Digite o CPF do cliente que deseja apagar: ")
    for cliente in clientes: #Dentro da lista clientes
        if cliente["cpf"] == cpf:
            nome = cliente["nome"] #Para aparecer o nome da pessa na mensagem
            confirmacao = input(f"Tem certeza que deseja apagar o cliente {nome}? (S/N) ")
            if confirmacao.upper() == "S":
                clientes.remove(cliente)  # Remove o cliente da lista de clientes
                print("Cliente removido com sucesso!")
                return
            else:
                print("Operação cancelada.")
                return
    print("Cliente não encontrado.")

def transferencia():
    cpf_origem = input("Digite o CPF do cliente que irá transferir: ")
    cliente_origem = autenticar() #Confere senha e CPF do cliente
    if cliente_origem is None:
        print("Cliente de origem não autenticado.")
        return
    for cliente_destino in clientes:
        if cliente_destino["cpf"] == cpf_origem:
            cpf_destino = input("Digite o CPF do destinatário: ")
            for cliente_destino in clientes:
                if cliente_destino["cpf"] == cpf_destino:
                    valor_transferencia = float(input("Qual o valor a ser transferido? "))
                    if valor_transferencia > cliente_origem["deposito"]:
                        print("Saldo insuficiente.")
                    else:
                        cliente_origem["deposito"] -= valor_transferencia
                        cliente_destino["deposito"] += valor_transferencia
                        registro_origem = {
                            "tipo": "TRANSFERENCIA",
                            "valor": valor_transferencia,
                            "destino": cliente_destino["nome"],
                            "horario": datetime.now()  # Armazena o horário da transação
                        }
                        registro_destino = {
                            "tipo": "TRANSFERENCIA",
                            "valor": valor_transferencia,
                            "destino": cliente_origem["nome"],
                            "horario": datetime.now()  # Armazena o horário da transação
                        }
                        cliente_origem["historico"].append(registro_origem)  # Registra a transação no histórico do cliente de origem
                        cliente_destino["historico"].append(registro_destino)  # Registra a transação no histórico do cliente de destino
                        print(f"Transferência de R${valor_transferencia:.2f} realizada com sucesso da conta de {cliente_origem['nome']} para a conta de {cliente_destino['nome']}.")
                    return
            print("Destinatário não encontrado.")
            return
    print("Cliente de origem não encontrado.")

def deposito():
    cliente = autenticar() #Confere o CPF e a senha
    if cliente is None:
        print("CPF ou senha invalidas")
        return
    cpf = input("Digite o CPF do cliente: ")
    for cliente in clientes:
        if cliente["cpf"] == cpf: #Procura a biblioteca que tem o CPF selecionado
            valor_deposito = float(input("Qual o valor a ser depositado? "))
            cliente["deposito"] += valor_deposito #O valor que está no deposito + ele mesmo + o valor digitado
            registro = {
                "tipo": "DEPOSITO",
                "valor": valor_deposito,
                "horario": datetime.now()  # Armazena o horário da transação
            }
            cliente["historico"].append(registro)  # Registra a transação no histórico do cliente
            print(f"Depósito de R${valor_deposito:.2f} realizado com sucesso na conta de {cliente['nome']}.")
            return
    print("Cliente não encontrado.")
#Mostra as taxas do banco
def instrução():
    print("BEM VINDO AO BANCO ECONÔMICO:\nNossas taxas da conta comum e plus são respectivamente:\nLimite negativo: 1000.00 e 5000.00\nTaxa de débito:0.5 e 0.3\nA poupança é 100%% segura e rende 1%%a.m\nSEMPRE SELECIONE 9 PARA SAIR E SALVAR SEUS DADOS\nAgradecemos sua escolha ;)")
    return

#FUNÇÃO MENU PRINCIPAL
def menu():
    clientes = carregar_clientes() #Carrega o arquivo primeiro
    while True:
        print("BEM VINDO AO BANCO ECONÔMICO: ")
        opcao = int(input("1. Registrar Cliente\n2. Apagar Cliente\n3. Mostrar Clientes\n4. Débito\n5. Depósito\n6. Extrato\n7. Transferência\n8. Poupança\n9. Salvar/Sair\n10. Taxas\nSalve antes de sair (aperte 9)\nOPÇÃO = "))
        # Verifica a opção selecionada
        if opcao == 1:
            cadastro()
            fim = input("Deseja voltar o menu inicial?\nSim ou Não\n ")
            if fim.upper() == "NÃO" or fim.upper() == "N" or fim.upper() == "NAO":
                print(clientes)
                print("Obrigado por usar nosso banco")
                break
        elif opcao == 2:
            apaga_cliente()
        elif opcao == 3:
            listar_clientes()
        elif opcao == 4:
            debito()
        elif opcao == 5:
            deposito()
        elif opcao == 6:
            extrato()
        elif opcao == 7:
            transferencia()
        elif opcao == 8:
            deposito_poupanca()
        elif opcao == 9:
            salvar_clientes()
            print("Obrigado por usar nosso banco")
            break
        elif opcao == 10:
            instrução()
        else:
            print("Opção inválida. Tente novamente.")
            

menu()