#lista para criar os clientes
clientes = []

#função que chama o cadastro com as perguntas
def cadastro():

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

def listar_clientes():
    print("Lista de clientes cadastrados:")
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
        opcao = int(input("1. Registrar Cliente\n2. Apagar Cliente\n3. Depositar\n4. Mostrar Clientes\n5. Débito\n9. Sair\n")) 
        
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
            deposito()

        elif opcao == 4:
            listar_clientes()

        elif opcao == 5:
            debito()
            
        elif opcao == 9:
            print("Obrigado por usar nosso banco")
            break
        
        else:
            print("Opção inválida. Tente novamente.")
menu()