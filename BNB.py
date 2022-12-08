import os,sqlite3,json
import time
import math
from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware

HTTPProvider = "https://bsc-dataseed.binance.org/"

address = "********"
# 这里填写下主钱包地址 用来给子钱包发送bnb
private_key = "******"
# 这里填写下主钱包私钥

def creat_wallet(number):
    pwd = os.getcwd()
    db_pwd = pwd + "/xen.db"
    print(db_pwd)
    conn = sqlite3.connect(db_pwd)
    c = conn.cursor()
    for i in range(number):
        c.execute("SELECT COUNT(*) FROM BSC;")
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
        c.execute("INSERT INTO BSC (id,address,private_key,phrases)VALUES('%s','%s','%s','%s')"%(count,address, private_key, phrases))
        conn.commit()
    conn.close()
def translate_BNB():





    pwd = os.getcwd()
    db_pwd = pwd + "/xen.db"
    conn = sqlite3.connect(db_pwd)
    c = conn.cursor()
    c.execute('SELECT * FROM BSC')
    rows = c.fetchall()
    web3 = Web3(Web3.HTTPProvider(HTTPProvider))
    from_address = web3.toChecksumAddress(address)
    for adds in rows[50:100]:
        count=adds[0]
        to_address=adds[1]
        print("第"+str(count)+"个地址")
        print ("发送代币到： "+to_address)
        from_address = Web3.toChecksumAddress(from_address)
        to_address = Web3.toChecksumAddress(to_address)
        nonce = web3.eth.getTransactionCount(from_address)
        from_address_balance = web3.eth.get_balance(from_address) / 1e18
        print("当前账户BNB余额： "+str(from_address_balance))
        target_address_balance = web3.eth.get_balance(to_address) / 1e18
        print("目标账户BNB余额： "+str(target_address_balance))
        params = {
            'from': from_address,
            'nonce': nonce,
            'to': to_address,
            'value': web3.toWei(0.001, 'ether'),
            'gas': 21000,
            'gasPrice':web3.toWei(5, 'gwei'),
            'chainId': 56,
        }
        try:
            signed_tx = web3.eth.account.signTransaction(params, private_key=private_key)
            txn = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print ("hash值： "+str(web3.toHex(txn)))
        except Exception as e:
            print (e)
        print("###############")
        time.sleep(5)
    conn.close()
def update_balance():

    pwd = os.getcwd()
    db_pwd = pwd + "/xen.db"
    conn = sqlite3.connect(db_pwd)
    c = conn.cursor()
    c.execute('SELECT * FROM BSC ')
    rows = c.fetchall()
    web3 = Web3(Web3.HTTPProvider(HTTPProvider))
    for adds in rows[0:100]:
        count=adds[0]
        print("第" + str(count) + "个地址")
        address = adds[1]
        BNB_balance = web3.eth.get_balance(address) / 1e18
        print("当前账户地址： " + str(address))
        print("当前账户BNB余额： " + str(BNB_balance))
        c.execute("UPDATE BSC SET BNB = '%s' where address=='%s';" % (BNB_balance, address))
        conn.commit()
        print("###############")
    conn.close()

def claimRank():
    web3 = Web3(Web3.HTTPProvider(HTTPProvider))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    xen_contract = web3.toChecksumAddress("0x2ab0e9e4ee70fff1fb9d67031e44f6410170d00e")
    with open ("xen.json","r") as f:
        abi = json.loads(f.read())
    contract = web3.eth.contract(address=xen_contract, abi=abi)

    pwd = os.getcwd()
    db_pwd = pwd + "/xen.db"
    conn = sqlite3.connect(db_pwd)
    c = conn.cursor()
    c.execute('SELECT * FROM BSC')
    rows = c.fetchall()
    for i in rows[50:100]:
        count=i[0]
        addresss=i[1]
        private_key=i[2]
        address = web3.toChecksumAddress(addresss)
        balance = web3.eth.get_balance(addresss) / 1e18
        print("第" + str(count) + "个地址")
        print("当前账户地址： " + str(address))
        print("当前账户密钥： " + str(private_key))
        print("当前账户BNB余额： " + str(balance))
        nonce = web3.eth.getTransactionCount(address)
        term=300
        params = {
            'from':address,
            'nonce': nonce,
            'gas': 172076,
            'gasPrice':web3.toWei(5, 'gwei'),
            'chainId': 56,
        }

        transaction = contract.functions.claimRank(term).buildTransaction(params)
        try:
            signed_tx = web3.eth.account.signTransaction(transaction, private_key=private_key)
            txn = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print("hash值： " + str(web3.toHex(txn)))
            c.execute("UPDATE BSC SET hash = '%s' where address=='%s';" % (str(web3.toHex(txn)), address))
            c.execute("UPDATE BSC SET status = '%s' where address=='%s';" % ("1", address))
            conn.commit()
        except Exception as e:
            print(e)
            c.execute("UPDATE BSC SET status = '%s' where address=='%s';" % ("0", address))
            conn.commit()
        time.sleep(5)
        print("################")
def userMints():
    web3 = Web3(Web3.HTTPProvider(HTTPProvider))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    xen_contract = web3.toChecksumAddress("0x2ab0e9e4ee70fff1fb9d67031e44f6410170d00e")
    with open("xen.json", "r") as f:
        abi = json.loads(f.read())
    contract = web3.eth.contract(address=xen_contract, abi=abi)

    pwd = os.getcwd()
    db_pwd = pwd + "/xen.db"
    conn = sqlite3.connect(db_pwd)
    c = conn.cursor()
    c.execute('SELECT * FROM BSC')
    rows = c.fetchall()
    for i in rows[0:100]:
        count = i[0]
        addresss = i[1]
        private_key = i[2]
        address = web3.toChecksumAddress(addresss)
        #balance = web3.eth.get_balance(addresss) / 1e18
        print("第" + str(count) + "个地址")
        print("当前账户地址： " + str(address))
        #print("当前账户密钥： " + str(private_key))
        #print("当前账户BNB余额： " + str(balance))
        userMints= contract.functions.userMints(addresss).call()
        print(userMints)
        term=int(userMints[1])
        maturityTs=int(userMints[2])
        rank=int(userMints[3])
        amplifier=int(userMints[4])
        eaaRate=int(userMints[5])
        #Estimated=term * math.log2(rank) * amplifier * eaaRate(rank)
        c.execute("UPDATE BSC SET term = '%s' where address=='%s';" % (term, address))
        conn.commit()
        c.execute("UPDATE BSC SET maturityTs = '%s' where address=='%s';" % (maturityTs, address))
        conn.commit()
        c.execute("UPDATE BSC SET rank = '%s' where address=='%s';" % (rank, address))
        conn.commit()
        c.execute("UPDATE BSC SET amplifier = '%s' where address=='%s';" % (amplifier, address))
        conn.commit()
        c.execute("UPDATE BSC SET eaaRate = '%s' where address=='%s';" % (eaaRate, address))
        conn.commit()
        print("################")
if __name__ == '__main__':
    #creat_wallet(2)
    #translate_BNB()
    #update_balance()
    #claimRank()
    #userMints()