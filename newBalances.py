import csv
from collections import OrderedDict
import time
import logging
from credentials import *
logging.basicConfig()
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
logging.getLogger("POSQ-RPC").setLevel(logging.DEBUG)



RPC = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(RPCUSER, RPCPASSWORD, RPCPORT))
OldCoin = .00000001
NewCoin = .0000000001
accounts = []
distribution = {}
circulation = 0
newCirculation = 0

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
    newbalance = balance * NewCoin
    if balance > 0:
        if newbalance < 1:
            newbalance = 1
        print("\n#", count, " Address = ", address)
        print('Old Balance = ', balance * OldCoin)
        print('New Balance = ', newbalance)
        distribution.update({address:'{0:.8f}'.format(float(newbalance))})
        circulation += balance
        newCirculation += newbalance
        balancecount += 1
    count += 1

print("\nTotal Addresses", count-1)
print("Total addresses with balance > 0 :", balancecount)
print('Total POSQ in circulation', circulation * OldCoin)

print('NEW Total circulation : ', newCirculation)

print("\nChecking RPC connection...")
time.sleep(3)

try :
    RPC.getinfo()
    print("RPC connection established")

except Exception as e:
    print("YOU FUCKED UP : ", e)
    print("sleeping 30 seconds")
    time.sleep(30)


print("\nBegin Distribution!\n")
count = 0
tot_distr = 0
total = 0
sendmany = {}
success = []
failures = []
totalDistributed = 0
length = len(distribution)
Ordered = OrderedDict(sorted(distribution.items(), key=lambda x: x[1],reverse=True))
for j, k in Ordered.items():

    totalDistributed += float(k)
    if count >=100:
        try:

            hash = RPC.sendmany("", sendmany)
            print("Distribution # : ", tot_distr, " | hash ", hash, " | sent : ", sendmany)
            count = 0
            success.append([hash, str(sendmany)])
            sendmany.clear()
            time.sleep(2)
            tot_distr = tot_distr + 1
        except Exception as e:
            print("Failure : ", e)
            failures.append(sendmany)
            print("Failed to send : ", sendmany)
            count = 0
            time.sleep(30)
            sendmany.clear()
    elif total == length - 1:
        try:
            print("Final Distribution")
            hash = RPC.sendmany("", sendmany)
            print("Distribution # : ", tot_distr, " | hash : ", hash, " | sent : ", sendmany)
            count = 0
            success.append([hash, sendmany])
            sendmany.clear()
            time.sleep(2)
            tot_distr = tot_distr + 1
        except Exception as e:
            print("Failure : ", e)
            failures.append(sendmany)
            print("Failed to send : ", sendmany)
            count = 0
            time.sleep(30)
            sendmany.clear()
    else:
        sendmany.update({j:float(k)})

    count = count + 1
    total +=1


print("\nWriting results to file ...")
file = open("FinishedDistribution", "w+")
file.write("Successful Distributions : \n" + str(success))
file.write("\n\n\nFailed Distributions : \n " + str(failures))
file.close()
print("Total POSQ Distributed = ", totalDistributed)

