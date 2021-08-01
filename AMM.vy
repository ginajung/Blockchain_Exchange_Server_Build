from vyper.interfaces import ERC20

tokenAQty: public(uint256) #Quantity of tokenA held by the contract
tokenBQty: public(uint256) #Quantity of tokenB held by the contract

invariant: public(uint256) #The Constant-Function invariant (tokenAQty*tokenBQty = invariant throughout the life of the contract)
tokenA: ERC20 #The ERC20 contract for tokenA
tokenB: ERC20 #The ERC20 contract for tokenB
owner: public(address) #The liquidity provider (the address that has the right to withdraw funds and close the contract)

@external
def get_token_address(token: uint256) -> address:
	if token == 0:
		return self.tokenA.address
	if token == 1:
		return self.tokenB.address
	return ZERO_ADDRESS	

# Sets the on chain market maker with its owner, and initial token quantities
@external
def provideLiquidity(tokenA_addr: address, tokenB_addr: address, tokenA_quantity: uint256, tokenB_quantity: uint256):
    assert self.invariant == 0 #This ensures that liquidity can only be provided once
    self.tokenA = ERC20(tokenA_addr)
    self.tokenB = ERC20(tokenB_addr)
    
    # the owner must first 'approve' the receiver before the transferFrom call
    if self.tokenA.approve(tokenA_addr, tokenA_quantity):
        self.tokenA.transferFrom(msg.sender, self, tokenA_quantity)
    if self.tokenB.approve(tokenB_addr, tokenB_quantity):    
        self.tokenB.transferFrom(msg.sender, self, tokenB_quantity)
    self.owner = msg.sender
    self.tokenAQty = tokenA_quantity
    self.tokenBQty = tokenB_quantity
    self.invariant = self.tokenAQty*self.tokenBQty 

    assert self.invariant > 0

# Trades one token for the other
@external
def tradeTokens(sell_token: address, sell_quantity: uint256):
    assert sell_token == self.tokenA.address or sell_token == self.tokenB.address
    
    
    self.sell_token.transferFrom(msg.sender, self, sell_quantity)
    new_A_tokens: uint256 = self.tokenA_quantity + sell_quantity
    new_B_tokens: uint256 = self.invariant / new_A_tokens
#     eth_to_send: uint256 = self.totalEthQty - new_total_eth
    # def transfer(_to : address, _value : uint256) 
    transfer(msg.sender, eth_to_send)
    self.tokenAQty = new_A_tokens
    self.tokenBQty = new_B_tokens    
    
#     #Your code here
#     def tokensToEth(sell_quantity: uint256):
#     self.token_address.transferFrom(msg.sender, self, sell_quantity)
#     new_total_tokens: uint256 = self.totalTokenQty + sell_quantity
#     new_total_eth: uint256 = self.invariant / new_total_tokens
#     eth_to_send: uint256 = self.totalEthQty - new_total_eth
#     send(msg.sender, eth_to_send)
#     self.totalEthQty = new_total_eth
#     self.totalTokenQty = new_total_tokens

# Owner can withdraw their funds and destroy the market maker

@external
def ownerWithdraw():
    assert self.owner == msg.sender

    #Your code here
    self.token_address.transfer(self.owner, self.totalTokenQty)
    selfdestruct(self.owner)