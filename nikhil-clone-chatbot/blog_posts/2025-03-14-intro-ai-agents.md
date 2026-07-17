---
layout: post
title: Introduction to AI agents
categories: [ai]
---

> This is the first couple pages of a report I worked on about AI agents.

### What are "AI Agents"?

In this section, we try to define what an agentic system is. Automation software(like email to calendar booking tools) are generally oversold as agentic systems and it's important to ensure we all have the same understanding of the lingo used in this space. 

Peter Norvig in his popular [book](https://www.amazon.in/Artificial-Intelligence-Modern-Approach-Prentice/dp/0136042597) defines an agent as anything that can perceive its environment and act upon that environment. A thermostat is an agent. A motion sensor light or smoke detector is also an agent. However, these are all dumb agents. We are more interested in building intelligent agents with LLM/AI as its core controller.

Interestingly, the definition of the term "AI agents" is [hotly](https://x.com/NickADobos/status/1714065139878482030) contested. Most of the common ones involve some version of putting LLMs + tools in a loop. Rather than looking at LLM systems in a binary way, it's more useful to think of them to be agent-like to a different degree. The degree of control given to the LLM in guiding an application's flow allows for varying levels of autonomy, which we shall call agentic. This helps us move away from the binary classification of systems and look at them as part of a spectrum. Ultimately, you want to give it a task and the AI is agentic enough to go and accomplish it.

<div align = "center">
<img  src="/assets/files/agentspectrum.png">
</div>

### What are the different types of AI agents?

Since we have established that all LLM+tool powered systems are agentic on some level, we need to first classify the different types of agents. Borrowing the definition from [Anthropic](https://www.anthropic.com/research/building-effective-agents, we have two types of agentic systems. 

<u>Workflow agents</u> are systems which are built by chaining together LLMs and tools which then are orchestrated through pre-defined code paths

Types of workflow agents:

- **Prompt chaining**, e.g. generating a document and then translating it to a separate language as a second LLM call. Real-world applications include marketing (drafting then localizing content), content creation (outlining then writing) or basic data analysis (cleaning then visualizing)
- **Routing**, where an initial LLM call decides which model or call should be used next (sending easy tasks to Haiku and harder tasks to Sonnet, for example). Can be used in customer service (sending different query types to specialized handlers)
- **Parallelization**, where a task is broken up and run in parallel (e.g. image-to-text on multiple document pages at once) or processed by some kind of voting mechanism. Parallelization is effective when the divided subtasks can be parallelized for speed, or when multiple perspectives or attempts are needed for higher confidence results
- **Orchestrator-workers**, where a orchestrator triggers multiple LLM calls that are then synthesized together, for example running searches against multiple sources and combining the results or in coding tools where the agent is making changes to multiple files at the same time
- **Evaluator-optimizer**, where one model checks the work of another in a loop and starts a feedback loop. This architecture is useful in scenarios where you need a second LLM to ensure the response is complete and correct


<div align = "center">
<img  src="/assets/files/workflowagent.png">
</div>

<u>Autonomous agents</u> are systems where the LLM dynamically directs the execution path and tool usage and maintain full ownership on how they accomplish the task. They have no predefined paths to take. They start their flow from a simple command or conversation with the user, plan the task and use tools to accomplish the task. They might choose to ask humans for feedback or when encountering blockers and automatically terminate themselves when the task is completed.



<div align = "center">
<img  src="/assets/files/autoagent.png">
</div>

They are particularly useful for open-ended tasks where it's hard to predict beforehand the number of steps required and where you can't really hard code a fixed path. Some real world applications include CX agents which, based on the user conversation, automatically decide to access customer data and perform actions like issuing refunds and updating ticket statuses. In software development, coding autonomous agents are excellent because the solutions are verifiable, agents can iterate based on feedback from automated tests and the problem space is well defined

<u>Workflow agents in general are more predictive, consistent, cheap and fast whereas the autonomous agents generally excel in complex tasks where you need flexibility at scale.</u>


### Architecture of autonomous agents

Before we jump into the tooling and infrastructure world for AI agents, it’s imperative to understand what exactly they are made of. While the LLM functions as the core brain, its complemented with some key components:

- **Planning and reasoning:** Breaking down tasks into subtasks, self reflecting on the progress, and iteratively improving the action plan
- **Memory:** Both short term memory (in context learning frameworks like MemGPT) and long term memory like a vector store
- **Tool use:** The LLM is trained to call external tools for tasks it can't do by itself like pulling up current information or executing code

<div align = "center">
<img  src="/assets/files/archagent.png">
</div>

#### Why did they blow up in 2024?

The LLM functions as the agent's brain and agents typically require much powerful and bigger models compared to non-agentic use cases. This is because mistakes in <u>multi step tasks get compounded</u>. If an LLM is accurate, say 90% on a single step, this accuracy drops to 35% over 10 steps(0.9^10) and 12% over 20 steps. Smaller LLMs (and LLMs not trained on agentic flows) are simply unfeasible for these use cases. 

Lot of core frameworks for agent planning were invented in 2022 and 2023. [CoT](https://arxiv.org/abs/2201.11903) or [Tree of thoughts](https://arxiv.org/abs/2305.10601) for example are standard prompting techniques for enhancing model performance on complex tasks. This forces the model to spend more test time compute in thinking step by step and break down big tasks into multiple smaller subtasks. Even self reflection frameworks (like [ReACT](https://arxiv.org/abs/2210.03629)) were invented in 2023 which help the LLM improve iteratively by refining past actions and correcting previous mistakes.

#### An action sequence of a simple multi step agent
Lets consider a scenario where you ask your AI data analytics agent this question - "Analyze customer churn rates for our app subscribers". This might make it go and perform the following:

- Reason about how to accomplish this task. It might decide that to analyze churn, it first needs historical subscriber data.
- Invoke data retrieval to get subscriber counts over the past year. (Text to SQL)
- Invoke data processing to calculate monthly retention and churn percentages. (Code execution)
- Reason about the initial findings and determine that user engagement metrics might provide valuable context for why customers are churning.
- Invoke additional data retrieval to obtain app usage frequency and session duration. (Text to SQL)
- Invoke statistical analysis to identify relationships between usage patterns and churn.(Code execution)
- Generate visualizations and insights about churn trends, highlighting key segments with highest churn risk. (Code execution)
- Reason that the task has been successfully completed with actionable recommendations to reduce churn.

### When and where are AI agents used?

The value add for agents is clear. Copilot was [40% of github revenue](https://virtualizationreview.com/Articles/2024/07/31/copilot-numbers.aspx) last year. Klarna AI agent handles 65% of the CX queries end-to-end. In this section, we look at ideal use cases and tasks for deploying AI agents. 

While we have briefly looked at which agent architecture works for which kind of flows, we should also define what makes a task agentic vs non-agentic.

<div align = "center">
<img  src="/assets/files/agenttask.png">
</div>

A market map from [Felicis](https://www.felicis.com/) showing some early winners in the AI agents space

<div align = "center">
<img  src="/assets/files/marketmapagents.png">
</div>

- Customer service  
  - AI agents analyze call data, manage chatbots, and handle complete support workflows autonomously from greeting to resolution, including processing refunds by checking orders and updating inventory without human intervention.  
  * Ex: [Decagon](https://decagon.ai/), [Sierra](https://sierra.ai/) , [Maven AGI](https://www.mavenagi.com/), [DevRev](https://devrev.ai/) and [Gradient Labs](https://gradient-labs.ai/)  
- Software development  
  - AI agents assist developers by automating code generation, debugging, quality assurance, and documentation creation. They can analyze codebases to identify potential bugs, suggest optimizations, generate unit tests, and maintain documentation as code evolves  
  * Ex: [Factory AI](https://www.factory.ai/) and [Cognition](https://www.cognition.ai/)  
- Research & Knowledge Work  
  - Agents gather information from trusted sources, summarize findings, format citations, and produce detailed reports  
  * Ex: DeepResearch from OpenAI, [Reflections](https://www.reflection.ai/) , [Sema4](https://sema4.ai/) for financial back office work, [NormAI](https://www.norm.ai/) for compliance reporting  
- Agent platforms are also performing well in other industries; ex: [11x](https://www.11x.ai/) is augmenting SDRs with better lead-gen, [Jasper](https://www.jasper.ai/) is solving for marketing/copyright use cases, [Mercor](https://mercor.com/) is solving the match problem in recruiting, [Abridge](https://www.abridge.com/) in healthcare, [Harvey](https://www.harvey.ai/) for legal workloads, or [Crescendo](https://crescendo.ai/) for contact centers. 
