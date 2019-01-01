from dbModels import *


class processData:
    """
    class takes 1 param :users [all users in DB]
    """
    def __init__(self, users):
        self.users = users
        self.convertData(users)

    def convertData(self, users):
        """
        convert users balances 100:1
        and clean up discord IDs
        """
        self.users = users
        print("Gathering New Balances and cleaning dIDs")
        for u in users:
            balance = u.total
            newbalance = "{0:0.8f}".format(float(balance / 100))
            u.id_number = self.cleanDiscordID(u.id_number)

            u.total = newbalance
            print("UID :", u.uid, " dID :", u.id_number,
                  "Old Balance : {0:0.8f}".format(balance), "\t New Bal :", newbalance)
        print("New Balances assigned and dIDs cleaned successfully!")
        self.addData(users)


    def cleanDiscordID(self, dID):
        """
        strip < @ > from discord IDs
        """
        self.dID = dID
        dID = str(dID).strip("<@").strip(">")
        return dID


    def prepNewDatabase(self):
        """
        check for existing database
        if it doesn't exist, create it
        """
        print("Checking Databases...")
        existing_databases = engine.execute("SHOW DATABASES;")
        # Results are a list of single item tuples, so unpack each tuple
        existing_databases = [d[0] for d in existing_databases]
        database = "posq"

        # Create database if not exists
        if database not in existing_databases:
            engine.execute("CREATE DATABASE {0}".format(database))
            print("Created database : '{0}'".format(database))
        engine2 = create_engine('mysql+pymysql://{0}:{1}@127.0.0.1/posq?host=127.0.0.1?port={2}/charset=utf8/'.format(DBUNAME, DBPASS, DBPORT))
        # create a configured "Session" class
        conn2 = engine2.connect()
        Session2 = sessionmaker(bind=conn2)
        # create a Session
        posqDB = Session2()
        print("Created posqDB session!")
        # Create all tables in meta
        metaModels(engine2)
        return posqDB

    def addData(self, users):
        posqDB = self.prepNewDatabase()
        print("Adding data to posqDB...")

        try:
            for u in users:
                transactions = session.query(Transactions)
                gambs = session.query(Gambles)
                user = pUsers()
                user.uid = u.uid
                user.bid = u.bct_id
                user.did = u.id_number
                user.uname = u.user_id
                user.bal = u.total
                user.addr = u.address
                user.Lflip = u.last_bet
                user.Lroll = u.last_roll
                posqDB.add(user)

            for t in transactions:
                tx = pTxs()
                tx.uid = t.uid
                tx.amount = t.amount
                tx.tid = t.total
                tx.type = None
                tx.hash = t.transactions
                posqDB.add(tx)

            for w in gambs:
                if w.game == "CoinFlip":
                    w.game = "flip"
                elif w.game == "dice":
                    w.game = "roll"
                gambles = pGambles()
                gambles.uid = w.uid
                gambles.gid = w.win_id
                gambles.bet = None
                gambles.game = w.game
                gambles.outcome = None
                gambles.paid = w.amount
                posqDB.add(gambles)

            posqDB.commit()
            print("Data added successfully!!!")
        except Exception as e:
            print("FAILED : ", e)


users = session.query(User).all()
processData(users)


"""
test
for u in users:
    for w in u.winnings:
        print(w)
        for t in u.transactions:
            print(t)
"""







