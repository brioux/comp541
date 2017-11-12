#  DFIN 541 mini bitcoin project
# A simple python script for recording string srgument on the bitcoin blockchain
# Uses python
from decimal import *
from bitcoin import *
# to convert string to hexadecimal
from binascii import *
# Import Python library for Bitcoins API calls
# 
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
#  For loading environment variables in python
import os

# Setup RPC connection to send Bitcoin API calls
# rpcuser rpcpassword are asssumed to have been stored in users environment variables
rpcuser = os.getenv("RPCUSER")
rpcpassword = os.getenv("RPCPASS")
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18332"%(rpcuser,rpcpassword))

# String argument to store on the blockchain
string = input('Type a message to store on the blockchain: ')
# Convert to hexadecimal format
hex = hexlify(string.encode())
#  string = unhexlify(b"%s"%(hex))
#  print('data hex: '+hex.decode())
#  print('string: '+string.decode())

# Get list of unspent transactions
unspent = rpc_connection.listunspent()

# Calculate a transaction relay fee (0.0001)
tx_fee = Decimal(1)/Decimal(10000)

# Loop over unspent transactions
i = 0
while i < len(unspent):

# Get amount listed unpent transaction
 amount=unspent[i]['amount']
# If balance is greater than fee proceed to create raw transaction
# A dumb function for selecting transaction inputs!
 if amount > tx_fee:

#  print("amount: "+str(amount))
#  print("address: "+unspent[i]['address']) 

# Get Transaction id and output of unspent transaction
  txid = unspent[i]['txid']
  vout = unspent[i]['vout']

# Remove the fee from the unspent transaction balance, to be returned to the senders change_address
  amount = amount - tx_fee
  change_address=rpc_connection.getrawchangeaddress()

# New transaction input
  input = [{"txid": txid, "vout": vout}]
# New transaction output including amount sent to change adress and the hexadecimal string
  output = {change_address : amount, "data": hex.decode()}

# Create unsigned transaction
  raw_tx = rpc_connection.createrawtransaction(input,output)

# Unlock user wallet before signing, assuming the pass[hrase is stored in environment variables as WALLET_PASS (safe?)
  rpc_connection.walletpassphrase(os.environ.get("WALLET_PASS"),100)

# Sign transaction and send
  signed_tx = rpc_connection.signrawtransaction(raw_tx)
  status = rpc_connection.sendrawtransaction(signed_tx["hex"])

#  decoded = rpc_connection.decoderawtransaction(signed_tx["hex"])
#  print("decoded_tx: "+str(decoded))
#  stop the while loop
  break
 else:
  i += 1
