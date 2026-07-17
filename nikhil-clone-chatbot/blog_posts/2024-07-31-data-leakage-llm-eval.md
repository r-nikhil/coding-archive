---

layout: post
title:  Testing LLMs for Data Leakage Vulnerabilities
categories: [ai, security]
---
------------------------

This post was cowritten by me and was originally published on [Dynamo AI's blog](https://dynamo.ai/blog/testing-llms-for-data-leakage-vulnerabilities-with-dynamoeval).

<div align = "center">
<img  src="/assets/files/dataleak1.png">
</div>

[Recent](https://arxiv.org/abs/2012.07805) [studies](https://arxiv.org/abs/2302.04460)  [highlight](https://arxiv.org/abs/2311.17035)  a critical issue: large language models (LLMs) can memorize and reproduce text verbatim from their training data when prompted.

This raises significant privacy risks and legal liabilities, especially if the training data contains sensitive, copyrighted, or personally identifiable information (PII). Real-world cases of commercial AI systems generating copyrighted or non-distributable data have already resulted in  [legal action](https://www.nytimes.com/2023/12/27/business/media/new-york-times-open-ai-microsoft-lawsuit.html).

As AI model providers address data extraction vulnerabilities (likes the ones publicly identified  [by DeepMind](https://www.zdnet.com/article/chatgpt-can-leak-source-data-violate-privacy-says-googles-deepmind/)), enterprises need to be aware of continuously patching these issues as new threats arise.

Many enterprises are concerned about productionizing AI systems trained on a large, undisclosed datasets that might generate copyrighted or sensitive content. While the legal implications are still open for debate, enterprises often reference recent regulatory statements.

For instance, the  [White House Executive Order](https://www.whitehouse.gov/briefing-room/presidential-actions/2023/10/30/executive-order-on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/)  has tasked the US Copyright Office to “issue recommendations to the President on potential executive actions relating to copyright and A Similarly, others refer to the  [FTC warning](https://www.ftc.gov/system/files/ftc_gov/pdf/p241200_ftc_comment_to_copyright_office.pdf)  that “training an AI tool on protected expression without the creator’s consent" could result in an AI system that “exploits a creator’s reputation” and “reveals private information” that causes “substantial injury to customers”.

Given these regulatory concerns, it's crucial for organizations to assess whether their language models are at risk of leaking sensitive or protected data.

## Addressing emerging risks in language models

Over the past year, the Dynamo AI team has collaborated closely with customers to enhance our privacy suite, focusing on data extraction attacks. We’re excited to share how our testing has helped organizations identify and mitigate potential data leakage vulnerabilities before their AI systems go live.

**Key features and benefits:**

-   **Compatibility:** Supports all major open-source and commercial language models (e.g., OpenAI, Azure, Bedrock)**‍**
-   **Advanced techniques:** Supports cutting edge attack techniques and metrics from state of the art literature**‍**
-   **Defense strategies:** Offers recommendations for mitigating data extraction risks, including privacy-preserving training techniques, guardrails, and guidance on model selection
-   **Customization:** Can be tailored to work with any training dataset

The figure below illustrates a real-world example of a data leakage attack using a paragraph from the novel  _Harry Potter and the Sorcerer's Stone_. We input the first 22 words of the paragraph (the prefix) into the Llama 2 13B language model, and ask it to complete the paragraph. The model is able to generate 40 words that match the original text (highlighted in red), which suggests that it has seen this paragraph in its training corpus.


<div align = "center">
<img  src="/assets/files/dataleak2.png">
</div>

## Evaluating data extraction attacks on AI models

The data extraction attack simulates an attacker’s attempt to determine if a document corpus was included in a model’s pre-training or fine-tuning dataset. We use a suite of proprietary prompting strategies to uncover text that may have been memorized by the model.

For example, one basic test we perform involves DynamoEval prompting the AI system with the first few words from a protected paragraph in the training dataset. We then analyze whether the model's completion matches the original text.

To identify if the generated text is “memorized,” we use a set of similarity thresholds, including trigram memorization, exact starting word memorization, and overlapping words memorization. This approach assumes the adversary has black-box access to the model, allowing them to observe the generated text in response to specific prompts.


<div align = "center">
<img  src="/assets/files/dataleak3.png">
</div>
## Running data extraction tests on the Dynamo AI platform

You can easily run a data extraction attack using either our SDK or the Dynamo AI dashboard. The figure below illustrates how to run a test using the SDK.

```javascript
dfl = DynamoFL(DYNAMOFL_API_KEY, host=DYNAMOFL_HOST)

test = dfl.data_extraction_test(
    name = "Data Extraction - Llama 2 - Harry Potter",
    model_key = model.key,
    dataset_id = dataset.id,
    gpu = GPUConfig(gpu_type = GPUType.V100, gpu_count = 1),
    memorization_granularity = "paragraph",
    sampling_rate = 1000,
    grid = [
        {
            'prompt_length': [256, 512],
            'temperature': [0, 0.5, 0.7, 1.0]
        }
    ]
)
```

-   `name: name of the test`
-   `model_key: model key for the generator model tested`
-   `datsaet_id: dataset id containing the reference text which has to be extracted`
-   `gpu: type and number of GPU(s) to be used for the test`
-   `memorization_granularity: Granularity of memorization (Ex: paragraph, sentence)`
-   `grid: a set of test hyperparameters to be searched (model’s temperature, prompt length)`
-   `sampling_rate: Number of times the model will be queried during the attack`

## Effective mitigation measures for data leakage

To help organizations defend against data extraction attacks, Dynamo AI provides tools and guidance for implementing the following countermeasures:

1.  **Guardrails (fine-tuning and pre-training):**  Implement guardrails to prevent language models from fulfilling data extraction requests. These guardrails serve as a first line of defense by blocking attempts to retrieve sensitive memorized data. Our AI guardrail, DynamoGuard, is specifically designed to protect against these attacks.
2.  **Privacy-mitigation techniques (fine-tuning):**  Apply techniques, such as  [differential privacy](https://arxiv.org/abs/2110.05679)  and  [deduplication,](https://arxiv.org/abs/2107.06499)  during fine-tuning. Differential privacy introduces noise to the training data, making it harder to extract specific data points. Deduplication removes exact copies of sensitive data from the training set, reducing the risk of memorization.  [DynamoEnhance](https://dynamo.ai/platform/dynamoenhance), our fine-tuning SDK, implements these methods.
3.  **Smaller models (fine-tuning):** [Research](https://arxiv.org/pdf/2202.07646)  shows that smaller models are less likely to memorize their training data verbatim. Use  [DynamoEval](https://dynamo.ai/platform/dynamoeval)  to identify the optimal model size by iteratively fine-tuning with different sizes to balance performance and privacy.

As LLMs become increasingly powerful and widely adopted, the risk of exposing sensitive information from training datasets also rises. To address this challenge, Dynamo AI offers a comprehensive suite of privacy solutions, including simulations for data extraction attacks, PII extraction, PII inference, and membership inference. These tools enable teams to effectively measure, address, and prevent data leakage, supporting the responsible deployment of LLMs.

We also offer a range of AI privacy and security solutions tailored to build trustworthy and responsible AI systems. For more information about how Dynamo AI can help you evaluate and improve your RAG models, or to explore our AI privacy and security offerings, please reach out to us to  [schedule a demo.](https://dynamo.ai/request-a-demo)

