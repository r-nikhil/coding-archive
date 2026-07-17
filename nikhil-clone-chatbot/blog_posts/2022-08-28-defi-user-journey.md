---
layout: post
title: Problem statements to solve for a retail investor in DeFi
categories: [crypto]
---


The first section of the article inspects the various user personas interacting with DeFi protocols and their individual requirements. The second section  identifies various products which solve for these use cases. We mostly look for on-chain use cases which already have a reasonable amount of adoption. This post simply surfaces the various participants across the value chain and identifies open problems. Some cutting-edge novel cases with nascent adoption might get overlooked. Nevertheless, we keep an eye out for unsolved/potential growth segments and see what we can build there. 

#### User Personas

Broad retail requirements for interacting with financial services and products can be classified as:

- Investing
- Speculating/Trading
- Remittances
- Bill/Utility payments
- Commerce
  - Collectibles
  - Shopping
- Gaming
- Entertainment
  - Social
  - Content
- Transfers (P2P)/Cross border payments
  - Want to transfer money to somebody instantaneously with the lowest fees.
  - User Requirement and priorities
    - Easy on-off ramp
    - Global availability
    - Access to Payment rails
    - Network of peers/merchants already on-boarded into the network
      - Chicken/egg problem
    - Trust /Safety
- New user personas who may start using on-chain products. The requirements for those users would be different and dependent on what use case they on-board for. 
    - For example, my mom started using online payments (UPI) after Quick commerce (10min delivery) became commonplace). 


Currently, the first two user personas (**Investor and the speculator**) are the most common place in DeFi. In fact every other use case is in fact a minority. Lets look at them deeper. 

| **Average investor** | **Speculator/ trader** |
|---|---|
| Wants economic exposure to DeFi. Is not every sophisticated, intends to make +ve ROI, wants an engaging experience. | Wants a platform get access to capital and trade/gamble. High returns on capital is the ultimate priority.  |
| *Product requirements*<br><br>    - Savings<br>    - Investing<br>    - Lending/Borrowing<br>    - Insurance | *Product Requirements*<br><br>    - Investing<br>    - Trading across asset classes <br>    - Coin/NFT launchpads<br>    - Credit (Lending/Borrowing/Leverage)<br>    - Other financial products (derivatives/swaps/bonds/etc)<br>    - Insurance<br>    - Data and Analytics |
| *First priorities*<br><br>    - Easy on-ramp and off-ramp<br>  - High yield products<br>     - Minimal friction while adding/removing/transferring/spending money<br>      - KYC/Identity<br>      - Regulatory/Compliance and clarity<br>      - Taxation/Ease of filing<br>    - Trust/Safety in the platform<br>    - Principal protection (low volatility) for investment products<br>    - Easy to use (non complicated) UX<br>      -  Wants a personalized UX which is engaging as well as efficient<br>    - Easy Access everywhere (on mobile while travelling)<br>    - Speed of transactions have to instantaneous <br>    - (Single preferably) centralized market place/platform access to all products<br>      - Variety of markets available<br>    - Custody/Asset management<br>    - Cheap transaction costs<br>    - Best APR/APY (for savings/investments) and credit products<br>    - Easy onboarding | *First priorities*<br><br>  - Everything from Average investor<br>     - Advanced feature rich snappy UX <br>      - Portfolio management<br>     - Strategy builder<br>  - Risk Management<br>   - Centralized market place/platform access to all products<br>     - Variety of markets available with sufficient liquidity to do big trades<br>      - Derivatives/Spot/Prediction/FX products<br>     - Integration with other DeFi protocols<br>    - Regulatory compliance/clarity<br>       - Custody/Asset management<br>      - Rakeback for transaction fees<br>     - Best margin funding rate/leverage tools<br>     - Lowest interest fees<br>         - Best bid/offer spread<br>     - Low slippage<br>  - Easy onboarding<br>    - Capital efficiency(DeFi composability)<br> - Loyalty programs       |

Broad institutional personas who interact with financial services and products can be classified as:

- HNIs/Banks/Hedge Funds/Trading firms/ Market makers
- MNC Companies
- SME
- Governments/Treasuries

They all want economic exposure to DeFi and to leverage the benefits of transacting on-chain (distributed/ decentralized/trust less/ permission less/cheaper / available/etc). 
Some requirements for the above actors: 

<u>Product Requirements</u>:

