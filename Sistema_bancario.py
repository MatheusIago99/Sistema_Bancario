import sqlite3  


conn = sqlite3.connect("sistema_bancario.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS contas (
    numero_conta INTEGER PRIMARY KEY,
    nome_cliente TEXT NOT NULL,
    saldo REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS historico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_conta INTEGER NOT NULL,
    operacao TEXT NOT NULL,
    valor REAL NOT NULL,
    FOREIGN KEY (numero_conta) REFERENCES contas(numero_conta)
)
""")

conn.commit()  


def criar_conta():
    nome = input("Digite o nome do cliente: ")
    numero_conta = int(input("Digite o número da conta (único): "))
    saldo_inicial = float(input("Digite o saldo inicial: "))

    
    cursor.execute("SELECT * FROM contas WHERE numero_conta = ?", (numero_conta,))
    if cursor.fetchone():  
        print("Número de conta já existe! Tente novamente.")
        return

    
    cursor.execute("INSERT INTO contas (numero_conta, nome_cliente, saldo) VALUES (?, ?, ?)",
                   (numero_conta, nome, saldo_inicial))
    conn.commit()
    print("Conta criada com sucesso!")


def consultar_saldo():
    numero_conta = int(input("Digite o número da conta: "))

   
    cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
    conta = cursor.fetchone()
    if conta:
        print(f"Saldo atual: R$ {conta[0]:.2f}")  
    else:
        print("Conta não encontrada!")  


def depositar():
    numero_conta = int(input("Digite o número da conta: "))
    valor = float(input("Digite o valor a ser depositado: "))

    
    cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
    conta = cursor.fetchone()
    if conta:
        novo_saldo = conta[0] + valor  
        
        cursor.execute("UPDATE contas SET saldo = ? WHERE numero_conta = ?", (novo_saldo, numero_conta))
        cursor.execute("INSERT INTO historico (numero_conta, operacao, valor) VALUES (?, 'Depósito', ?)",
                       (numero_conta, valor)) 
        conn.commit()
        print(f"Depósito realizado com sucesso! Novo saldo: R$ {novo_saldo:.2f}")
    else:
        print("Conta não encontrada!")  


def sacar():
    numero_conta = int(input("Digite o número da conta: "))
    valor = float(input("Digite o valor a ser sacado: "))

    
    cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
    conta = cursor.fetchone()
    if conta:
        if conta[0] >= valor:  
            novo_saldo = conta[0] - valor  
            cursor.execute("UPDATE contas SET saldo = ? WHERE numero_conta = ?", (novo_saldo, numero_conta))
            cursor.execute("INSERT INTO historico (numero_conta, operacao, valor) VALUES (?, 'Saque', ?)",
                           (numero_conta, valor)) 
            conn.commit()
            print(f"Saque realizado com sucesso! Novo saldo: R$ {novo_saldo:.2f}")
        else:
            print("Saldo insuficiente!")  
    else:
        print("Conta não encontrada!")  


def encerrar_conta():
    numero_conta = int(input("Digite o número da conta: "))

    
    cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
    conta = cursor.fetchone()
    if conta:
        if conta[0] == 0:  
            cursor.execute("DELETE FROM contas WHERE numero_conta = ?", (numero_conta,))
            conn.commit()
            print("Conta encerrada com sucesso!")
        else:
            print("Não é possível encerrar a conta. O saldo deve ser zero!") 
    else:
        print("Conta não encontrada!")  


def menu():
    while True:
        print("\n--- Sistema Bancário ---")
        print("1. Criar conta")
        print("2. Consultar saldo")
        print("3. Depositar")
        print("4. Sacar")
        print("5. Encerrar conta")
        print("6. Sair")

        opcao = input("Escolha uma opção: ")

        
        if opcao == "1":
            criar_conta()
        elif opcao == "2":
            consultar_saldo()
        elif opcao == "3":
            depositar()
        elif opcao == "4":
            sacar()
        elif opcao == "5":
            encerrar_conta()
        elif opcao == "6":
            print("Saindo do sistema...")  
            break
        else:
            print("Opção inválida! Tente novamente.")  


menu()


conn.close()
