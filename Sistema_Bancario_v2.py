def menu():
    """Exibe o menu de opções e retorna a escolha do usuário."""
    menu_text = """

============ MENU ==============
[d]  Depositar
[s]  Sacar
[e]  Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuário
[lu] Listar usuários
[q]  Sair
===> """
    return input(menu_text).strip().lower()

def depositar(saldo, valor, extrato, /):
    """Realiza um depósito na conta."""
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """Realiza um saque na conta, com validações."""
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    """Exibe o extrato da conta."""
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    """Cria um novo usuário (cliente)."""
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    """Busca um usuário pelo CPF."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def listar_usuarios(usuarios):
    """Lista todos os usuários cadastrados."""
    if not usuarios:
        print("\n@@@ Nenhum usuário cadastrado. @@@")
        return
    
    print("\n================ LISTA DE USUÁRIOS ================")
    for usuario in usuarios:
        print(f"Nome: {usuario['nome']}, CPF: {usuario['cpf']}")
    print("==================================================")


def criar_conta(agencia, usuarios, contas):
    """Cria uma nova conta para um usuário existente."""
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Usuário não encontrado. Crie o usuário primeiro. @@@")
        return

    numero_conta = len(contas) + 1
    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0.0,
        "extrato": "",
        "numero_saques": 0
    }
    contas.append(conta)
    print(f"\n=== Conta número {numero_conta} criada com sucesso para {usuario['nome']}! ===")

def listar_contas(contas):
    """Lista todas as contas cadastradas."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        usuario = conta['usuario']
        print(
            f"Agência: {conta['agencia']} | "
            f"C/C: {conta['numero_conta']} | "
            f"Titular: {usuario['nome']} | "
            f"Saldo: R$ {conta['saldo']:.2f}"
        )
    print("================================================")

def encontrar_conta(contas):
    """Pede o número da conta e a retorna se for encontrada."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. Crie uma conta primeiro. @@@")
        return None

    try:
        num_conta = int(input("Informe o número da conta: "))
        for conta in contas:
            if conta['numero_conta'] == num_conta:
                return conta
        print("\n@@@ Conta não encontrada. @@@")
        return None
    except ValueError:
        print("\n@@@ Número de conta inválido. Digite apenas números. @@@")
        return None


def main():
    """Função principal que executa o sistema bancário."""
    AGENCIA = "0001"
    LIMITE_SAQUES = 3
    LIMITE_VALOR_SAQUE = 500

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            conta_selecionada = encontrar_conta(contas)
            if conta_selecionada:
                try:
                    valor = float(input("Informe o valor do depósito: R$ "))
                    saldo_atualizado, extrato_atualizado = depositar(
                        conta_selecionada['saldo'],
                        valor,
                        conta_selecionada['extrato']
                    )
                    # Atualiza os dados da conta original na lista
                    conta_selecionada['saldo'] = saldo_atualizado
                    conta_selecionada['extrato'] = extrato_atualizado
                except ValueError:
                    print("\n@@@ Valor inválido. Digite um número. @@@")

        elif opcao == 's':
            conta_selecionada = encontrar_conta(contas)
            if conta_selecionada:
                try:
                    valor = float(input("Informe o valor do saque: R$ "))
                    saldo_atualizado, extrato_atualizado, saques_atualizado = sacar(
                        saldo=conta_selecionada['saldo'],
                        valor=valor,
                        extrato=conta_selecionada['extrato'],
                        limite=LIMITE_VALOR_SAQUE,
                        numero_saques=conta_selecionada['numero_saques'],
                        limite_saques=LIMITE_SAQUES,
                    )
                    # Atualiza os dados da conta original na lista
                    conta_selecionada['saldo'] = saldo_atualizado
                    conta_selecionada['extrato'] = extrato_atualizado
                    conta_selecionada['numero_saques'] = saques_atualizado
                except ValueError:
                    print("\n@@@ Valor inválido. Digite um número. @@@")

        elif opcao == 'e':
            conta_selecionada = encontrar_conta(contas)
            if conta_selecionada:
                exibir_extrato(conta_selecionada['saldo'], extrato=conta_selecionada['extrato'])

        elif opcao == 'nu':
            criar_usuario(usuarios)
        
        elif opcao == 'lu':
            listar_usuarios(usuarios)

        elif opcao == 'nc':
            criar_conta(AGENCIA, usuarios, contas)

        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'q':
            print("\nSaindo do sistema... Obrigado por usar nossos serviços!")
            break

        else:
            print("\n@@@ Opção inválida! Por favor, selecione novamente a operação desejada. @@@")

# Inicia o programa
main()