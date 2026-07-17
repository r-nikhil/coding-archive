---

layout: post
title: Derivative protocols in DeFi
categories: [crypto, markets]
---


This post is a summary of all the options products available in the DeFi space. I embarked on doing a bit of research after I wanted to hedge my LP positions given the current volatile market and the impending [merge](https://ethereum.org/en/upgrades/merge/). 

Before going ahead, it helps the reader to have  a basic understanding of what options/futures are. You can read a basic primer [here](https://zerodha.com/varsity/module/option-theory/) from [Zerodha](https://zerodha.com/) which elaborates on the fundamentals of an options contract in TradFi. 

One of the main differences between TradFi options and DeFi options is the additional component of a liquidity pool. Since we can't have order books (due to limited TPS, available block space etc) in DeFi, liquidity providers come together to provide liquidity to the pool in return for earning some yield. You can think of these LP's as the equivalent of market makers(banks/hedge funds/prop trading shops) in TradFi.

Most of these product are inspired from the equivalent TradFi products and follow along closely in terms of their equivalent implementation. 

[Perp.com](https://perp.com) 

- One of the first on-chain futures which were composable. Deribit/Bybit might predate them but they we based on CEX's.

- Everlasting contracts with no expiry. Imagine a NIFTY futures contract without an expiry date. 

In TradFi, the price of the futures contract is usually different from the underlying's prices and converges to the value of the underlying on the expiry date. The deviation is caused by the risk free interest rate and/or any dividend given out by the underlying before the expiry period. Since we don't have expiry dates here, we need a mechanism to price these contracts. Enter funding rates which the longs pay the shorts to help keep the futures price close to it underlying.

![perp](/assets/files/funding.png){:class="img-responsive"}

Basically funding rates will always tend towards zero as other market participants (traders/arbitrageurs/etc) will take advantage of the rate by going long when its negative or going short when its positive, thereby aligning the price of the of the perp with the underlying. 
If the funding rate is positive, you can short perps and buy ETH on the spot market for a delta neutral strategy. A bunch of start-ups have automated this trade: 

- Diamond protocol does this cash and carry strategy (as a vault) using an algorithm to find the best rebalance frequency for the current market and rebalance automatically for the vault's depositors.

- Due to the fact that these primitives are composable, there are also tokens which represent the above trade. Holding them would earn you funding payment without exposure to price. $BYE (Basis Yield ETH) is one such token. 

[Opyn](https://www.opyn.co/)

- I stumbled onto them quite late (by crypto standards) while reading this [paradigm article](https://www.paradigm.xyz/2021/08/power-perpetuals) 

- While they have "normal" perp options, I am interested in power perps (power contracts are basically attached to the square of the underlying's price. If BTC goes 2x, the power^2 perp goes, 4x) because of their non linear returns similar to how options behave

- Squeeth (that's how they call their square perp) doesn't have expiry dates or even strike prices for that matter.They run distributed option vaults (DOVs) with their inhouse product Squeeth instead of "regular" options these days.

- For detailed payoff diagrams and explanations on how Squeeth behaves during different market conditions, you can check this article [here](https://medium.com/opyn/the-best-market-conditions-to-squeeth-3e92d868b533) 
 
[Hegic](https://www.hegic.co/)

- They run a liquidity pool marketplace for operating an American style option. American options are slightly expensive than European options for the fact that they can be exercised anytime. 

- Options trade in secondary markets where market makers/option writers can define the price of the option using their internal model. It looks like Hegic controls the IV variable and thereby the price of option as well. 

- Options purchased on this platform are not composable meaning, I cant trade/use this position somewhere else in the DeFi ecosystem

[Zeta](https://www.zeta.markets/)

- Given really long block times and the inability to structure atomic trades, most of these option writers require full collateralization. However, due to faster L2's and alternative L1's going mainstream, we can now have faster M2M update which will help us price our options better which in turn means ability to offer under collateralized options

- Zeta provides under-collateralized options with an on-chain pricing engine and margin system.


While the above platforms mostly work on fundamental primitives, there are also a lot of companies providing pre-made option strategies for retail participants to invest in. These are particularly attractive to the less-complicated user who wants a quicker investing/gambling experience. 

### Distributed Option Vaults (DOVs)

- DOVs are a new form of structured product which are mostly a collection of pre-defined option strategies. DOV's are pretty important because they are able to democratize access to options without the user needing to understand complex jargon, choosing strikes/expiry or the risk of losing a lot.

- In TradFI, a specific combination of derivatives are selected, packaged and sold to clients looking for custom non-traditional payout curves. These clients are usually HNI's/institutions and the intermediary (banks mostly) charge a fee for setting this up. 

Let's look at how these products are structured in the DeFi space:

[Ribbon Finance](https://www.ribbon.finance/)

- DOVs, with most of them running a basic covered call strategy. The call options are minted from the Opyn vault.

- They usually run covered call or cash covered put strategies which is a great on-ramp solve for retail traders looking to get some exposure in derivatives. 

- Imagine Zerodha having a one click auto compounding covered call strategy against all your stock holdings. That would be really convenient. 
 
[Friktion](https://friktion.fi/)

- **Volt1**: This is a basic DOV with covered call strategy on SOL, BTC, ETH etc.

- **Volt2**: Cash secured puts on the same assets as above.

- **Volt3**: Deltra neutral  crab strategy. In TradFi, I would usually express this sentiment with a stradle or a strangle. Here, they use power perps to come up with a novel way to delta hedge. Payoff looks something like this:

    -  ![payoff](/assets/files/payoff.png){:class="img-responsive"}


- **Volt4**: Basis yield (delta neutral strategy which is used for eating the funding rate in perps as discussed above). During a positive funding environment, this strategy goes short on the perp contract and long on the spot to earn the funding rate and vice verse during negative funding environments. 

 
[BrahmaFi](https://www.brahma.fi/)

- PMUSDC
    - A simple vault which does LP yield farming (boost LP rewards through convex and reinvest back into LP pool. sort of like yearn finance) with an added addition of taking a momentum trade using the yield on Lyra/perp.com

    - The extra edge in this strategy comes mainly from their internal momentum bot. Otherwise, its just a yearn finance strategy with extra fees. They used to do the same trade on GMX earlier 

There are a lot more derivate platforms which further build on top of yield aggregators, DOVs etc. We shall have a look at them in the next post. 

Disclosere: I use the above platforms and don't endorse any of them. 

If you like it, check out my other posts too: 

- [We should all have something to hide - Tornado cash takedown](https://rnikhil.com/2022/08/09/tornado-cash-block.html)