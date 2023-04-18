import logging

import algosdk.account
from algosdk.mnemonic import from_private_key
from algosdk.v2client.algod import AlgodClient

from algokit_utils import TransferParameters, transfer
from algokit_utils.account import Account, get_dispenser_account

logger = logging.getLogger(__name__)


__all__ = [
    "generate_test_account",
]


def generate_test_account(
    *,
    initial_funds: int,
    algod_client: AlgodClient,
    supress_log: bool = False,
) -> Account:
    pk, addr = algosdk.account.generate_account()
    if not supress_log:
        logger.info(f"New test account created with address {addr} and mnemonic {from_private_key(pk)}")

    dispenser = get_dispenser_account(algod_client)
    transfer(
        algod_client,
        TransferParameters(
            from_account=dispenser,
            to_address=addr,
            micro_algos=initial_funds,
            note="Funding test account",
        ),
    )
    acct_info = algod_client.account_info(addr)
    assert isinstance(acct_info, dict)
    if not supress_log:
        logger.info(f"Test account funded; account balance {acct_info.get('amount')} µAlgos")
    return Account(private_key=pk, address=addr)
