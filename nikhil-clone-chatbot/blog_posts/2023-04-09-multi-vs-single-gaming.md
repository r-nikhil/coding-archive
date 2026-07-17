---
layout: post
title: Do multi-gaming apps make sense? 
categories: [markets, poker]
---

I've been thinking about multi-gaming platforms due to their recent meteoric rise to [capture about 10%](https://rnikhil.com/2023/04/03/gaming-state-india.html) of the RMG market and the fact that I have to make a decision at work on bundling a mini-game with our main app. The multi-gaming segment is also growing at about 40% y-o-y which is the highest among all RMG segments. While one can argue that this growth was mostly driven by monstrous advertisement spends, this document tries to dig a bit deeper into the user behavior/personas between Multi Gaming Platforms and Single Gaming Platforms, framework to define value of adding/removing each game in the bundle, mental models for packaging games and finally some perspectives on user requirements/needs and way forward for building multi gaming apps. We want to basically explore why everybody is packaging games together or building yet another subscription service?

### Background

If you talk to my colleagues at work, they will tell you that I've been a fan of single gaming apps and against bundling random games together. I've been a power user (was playing [PLO](https://www.pokerstars.in/poker/games/omaha/) professionally) and I personally never saw any user (in my bubble) splitting their sessions between playing 500 hands of poker and 100 rounds of rummy. Both are skill games and played with cards but I've never seen them played together. If thats the case, why do apps bundle them together? Even worse, they bundle Poker and Fruit Ninja together.

Moreover, given that majority of your revenue is going to come from these power users, I never really understood bundling random games like Fruit Ninja, Ludo etc along with the target game of the power user. In fact, the product folks behind Hike seemed to have reached a similar conclusion. A quote from their post: "Even though we have 10+ games on the platform, most users preferred to play 1 or 2 specific games that they liked the most. Users like to have options but have specific preferences when it comes to actual game play". You can read the full post [here](https://blog.hike.in/rush-homescreen-d64a7406dc78). Plus, ARPU of single gaming platforms is 3-4x higher than multi-gaming platform. Users seem to spend more on the same game inside the standalone app compared to the multi-gaming app as we can see from the below table:

<div align = "center">
<img  src="/assets/files/poker.png"  height = "400" width ="650">
</div>

Given these obvious pros of standalone apps (better ARPU, filled with power users) and cons of multi gaming apps(no obvious user overlap, bad ARPU), why are multi gaming platforms growing? This blog post basically tries to prove the above premise (single gaming is generally better than multi gaming) <b> wrong.

### Content

- Is bundling games good or bad?
- What is a "correct" package of games?
- How to package games?

<h4 align = "center">Is bundling games good or bad?</h4>

For the rest of the discussion, we will consider these 4 games: Rummy, Poker, Ludo, Fantasy and debate on whether to build a stand alone app or a multi-gaming app comprising all the games. Let's also split our users and their behavior like this:

<div align = "center">
<img  src="/assets/files/usertype.png"  height = "400" width ="650">
</div>

Now that we have our four games and three types of users, lets consider two scenarios:

<b>Scenario 1:</b> We build single gaming apps for the games and market them independently. This means, we are primarily trying to attract power users (only fans of Poker would have Poker installed) and will only collect revenue from them. Moreover, a consumer would only have access to game of which they are fans of. They miss out on the other games they otherwise might have played and enjoyed inside a multi-gaming platform. Clearly in this case, we lose out on the casual user revenue if we do single gaming apps and consumers lose out on discovering games they might have liked.

<div align = "center">
<img  src="/assets/files/gamebundle.png"  >
</div>

<b>Scenario 2:</b> We build a multi gaming app which has all the games bundled into it. In this scenario, we not only provide power users their favorite game but also allows them access to game they might be "casual users" of. A poker power user might be a "casual user" of Fantasy sports. Also, from a business standpoint, my total addressable market(TAM) is much bigger than my earlier user base because I am now targeting the casual user market of all the games as well.

We can see that, both the platform and the user benefit from multi gaming apps. While the core power user hasn't changed their behavior much, we have now allowed for casual users to participate and discover new games. Having casual users on the platform is super beneficial especially in real money gaming(RMG) setting where most match-ups are PvP and prizes are pooled in from the players. The utility or value of a gaming network is exponentially proportional to the number of nodes (players) in the network. Once you have a critical mass of users, you can see hyper exponential growth due to the above relationship. Multi-gaming platforms capitalize on these factors to grow fast and big. Clearly, Single Gaming Platform model doesn't maximize value because power users don't get games which they maybe interested in and platform providers clearly cannot run a sustainable business without casual users. We can also philosophically say that having <b>multi gaming apps is mostly about serving casual users</b>. (this point will become important towards the end)

Couple things stand out from the above scenarios:

- If you go down the Single Gaming Platform route, you clearly isolate your power users preventing any kind of interaction with casual users. However, power users mainly come for the casual user population to play against and your player volume will suffer. Ultra important for RMG.

- Each power user gets access to a platform which has only the game that they wanted. Even if they wanted to try Fantasy sports during cricket season, that isn't possible


For example, take the poker variant called Pot Limit Omaha (5card) game. If you ask a random person what it is, you most likely would get a binary answer - either they say that they play the game regularly or ask the full form of the abbreviation. This is because PLO5 has very little casual users - which I believe is attributed to the fact that its never bundled outside of poker apps. A fruit ninja /hyper casual gamer never got PLO5 as part of their Multi Gaming Platforms. However, if you ask a random person if they are a fan of Fantasy sports, the answer this time would fall in a continuous range between a power user(I play every match) to non-user( I've tried it once or heard about it somewhere). Fantasy sports certainly has power users but has a big population of casual users too. Interestingly, most of these gamers don't even know where they started playing Fantasy. It looks like by virtue of signing up for a multi gaming platform, they randomly played a match.

> <b><u>Conclusion</u>: Bundling is good for gaming apps when done correctly.

But, what does "correctly" mean? We also know that ARPU suffers from bundling? How do we measure and understand them? Continue reading the next part to know more.

<h4 align = "center">What is a "correct" package of games?</h4>

In the previous section, we concluded that bundling games together is beneficial for both the platform and the customer. In this section, we look at some frameworks which will help us decide on which games to add/remove from a bundle? We try to dig deep about what each of our user personas value inside our app and try to look for possible solutions. We also explore some thoughts around evaluating individual games inside a bundle.

By now, most readers of my blog would have understood three basic things about RMG businesses:

- 85% of money is made from 15% power users
- Power users come to your platform for casual user population
- Recreational users come for big bonuses/awards/prizes/competitions

<b>Question to the reader:</b> You are a multi-gaming app. You have both Poker and Ludo. They both make the same daily revenue. Which game is better is for the platform? Or in other words, which game is the platform fine with removing?

<b>Another question to the reader: </b>You are a multi-gaming app. You are exploring acquiring a game studio and integrate their games into your app. How should both the parties in this transaction think about their decisions?

To answer these questions, we need to define the marginal utility of having the game on the platform. The marginal utility of this game is evaluated based on its ability to acquire new users and retain the existing user base. Or put another way, we should evaluate "how many players would leave my platform, if I remove this game today"? Or from an acquisition POV, "how many players will join my platform if I add this game today?" The quantitative answer to these questions is tightly correlated with the value of the game. 

To visualize, this, lets look at at the example between Fantasy and Poker. While Fantasy has lot more users, Poker has higher marginal utility in preventing churn and attracting high value users.  

<div align = "center">
<img  src="/assets/files/usage.png" width = "600" >
</div>

For example, lets imagine that if Poker was removed from our multi-gaming app, then 10% of the users would churn. If the overall platform ARPU is about Rs. 300/month and say 1M users play, this would be mean about 100k users churning out, which means a loss of 100k * Rs.300 * 12 (yearly) = Rs. 36Cr/yr in revenue at risk. This means, Poker is valued at about Rs.36Cr to the platform*. This would be somewhat the amount, a gaming studio should be paid yearly if they are running the poker business for multi-gaming app.

Why is Fantasy sports valued at lesser even though it has substantially more usage? Because, the percent of power users who are going to churn out of the app is going to be substantially lesser (Fantasy has a very small power user base). Casual users won't care much and the platform won't be affected either.

Lets try to mathematically define this relationship:
> <i><b>Value of game to the multi gaming platform = Value of an average user of the platform * Marginal utility of the game in preventing churn.</b>

Marginal utility of the game in preventing churn is basically the percentage of people who would churn out if you remove the game from the platform. The idea is that the value of the game is related to its impact on EVERY user of the platform. In some sense, we are distributing the power user value of the multi-gaming platform into the broader population of casual users and non-users of the platform. We are exposing them to these games for free which they otherwise would never have found on their own. Finally, to exactly calculate the value of the game, you should remove it from your app, calculate the customers you will lose and establish the revenue loss due to it.

However, this approach is not exactly practical. I cannot remove a game from my app tomorrow to prove that it has value. For a company/product manager to do this exercise, we need an alternate approach to define value of the game. Remember that earlier, I had mentioned that from an acquisition POV, value of a game is the "number of new users" it will bring to the platform because of its addition.

Lets again take the Poker example to explain this situation. I am trying to decide on including Poker into my Multi Gaming Platform. Lets assume that the value of the game standalone is X(whatever an individual game studio makes running it alone). So, if I have to think about integrating poker, how much extra revenue/value would I get? The answer definitely cannot be equal to X. To figure this out, we first need to understand our current user base and how it will overlap with Poker in the first place. Does adding this game unlock an entirely new Total addressable market (TAM) for me? or the players of this new game are already my customers?

Lets consider two extreme scenarios to answer these questions: 

<b>Case 1:</b> Fully overlapped power user base. Remember, we inherently assume that single gaming apps are composed of power users only(refer to the first section of this post for clarity). This means, all the power users of poker are already an user of the Multi Gaming Platform.

To elaborate further, lets assume that the multi gaming app has 1M users with Rs. 300/month as ARPU. Poker standalone has 250k users with ARPU of Rs. 400/month. In this case of full overlap between the power user base, all these 250k Poker users are already a customer of the multi gaming app. They are poker power users but playing some casual game inside the multi gaming app for now.

In this case, so how much does the platform expect to make when they integrate/launch poker? They are still going to have the same amount of users but they with the addition of poker, the power users get activated(they were casual users before) and start playing the game inside the multi gaming app. A lot of casual users are now getting exposed to poker and power users have increased engagement inside multi-gaming app because they now have their favorite game as well. Power users like the fact that the game is bundled and they don't have to split their deposits between two platforms and thereby have higher retention too. While some value is getting created, its hard to quantify. 

However, this is the worst scenario and adds very little value to the platform. Lets look at the other case.


<div align = "center">
<img  src="/assets/files/overlap.png"  height = "400" width ="650">
</div>

<b>Case 2:</b>Zero overlap between power user base. This means, all the poker power users are isolated and currently don't play inside the Multi Gaming Platform. They only play on their standalone poker app. From the platforms POV, this is exciting because of new addition of all these power users who are now coming to your Multi Gaming Platform for the game plus the fact that existing customers of Multi Gaming Platform get Poker for free(without installing any extra app). This contributes to direct increase in revenue.

To elaborate further, lets assume that the multi gaming app has 1M users with Rs. 300/month as ARPU. Poker standalone has 250k users with ARPU of Rs. 400/month. Lets look at this integration form the eyes of both the platform and poker standalone app.

Platform: They get these 250k new users directly and get Rs. 300 * 250k = Rs. 7.5Cr per month extra. If you go back to my first equation which is <i>value of game to the multi gaming platform = Value of an average user of the platform * Marginal utility of the game in preventing churn</i> and plug the numbers, power users who will leave the platform if you remove the game =  value of game (Rs. 7.5cr)/Rs. 300 = 25% This is the percent of the user base which will churn out if you remove Poker which is about 250k users.

Poker standalone: They were making Rs. 10cr earlier, but the platform has assigned a value of only Rs. 7.5cr to it which means they obviously won't agree with this integration. So, why where will the extra 2.5cr come from? Where is the calculation issue?

To understand this, we need a different way for the platform to calculate value of poker (post integration). They cannot simple use old ARPU numbers. Lets double click on this thought and try to define a practical mathematical relationship:

> <i>Value of game to the platform = Value of power user (ARPU) of standalone app* percentage of customers who are power users of your game inside the Multi Gaming Platform post integration</i>

<i>Note: LHS of both equations is same.(this will matter later on).If you integrate Poker and 100% of your users become power users of poker, your platform will basically have same value as a standalone app. If nobody becomes a power user, then value of Poker is zero for the platform.</i>

Assuming 25% of them convert to power users inside the app, now the value of the game to the platform = 250k users * Rs. 400 (new power user ARPU) = Rs. 10Cr. Now they can happily pay the 10Cr that the standalone app wants.

This is the best scenario that the platform as well as the poker standalone app wants. Everybody makes more or equal money than they made before.

Great!. We have established some equations for defining value of a game inside a multi-gaming platform. However, this section started with the promise of teaching you to find the "optimal" packaging of games.

We introduced two ways to define value of a game. One is through understanding churn and another is through understand acquisition. Now, if we equate both sides of this equation, we have:

> <i>Value of an average user in Multi Gaming Platform * Marginal utility of the game in preventing churn = Value of power user (ARPU) of standalone app* percentage of customers who are power users of your game inside the Multi Gaming Platform post integration</i>

When both the previous equations match, the platform packaging the game and the game provider are in equilibrium. Both of their interests get satisfied and it makes logical sense to package the game instead of running it standalone. I would call this bundle of games "correct".This summary is interesting because Power user% (RHS) is easer to understand and measure compared to "marginal utility in preventing churn". For the latter, you can just look at a standalone Poker app for proxy (assuming these newly converted power users will behave the same as standalone app users) but for the former, you will have to remove Poker from a Multi Gaming Platform to measure it accurately.

>Conclusion: We defined what an optimal bundling of games should look like and various parameters affecting it. We came up with an interesting equation which can be used to form mental models regarding relationships about games and how they interact with game bundles.

But what is the implication of this equation? What does it mean for the kind of games I have to choose for my bundle? Is Poker + Ludo a better bundle or Poker + Rummy? Continue reading to answer these questions.

<h4 align = "center">How to package games? </h4>

In first section, we concluded that, Bundling games is good when done "correctly" and in the second section we defined how to quantify what a correct bundle looks like. Now that we have concluded that we have to bundle games, we need to establish a framework around choosing and picking games to bundle inside a Multi Gaming Platform.

Lets start with the commonly established logic. You should pick and pack games which have the least amount of power user overlap and maximum amount of casual user overlap. This means, you package Poker along with card games but not with candy crush/wordle/bubble shooter etc. This also makes logical sense and I was a firm believer of this as well.

However, this section we try to determine if this is actually true and if you should actually bundle Poker with something like another card game/chess or wordle/racing game/etc.

Lets go back to the second section, where we were trying to ascertain what the game vs game bundle relationship looks like. Lets restate the equation here again:

> <i>Value of an average user in Multi Gaming Platform * Marginal utility of the game in preventing churn = Value of power user (ARPU) of standalone app* percentage of customers who are power users of your game inside the Multi Gaming Platform post integration</i>

We ascertained that the packaging of games will be optimal(Case 2 is best scenario to package) when there was a completely distinct power user base. The power user base of poker is being used to it maximum value by adding new customers to the platform. In the above equation, given that ARPU of users are unaffected (for our purposes), we can observe that the extra utility of having power user in the platform(preventing churn) is becoming equal to the percentage of customers who are power users of the game inside the Multi Gaming Platform.

So, what does it mean? We have proved that adding a game which already has power user overlap with your app is not the most ideal but rather adding a game which has the least overlap is beneficial. Why though? as you can see below, from the perspective of an user, if you are a power user of rummy or poker or ludo, the Multi Gaming Platform is a good value. From the platforms POV, it gets to add new users because of adding the extra game. From the customers POV, if they are a power user of either Poker or Rummy or Ludo, the app is a good deal. You can the Shishir's post linked at the bottom for a generalized explanation of this behavior. 

Now if the Multi Gaming Platform is already valuable to the user (they installed it for some game of which they are a power user of), they will not care about adding another game to it. The value of the app for the power user comes only from their target game. So, you are better off adding a game that someone else (ideally a non-user) would be a power user of instead of adding another similar game.

<div align = "center">
<img  src="/assets/files/mgp.png"  height = "400" width ="650">
</div>

The customer will see value in the Multi Gaming Platform compared to the Single Gaming Platform if

- it has the game he is a power user of
- product experience of that game is equal to Single Gaming Platform
- it has at least one more game that he is a casual user of, that he wants to play. (else he will install the standalone app only)

To take this to an extreme, the best multi gaming platform would have all the games its users are power users of. Everyone gets their favorite game and also gets access to a game there are casual users of(1 game per user basically). If there are no casual users (meaning, I play only one game), then this is no worse than installing the game separately. But any amount of casual user overlap will justify the packaging of games. Fundamentally, this basically tells that multi gaming apps is more about providing value for casual users than power users.

> Conclusion: Add games which have minimum power user overlap and maximum casual user overlap. This is why Poker + Ludo is better than Poker + Rummy.

This section is the most counter intuitive of all the other sections. Because, we basically concluded that we should be adding games which are diverse and have the least amount of power user overlap. Does this mean, I will add a racing game to my Poker platform? Short answer is yes, but with some nuances. It is hard to market super diverse bundles. If very hard to market a poker + racing Multi Gaming Platform compared to poker+rummy Multi Gaming Platform. But that is just a marketing challenge because we now know for a fact that our games have to super diverse and minimize power user overlap. Same reason Amazon is bundling Prime Video with fast shipping. To summarize :

- Put together a list of games with minimum power user overlap and maximum casual user overlap
- Ensure that there is no downgrade in user experience for power users in each of these games
- Show users only the games that they are likely to be a power user of
- Make sure there is clear integration value and the app is overall coherent.

<b><i><u>Final thoughts

Bundling is a natural evolution for many businesses and can lead to increased productivity and value. Amazon, Netflix, McDonald's, etc all use it to their advantage and continue to add very diverse items into their bundles. Netflix has games. McDonald's hands out toys with burgers and the Amazon Prime package is massive and diverse.

However, we should be cautious as well. There are some unmeasured factosr which I have omitted in the article like:

- conversion% of power users after you integrate may not be 100%
- power user behavior can change with time (influenced by losing money)
- matching product experiences between SGP and MGP is hard
- this framework doesn't work if the ARPU difference is very high between the game and the platform

This framework can be applied to more general product development, such as contemplating which set of features to put behind a subscription service. You can use this framework to decide the marginal utility of any single feature/product. Bundles of the future will be larger and more diverse than what we have today because packaging has a natural economy of scale attached to it. It is much easier to go from 100M users to 101M users than it is to go from 0 to 1M users. This is largely caused by casual user overlap (there are no 100M power users) - the larger your bundle, the more casual users you can amortize costs between and faster you grow. 

If you liked reading this post, please share it with your product and business friends and checkout my other posts too:

- [GTO Inspector - My attempt at building an online business](https://rnikhil.com/2022/06/15/gtoinspector-startup.html)
- [Some notes on RMG market in India](https://rnikhil.com/2023/04/03/gaming-state-india.html)
- [Make Poker Fun again](https://rnikhil.com/2022/08/22/profit-growth-gamification.html)

Further Reading and Sources:

- [The effect of anchoring in product bundles](https://repositorio.ucp.pt/bitstream/10400.14/26226/1/152116038%20Marta%20Gomes%20W.pdf)
- [How Buyers Evaluate Product Bundles: A Model of Anchoring and Adjustment](https://www.jstor.org/stable/2489825)
- [Shishir Mehrotra's post on bundling in general](https://coda.io/@shishir/four-myths-of-bundling)
- [The OG Chris Dixon post on "How bundling benefits sellers and buyers"](https://cdixon.org/2012/07/08/how-bundling-benefits-sellers-and-buyers)

*Do notice the fact that we aren't talking about game revenues here but some intrinsic concept called "value of the game" which we are trying to define.
