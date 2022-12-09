<h1 align="center">:owl: web3兼职 :rooster: </h1>
<p align="center">========================================
<p align="center">心有山海，静而不争</p>
<p align="center">There are mountains and seas in the heart 
<p align="center">quiet but without contention 
<p align="center">如果喜欢我，您的支持将给予我无限分享下去的动力
<p align="center">========================================
<p align="center">:dog2: Email | zw97073966@gmail.com</p>
<p align="center">:cow: Github | https://github.com/0x024</p>
<p align="center">:owl: Twitter | https://twitter.com/_0x024</p>
<p align="center">:cat2: Mirror | https://mirror.xyz/1x024.eth</p>
<p align="center">:rabbit2: ERC-20 | 0x14bCa363445462082101164Eff599F83fbBEbab1</p></p>
<p align="center">========================================




## 0x01 项目背景
这两天 XEN 特别火，看了看代码，相对比较简单。这篇文章就来结合文档来解读一下合约代码，仅做学习交流用。

整个玩法分成两部分，我这里将其区别为：

时间挖矿（claim to mint），也就是在参与时指定时间，时间到期后即可领取对应的 XEN，唯一付出的成本就是 gas 费用和等待的时间

stake 挖矿，通过质押 XEN 来挖矿

## 0x02 环境准备

```

mac os ventura Pycharm 
pip3 install web3
git clone git@github.com:0x024/xen.git
```
## 0x03 目录结构

```
BSC.py---运行与BSC网络下
polygon.py----运行与polygon网络下
xen.db----用来存放地址私钥及mint信息
```
## 0x04 运行方式

### step1: 创建钱包，

1:取消`creat_wallet()`前面的注视，

2:在creat_db传入钱包数量，例如要创建1000个钱包及`creat_wallet(1000)`

3:最后运行 `python3 BSC.py`

4:运行过程中会直接写入到sqlite数据库中

```
id -钱包序号
address -钱包地址
private_key -钱包密钥
phrases -钱包助记词
BNB -BNB余额
status -状态值 1代表已经mint
hash-mint的哈希值
```

### step2: 分发gas费

1:取消`translate_BSC()`前面的注视，

2:运行 `python3 BSC.py`  
 
3:该步骤是给子钱包发送BNB的gas费，基本每个钱包发送0.001gas即可，

PS:需要在顶部填写好主钱包的地址和私钥，

### step3: 查询每个钱包余额

1:取消`update_balance()`前面的注视，

2:运行 `python3 BSC.py`  

3：主要是更新钱包余额

### step4: 进行mint

1:取消`claimRank()`前面的注视，

2:运行 `python3 BSC.py`  

3:该过程会根据选定的钱包数量进行mint，其中term的值设置mint天数，







