Everything from a retail speculator |
Risk Management | Portfolio management 
Data and Analytics services |  Credit management
Client relationship management | Invoice financing 
Supply chain financing | Equity financing
B2B payments and transfers | Payroll 
Insurance | Foreign exchange | 
Principal protected yield | Treasury management

---------

Products which solve core user requirements which overlap across the most number of personas have the highest likelihood of attaining scalable PMF (duh!). Now, we shall the investigate the user journey of these personas and try to understand the active participants in the value chain.  

Profit pools are nothing but the total profit earned at all points along the value chain of an industry. When we analyse a value chain, it becomes imperative to define the boundaries of the sub-segment before digging deeper. Each of these segment profitability  may, for example, vary widely by customer group, product category, geographic market, or distribution channel. Moreover, the pattern of profit concentration in an industry is often very different from the pattern of revenue concentration. You can check this [article](https://hbr.org/1998/05/how-to-map-your-industrys-profit-pool) on HBR to know how to map an industry's pool. 

In this section, we attempt to dig deeper into some open problem statements and propose possible solutions. In the next article, we shall investigate these participants from a profit/operating margin PoV to understand which problem statement is worth solving financially. 

#### User Journey

Lets pick an **average retail DeFI investor** and look at their user journey.

Intent to invest
- High level actions in the user journey
    - On-boarding into a custody platform (interoperable platform)
    - Infrastructure plumbing (equivalent of the payment rails)
    - Fiat to crypto purchase 
    - Transfers/uses it on a Dapp

Now, lets break down each of these steps and inspect the actors. 


**<u>Custody and Asset Management</u>**

Similar to how fiat money is usually stored in savings accounts, central depositories, etc, crypto currencies have to stored in an online equivalent. Blockchains use digital signatures to secure money. Digital signatures are a pair of random keys, where one key is a “private key” and the other a “public key”. Through digital signatures, any person with the “private key” can “sign” a transaction and spend the digital currencies. Therefore, it is crucial to safeguard the “private key”. Some tech-savvy users of blockchains opt to safeguard this key themselves, and accept the risk of theft or loss of the key (and therefore the loss of their funds). In contrast, other blockchain users trust online wallets or exchanges with the safeguarding of their keys.

Custody management solutions overlap typically with the first step in the boarding process.Here, we are primarily focussing on the DeFi custody experience and not CeX related on-boarding flows. 

Using the user requirements we looked at in the first step, lets see where the current gaps exist: 

- Recovery/Portability is cumbersome and user has to remember a key phrase usually.  
- UX while using it across Dapps is broken (identity and auth).
    - It is a multi-step process. Sign/Approve spend/Transact. No standardized experience
    - Transaction details are hard to understand
        - Txn costs are hard to predict
        - Txn details include lengthy hex strings which don't mean much to the user. 
        - Multiple confirmation steps and non-instantaneous transactions leads the user to confusion  
- Managing multiple wallets/addresses is cumbersome
- From a first time web3 user perspective, its hard to understand what to do with the wallet after you install it on your phone. Onboarding through the specific Dapp directly has been more successful maybe for this reason.  
- Interoperability across the ecosystem is not mature

Let's look at the current type of wallets and understand what they do: 

**Self-custodial**

- User is responsible for their private keys
    - Typically stored locally in the user browser/device/mobile
    - Recovery through a key phrase only 
    - Easy to create and discard.
    - Examples:
        - Metamask
        - Trustwallet


**Exchange wallets**

- Investor allocates the control and management of private and public keys to exchanges.
- Gives control of keys in return for seamless access, lower fess but added counter party risk
- Examples of exchange wallets: 
    - Coinbase
    - Binance
    - Vauld

**Third party custody**

- Service providers storing digital assets on behalf of (business)customers
- Custom-defined features and controls for controlled management of the asset.
- Ideal for institutional crypto custody 
- Enterprise security and insurance is usually offered
- Examples (usually institutional):
    - Bitgo
    - Coinbase Prime
    - Instadapp sort of does this for retail. 


    - *Wallet as a service*
        - MPC wallets where the key is split between you and a third party. 
        - This means if you lose access to your private key, the key to your  wallet is still safe and recoverable. This helps with portability and availability across devices
        - Sort of like multi-sig wallets where both the third party and you have to sign transactions
        - Examples of wallets powered by this:
            - Coinbase dappbrowser
            - Coindcx Okta

*What can we work on?*: 

- Onboarding and discovery solutions helping a new user navigate web3 DeFi products
    - Unified payments/transaction experience across chains/wallets
    - Multi chain interoperable wallets
        - User ideally wants to live inside one wallet. Chains/protocols/etc should all be interoperable and talking to each other to provide a unified experience
- MPC based wallets offer the ideal mix of good onboarding/operating experience without trade off on security/privacy

Identity (Polygon ID, dynamic.xyz)

- Identity and authentication while preserving privacy
    - Unified standards for interaction with protocols (authorization and authentication)
        - Ethereum foundation is working on account abstractions ([EIP-4337](https://eips.ethereum.org/EIPS/eip-4337)) 
            - ZK proofs powered stealth address (where you can have a DeFi app level address which you can control but nobody else will know that you control it)
            - Social recovery features 
    - Decentralized identity provider 
        - Attach a name (ENS)
        - Attach POAP or Proof of Humanity (privacy preserving using zk proofs) 
        - Imagine an identity provider who can log you into web2 apps also because we can basically verify identity and the users also have way more control over their data


These Dapps which the users want to interact with are built on top of blockchains which we will investigate in the next section. While an average CeX user may not even interact with blockchains (just buys on Coinbase and doesn't do anything else), we are discussing about a web3 DeFi investor here. The user also doesn't pay for these services as they are usually available for free but instead monetized through adjacent offerings. In the next section, we shall look at some of the core infra DeFi products as well. 


**<u>Infrastructure</u>**


This is the plumbing needed for all of web3 to function. As an user, I don't really care how what the name of the chain is or the infrastructure complexity. The only requirements here are: 

- Availability across Dapps. (interoperability)
- Speed and security
- No overheads, cheap txn costs

The participants here include: 

- L1/L2 chains. The block chains on which the Dapps are built on. Some core participants here include:
    - Mining
        - Mining pools
            - Mining as a service
        - Node operators
    - Staking
        - Validator Node operators 
        - Delegators
            - Staking as a service 
    - Searchers extracting MeV
        -   ![mev](/assets/files/mev.png){:class="img-responsive"}
    - Multi chain protocols (shared liquidity/data layers)
    - Identity (authentication and authorization) layers

*What can we work on?*: 

- L1/L2 scaling and its subdivisions
- Staking 
    - Staking as a service for institutions
        - Controls for returns/risk adjustments
        - Taxation/Regulation/Compliance solutions based on geography
    - Given that most chains are moving to PoS, staking providers become one of the key participants in the value chain. Loads of capital is going to be locked up and further hypothecated for use across DeFi. Proving a plumbing solution is imperative here. 
    - Multi chain staking + interop solve for staking
        - When I stake and get a liquid token in return, most of the user cases are siloed into the particular chain on which staking happens. As a staking provider, I should be able to provide cross chain liquid tokens which are easily transferrable. 
- Block chain interoperability related problems
    - Given the fact that the user doesn't bother with actual chain names and their respective trade offs and just wants a simple investing experience, it becomes imperative to find a solution to abstract away all the noise. 
    - Multi chain protocols primarily solve for sharing of data and liquidity across chains. Use cases include cross chain governance, basic state share, cross chain lending/borrowing
    - Generic message transfer
        - Example: What does it mean for a lending protocol
            - Currently you put ETH as collateral (on ETH chain) and borrow. Then bridge it (to yield farming chain), swap (for yield token), yield farm, swap back again, bridge back again, then unlock collateral on ETH chain. Clearly this flow is broken. 
            - Ideal flow should be something like "lock collateral on ETH" chain, message goes to destination chain and you borrow directly there. Repay in destination chain and message comes back to ETH chain where your collateral gets unlocked. 
            - State transfer 
                - Transfer any piece of critical information across chain from your protocol. 
                - Unified governance where votes are cast across chains
    - Liquidity transfer layer
        - Instead of maintaining individual pair wise pools across chains (ETH on mainnet + ETH on Solana) to facilitate bridging, a more capital efficient way would be to do a common shared liquidity pool across all path ways. 
        - Collateral bridging
            - How to power Dapps to have their own liquidity transfer layer across chain
                - aave v3 has aave portal
        - Yield aggregation
                - Ultimately user just wants to deploy on the most profitable farm
        - DeFi apps
            - Uniswap doesnt want users to leave the platform to go to a bridge and the come back for swapping. It should be able to provide a much unified experience 
    
    - Current ecosytem
        - Middle chain
            - You start with two chains which are atomic and have their own state. Most solutions involve putting in a chain in middle for communicating data. The middle chain comes to consensus on the validity of the transactions and writes to the destination chain
                - You are implicitly trusting the middle chains which makes a big honeypot. Polynetwork is one example
                - Thorchain sort of does this with their common layer where all assets are trading against RUNE
            - Hub - Spoke model
                - System where everything is routed through the middle hub in the center (Polkadot)
                - Entire security requirements are offloaded to the hub
        - Cosmos IBC stuff
            - Takes the block header of all blocks and write it on the destination chain. Repeats the process vice versa
            - Once you have the entire block history, you can validate
                - Very expensive to do this
        - LayerZero/Router protocol (interop as a service)
            - Take single block, stream it on demand and validate it on other chain. Mostly a two part system with a oracle and a relayer. Oracle takes a block header and submits to destination chain and you can plug this oracle layer to different oracles like chainlink etc. The relayer simply takes the transaction proof and submits it on the destination chain. 
            - Each Dapp can wrap their contract with these to enable instant interop across any L1 to L2 EVM compatible or not
                - Security is split across multiple parties (multiple oracles and relayers)
        - CeX are basically interop solves as well
        - Native bridges and bridge aggregators (socket.tech)

    - Every chain is going to become interoperable and future users onboarded aren't even going to recognize the difference between yield farming on Solana vs ETH. Wallet experience and Dapp discovery is going to change because of this.  L1/L2 chains which support the most amount of modularity would eventually be best suited to capture this future .

- MeV aware solutions
- Blockchain API and data providers
    - Analytics on blockchain
    - Providing blockchain as a service


---

Above DeFi actors capture majority of the value in this step. They are directly/in-directly involved with every user transacting on chain and thereby also are at an intersection of the most value transferred. In the next post, we shall look at some key metrics to evaluate these actors across the value chain. 

Now the user has a wallet and connected to a chain to transact. Its time to move on to looking at the next participants in this value chain

**<u>On-Ramp and exchanges</u>**

Remembering that our user is a **retail DeFi investor**, lets look at some user requirements and pain points: 
- User just wants to convert his/her fiat into crypto
- Wants to pay the least amount of fees (slippage, txn fees) and wants the best price 

Some participants here: 

- KYC(if you are going to be regulated anyway, doublick click here for proof for identity/etc like polygon id/ platforms adhering to regulatory compliance are the first step in the on-boarding process (application include aadhar)
- On-ramp solutions which is the primary place to convert fiat to crypto
    - Exchanges usually interact with tradFi banking/payment system to take in fiat money        
- Exchange + Liquidity to convert fiat to crypto (swaps)
    - Liquidity protocols providing the markets for the user to trade in. 
    - Stable coins

- Gateway products which convert fiat to crypto (banking integrations)
- Stable coin issuers (primarily purchased first because of their ubiquity in web3)


what problems to work on? 

- Reduce the number of steps needed to convert crypto through block chain interop
- Geography aware KYC solutions

**<u>Dapp interaction</u>**

Now that the user has converted his/her to fiat to crypto, lets look at the journey to invest in Dapps.
As an user, my primary requirements would be: 

- Investing
    - Yield farming
        - Staking pools
        - Lending/Borrowing
        - Liquidity pool
            - Yield aggregators/boosters/auto compounders
            - Bribes/Governance co-ordination
            - Derivatives


For the next wave of Defi products to be bigger than the previous/current state we need an influx of new set of users who have never used these products before. Making these investment Dapp retail-newbie friendly is paramount. 
 

#### Summary

As we look across the value chain of a **retail investor**, we notice that major value transacts across these players: 

- Custody management
- Staking
- Blockchain interop

Now, depending on which business we are trying to enter, you can further double click to understand all adjacent offerings as well. A liquid staking service would eventually move into wallets to capture more TVL or approach the same problem from the perspective of an institution to offer DeFi products with access controls for risk profile/taxation/regulations etc. 

Checkout my other related posts too: 


- [We should all have something to hide - Tornado cash takedown](https://rnikhil.com/2022/08/09/tornado-cash-block.html)
- [Option protocols in DeFi](https://rnikhil.com/2022/08/15/defi-derivatives.html)
- [Blockchain gaming - Current state](https://rnikhil.com/2022/06/27/web3-gaming.html)