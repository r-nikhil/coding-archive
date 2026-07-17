---
layout: post
title: LLM security - Introduction
categories: [ai, security]
---

Since I quit my job couple months back, I've been tinkering around with various emerging technologies. I have been pretty obsessed with the current AI evolution of large language models (LLMs) and their surprising text generation capabilities. Whether you are surprised or not, people have started integrating them into just about every software we interact with and after spending countless hours asking it to generate song lyrics, I eventually wanted to understand what was happening behind the scenes. I am no AI engineer and I barely remember the Machine learning/ Neural network courses I took in college, but given my computer security background, what better way to learn how these LLM's work than by trying to break them? In this post, we look at the basics of AI security, current "known" attacks, common defenses and some CTF challenges. I've been meaning to write this post for a while but this field was moving so fast that keeping up latest publications is a full time job. Now that NeurIPS is over and things have calmed down, I finally got time to work on this.

<div align = "center">
<img  src="/assets/files/attacks.png">
</div>

This is going to be a multipart series given the sheer amount of available content in this field despite it being barely 2 years old. Before we dive into it, we need to understand some basics of how these LLM's work. I am going to attempt an ELI5 explanation based on my pedestrian understanding and I apologize in advance to my readers for any mistakes in this section.

#### Text generation

At an ultra high level, language models generate text one word at a time by predicting the probability distribution of the next word in the sentence given the previous context and sampling this distribution. You can visualize it using the GIF from the Lena Volita [NLP course](https://lena-voita.github.io/nlp_course/language_modeling.html) below

<div align = "center">
<img  src="/assets/files/generation_example.gif" width = "400" height = "200">
</div>

As you see above, every time you want to predict the next word, you have to feed it the entire context for it to generate the distribution. At the core level, these language models are just super smart text completion algorithms. But how does this work in a chatbot setting? Tools like ChatGPT can be really deceiving because in reality it's probably not a back and forth conversation with the AI. Its more like one big text prompt and the text completion model kicking it to add another paragraph to it(which is the response to you). Its been [manually tuned](https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback) by humans to tailor the responses to make it seem like a back and forth conversation. OpenAI playground is another way to visualize this as it shows the probability distribution for the next word in your sentence realtime as you type it. Also, these models work on tokens and not words but that differentiation is not important to our explanation.

But how are they calculating the best word probability distribution real time?

#### Neural networks

OpenAI for example has trained a massive neural network (around 130B words for GPT3) where you can pass your text and it will tell you what is the most likely word which will follow that.

<div align = "center">
<img  src="/assets/files/neural.png">
</div>

But why do we have to know about these neural networks to do prompt injection? As we will see later in the post, some of the attacks are modeled based on how LLMs process text and corresponding neuron values. Some neurons track the [length](https://arxiv.org/abs/1506.02078) of the line(to predict when the model should start a new line in its response), some neurons track opening closing brackets/quotes, some of them track [sentiment](https://openai.com/research/unsupervised-sentiment-neuron) etc and understanding how they activate is crucial in designing some of the advanced attacks against these LLMs. Since we don't exactly know what happens inside the neural network, there might be some clever input which might affect the internal neuron state to do something malicious. 


#### What is prompt injection and why does it matter?

*Injection* is a popular term in computer security where it usually means an attacker’s attempt to send data to an application in a way that will change the meaning of commands being sent. There are many kind of [injection attacks](https://www.acunetix.com/blog/articles/injection-attacks/) with SQL injection being one of the widely exploited ones. Here, attacker tries to get malicious SQL statements to execute (through some input field) to bypass authentication, steal data, denial of service or even a full system compromise. Prompts these days are nothing but instructions to the AI. Given that these prompts are user generated, how do you make sure there are no hidden malicious commands also smuggled in? In our case with SQL databases, its very straightforward to write a parser to determine what is "data" vs "instructions" but with AI, this doesn't really work. Everything is just one big blob of text.

What is the thread model? Well, the LLMs works with a text prompt. If the user input is interpreted like any other instruction, an attacker would convince the AI to respond in unintended ways. How does it matter? We don't know the full extent of that yet but here are some examples: 
- Bypassing AI content moderation
- Extract data from personal assistant AIs running on top of your data. 
- Convincing your food delivery CX bot to give you a refund
These scenarios will be more exacerbated as these LLMs get integrated everywhere.  

#### Different types of prompt injection

There is a lot of content online about various prompt hacking methods. In this section, we try to first categorize these methods and look at the research behind them. Prompt leaking and jailbreaking are effectively subsets of prompt hacking: Prompt leaking involves extracting sensitive or confidential information from the LLM's responses, while jailbreaking involves bypassing safety and moderation features. We will also discuss specific offensive techniques as well as defensive techniques. 

#### Attacking LLMs

- Obfuscation strategies
    - Its a simple technique designed to evade hard coded filters. Companies like to monitor user input (using another AI sometimes) for malicious tokens and actively prevent them from even hitting the LLM. Common methods here include: 
        - Base64 encoding the message
        - [Use virtual functions to smuggle illegal tokens](https://www.reddit.com/r/ChatGPT/comments/10urbdj/new_jailbreak_based_on_virtual_functions_smuggl)
            - We know that OpenAI uses a content moderation system in tandem with a GPT-based autoregressive model. Further, RLHF-based learning has made it less prone to output inflammatory content. 

<div align = "center">
<img  src="/assets/files/mask.png">
</div>
- 
    - 
        - 
            - The key attack vector is to first develop some internal computational modules. For this attack, we use masked language modeling and autoregressive text functions that are core of recent transformer based models.
            
<div align = "center">
<img  src="/assets/files/functions.png">
</div>

- 
    - 
        - 
            - Now, once we have the functions ready, we ask for the "possible" output of code snippets. (tried to use 4chan here). Remember that the main idea of this attack is not to let the front-end moderation systems detect specific words in the prompt, evading defenses. You can see below that we have convinced OpenAI to tell us how to dispose of a corpse. Not what I saw in Breaking Bad. 

<div align = "center">
<img  src="/assets/files/out.png">
</div>
<div align = "center">
<img  src="/assets/files/outres.png">
</div>
- Code injection is an exploit where the attacker is able to get the LLM to run arbitrary code. This can occur in tool-augmented LLMs, where the LLM is able to send code to an interpreter, but it can also occur when the LLM itself is used to evaluate code. If you check this [example](https://atlas.mitre.org/studies/AML.CS0016/), people were able to extract the OpenAPI keys from a startup called MathGPT but just asking for it.  


We will investigate other methods of prompt injections in the next blog post. 