import time,os,sqlite3,json
from eth_account import Account


def creat_wallet(number):
    pwd = os.getcwd()
    db_pwd = pwd + "/xen.db"
    print(db_pwd)
    conn = sqlite3.connect(db_pwd)
    c = conn.cursor()
    for i in range(number):
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
        c.execute("INSERT INTO zelta (id,address,private_key,phrases)VALUES('%s','%s','%s','%s')"%(count,address, private_key, phrases))
        conn.commit()
    conn.close()



def translate_MATIC():
    count =0
    pwd = os.getcwd()
    db_pwd = pwd + "/xen.db"
    conn = sqlite3.connect(db_pwd)
    c = conn.cursor()
    c.execute('SELECT * FROM (SELECT * FROM  xen limit  150) WHERE  MATIC < 0.02')
    rows = c.fetchall()
    web3 = Web3(Web3.HTTPProvider("https://polygon-mainnet.g.alchemy.com/v2/h1fxey3Vh4o4l-jg-KWXZlEjvNFs28zP"))
    from_address = web3.toChecksumAddress("0x14bCa363445462082101164Eff599F83fbBEbab1")
    private_key = "006724ea4ee9b1e6c1c34c978bf72d589c9443b2a13a14ac50e449caae81974b"
    print(len(rows))
    for adds in rows:
        print("第"+str(count)+"个地址")
        to_address=adds[1]
        print ("发送代币： "+to_address)
        from_address = Web3.toChecksumAddress(from_address)
        to_address = Web3.toChecksumAddress(to_address)
        nonce = web3.eth.getTransactionCount(from_address)  # 获取 nonce 值
        print(nonce)
        from_address_balance = web3.eth.get_balance(from_address) / 1e18
        print("当前账户MATIC余额： "+str(from_address_balance))
        target_address_balance = web3.eth.get_balance(to_address) / 1e18
        print("目标账户MATIC余额： "+str(target_address_balance))
        params = {
            'from': from_address,
            'nonce': nonce,
            'to': to_address,
            'value': web3.toWei(0.05, 'ether'),
            'gas': 21000,
            'maxFeePerGas': web3.toWei(300, 'gwei'),
            'maxPriorityFeePerGas': web3.toWei(31, 'gwei'),
            'chainId': 137,
        }
        try:
            signed_tx = web3.eth.account.signTransaction(params, private_key=private_key)
            txn = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print ("hash值： "+str(web3.toHex(txn)))
        except Exception as e:
            print (e)
        count=count+1
        print("###############")
        time.sleep(5)
    conn.close()
def update_balance():
    pwd = os.getcwd()
    db_pwd = pwd + "/xen.db"
    conn = sqlite3.connect(db_pwd)
    c = conn.cursor()
    c.execute('SELECT * FROM atlendis')
    rows = c.fetchall()
    count = 0
    web3 = Web3(Web3.HTTPProvider("https://polygon-mainnet.g.alchemy.com/v2/h1fxey3Vh4o4l-jg-KWXZlEjvNFs28zP"))
    abi = json.loads(
        '[{"constant": true,"inputs": [{"name": "who", "type": "address"}],"name": "balanceOf","outputs": [{"name": "", "type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},'
        '{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
    USDT_contract = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    contract = web3.eth.contract(address=USDT_contract, abi=abi)
    web3 = Web3(Web3.HTTPProvider("https://polygon-mainnet.g.alchemy.com/v2/h1fxey3Vh4o4l-jg-KWXZlEjvNFs28zP"))
    for adds in rows[100:150]:
        print("第" + str(count) + "个地址")
        to_address = adds[1]
        to_address_MATIC_balance = web3.eth.get_balance(to_address) / 1e18
        to_address_USDC_balance = web3.fromWei(contract.functions.balanceOf(to_address).call(), 'ether')
        to_address_USDC_balance = float(to_address_USDC_balance) * 1E12
        print("当前账户地址： " + str(to_address))
        print("当前账户MATIC余额： " + str(to_address_MATIC_balance))
        print("当前账户USDC余额： " + str(to_address_USDC_balance))
        c.execute("UPDATE atlendis SET MATIC = '%s' where address=='%s';" % (to_address_MATIC_balance, to_address))
        c.execute("UPDATE atlendis SET USDC = '%s' where address=='%s';" % (to_address_USDC_balance, to_address))
        conn.commit()
        count = count + 1
        print("###############")
    conn.close()