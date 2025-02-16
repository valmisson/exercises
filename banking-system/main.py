RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

balance = 500
limit = 500
withdrawals = 3
extract = []

menu = '''
###############################
# Selecione a opção desejada: #
#                             #
# Depósito: 1        Saque: 2 #
# Extrato:  3        Sair:  4 #
#                             #
###############################
'''

while True:
    print(menu)
    operation = int(input('> '))
    print('')

    if operation == 1:
        value = int(input('Digite um valor para depósito: '))

        if value <= 0:
            print(f'{RED}Valor para depósito invalido.{RESET}')
            continue
        
        balance += value
        extract.append(f'Depósito: R$ {value:.2f}')

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
        extract.append(f'Saque: R$ {value:.2f}')

        print(f'{GREEN}\nSaque realizado com sucesso.{RESET}')
    elif operation == 3:
        print(f'Saldo: R$ {balance:.2f}')
        if len(extract):
            print('\nExtrato')
            print('\n'.join(extract))
    elif operation == 4:
        break
    else:
        print(f'{RED}Operação inválida.{RESET}')