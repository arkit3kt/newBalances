from sqlalchemy import create_engine, MetaData, Column, VARCHAR, INT, BIGINT, FLOAT, ForeignKey, Table, collate
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
import logging
from credentials import *

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="test.log", level=logging.INFO, format=LOG_FORMAT, filemode='w')
logger = logging.getLogger()
logging.basicConfig()
logging.getLogger("sqlalchemy").setLevel(logging.DEBUG)

base = declarative_base()
engine = create_engine('mysql+pymysql://{0}:{1}@127.0.0.1/{2}?host=127.0.0.1?port={3}/charset=utf8/'.format(DBUNAME, DBPASS, DB, DBPORT))
# create a configured "Session" class
conn = engine.connect()
Session = sessionmaker(bind=conn)
# create a Session
session = Session()


"""
First group of DB models is for original database
Second group of DB class models is for new database
"""
class User(base):
    __tablename__ = "poseidon"
    uid = Column(BIGINT, primary_key=True)
    user_id = Column(VARCHAR)
    address = Column(VARCHAR)
    id_number = Column(VARCHAR)
    total = Column(FLOAT)
    bct_id = Column(INT)
    last_bet = Column(BIGINT)
    last_roll = Column(BIGINT)
    transactions = relationship('Transactions', backref='owner')
    winnings = relationship('Gambles', backref='owner')

    def __repr__(self):
        return "<Users(uid=%s, did=%s, uname=%s, addr=%s bal=%s, bid=%s, L_flip=%s, L_roll=%s, tx=%s)>" \
               % (self.uid, self.id_number, self.user_id, self.address, self.total, self.bct_id, self.last_bet, self.last_roll, self.transactions)

class Transactions(base):
    __tablename__ = "transactions"
    amount = Column(FLOAT)
    transactions = Column(VARCHAR)
    uid = Column(BIGINT, ForeignKey('poseidon.uid'))
    total = Column(BIGINT, primary_key=True)

    def __repr__(self):
        return "<Txs(uid=%s, txid=%s, amount=%s, hash=%s)>" % (self.uid, self.total, self.amount, self.transactions)

class Gambles(base):
    __tablename__ = "winnings"
    uid = Column(BIGINT, ForeignKey('poseidon.uid'))
    amount = Column(FLOAT)
    game = Column(VARCHAR)
    win_id = Column(BIGINT, primary_key=True)

    def __repr__(self):
        return "<Gambles(uid=%s, wid=%s, amount=%s, game=%s)>" % (self.uid, self.win_id,self.amount, self.game)

"""
**POSQDB MODELS**
"""


class pUsers(base):
    __tablename__ = "users"
    uid = Column(BIGINT, primary_key=True)
    did = Column(VARCHAR)
    bid = Column(INT, default=None)
    uname = Column(VARCHAR)
    addr = Column(VARCHAR)
    bal = Column(FLOAT)
    LFlip = Column(BIGINT, default=None)
    LRoll = Column(BIGINT, default=None)
    txs = relationship('pTxs', backref='owner')
    gambles = relationship('pGambles', backref='owner')

    def __repr__(self):
        return "<Users(uid=%s, did=%s, bid=%s, uname=%s addr=%s, bal=%s, Lflip=%s, Lroll=%s, tx=%s, wins=%s)>" \
               % (self.uid, self.did, self.bid, self.uname, self.addr, self.bal, self.Lflip, self.Lroll, self.txs, self.gambles)

class pTxs(base):
    __tablename__ = "txs"
    tid = Column(BIGINT, primary_key=True)
    uid = Column(BIGINT, ForeignKey('users.uid'))
    type = Column(VARCHAR)
    amount = Column(FLOAT)
    hash = Column(VARCHAR, default=None)


    def __repr__(self):
        return "<Txs(uid=%s, txid=%s, amount=%s, type=%s, hash=%s)>" % (self.uid, self.tid, self.amount, self.type, self.hash)

class pGambles(base):
    __tablename__ = "gambles"
    gid = Column(BIGINT, primary_key=True)
    uid = Column(BIGINT, ForeignKey('users.uid'))
    game = Column(VARCHAR)
    outcome = Column(VARCHAR)
    bet = Column(FLOAT)
    paid = Column(FLOAT, default=None)


    def __repr__(self):
        return "<Gambles(uid=%s, gid=%s, amount=%s, game=%s, outcome=%s)>" % (self.uid, self.gid, self.amount, self.game, self.outcome)

class Counter(base):

    __tablename__ = "counter"
    count = Column(BIGINT, default=None, primary_key=True)

    def __repr__(self):
        return "<counter(count=%s)>" % (self.count)


"""
**TABLE METADATA MODELS FOR NEW DB**
"""
def metaModels(engine):
    meta = MetaData(engine)
    # Register users, txs, gambles, and counter to metadata
    t1 = Table('users', meta,
               Column('uid', INT, primary_key=True),
               Column('did', VARCHAR(50)),
               Column('bid', BIGINT),
               Column('bal', FLOAT, default=None),
               Column('uname', VARCHAR(100), default=None),
               Column('addr', VARCHAR(34)),
               Column('Lflip', BIGINT, default=None),
               Column('Lroll', BIGINT, default=None),
               mysql_engine='InnoDB',
               mysql_charset='utf8mb4'
               )

    t2 = Table('txs', meta,
               Column('tid', BIGINT, primary_key=True),
               Column('uid', BIGINT),
               Column('type', VARCHAR(3)),
               Column('amount', FLOAT),
               Column('hash', VARCHAR(100), default=None),
               mysql_engine='InnoDB',
               mysql_charset='utf8mb4'
               )

    t3 = Table('gambles', meta,
               Column('gid', BIGINT, primary_key=True),
               Column('uid', BIGINT),
               Column('game', VARCHAR(4)),
               Column('outcome', VARCHAR(1)),
               Column('bet', FLOAT),
               Column('paid', FLOAT, default=None),
               mysql_engine='InnoDB',
               mysql_charset='utf8mb4'
               )
    t4 = Table('counter', meta,
               Column('count', BIGINT, default=None, primary_key=True),
               mysql_engine='InnoDB',
               mysql_charset='utf8mb4'
               )
    meta.create_all()