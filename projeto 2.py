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

    
    
#FUNÇÃO MENU PRINCIPAL
def menu():
    while True:
        print("BEM VINDO AO BANCO TISTRESA: ")
        opcao = int(input("1. Registrar Cliente\n2. Apagar Cliente\n9. Sair\n")) 
        
        if opcao == 1:
            cadastro()
            
            fim = input("Deseja Sair? S/N ")
            if fim.upper() == "S":
                print(clientes)
                print("Obrigado por usar nosso banco")
                break
        
        elif opcao == 2:
            apaga_cliente()
            
        elif opcao == 9:
            print("Obrigado por usar nosso banco")
            break
        
        else:
            print("Opção inválida. Tente novamente.")
menu()