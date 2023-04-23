from random import choice

from . import puii_cmd

@puii_cmd(pattern="toss$")
async def coin_toss(event):
    await event.eor(f"`The Coin Landed on {choice(('Heads', 'Tails'))}`")