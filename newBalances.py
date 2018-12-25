import csv
import time
import logging
logging.basicConfig()
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
logging.getLogger("POSQ-RPC").setLevel(logging.DEBUG)

rpc_user = "posqrpc"
rpc_password = "password"

RPC = AuthServiceProxy("http://%s:%s@127.0.0.1:16978"%(rpc_user, rpc_password))

OldCoin = .00000001
NewCoin = .0000000001
accounts = []
distribution = []

circulation = 0


# open csv and add addresses + balances to accounts list
with open('balances.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        accounts.append([{'address':row[1], 'balance':row[2]}])

# Determine new Balance + Circulation
count = 1
balancecount = 0
for i in range(len(accounts) - 1):
    balance = accounts[count][0]['balance']
    address = accounts[count][0]['address']
    address = str(address)
    balance = float(balance)
    if balance > 0:
        newbalance = balance * NewCoin
        #print("\n#", count, " Address = ", address)
        #print('Old Balance = ', balance * OldCoin)
        #print('New Balance = ', newbalance)
        distribution.append(["{0:.8f}".format(newbalance), address])
        circulation += balance
        balancecount += 1
    count += 1

print("\nTotal Addresses", count-1)
print("Total addresses with balance > 0 :", balancecount)
print('Total POSQ in circulation', circulation * OldCoin)
print("Current ratio = {}:1".format(int(NewCoin * 1000000000000)))
print('NEW Total circulation : ', circulation * NewCoin)


## LEAVE HASH, TIMER AND RPC TEST COMMENTED OUT TILL PREP
#print("*** TESTING RPC ***")
#print(RPC.getinfo())

print("\nBegin Distribution!\n")
count = 0
distribution.sort(reverse=True)
failures = []
success = []
for i in distribution:
    amount = i[0]
    address = i[1]
    try:
        #hash = RPC.sendtoaddress(address, amount)
        success.append([address, amount])#, hash])
        print("Distribution # {0} | {1} sent | {2} | {3}".format(count, address, amount, "hash"))

        # time.sleep(5)
    except:
        failures.append([address, amount])
        print("Failed to send {0} to {1}".format(amount, address) )
    count+=1


print("\nWriting results to file ...")
file = open("FinishedDistribution", "w+")
file.write("Successful Distributions : \n" + str(success))
file.write("\n\n\nFailed Distributions : \n " + str(failures))
file.close()
print("Distribution Complete!")

