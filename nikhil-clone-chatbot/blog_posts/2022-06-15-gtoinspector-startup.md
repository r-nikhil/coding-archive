---

layout: post
title: GTO Inspector - My attempt at building an online business
youtubeId: VdmHds-lylY
categories: [poker, markets]
---

This document explores the hypothesis and my experience running an online business in the Indian poker ecosystem. 

- Quick rundown of events:

    - It is 2019 and I've been playing poker for about a year (it all started after I won a big tournament through a satellite right out of college). I then went and joined [Indian Poker Pros](https://www.indianpokerpros.com/) (now defunct) to be staked and coached by them. Although I was crushing mid stakes MTTs comfortably; most of my shot taking didn't work out because I was severely let down by my inability to put in volume partly due to my day job at Flipkart. Grinding a 9hr day job and 10hrs of poker takes a toll on body and mind as well. 

        - Due to aforementioned reasons, I moved to [PLO cash](https://www.pokernews.com/strategy/plo-poker-beginner-guide-pot-limit-omaha-23724.htm) for a flexible time schedule and a possible bigger edge vs opponents (Indians were studying MTTs harder than PLO).


    - Sometime in 2020, I quit my job to focus on poker full time. Along the way, I met an amazing poker player named [Kunal Agarwal](https://in.linkedin.com/in/kunal-agarwal-7b6a76162) and we built some tools to help improve my own game(he was my coach) and one such tool picked up steam in my stable across PLO players. Kunal had a bunch of scripts for analyzing our post game history and I worked alongside him to build a productized version of the software which is sellable to poker stables and professional players. While I won't go into the details of the product in this post, you can watch a quick demo/tutorial video that I made, here: {% include youtubePlayer.html id=page.youtubeId %}


#### What problem are we solving? 

- While there are coaches doing post game hand analysis and hand reviews, there was no systemic/automated way to figure out how much a player is deviating away from [GTO](https://upswingpoker.com/glossary/gto/) and how much money he/she is losing because of it. Preflop poker studying is broken. 

- A tool which narrows down pre flop mistakes super fast in an accurate fashion at a position*action level would help the player improve in preflop PLO (which is super hard to study, 270k starting hands vs 1.3k in NLHE ). 

#### Why?

- There was no such tool available in the market to help professional poker players. Serious players will pay real money for this because of the direct impact on their bottom line. 

- We had already built a crude version for my own personal use. Other professionals wanted it and it was easy for me to start a poker business starting from this PLO tool.  

- **Market potential**

    - All professional PLO players in the world given we are making a global product. [Jnandez](https://plomastermind.com/) showing his financials sort of helped clarify the scope of the market as well. Coaching is super high ARPU business. 
<!-- - This was the biggest mistake was made (in hindsight). The idea was to launch the PLO tool first and then build a poker learning universe around it. I underestimat -->


#### How? 

Validation approach

1. Distribute the crude version among the poker stable members (About 10 folks)

    - Everybody loved the tool and wanted a full fledged dashboard. Coaches were willing to pay me to work on this full time (apart from my coaching fees on newer players)

2. Given the positive feedback from my circle (read: bubble), and the market potential, we went ahead building a MVP of the tool. The idea was to first launch the PLO version and then eventually expand into more popular game formats like NLHE/Tournaments. 

GTM

- We ended up building a small internet business around the product selling to PLO professionals in India, Europe and Mexico. Our early acquisition costs were high but we didn't pay heed due to high premiums we were charging in the early days (mostly high stakes regs)

    - *Lesson* : Keep a close eye on the acquisition channels and their corresponding costs from early on. A simple forecast would have helped us avoid some expensive mistakes (Lot of paid marketing)

- Within the first month, we had almost every professional PLO player in India as a customer. Initial customers loved it. 

    - Notable Anecdotes:
        - *"A  PLO professional"*: I found out I was leaking close to 25bb/100 cold calling 2bets which I didn't realize before. Made me tighten up and study by calling ranges again. 

        - *"A seasoned recreational PLO player"*: After you made me upload my Adda52 hand history of 3L hands, I understood that playing GTO makes money in the long run. Knowing that I am not skilled to deviate profitably from GTO has been eye opening. 

- When we tried to scale the business, the obvious issues started showing up. They included high acquisition costs, bad retention rates for foreign players and the general lack of a sizable market for such a product. 

#### Conclusion

I had a couple paths forward after reaching monopoly in the Indian PLO market. I could continue scaling the PLO tool or build newer poker tools for bigger audiences. 

- Sell the PLO tool to more players (India and abroad)

    -  Recreational players found it expensive and hard to learn the terminologies

        - One direct solution was to start building PLO education content around the product and give it away for free. I personally did not find this enjoyable to work on. Re-visiting the basics didn't seem fun to me.

            - I could also take in interested players, coach them using my tools, in return for their future profits. I eventually ended up starting a poker stable (a staking operation. Same concept as prop trading firms) structured around this tool and other such proprietary tools to monetize the new-to-poker-theory players and PLO regulars wanting to improve/get staked. 

            - <b>This ended up working out super well and still does to some extent. At its peak we had 15 students playing for us. </b>

    -  Professionals abroad found it basic

        - This was expected. I had a long roadmap of cooler stuff I wanted to build and monetise. I had crude python scripts ready for studying post flop GTO as well. 

        - Never got there due to the way I decided to scale the business.  The entire thing was also bootstrapped by friends plus I was running out of patience.

    - Recreational players abroad are super expensive to acquire and retain

        - Supporting multiple poker web site hand history formats and building hand converters also became a nightmare with our limited engineering bandwidth



- Build more poker tools for popular variants like NLHE and tournaments

    - My experience trying to scale the PLO business made me understand how small the entire market is. Definitely wasn't worth the time and effort. I was no longer naively optimistic.

    - I was asked super often to build a version of the tool for MTTs by my poker friends. Glad I didn't blindly follow my customers.   

- Start monetising other proprietary tools (custom built for my staking operation) by selling it to poker websites

    - We had built some chip dumping and collusion detection tools to help our stable players identify profitable tables. On the flip side, there was demand from poker companies willing to use this to find multi-accounters, colluders, bonus chip abusers, RTA users etc. 

        - <b>I ended up personally consulting and working with leading poker sites in India to build their anti-fraud systems.</b>

- Continue selling it to stables and professionals and figure different opportunities

    - I ended up doing the above two.

    - While I was exploring options, I was reached out by a recruiter looking to hire somebody to build their poker business at Paytm. I found this to be decent opportunity to learn the ropes of building a scalable business and joined them at the start of 2022


#### Afterthought

- If I have to do it all over again, I would:

    - Definitely pick a better market. Poker needs to grow as a game globally before there is a meaningful sized market for study tools especially in a country like India. I wasn't okay serving just 100 customers. 

    - Experiment faster. I wasted a lot of time perfecting the tool for my initial PLO customers.  PG argues the [opposite](http://paulgraham.com/ds.html), but with a different context. Airbnb folks eventually had a massive market to get into which I didn't have.
   
