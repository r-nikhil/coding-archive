---
layout: post
title: AI.Engineer 2025 conference - Key takeaways
categories: [ai]
---


I attended the [AI.engineer](https://www.ai.engineer/) conference held in the first week of June at San Francisco. It was the largest technical AI conference of the year, bringing together over 3,000 engineers and leaders building with AI. The event featured 18 specialized tracks with 150+ sessions running simultaneously plus an expo with 50+ companies across the AI engineering landscape.

Key Participants: Major AI labs (OpenAI, Anthropic, DeepMind, Cartesia), infrastructure platforms (Modal, Baseten, Temporal, Vapi, Daily), GPU leaders (NVIDIA, Cerebras, Groq), and a ton of other AI startups. You can find the entire list of companies [here](https://www.ai.engineer/#SpeakersList). Unlike theoretical AI conferences, this event focuses on engineers building and deploying AI systems. Sessions emphasized practical implementation, live demos, and real-world technical challenges rather than speculative discussions. They also had an online track with about 70 lectures. You can find them [here](https://www.youtube.com/watch?v=J3oJqan2Gv8&list=PLcfpQ4tk2k0Vu8ZKg_5TzN87mRhRJt71Y&index=2). You can watch some of the live streams from the conference [here](https://www.youtube.com/@aiDotEngineer/streams). I personally liked the keynotes from Greg Brockman and swyx. 

Some key trends: 

1. Multi-Agent Orchestration - The platform opportunity for AI infrastructure
2. MCP Protocol Standardization - Creating the "app store" for AI tools
3. Evaluation as Competitive Moat - Critical infrastructure as AI moves to production
4. Development Parallelization - The rise of ambient agents
5. Tiny Teams Revolution - New capital-efficient business models


<u>Multi-Agent Orchestration</u>

The biggest technical shift is from single agents to "agent swarms." OpenAI's Greg Brockman articulated the future as "not one big AI in the sky, but a panel of specialized agents working together." Google Labs demonstrated "Jules" - their parallel coding agent that requires developers to orchestrate multiple agents simultaneously. Microsoft showcased Project Amelie - an autonomous ML engineering agent that can be @mentioned in GitHub to analyze codebases and generate ML models(like Automl copilot). We did multiple workshops where we had to play the role of an "AI agent manager" just orchestrating and prompting agents to get some work done which was a lot of fun. 

**Investment takeaway:** Multi-agent infrastructure is the next platform for AI opportunity. (think Kubernetes for AI agents). Early winners will build orchestration frameworks handling agent communication/coordination, task delegation, and context management, latency optimisation and cross agent memory management. Winners here will have deep tech expertise and strong evaluation frameworks for their domain specific agent workflow. 

<u>MCP Protocol Standardization</u>

Every AI startup has adopted MCP. Technical advantages include dynamic tool discovery, sampling (agents requesting LLM completions through clients), and bidirectional communication via streamable HTTP. Anthropic issued an explicit "Request for Startups" seeking MCP servers in sales, finance, legal, and education verticals. 

**Investment takeaway:** MCP creates a massive platform play similar to early mobile app stores. First-mover advantage goes to teams building vertical MCP servers (collapsing domain expertise like legal, accounting etc into standardized tools) and horizontal infrastructure (automated MCP generation, enterprise hosting, security and observability). Security focused MCP infrastructure is pretty hot too since enterprises demand compliance and auditability. 

<u>Evaluation as Competitive Moat</u>

Traditional generic benchmarks(like MMLU, GSM8k etc) fail to capture real-world AI application performance for your particular AI company in a specific domain. New approaches include hierarchical evaluation models, AI-assisted manual evaluation, and some complex LLM as judge rubrics fine tuned for your specific domain and task.  Pi Labs (our portfolio) demonstrated breaking AI outputs into 300+ distinct signals - similar to Google's search ranking. Each signal gets automatically scored, then weighted into overall quality scores. The companies with robust eval pipelines can iterate faster and deploy more confidently. The biggest most for most of these companies has become their eval pipeline.

**Investment takeaway:** Evaluation tooling represents critical infrastructure spending as AI moves to production. However, out of the three components of an eval tooling startup (datasets, platforms, judges), the central platform component has commoditized. It's all mostly a dashboard to do prompt management and define your scoring metrics. We should be looking for startups building generation pipelines for proprietary evaluation datasets, domain-specific metrics, and proprietary judging mechanisms. 

*I would personally start checking if AI startups(across domains/verticals) can articulate their eval strategy in the pitch meetings. This is such an important part of building with LLMs.*

<u>Development Parallelization</u>

Multiple teams (Dagger, Morph Labs, Google, Factory AI) demonstrated development parallelization: AI agents exploring multiple solution paths simultaneously. Engineers are moving from sequential coding into orchestrating parallel agents. Technical architecture enables spinning up isolated environments to test variations (code architectures, product features, bug fixes) in parallel, then merging successful approaches. Windsurf demonstrated their "shared timeline" between human and AI, handling everything from code generation to API provisioning to deployment. 

**Investment takeaway:** Parallelization infrastructure will become as foundational as CI/CD, but technical challenges around merging, arbitration, and cost control still exist. Market parallels the early containerization wave : Docker-equivalent opportunities for AI parallelization(the Docker CEO itself is building in this space). We should look for vertical coding agents (e.g., infrastructure, mobile, ML pipelines, or any specific domain) and agent orchestration tools for development teams. 

<u>Tiny Teams Revolution</u>

The emerging success metric: companies with "more millions in ARR than employees". Met some VC's who are using this to judge companies. Companies like Gumloop, Gamma, Harvey, HeyGen, Windsurf spoke about their "path to 10-person unicorn" via AI-leveraged teams. These teams achieve extreme capital efficiency by building AI-first from day one rather than retrofitting traditional operations.

**Investment takeaway:** Massive opportunity for B2B automation tools that enable tiny teams to punch above their weight. We should look for companies where AI handles the "middle management" layer - orchestrating work between human experts rather than replacing them entirely. The key differentiator is execution speed, not defensible IP. First-mover advantage matters more when you can build 10x faster than incumbents can respond.

---

There were also tracks like GraphRAG, PMs in the time of AI and agent reliability which were also quite popular. Also, please reach out to me if you want to learn more about any particular topic or if you want the slides/workshop material. 