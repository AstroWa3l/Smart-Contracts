from opshin.prelude import *


@dataclass()
class Bet(PlutusData):
        amount: int
        better: Address
        winner: PubKeyHash
 

@dataclass()
class PlaceBet(PlutusData):
        CONSTR_ID = 0

        
@dataclass()
class PayWinner(PlutusData):
        CONSTR_ID = 1
        

BettingAction = Union[PlaceBet, PayWinner]

def check_single_utxo_spent(txins: List[TxInInfo], addr: Address) -> None:
    """To prevent double spending, count how many UTxOs are unlocked from the contract address"""
    count = 0
    for txi in txins:
        if txi.resolved.address == addr:
            count += 1
    assert count == 1, "Only 1 contract utxo allowed"
    
def check_paid(txouts: List[TxOut], addr: Address, price: int) -> None:
    """Check that the correct amount has been paid to the vendor (or more)"""
    res = False
    for txo in txouts:
        if txo.value.get(b"", {b"": 0}).get(b"", 0) >= price and txo.address == addr:
            res = True
    assert res, "Did not send required amount of lovelace to vendor"



def validator(datum: Bet, redeemer: BettingAction, context: ScriptContext) -> None:
        purpose = context.purpose
        tx_info = context.tx_info
        
        if isinstance(purpose, Spending):
                own_utxo = resolve_spent_utxo(tx_info.inputs, purpose)
                own_addr = own_utxo.address
        else:
                assert False, "Wrong script purpose"
                
        check_single_utxo_spent(tx_info.inputs, own_addr)
        # if isinstance(redeemer, PlaceBet):
        #         check_paid(tx_info.outputs, datum.better, datum.amount)
        # elif isinstance(redeemer, PayWinner):
        #         check_owner_signed(tx_info.signatories, datum.winner)
        # else:
        #         assert False, "Wrong redeemer"
