---
layout: post
title: Quick thoughts on evaluating agents
categories: [ai]
---

I recently encountered some companies which are in the due diligence and report generation space. They all use a multitude of AI agents to plan and do the research and this made me wonder how these agent stacks are evaluated.

Primarily we can simplify AI agents to be nothing but LLMs + tool use + some logic flows which might be controlled by an LLM. While evaluating these agents, we are primarily concerned about:  
  - Are they saying the right things? 
  - Are they acting the right way? 

<u>Do they say the right thing? - What does it mean? </u>
  - This is primarily evaluating the textual output of the systems. I have written a lot about evaluating LLM outputs for safety, consistency, hallucinations(RAG and otherwise), compliance and any custom policies. This is a fairly well known topic and you can refer to my older blogs for that. 
  - Do bear in mind that some of these agents could be running in a loop and we will also have to think about evaluating a multi-turn agent too. Here we have to consider things like
    - Conversation consistency - is the agent keeping up with relevance scores in a multi turn conversation? Is it consistent with the facts used across all the turns? Is it adhering to the topic and is it reasoning well? You will basically have to construct a compound metric from the single turn step to measure this.

<u>Are they acting the right way?  - What does that mean? </u>
  - Are they following the instruction loop and logic related to the usecase? 
  - Are they using the right parameters and inputs for calling the tools? Are they selecting the correct tool consistently and accurately? How is it handling errors with tool calling(ex: structure/format issues) and instruction loops? Does it fail gracefully? 
  - Multi step considerations: 
    - Is the agent breaking down the task sensibly? Is each individual task progressing and helping the agent achieve the goal? Is the plan devised by the agent of high quality and aligns with the use case? 

<b>Real life evaluation considerations: </b>

  - First, you need to break down your AI application into logical components and define metrics to measure the items mentioned above. While there are a lot of pre-defined metrics available for the first part (how does the LLM talk), you need to come up with internal task-specific and tool-specific metrics for the second part. Ultimately, evaluating agents are very similar to evaluating any LLM system. All the outputs must be grounded in reality and compliant. Every action of the LLM system must be accurate and the ultimate metrics of this agent system will be its goal completing rate. 
  - Set up a tracing/debugging stack to observe the inputs/outputs of each LLM component. Make sure error management is baked in. Lot of the agent stacks have a "replay" feature which will help run simulations of your agent stack. 
  - Start thinking about cost and latencies too. You want to serve your stack as fast as possible and as cheaply as possible. While this won't matter in the early days, this will definitely start rearing its ugly face as soon as you scale. 
