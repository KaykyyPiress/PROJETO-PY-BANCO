from datetime import datetime

#lista para criar os clientes
clientes = []

#função que chama o cadastro com as perguntas
def cadastro():
    #pede os dados para o cliente
    nome = input("Qual seu nome? ")
    cpf = input("Qual seu CPF? Ex: 123.456.789-10 ")
    conta = input("Qual tipo de conta? Comum ou Plus? ")
    deposito = float(input("Qual deposito inicial? "))
    senha = input("Crie uma senha: ")

#cria um dicionario com os dados da pessoa
    pessoa = {
        "nome": nome,
        "cpf": cpf,
        "tipo conta": conta,
        "deposito": deposito,
        "senha": senha
    }

#adiciona o dicionario pessoa na lista clientes
    clientes.append(pessoa)
    print(pessoa)
    print("Registrado com sucesso!")

def autenticar():
    cpf = input("Digite seu CPF: ")
    senha = input("Digite sua senha: ")
    for cliente in clientes:
        if cliente["cpf"] == cpf and cliente["senha"] == senha:
            return cliente
    return None

def extrato():
    cliente = autenticar()
    if cliente is None:
        print("CPF ou senha inválidos. Tente novamente.")
        return
    print(f"Extrato de {cliente['nome']}:")
    print(f"Saldo atual: R${cliente['deposito']:.2f}")
    for acontecimento in cliente['historico']:
        if acontecimento['tipo'] == 'DEPOSITO':
            print(f"Depósito: R${acontecimento['valor']:.2f}")
        elif acontecimento['tipo'] == 'DEBITO':
            print(f"Débito: R${acontecimento['valor']:.2f}")
        elif acontecimento['tipo'] == 'TRANSFERENCIA':
            print(f"Transferência para {acontecimento['destino']}: R${acontecimento['valor']:.2f}")



def operacao_livre():
    print("ERRRRROO")

def listar_clientes():
    print("Lista de clientes cadastrados:")
    #percorre a lista clientes
    for x in clientes:
        print(f"Nome: {x['nome']}, CPF: {x['cpf']}, Tipo de conta: {x['tipo conta']}, Saldo: R${x['deposito']:.2f}")

def debito():
    cpf = input("Digite o CPF do cliente: ")
    for cliente in clientes:
        if cliente["cpf"] == cpf:
            valor_debito = float(input("Qual o valor a ser debitado? "))
            if valor_debito > cliente["deposito"]:
                print("Saldo insuficiente.")
            else:
                cliente["deposito"] -= valor_debito
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
                clientes.remove(cliente)
                print("Cliente removido com sucesso!")
                return
            else:
                print("Operação cancelada.")
                return
    print("Cliente não encontrado.")

def transferencia():
    cpf_origem = input("Digite o CPF do cliente que irá transferir: ")
    for cliente_origem in clientes:
        if cliente_origem["cpf"] == cpf_origem:
            cpf_destino = input("Digite o CPF do destinatário: ")
            for cliente_destino in clientes:
                if cliente_destino["cpf"] == cpf_destino:
                    valor_transferencia = float(input("Qual o valor a ser transferido? "))
                    if valor_transferencia > cliente_origem["deposito"]:
                        print("Saldo insuficiente.")
                    else:
                        cliente_origem["deposito"] -= valor_transferencia
                        cliente_destino["deposito"] += valor_transferencia
                        print(f"Transferência de R${valor_transferencia:.2f} realizada com sucesso da conta de {cliente_origem['nome']} para a conta de {cliente_destino['nome']}.")
                    return
            print("Destinatário não encontrado.")
            return
    print("Cliente não encontrado.")

def deposito():
    cpf = input("Digite o CPF do cliente: ")
    for cliente in clientes:
        if cliente["cpf"] == cpf:
            valor_deposito = float(input("Qual o valor a ser depositado? "))
            cliente["deposito"] += valor_deposito
            print(f"Depósito de R${valor_deposito:.2f} realizado com sucesso na conta de {cliente['nome']}.")
            return
    print("Cliente não encontrado.")
    
#FUNÇÃO MENU PRINCIPAL
def menu():
    while True:
        print("BEM VINDO AO BANCO TISTRESA: ") 
        opcao = int(input("1. Registrar Cliente\n2. Apagar Cliente\n3. Mostrar Clientes\n4. Débito\n5. Depósito\n6. Extrato\n7. Transferência\n8. Operação livre\n9. Sair\n")) 
        #vê qual opção que a pessoa digitou
        if opcao == 1:
            cadastro()
            fim = input("Deseja Sair? S/N ")
            if fim.upper() == "S":
                print(clientes)
                print("Obrigado por usar nosso banco")
                break
        
        elif opcao == 2:
            apaga_cliente()

        elif opcao ==3:
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
