from datetime import datetime

# Lista para armazenar os clientes
clientes = []

# Função para cadastrar um novo cliente
def cadastro():
    # Pede os dados do cliente
    nome = input("Qual seu nome? ")
    cpf = input("Qual seu CPF? Ex: 123.456.789-10 ")
    conta = input("Qual tipo de conta? Comum ou Plus? ")
    deposito = float(input("Qual o depósito inicial? "))
    senha = input("Crie uma senha: ")

    # Cria um dicionário com os dados do cliente
    pessoa = {
        "nome": nome,
        "cpf": cpf,
        "tipo conta": conta,
        "deposito": deposito,
        "senha": senha,
        "historico": []  # Histórico vazio para armazenar as transações
    }

    # Adiciona o dicionário 'pessoa' na lista 'clientes'
    clientes.append(pessoa)
    print(pessoa)
    print("Registrado com sucesso!")

# Função para autenticar um cliente
def autenticar():
    cpf = input("Digite seu CPF: ")
    senha = input("Digite sua senha: ")
    for cliente in clientes:
        if cliente["cpf"] == cpf and cliente["senha"] == senha:
            return cliente
    return None

# Função para exibir o extrato de um cliente
def extrato():
    cliente = autenticar()
    if cliente is None:
        print("CPF ou senha inválidos. Tente novamente.")
        return
    print(f"Extrato de {cliente['nome']}:")
    print(f"Saldo atual: R${cliente['deposito']:.2f}")
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
# Função para realizar operações livres
def operacao_livre():
    print("ERRRRROO")  # Ação livre não implementada

# Função para listar os clientes cadastrados
def listar_clientes():
    print("Lista de clientes cadastrados:")
    for x in clientes:
        print(f"Nome: {x['nome']}, CPF: {x['cpf']}, Tipo de conta: {x['tipo conta']}, Saldo: R${x['deposito']:.2f}")

def debito():
    cpf = input("Digite o CPF do cliente: ")
    cliente = autenticar()
    for cliente in clientes:
        if cliente["cpf"] == cpf:
            valor_debito = float(input("Qual o valor a ser debitado? "))
            if valor_debito > cliente["deposito"]:
                print("Saldo insuficiente.")
            else:
                cliente["deposito"] -= valor_debito
                registro = {
                    "tipo": "DEBITO",
                    "valor": valor_debito,
                    "horario": datetime.now()  # Armazena o horário da transação
                }
                cliente["historico"].append(registro)  # Registra a transação no histórico do cliente
                print(f"Débito de R${valor_debito:.2f} realizado com sucesso na conta de {cliente['nome']}.")
            return
    print("Cliente não encontrado.")


def apaga_cliente():
    cpf = input("Digite o CPF do cliente que deseja apagar: ")
    for cliente in clientes:
        if cliente["cpf"] == cpf:
            nome = cliente["nome"]
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
    cliente_origem = autenticar()
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
    cpf = input("Digite o CPF do cliente: ")
    for cliente in clientes:
        if cliente["cpf"] == cpf:
            valor_deposito = float(input("Qual o valor a ser depositado? "))
            cliente["deposito"] += valor_deposito
            registro = {
                "tipo": "DEPOSITO",
                "valor": valor_deposito,
                "horario": datetime.now()  # Armazena o horário da transação
            }
            cliente["historico"].append(registro)  # Registra a transação no histórico do cliente
            print(f"Depósito de R${valor_deposito:.2f} realizado com sucesso na conta de {cliente['nome']}.")
            return
    print("Cliente não encontrado.")

    
#FUNÇÃO MENU PRINCIPAL
def menu():
    while True:
        print("BEM VINDO AO BANCO TISTRESA: ")
        opcao = int(input("1. Registrar Cliente\n2. Apagar Cliente\n3. Mostrar Clientes\n4. Débito\n5. Depósito\n6. Extrato\n7. Transferência\n8. Operação livre\n9. Sair\n"))
        # Verifica a opção selecionada
        if opcao == 1:
            cadastro()
            fim = input("Deseja Sair? S/N ")
            if fim.upper() == "S":
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
            operacao_livre()
        elif opcao == 9:
            print("Obrigado por usar nosso banco")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()
