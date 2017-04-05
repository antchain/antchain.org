# antchain.org 
AntShares 小蚁区块链浏览器  
Blockchain explorer for AntShares.  


###使用指南
1. 搭建 mongodb + python + flask 运行环境。
2. 从官方RPC接口读取区块数据进行入库mongodb，运行：
   * python db/main.py （同步区块）
   * python db/main.py height （回滚到height，并从这个高度开始同步区块）
3. 网站入口 web/web.py, enjoy.  


###数据库结构
1. blocks表，只存储 blockdata 结构，将 transaction 剔除。
2. txs表，存储 transaction 完整结构。
3. coins表，将每一笔 vin / vout 状态存入，如果是vin，则根据txid/vout标记该笔资产已花费，如果是vout，则标记该笔资产被创建。
4. ads表，表示每个 address 对应的 asset 资产余额信息。ads表可通过计算coins表进行构建。 

Web: http://www.antchain.org  
Mail: zhengq1#hotmail.com  