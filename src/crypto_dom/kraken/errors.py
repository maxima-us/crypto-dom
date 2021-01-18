from typing_extensions import Literal

ERROR = Literal[
    'EOrder:Rate limit exceeded',
    'EGeneral:Temporary lockout',
    'EAPI:Rate limit exceeded',

    # General usage errors
    'EQuery:Unknown asset pair',
    'EGeneral:Invalid arguments',
    'EGeneral:Internal error',
    'EGeneral:Permission denied',
    'EGeneral:Unknown method',      # when the URL is invalid
    'EAPI:Invalid key',
    'EAPI:Invalid signature',
    'EAPI:Invalid nonce',
    'EAPI:Feature disabled',

    # Service status errors
    'EService:Unavailable',
    'EService:Busy',

    # Trading errors
    'ETrade:Locked',

    # Order placing errors
    'EOrder:Cannot open position',
    'EOrder:Cannot open opposing position',
    'EOrder:Margin allowance exceeded',
    'EOrder:Insufficient margin',
    'EOrder:Insufficient funds',
    'EOrder:Order minimum not met',
    'EOrder:Orders limit exceeded',
    'EOrder:Positions limit exceeded',
    'EOrder:Trading agreement required',
    

    # Network timeout errors

    # Not documented by Kraken
    'EGeneral:Invalid arguments:volume',
    'EOrder:Invalid order',
    'EQuery:Invalid asset pair',
    'EFunding:Unknown withdraw key',
    'EFunding:Invalid amount',
    'EDatabase:Internal error',
    'EQuery:Unknown asset',
    'EOrder:Unknown position',
    'EOrder:Scheduled orders limit exceeded',
    'EOrder:Margin level too low',
]