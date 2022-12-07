import time,os,sqlite3,json
from eth_account import Account


def createNewETHWallet():
    pwd = os.getcwd()
    db_pwd = pwd + "/xen.db"
    print(db_pwd)
    conn = sqlite3.connect(db_pwd)
    c = conn.cursor()
    for i in range(100000):
        c.execute("SELECT COUNT(*) FROM xen;")
        count = c.fetchall()[0][0]
        print(count)
        Account.enable_unaudited_hdwallet_features()
        account,mnemonic=Account.create_with_mnemonic()
        address=account.address
        private_key= account.key.hex()
        phrases=mnemonic
        print("current count:"+str(count))
        print("address: "+address)
        print("hex: "+private_key)
        print("mnemonic: "+phrases)
        c.execute("INSERT INTO atlendis (id,address,private_key,phrases)VALUES('%s','%s','%s','%s')"%(current,address, private_key, phrases))
        conn.commit()
    conn.close()
