# ASR check (large-v3)

| line | result | differences (script → heard) | heard |
|---|---|---|---|
| a1 | BAD 0.67 | the twenty ninth of → 29; eighty → 80 | On 29 September, one Bitcoin address received 80 coins. |
| a2 | CHECK 0.94 | dollars → ∅ | At the time, that was roughly $5 million. |
| a3 | OK 1.00 |  | The coins went onto a ledger, a hardware wallet, a small device that keeps your keys away from the internet. |
| a4 | CHECK 0.94 | twenty four → 24 | It's the advice everyone gets. Don't leave your coins on an exchange. Buy a cold wallet. Write the 24 words on paper. Keep them safe. |
| a5 | BAD 0.89 | crypto bilis → cryptobillis; authorised → authorized | The device came from CryptoBillis, not a stranger on a marketplace, an authorized ledger reseller listed for Malaysia, Indonesia and the Philippines. |
| a6 | BAD 0.89 | eighty → 80 | But 10 days later, the 80 coins were gone. |
| a7 | BAD 0.85 | one hundred and ten → 110 | They left in a single Bitcoin block, together with the coins of 110 other wallets. |
| a8 | OK 1.00 |  | No phishing link. No fake support call. No malware on a laptop. |
| a9 | OK 1.00 |  | So how do you rob a wallet that never goes online? |
| a10 | OK 1.00 |  | To answer that, we have to open the box. |
| b1 | OK 1.00 |  | A ledger has two brains. |
| b2 | OK 1.00 |  | The first is a secure chip. It holds your keys, and it's built never to let them out. |
| b3 | OK 1.00 |  | The second is an ordinary chip. It runs the buttons, the Bluetooth, and the screen. |
| b4 | CHECK 0.94 | twenty twenty → 2020 | In 2020, Ledger wrote down a rule for the Nano X, that second chip could be fully compromised and the funds would still be safe. |
| b5 | OK 1.00 |  | Because the secret never leaves the secure chip, except once. |
| b6 | CHECK 0.94 | twenty four → 24 | When you set the device up, it shows you your recovery phrase, 24 words, on the screen. So you can copy them down. |
| b7 | OK 1.00 |  | For a few minutes, your most valuable secret is on display. |
| b8 | OK 1.00 |  | Now look behind that screen. |
| b9 | CHECK 0.95 | e sim → esim | Researchers who opened tampered units found an extra board, tucked where a strip of padding should be, a microcontroller, a cellular modem, an antenna, and an eSIM. |
| b10 | OK 1.00 |  | To make room, the original battery had been swapped for a smaller one. |
| b11 | OK 1.00 |  | Ledger's own security team, the Donjon, described what the implant does. |
| b12 | CHECK 0.93 | l t e → lte | It reads the data going to the screen. When it sees the recovery words, it decodes them. Then it sends them out over LTE, the mobile network. |
| b13 | OK 1.00 |  | It doesn't touch the secure chip. It doesn't change a single transaction. |
| b14 | OK 1.00 |  | And it doesn't need your laptop or your phone. It brought its own connection. |
| b15 | OK 1.00 |  | No virus to catch, no link to click, just a box. |
| b16 | OK 1.00 |  | Ledger's genuineness check is built to test the secure chip, and in these devices the secure chip was the real one. |
| c1 | OK 1.00 |  | But this board wasn't new. |
| c2 | BAD 0.89 | tibane → tiban; twenty twenty five → 2025 | According to Tiban Labs, a research group that documented the implant, the first public warning about a tampered Nano X appeared on Reddit in August 2025. |
| c3 | OK 1.00 |  | This year, the hardware hacker Joe Grand took one apart on stage. He showed the smaller battery and the board that shouldn't be there. |
| c4 | BAD 0.83 | the sixteenth of → 16; karpeles → carpelli's | On 16 September, Mark Carpelli's posted photos of a newer version. He called it quite an evolution. |
| c5 | CHECK 0.93 | bilis → billis | Those research units came from other channels. Online marketplaces in Japan. Not from Crypto Billis. |
| c6 | OK 1.00 |  | So the implant was public. What nobody had yet shown was a wave of real losses. |
| c7 | OK 1.00 |  | That was about to change. |
| c8 | BAD 0.80 | crypto bilis → cryptobillis | Back in March, CryptoBillis had changed hands. |
| c9 | OK 1.00 |  | Its founders later said the company was sold to a new team, and that they handed over all operations. They haven't named the buyer. They deny any involvement. |
| c10 | OK 1.00 |  | Who owned the shop by October? Nobody has said publicly. |
| d1 | OK 1.00 |  | So the thief started preparing, and the blockchain kept the receipts. |
| d2 | BAD 0.86 | the twenty fourth of → 24 | On 24 September, a withdrawal from the exchange Bybit landed in a wallet on the Tron network. |
| d3 | BAD 0.86 | attack's → attacks | That money later paid the attacks fees. |
| d4 | BAD 0.75 | twenty fifth → 25th; twenty one → 21; twenty → 20 | From the 25th, the thief ran tests. 21 small loops on Tron, 20 on Ethereum. |
| d5 | OK 1.00 |  | Remember one thing from this, a single Tron address acting as the thief's control wallet. |
| d6 | BAD 0.90 | bit query → bitquery; ninety → 90 | Meanwhile, the victims kept loading their wallets. BitQuery found that about 6 in 10 drained wallets were first funded within the last 90 days. |
| d7 | OK 1.00 |  | someone had the keys in advance and waited. |
| d8 | BAD 0.74 | fifty nine → 59; thirty → 30; one hundred t r x → 100 trx | At 4.59 in the morning, UTC, 30 Tron wallets got a new key added. Each paid a 100 TRX fee. |
| d9 | OK 1.00 |  | The thief didn't steal yet. The thief changed the locks. |
| d10 | BAD 0.55 | seven minutes past five twenty five → 07 05 25; wallets sign → wallet signed | At 07.05.25, Tron Wallet signed the same approval, within three seconds. |
| d11 | BAD 0.71 | twenty nine → 29; dollars → ∅ | $29 million leaves in six seconds. |
| d12 | BAD 0.71 | b n b → bnb | Then BNB chain, Polygon Ethereum, Solana. |
| d13 | BAD 0.72 | fifty four → 54; one hundred and eleven → 111; eighty → 80 | At 5.54, one Bitcoin block, 111 wallets, emptied together, the 80 coins were in it. |
| d13b | BAD 0.86 | the fifteenth of → 15; dollars → ∅ | Another wallet, first funded on 15 September, lost $7 million in Tether in a single transaction. |
| d13c | BAD 0.88 | thirty three → 33; dollars → ∅ | One Tron wallet had taken in $33 million since October began. It looked like a business. |
| d14 | BAD 0.62 | bit query's → bitquery's; one hundred and two → 102; dollars → ∅; three hundred and thirty five → 335 | By Bitquery's count, the full tally reached $102 million from 335 wallets on six networks. |
| d15 | OK 1.00 |  | Most of it was gone before anyone raised the alarm. |
| e1 | OK 1.00 |  | But stablecoins can be frozen, and by noon, Tether was freezing. |
| e2 | CHECK 0.91 | dollars → ∅ | About $10 million stayed locked. |
| e3 | BAD 0.79 | twenty three point → 23; dollars → ∅; u s d d → usdd | The thief had planned for that too. $23.7 million in Tether was swapped into USDD, a token Tether can't freeze. |
| e4 | BAD 0.65 | moved → move; thor chain → thorchain; tornado cash → tornadocache; z cash → zcache | The rest move through ThorChain, ChainFlip and other swap services, into TornadoCache, through Zcache. |
| e4b | CHECK 0.96 | ninth → 9th | Back on the 9th itself, Mark Karpeles opened a Nano X sent to him from Malaysia. It arrived still in its shrink wrap. |
| e4c | OK 1.00 |  | Behind the screen where the padding should be, he found the board. |
| e5 | BAD 0.77 | the tenth of → ten; the thirteenth → 13; l t e → lte; crypto bilis → cryptobillis | On 10 October, Ledger confirmed an implant in one victim's device. On 13, it described the LTE board. It said every confirmed loss involved devices sold through CryptoBillis. |
| e6 | OK 1.00 |  | Two days later, it blamed a sophisticated criminal group and tightened the rules for its resellers. No devices on display. Handed over at purchase, no resale of returns. |
| e7 | BAD 0.89 | the tenth of → ten; point → ∅ | Then Singapore police reported at least two cases since 10 September. About 3.5 million Singapore dollars, devices bought in local shops. |
| e7b | BAD 0.86 | mediamarkt → media markt | In Europe, the electronics chain Media Markt paused its ledger sales. |
| e8 | OK 1.00 |  | So it wasn't just one reseller in one country. |
| f1 | BAD 0.86 | fourteenth → 14th; forty three → 43 | Then on the 14th of November at 7.43 in the evening, UTC, 4 Tron wallets emptied. |
| f2 | OK 1.00 |  | 10 minutes later, 9 Bitcoin wallets in one block, then more. |
| f3 | OK 1.00 |  | This time the devices didn't come from Southeast Asia. A Ledger Flex and a Ledger Stax bought in Dubai. A Flex bought in Berlin. |
| f4 | BAD 0.53 | point six eight → 68; dollars → ∅; sixteen → 16 | $1.68 million from 16 wallets. |
| f5 | OK 1.00 |  | And in the same block as the drain, one Tron address paid the network fees. |
| f6 | BAD 0.84 | bit query → bitquery | According to BitQuery, it was the same control address. |
| f7 | CHECK 0.91 | the nineteenth of → 19 | On 19 November, Ledger wrote that it is the same incident. Tampered devices outside Southeast Asia, and more may be found. |
| f8 | OK 1.00 |  | Ledger now offers worried owners an X-ray inspection at its factory in Vierzon, France. |
| g1 | OK 1.00 |  | As we make this video we found no public arrest and no charges. |
| g2 | CHECK 0.95 | bilis → billis | we don't know who fitted the boards or where along the chain we don't know who bought crypto billis |
| g3 | OK 1.00 |  | Ledger hasn't confirmed how many devices were tampered with, or how much was lost in total. |
| g4 | OK 1.00 |  | And we don't know if it's over. Ledger itself says, more devices may surface. |
| g5 | OK 1.00 |  | Here's what we do know. The chip was never broken. |
| i1 | OK 1.00 |  | I'm Thomas Archer, the AI narrator of Siphon Files. |
| i2 | OK 1.00 |  | Every claim in this video comes with a source. |
| i3 | OK 1.00 |  | Ledger hasn't confirmed the totals. So we'll tell you who counted. |
| k1 | OK 1.00 |  | Somewhere there's a box like this one, plastic tight. Seal intact. |
| k2 | OK 1.00 |  | A seal proves the box hasn't been opened since someone closed it. It doesn't tell you who that someone was. |
| k3 | OK 1.00 |  | and the thief's money trail starts with a withdrawal from an exchange. Exchanges keep records. |
| k4 | OK 1.00 |  | Whether those records lead to a name, no one has said. So far. |
| k5 | OK 1.00 |  | Before you trust a seal, ask who sealed it. |
| k6 | OK 1.00 |  | I'm Thomas Archer, this was Siphon Files. |
| t1 | OK 1.00 |  | This box has never been opened. |
| t2 | OK 1.00 |  | The plastic is tight. The seal is intact. |
| t3 | OK 1.00 |  | Inside is a genuine hardware wallet, the real chip, the real software. |
| t4 | BAD 0.81 | ninth → 9th; three hundred and thirty five → 335 | On the 9th of October, 335 wallets were emptied. Ledger tied the confirmed losses to devices like this one. |
| t5 | BAD 0.70 | one hundred and two → 102; dollars → ∅ | about $102 million by one on-chain count. |
| t6 | OK 1.00 |  | Nobody broke the chip. Nobody cracked the code. |
| t7 | OK 1.00 |  | Someone just read the screen. |

40 lines to look at

## Words heard with low confidence (p < 0.5)

| line | words |
|---|---|
| c2 | Tiban@0.9s p0.49, X@7.2s p0.49 |
| e5 | 10@0.5s p0.44 |
| f1 | 4@5.1s p0.42 |
| g2 | we@0.0s p0.31 |
