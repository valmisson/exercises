from datetime import datetime, timedelta

RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

balance = 500
limit = 500
withdrawals = 3
transaction_limit = 10
extract = []
clients = []
accounts = []
client_logged = None
date_start = datetime.now()

menu = '''
#######################################
# Selecione a opção desejada:         #
#                                     #
# Entrar conta:  1    Lista contas: 2 #
# Criar cliente: 3    Criar conta:  4 #
#                                     #
# Sair:          5                    #
#                                     #
#######################################
'''

operations_menu = '''
###############################
# Selecione a opção desejada: #
#                             #
# Depósito: 1        Saque: 2 #
# Extrato:  3                 #
#                             #
# Voltar:   4        Sair:  5 #
#                             #
###############################
'''

def date_now ():
    return datetime.now().strftime('%d/%m/%Y %H:%M')

def get_client(cpf):
    client_found = [client for client in clients if client.get('cpf') == cpf]
    return client_found[0] if client_found else None

def get_account(number):
    account_found = [account for account in accounts if account.get('account_number') == number]
    return account_found[0] if account_found else None

def new_clients(name, age, cpf, address):
    if get_client(cpf):
        print(f'\n{RED}Cliente já cadastrado.{RESET}')
        return
    
    clients.append({ 'name': name, 'age': age, 'cpf': cpf, 'address': address })

    print(f'{GREEN}\nCliente criado com sucesso.{RESET}')

def new_account(client_cpf):
    if not get_client(client_cpf):
        print(f'\n{RED}Cliente não cadastrado.{RESET}')
        return
    
    account_number = len(accounts) + 1

    accounts.append({ 'agency': 0o1, 'account_number': account_number, 'client': client_cpf })

    print(f'{GREEN}\nConta criada com sucesso.{RESET}')
    print(f'\nAgencia: 0001, Conta: {account_number}')

def list_client_accounts(client_cpf):
    if not get_client(client_cpf):
        print(f'\n{RED}Cliente não cadastrado.{RESET}')
        return
    
    accounts_found = [account for account in accounts if account.get('client') == client_cpf]

    if accounts_found:
        print('\nContas cadastradas:')
        for account in accounts_found:
            account_number = account.get('account_number')
            print(f'Agencia: 0001 - Conta: {account_number}')
    else:
        print('\nNenhuma conta cadastrada.')

def withdrawal(value):
    if value <= 0:
        print(f'\n{RED}Valor para saque inválido.{RESET}')
        return
    elif value > limit:
        print(f'\n{RED}Valor máximo para saque e de R$ {limit:.2f}.{RESET}')
        return
    elif value > balance:
        print(f'\n{RED}Saldo insuficiente.{RESET}')
        return

    balance -= value
    withdrawals -= 1
    transaction_limit -= 1

    extract.append(f'Saque: R$ {value:.2f}. \nData: {date_now()}')

    print(f'{GREEN}\nSaque realizado com sucesso.{RESET}')

def deposit(value: int):
    if value <= 0:
        print(f'{RED}Valor para depósito invalido.{RESET}')
        return
    
    balance += value
    transaction_limit -= 1

    extract.append(f'Depósito: R$ {value:.2f}. \nData: {date_now()}')

    print(f'{GREEN}\nDepósito realizado com sucesso.{RESET}')

def get_extract():
    print(f'Saldo: R$ {balance:.2f}')

    if len(extract):
        print('\nExtrato:\n')
        print('\n---\n'.join(extract))

    print(f'\n{date_now()}')

while True:
    if not client_logged:
        print(menu)
        operation = int(input('> '))
        print('')

        if operation == 1:
            account_number = int(input('Informe o numero da conta: '))

            account = get_account(account_number)

            if not account:
                print(f'\n{RED}Conta inválida.{RESET}')
                continue
            
            client_logged = account.get('client')
        elif operation == 2:
            client_cpf = input('Informe o CPF (somente número): ')

            list_client_accounts( client_cpf)
        elif operation == 3:
            cpf = input('Informe o CPF (somente número): ')

            if get_client(cpf):
                print(f'\n{RED}Cliente já cadastrado.{RESET}')
                continue
            
            name = input('Informe o nome completo: ')
            age = input('Informe a data de nacimento (dd/mm/aaaa): ')
            address = input('Informe o endereço (rua, numero, bairro - cidade/sigla estado): ')

            new_clients(name, age, cpf, address)
            new_account(cpf)
        elif operation == 4:
            client_cpf = input('Informe o CPF (somente número): ')

            new_account(client_cpf)
        elif operation == 5:
            break
        else:
            print(f'{RED}Operação inválida.{RESET}')
    else:
        print(operations_menu)
        operation = int(input('> '))
        print('')

        if transaction_limit == 0 and operation in (1, 2):
            now = datetime.now()

            if now - date_start < timedelta(hours=24):
                print('Você atingiu o limite diário de transações.')
                continue

            transaction_limit = 10
            date_start = now

        if operation == 1:
            value = int(input('Digite um valor para depósito: '))

            deposit(value)
        elif operation == 2:
            if withdrawals == 0:
                print('Você atingiu o limite diário de saques.')
                continue

            value = int(input('Digite um valor para saque: '))

            withdrawal(value)
        elif operation == 3:
            get_extract()
        elif operation == 4:
            client_logged = None
            continue
        elif operation == 5:
            client_logged = None
            break
        else:
            print(f'{RED}Operação inválida.{RESET}')