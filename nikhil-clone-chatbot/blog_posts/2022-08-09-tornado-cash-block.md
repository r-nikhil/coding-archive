---

layout: post
title: We should all have something to hide - Tornado cash takedown
categories: [personal, security, crypto]
---

[HN Discussion](https://news.ycombinator.com/item?id=32403504)

> " If you have nothing to hide, you have nothing to fear" 


This is a common saying parroted by folks  (made popular in the US after 9/11) for justifying many types of surveillance. It is also sometimes mistakenly used to justify the current blanket surveillance we all are a victim of.  With the development in technology and rapid increase of surveillance budgets, law enforcement has gotten a lot easier as well. 

Recently, Tornado cash, a [mixer website](https://en.wikipedia.org/wiki/Cryptocurrency_tumbler) used to obfuscate the origin and destination of your money has been [blacklisted](https://home.treasury.gov/news/press-releases/jy0916) by the US Treasury. The implications prevent anybody from transacting with them which means, all the money held in their smart contract is effectively tainted. Funnily enough, they blacklisted only the contract address on the Ethereum but not the contract on Arbitrum or BSC. While it is no secret that this service was used by criminals (like DPRK) to launder their money, there are some legitimate use cases for such a product as well. 

Since all transaction data is on-chain (which is public) and can be queried by anybody, it poses serious risks to privacy of individuals. Connecting their wallet address with their real life identity and to their rest of of their transaction data leads to some disturbing scenarios like:  

- Any (d)app you use will instantly know your entire transaction history

    - Imagine you sign up with your email on a random website and they suddenly now have access to your entire bank statement.  Higher medical insurance premiums because they know that you transacted often in an online pharmacy. Expensive delivery charges because they know you can afford it. 

- Any donations to a controversial cause (which is legal) is attached to you but you don't want to handle the repercussions

    - You don't want your patriotic Russian neighbors knowing that you donated to the Ukraine fund or your co-workers knowing that you donated to a particular political party

- Everybody will know your net worth

- Your employer will know how exactly you spend your funds.

These are just use cases which are commonly known and well extrapolated already. However, there are so many scenarios and use cases which we haven't even discovered yet as a society which one day which be also legitimate and common. 

For example, In the last decade, there has been an increasing number of headline-grabbing legal changes everywhere in the world: growing number of countries are working towards legalizing marijuana and same-sex marriages. While people laud these countries for being forward thinking and developed, these "legal" victories were mostly improbably without the ability to break the law at some point. If we lived in a dystopian future where the cops are 100% effective such that any and all law offenders would be caught magically, the above changes may not have come to happen. How would the country legalize a drug if nobody has ever used it? How could states decide that same sex marriage should be permitted, if nobody had ever seen or participated in a same sex relationship? 

We can only desire for a change based on what we know. If our present experiences are limited and controlled tightly, its gets  harder to understand what is possible and should be allowed. In a liberal democracy, these marketplace of possibilities are presented in front our political system to eventually made into laws based on what the society wants. This is why illegal drug consumption is a necessary pre-condition to eventual drug legalizations. Even the internet originally was used for illegal commerce and was shunned away from adoption.

While I digressed (ranted) away on the reasons why such bans are bad,  the current scenario poses some other questions as well: 

- What happens to the FOSS developers who contributed to the project? Are they sanctioned as well? 
- What will happen to the tainted money? This figure is about $400M. I expect a secondary market for TCtETH (Tornado cash tainted ETH)
- What about the people who donated through Gitcoin? 
- What happens to the protocols/pools/(d)apps which interacted with it? 


*This also might be the first time where a piece of code got sanctioned.*

I really hope that the political authorities dig deeper and technically understand services like Tornado cash and come to a realization that criminal behavior exists everywhere and cannot be blanket banned by shutting down legitimate services. You can't just end up banning hard cash just because its used by criminals and for money laundering. [(They tried this in India but it didn't go as expected)](https://en.wikipedia.org/wiki/2016_Indian_banknote_demonetisation).