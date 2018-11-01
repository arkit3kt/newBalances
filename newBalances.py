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
        accounts.append([{'address':row[1], 'balance':row[2]}])

# Determine new Balance + Circulation
balancecount = 0
for i in range(len(accounts) - 1):
    balance = accounts[count][0]['balance']
    address = accounts[count][0]['address']
    address = str(address)
    balance = float(balance)
    if balance > 0:
        print("\n#", count, " Address = ", address)
        print('Old Balance = ', balance * OldCoin)
        print('New Balance = ', balance * NewCoin)
        newbalance += balance
        balancecount += 1
    count += 1

print("\nTotal Addresses", count-1)
print("Total addresses with balance > 0 :", balancecount)
print('Total POSQ in circulation', newbalance * OldCoin)
print('NEW Total circulation : ', newbalance * NewCoin)




