import csv
OldCoin = .00000001
NewCoin = .000000001
accounts = []
count = 1
newbalance = 0
# open csv and add addresses + balances to accounts list
with open('C:\posqdbSnapshot1\Addresses.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            accounts.append([{'address':row[1], 'balance':row[2]}])
        except:
            accounts.append([{'address':row[1], 'balance':row[2]}])
# Determine new Balance + Circulation
for i in range(len(accounts) - 1):
    balance = accounts[count][0]['balance']
    address = accounts[count][0]['address']
    address = str(address)
    balance = float(balance)
    print("\nAddress = ", address)
    print('Old Balance = ', balance * OldCoin)
    print('New Balance = ', balance * NewCoin)
    newbalance += balance

    count += 1
print('\nTotal POSQ in circulation', newbalance  * OldCoin)
print('NEW Total circulation : ', newbalance * NewCoin)




