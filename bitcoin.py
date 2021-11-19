# Bitcoin cli based simple wallet
from bit import PrivateKeyTestnet

def main():
    print(f'''
    [1] Create New Bitcoin Account
    [2] Import Account
    [3] Show All Accounts
    [4] Exit
    ''')

    command = int(input('Enter Number : '))

    if(command == 1):
        # create new bitcoin keys
        wallet_name = str(input('Enter Wallet Name : '))
        my_wallet = PrivateKeyTestnet()
        my_wallet_private_key = my_wallet.to_wif()
        my_wallet_public_key = my_wallet.pub_to_hex()
        my_wallet_address = my_wallet.address
        # my_wallet_balance = my_wallet.get_balance('btc')

        f_wallet = open('bitcoin-wallet.wallet', 'a')
        f_wallet.write(f'{wallet_name}:{my_wallet_private_key}\n')
        f_wallet.close()

        print('>> Your Bitcoin Account Created')
        print(f'''
        Wallet Name     : {wallet_name}
        Private Key     : {my_wallet_private_key}
        Public Key      : {my_wallet_public_key}
        Address         : {my_wallet_address}
        ''')
        wallet(wallet_name, my_wallet_private_key)
        
    elif(command == 2):
        # import new bitcoin wallet
        wallet_wif = str(input('Enter Bitcoin Account WIF : '))
        new_wallet_name = str(input('Enter Wallet Name : '))
        f_wallet = open('bitcoin-wallet.wallet', 'a')
        f_wallet.write(f'{new_wallet_name}:{wallet_wif}\n')
        f_wallet.close()
        wallet(new_wallet_name, wallet_wif)
        

    elif(command == 3):
        # show all bitcoin wallets
        f_wallet_all = open('bitcoin-wallet.wallet', 'r')
        wallets = f_wallet_all.read().split('\n')
        wallets.pop()
        wallet_list = []
        
        for account in wallets:
            item = account.split(':')
            wallet_list.append((item[0], item[1]))
        
        for i in range(len(wallet_list)):
            print(f'{i + 1} > {wallet_list[i]}')

        wallet_num = int(input('Enter number to chose wallet : '))
        if(wallet_num > len(wallet_list)):
            print('Please try again')
            main()
        
        _wallet = wallet_list[wallet_num - 1]
        wallet(_wallet[0], _wallet[1])

    elif(command == 4):
        print('Good Bye')
    
    else:
        print('Please Try Again')
        main()

# main wallet function for control your wallets
def wallet(wallet_name, wif):
    my_wallet = PrivateKeyTestnet(wif)
    print(f'>> ({wallet_name})')
    print('''
    [1] Send
    [2] Recive
    [3] Balance
    [4] Transaction History
    [5] Wallet Information
    [6] Go Back
    ''')

    w = int(input('Enter Number : '))
    
    if(w == 1):
        reciver_address = str(input('Enter Valid Bitcoin Address : '))
        amount = float(input('Enter amount in btc : '))
        outputs = [(reciver_address, amount, 'btc')]
        tnx_res_hash = my_wallet.send(outputs)
        print(f'>> Tnx Hash : {tnx_res_hash}')
        wallet(wallet_name, wif)

    elif(w == 2):
        _address = my_wallet.address
        print(f'({wallet_name}) Address : {_address}')
        wallet(wallet_name, wif)
    
    elif(w == 3):
        balance = my_wallet.get_balance('btc')
        print(f'({wallet_name}) Balance : {balance} BTC')
        wallet(wallet_name, wif)

    elif(w == 4):
        tnx = my_wallet.get_transactions()
        for _tnx in tnx:
            print(_tnx)
        wallet(wallet_name, wif)
    
    elif(w == 5):
        my_wallet_private_key = my_wallet.to_wif()
        my_wallet_public_key = my_wallet.pub_to_hex()
        my_wallet_address = my_wallet.address
        my_wallet_balance = my_wallet.get_balance('btc')

        print(f'''
        Wallet name     : {wallet_name}
        Private Key     : {my_wallet_private_key}
        Public Key      : {my_wallet_public_key}
        Address         : {my_wallet_address}
        Balance         : {my_wallet_balance} BTC
        ''')
        wallet(wallet_name, wif)
    
    elif(w == 6):
        main()

if __name__ == '__main__':
    main()