from datetime import datetime, timedelta

RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

balance = 500
limit = 500
withdrawals = 3
transaction_limit = 10
extract = []
date_start = datetime.now()

menu = '''
###############################
# Selecione a opção desejada: #
#                             #
# Depósito: 1        Saque: 2 #
# Extrato:  3        Sair:  4 #
#                             #
###############################
'''

def date_now ():
    return datetime.now().strftime('%d/%m/%Y %H:%M')

while True:
    print(menu)
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

        if value <= 0:
            print(f'{RED}Valor para depósito invalido.{RESET}')
            continue
        
        balance += value
        transaction_limit -= 1

        extract.append(f'Depósito: R$ {value:.2f}. \nData: {date_now()}')

        print(f'{GREEN}\nDepósito realizado com sucesso.{RESET}')
    elif operation == 2:
        if withdrawals == 0:
            print('Você atingiu o limite diário de saques.')
            continue

        value = int(input('Digite um valor para saque: '))

        if value <= 0:
            print(f'\n{RED}Valor para saque inválido.{RESET}')
            continue
        elif value > limit:
            print(f'\n{RED}Valor máximo para saque e de R$ {limit:.2f}.{RESET}')
            continue
        elif value > balance:
            print(f'\n{RED}Saldo insuficiente.{RESET}')
            continue

        balance -= value
        withdrawals -= 1
        transaction_limit -= 1

        extract.append(f'Saque: R$ {value:.2f}. \nData: {date_now()}')

        print(f'{GREEN}\nSaque realizado com sucesso.{RESET}')
    elif operation == 3:
        print(f'Saldo: R$ {balance:.2f}')

        if len(extract):
            print('\nExtrato:\n')
            print('\n---\n'.join(extract))

        print(f'\n{date_now()}')
    elif operation == 4:
        break
    else:
        print(f'{RED}Operação inválida.{RESET}')