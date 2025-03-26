from datetime import datetime
from typing import List, Optional, Dict
from abc import ABC, abstractmethod
import os

# Base Transaction classes
class Transaction(ABC):
    def __init__(self, amount: float):
        self.amount = amount
    
    @abstractmethod
    def register(self, account: 'Account') -> None:
        pass

class Deposit(Transaction):
    def register(self, account: 'Account') -> None:
        account.deposit(self.amount)

class Withdrawal(Transaction):
    def register(self, account: 'Account') -> None:
        account.withdraw(self.amount)

# History tracking
class History:
    def __init__(self):
        self.transactions: List[str] = []
    
    def add_transaction(self, transaction: str) -> None:
        self.transactions.append(f"{transaction} - Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Client classes
class Client:
    def __init__(self, address: str):
        self.address = address
        self.accounts: List['Account'] = []
    
    def add_account(self, account: 'Account') -> None:
        self.accounts.append(account)
    
    def perform_transaction(self, account: 'Account', transaction: Transaction) -> None:
        transaction.register(account)

class Person(Client):
    def __init__(self, cpf: str, name: str, birth_date: datetime, address: str):
        super().__init__(address)
        self.cpf = cpf
        self.name = name
        self.birth_date = birth_date

# Account classes
class Account:
    def __init__(self, client: Client, number: int, branch: str):
        self._balance = 0.0
        self.number = number
        self.branch = branch
        self.client = client
        self.history = History()
        self._daily_withdrawals = 0
        self._daily_transactions = 0
        self._last_transaction_date = datetime.now().date()
        client.add_account(self)

    @property
    def balance(self) -> float:
        return self._balance

    def _reset_daily_limits(self) -> None:
        current_date = datetime.now().date()
        if current_date != self._last_transaction_date:
            self._daily_transactions = 0
            self._last_transaction_date = current_date

    def withdraw(self, amount: float) -> bool:
        self._reset_daily_limits()
        if isinstance(self, CheckingAccount):
            if (amount <= 0 or 
                amount > self._balance or 
                amount > BankSystem.WITHDRAWAL_LIMIT or
                self._daily_withdrawals >= BankSystem.DAILY_WITHDRAWAL_LIMIT or
                self._daily_transactions >= BankSystem.DAILY_TRANSACTION_LIMIT):
                return False
            
            self._balance -= amount
            self._daily_withdrawals += 1
            self._daily_transactions += 1
            self.history.add_transaction(f"Saque: R$ {amount:.2f}")
            return True
        else:
            if amount <= self._balance:
                self._balance -= amount
                self.history.add_transaction(f"Saque: R$ {amount:.2f}")
                return True
            return False

    def deposit(self, amount: float) -> bool:
        self._reset_daily_limits()
        if amount <= 0 or self._daily_transactions >= BankSystem.DAILY_TRANSACTION_LIMIT:
            return False
            
        self._balance += amount
        self._daily_transactions += 1
        self.history.add_transaction(f"Depósito: R$ {amount:.2f}")
        return True

class CheckingAccount(Account):
    def __init__(self, client: Client, number: int, branch: str, limit: float, withdrawal_limit: int):
        super().__init__(client, number, branch)
        self.limit = limit
        self.withdrawal_limit = withdrawal_limit

# Main system class
class BankSystem:
    # Constants as class attributes
    RED = '\033[31m'
    GREEN = '\033[32m'
    RESET = '\033[0m'
    
    # Transaction limits as class attributes
    WITHDRAWAL_LIMIT = 500.0
    DAILY_TRANSACTION_LIMIT = 10
    DAILY_WITHDRAWAL_LIMIT = 3

    def __init__(self):
        self.clients: Dict[str, Person] = {}
        self.accounts: Dict[int, Account] = {}
        self.logged_client: Optional[Person] = None
        self.current_account: Optional[Account] = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_main_menu(self) -> str:
        return '''
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

    def display_operations_menu(self) -> str:
        return '''
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

    def create_client(self) -> None:
        cpf = input('Informe o CPF (somente número): ')
        if cpf in self.clients:
            print(f'\n{self.RED}Cliente já cadastrado.{self.RESET}')
            return

        name = input('Informe o nome completo: ')
        date_str = input('Informe a data de nascimento (dd/mm/aaaa): ')
        address = input('Informe o endereço: ')
        
        try:
            birth_date = datetime.strptime(date_str, '%d/%m/%Y')
            client = Person(cpf, name, birth_date, address)
            self.clients[cpf] = client
            print(f'{self.GREEN}\nCliente criado com sucesso.{self.RESET}')
            
            self.create_account(cpf)
        except ValueError:
            print(f'{self.RED}Data de nascimento inválida.{self.RESET}')

    def create_account(self, cpf: str) -> None:
        if cpf not in self.clients:
            print(f'\n{self.RED}Cliente não encontrado.{self.RESET}')
            return
            
        account_number = len(self.accounts) + 1
        client = self.clients[cpf]
        account = CheckingAccount(
            client=client,
            number=account_number,
            branch="0001",
            limit=500.0,
            withdrawal_limit=3
        )
        self.accounts[account_number] = account
        
        print(f'{self.GREEN}\nConta criada com sucesso.{self.RESET}')
        print(f'\nAgência: 0001, Conta: {account_number}')

    def list_accounts(self, cpf: str) -> None:
        if cpf not in self.clients:
            print(f'\n{self.RED}Cliente não encontrado.{self.RESET}')
            return
            
        client = self.clients[cpf]
        if not client.accounts:
            print('\nNenhuma conta encontrada.')
            return
            
        print('\nContas cadastradas:')
        for account in client.accounts:
            print(f'Agência: {account.branch} - Conta: {account.number}')

    def make_deposit(self) -> None:
        try:
            amount = float(input('Digite o valor para depósito: '))
            if amount <= 0:
                print(f'\n{self.RED}Valor inválido para depósito.{self.RESET}')
                return
            
            if self.current_account._daily_transactions >= BankSystem.DAILY_TRANSACTION_LIMIT:
                print(f'\n{self.RED}Limite de transações diárias excedido.{self.RESET}')
                return
                
            deposit = Deposit(amount)
            self.logged_client.perform_transaction(self.current_account, deposit)
            print(f'{self.GREEN}\nDepósito realizado com sucesso.{self.RESET}')
        except ValueError:
            print(f'{self.RED}Valor inválido.{self.RESET}')

    def make_withdrawal(self) -> None:
        try:
            amount = float(input('Digite o valor para saque: '))
            if amount <= 0:
                print(f'\n{self.RED}Valor inválido para saque.{self.RESET}')
                return
            
            if amount > self.WITHDRAWAL_LIMIT:
                print(f'\n{self.RED}Valor excede o limite máximo de R$ {self.WITHDRAWAL_LIMIT:.2f} por saque.{self.RESET}')
                return
            
            if isinstance(self.current_account, CheckingAccount):
                if self.current_account._daily_withdrawals >= BankSystem.DAILY_WITHDRAWAL_LIMIT:
                    print(f'\n{self.RED}Limite de saques diários excedido.{self.RESET}')
                    return
                
                if self.current_account._daily_transactions >= BankSystem.DAILY_TRANSACTION_LIMIT:
                    print(f'\n{self.RED}Limite de transações diárias excedido.{self.RESET}')
                    return
                    
                if amount > self.current_account.balance:
                    print(f'\n{self.RED}Saldo insuficiente. Seu saldo é R$ {self.current_account.balance:.2f}{self.RESET}')
                    return
                
                withdrawal = Withdrawal(amount)
                self.logged_client.perform_transaction(self.current_account, withdrawal)
                print(f'{self.GREEN}\nSaque realizado com sucesso.{self.RESET}')
                
        except ValueError:
            print(f'{self.RED}Valor inválido.{self.RESET}')

    def show_statement(self) -> None:
        if not self.current_account:
            return
            
        print(f'Saldo atual: R$ {self.current_account.balance:.2f}')
        if isinstance(self.current_account, CheckingAccount):
            print(f'\nSaques disponíveis no dia: {self.DAILY_WITHDRAWAL_LIMIT - self.current_account._daily_withdrawals}')
            print(f'Transações disponíveis hoje: {self.DAILY_TRANSACTION_LIMIT - self.current_account._daily_transactions}')
        print('\nExtrato:')
        for transaction in self.current_account.history.transactions:
            print(f'{transaction}')

    def run(self) -> None:
        while True:
            if not self.logged_client:
                print(self.display_main_menu())
                try:
                    option = int(input('> '))
                    print()

                    if option == 1:
                        account_number = int(input('Informe o número da conta: '))
                        if account_number in self.accounts:
                            self.current_account = self.accounts[account_number]
                            self.logged_client = self.current_account.client
                        else:
                            print(f'\n{self.RED}Conta não encontrada.{self.RESET}')
                    
                    elif option == 2:
                        cpf = input('Informe o CPF: ')
                        self.list_accounts(cpf)
                    
                    elif option == 3:
                        self.create_client()
                    
                    elif option == 4:
                        cpf = input('Informe o CPF: ')
                        self.create_account(cpf)
                    
                    elif option == 5:
                        break
                    
                    else:
                        print(f'{self.RED}Opção inválida.{self.RESET}')
                
                except ValueError:
                    print(f'{self.RED}Entrada inválida.{self.RESET}')
            
            else:
                print(self.display_operations_menu())
                try:
                    option = int(input('> '))
                    print()

                    if option == 1:
                        self.make_deposit()
                    elif option == 2:
                        self.make_withdrawal()
                    elif option == 3:
                        self.show_statement()
                    elif option == 4:
                        self.logged_client = None
                        self.current_account = None
                    elif option == 5:
                        break
                    else:
                        print(f'{self.RED}Opção inválida.{self.RESET}')
                
                except ValueError:
                    print(f'{self.RED}Entrada inválida.{self.RESET}')

if __name__ == "__main__":
    system = BankSystem()
    system.run()