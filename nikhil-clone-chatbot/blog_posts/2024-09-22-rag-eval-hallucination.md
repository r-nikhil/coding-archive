---

layout: post
title:  Tackling the Explainability Gap in RAG Hallucination Evals
categories: [ai]
---

------------------------

This post was cowritten by me and was originally published on [Dynamo AI's blog](https://dynamo.ai/blog/tackling-the-explainability-gap-in-open-source-hallucination-evals).



<div align = "center">
<img  src="/assets/files/rag1.png">
</div>

As many of our enterprise customers move from PoC to production LLM deployment, we find that enterprises need to demonstrate robust reliability testing of their AI systems. The tendency for LLMs to "hallucinate" incorrect or inconsistent outputs remains a major challenge for enterprises at this stage.

In a recent example,  [Air Canada's chatbot](https://www.bbc.com/travel/article/20240222-air-canada-chatbot-misinformation-what-travellers-should-know)  hallucinated information about refunds and discounts, leading to significant confusion and complaints. Moreover, for highly-regulated enterprises such as financial institutions, regulators like the Consumer Financial Protection Bureau have highlighted that “deficient chatbots” can lead to a “risk of noncompliance with federal consumer financial laws.”

Specifically, the  [CFPB states](https://www.consumerfinance.gov/data-research/research-reports/chatbots-in-consumer-finance/chatbots-in-consumer-finance/)  that a chatbot “providing inaccurate information regarding a consumer financial product or service, for example, could be catastrophic. It could lead to the assessment of inappropriate fees, which in turn could lead to worse outcomes such as default, resulting in the customer selecting an inferior option or consumer financial product, or other harms."

While retrieval-augmented generation (RAG) aims to reduce hallucinations by grounding outputs in retrieved passages, enterprises deploying RAG still typically see high degrees of hallucinations during their testing. To safely deploy LLMs, enterprises are beginning to widely integrate routine hallucination evaluators to measure and trace the root causes of hallucinations in their RAG pipelines.

While open-source LLM evaluators have played an important role in the evolution of this space, we find that regulated enterprises that are moving LLMs into real production environments require an enterprise-grade solution that includes more explainable metrics and alignment with regulatory standards for comprehensive red-teaming. For example, most of our customers who have experimented with open-source LLM evaluators are still left with key unresolved questions such as:

1.  Without an interpretable hallucination risk score, what is an acceptable “threshold score” for deploying LLMs into production?
2.  If my AI system is not meeting a satisfactory hallucination risk score, what actionable steps can I take to mitigate hallucinations?
3.  How can I explain the testing I’ve performed to regulators and meaningfully explain residual risk that may exist?

In this post, we'll explore the challenges enterprises face in tackling RAG hallucinations, the limitations of existing tools, and introduce Dynamo AI's comprehensive solution for measuring and tracking these issues.

## Limitation of existing tools

While many tools exist for evaluating the degree of hallucination for RAG applications, major limitations include the following:

-   _Less interpretable metrics._  Usually, evaluation metrics will simply output a score value between 0 and 1. Oftentimes, these scores may not be well-calibrated or can be too difficult to understand. For instance, one prominent metric for measuring text relevance is embedding similarity, which uses the cosine distance of two embedded texts. While the range of this distance value is normalized to be between 0 and 1, it is generally unclear how to interpret these scores and what range of scores is considered good or bad.
-   _Lack of fine-grained, actionable analysis for model improvements._  Usually, the evaluation stops at the point where the evaluation scores are computed. Further analysis of detailed error cases that can lead to potential improvements of the system is not present in most of the tools.
    -   It's not clear which part of the RAG pipeline, the retriever or the response generator, needs to be improved based on the metrics and diving deeper into a topic level analysis is also not straightforward.

## Dynamo AI’s RAG hallucination evaluation

Dynamo AI provides a comprehensive RAG evaluation solution that assesses model performance across multiple metrics:

1.  **Retrieval relevance:**  Represents the relevance of the documents retrieved from the vector database using the embedding model for each query.
2.  **Faithfulness:**  Evaluates whether the generated response is consistent with the retrieved documents.
3.  **Response relevance:**  Determines if the generated response adequately addresses the given query.

Dynamo AI leverages purpose-built models for each evaluation task, ensuring cost-efficiency and enabling in-depth analysis. Further, the platform offers actionable insights by identifying topic clusters where the RAG pipeline underperforms and categorizing errors by issue type for in-depth analysis. To demonstrate our solution, we ran our RAG hallucination tests against the MultiDoc2Dial dataset and compared the results with  [RAGAS](https://docs.ragas.io/en/latest/index.html)  for reference.

### Accurate and interpretable performance metrics

In a head-to-head comparison, DynamoEval’s RAG hallucination suite outperformed RAGAS in a classification task of identifying good/bad context/responses given a query. We measured accuracy and area under the receiver operating characteristic (AUROC) across the following metrics: Retrieval Relevance, Faithfulness, and Response Relevance. The following improvements in performance have been achieved through additional prompt optimizations and the use of performant task-specific models.


<div align = "center">
<img  src="/assets/files/rag2.png">
</div>

[DynamoEval](https://dynamo.ai/platform/dynamoeval), unlike RAGAS, returns both the relevance/faithfulness scores and binary labels (good/bad). Test results with only the scores tend to be more ambiguous due to the difficulties associated with drawing a clear threshold demarcating good and bad.

The receiver operating characteristic (ROC) curves and the resulting AUROC values shown below demonstrate that the relevance/faithfulness scores from DyamoEval are more accurate in diagnosing Retrieval Relevance, Faithfulness, and Response Relevance.


<div align = "center">
<img  src="/assets/files/rag3.png">
</div>


<div align = "center">
<img  src="/assets/files/rag4.png">
</div>

Easier interpretation of Response Relevance test results

![](https://cdn.prod.website-files.com/66030bc3057ae1e90ac956b7/66b694054e7371362faee8f8_66294456ae6ed9a24e4a9b71_Retrieval%2520Relevance.png)


Easy interpretation of Retrieval Relevance test results

### Investigate sources of error using topic level clustering

DynamoEval does not stop at generating classification labels and scores for each metrics, but further clusters the input queries based on different topics to provide additional insights for sources of errors and improvements. Analyzing hallucination metrics at a topic-level enables targeted data augmentation and model fine-tuning to address weak areas.

The results explored below are based on the aforementioned test between DynamoEval and RAGAS, wherein we constructed a binary classification dataset from Multidoc2dial, evaluated RAGAS and DynamoEval using accuracy and AUROC, and compared their performance. We also analyzed individual topics for their RAG metrics to dive deeper into specific areas of performance within the RAG pipeline.

For the "student scholarship" topic, Retrieval Relevance is low at  **0% (0% of tested queries in this topic retrieved the correct document chunk).**  This suggests that there may be opportunities for improvements in the retrieval mechanism. One possible reason for the low Retrieval Relevance score could be that the vector database used in the test lacks sufficient information on student scholarships, which could be improved through the injection of additional scholarship-topic related documents to the vector database.

Another possible reason for the low Retrieval Relevance score could be that the embedding model used as part of the retriever is not performant enough to identify the correct scholarship-topic related documents, in which case additional fine-tuning of the embedding model may be necessary.


<div align = "center">
<img  src="/assets/files/rag6.png">
</div>
Faithfulness is also relatively low for the “disability eligibility” topic at 9%, indicating that the generator model struggles to produce information consistent with the retrieved documents, even if they are relevant. Augmenting the training data with more ground-truth, question-context-answer pairs related to disabilities could help fine-tune the generator to be more faithful.


<div align = "center">
<img  src="/assets/files/rag7.png">
</div>

Using the labels from the above section, we can drill deeper into our topic-specific metrics to find out whether any poor-performance metric was related to either a generator or retriever related problem. The analysis looks at combinations of Retrieval Relevance, Faithfulness, and Response Relevance to pinpoint issues.

For example, if Retrieval Relevance and Response Relevance are both high but Faithfulness is low, it may suggest that the generator is not leveraging the retrieved information properly; or if Retrieval Relevance is low but Faithfulness and Response Relevance are high, the retriever may be the source of the problem (see the example below).


<div align = "center">
<img  src="/assets/files/rag8.png">
</div>

In conclusion, Dynamo AI’s evaluation suite for RAG addresses two major limitations in existing tools:

1.  A lack of interpretable metrics, which is addressed via more intuitive and accurate set of classification labels and scores
2.  A lack of fine-grained, detailed analysis of the errors for actionable improvements, which is addressed with topic-level clustering and error type analysis

### Comparison methodology with RAGAS

-   Dynamo AI took the Multidoc2dial  [dataset](https://doc2dial.github.io/multidoc2dial/)  as the base dataset and constructed a classification dataset with binary labels
    -   Positive data points were taken directly from the original dataset.
    -   Negative data points were taken by perturbing the context and answers from the original dataset.
-   Dynamo AI then ran RAGAS and DynamoEval on both positive and negative data points to compare their classification performance.
-   The performance metrics used were Accuracy and AUROC. AUROC computes the area under the  [ROC curve](https://en.wikipedia.org/wiki/Receiver_operating_characteristic), plotting the true positive rate (i.e., probability of positive classification given the positive example) against the false positive rate (i.e., probability of positive classification given the negative example) for various thresholds. Bigger values that are closer to 1 are considered better.
-   To compute accuracy, Dynamo AI chose the threshold that maximized the F1 score for RAGAS to binarize the generated scores into labels, and directly used the labels generated by DynamoEval.

### Running a DynamoEval RAG hallucination test from the SDK

Dynamo AI provides an easily configurable SDK method to set up and run the RAG hallucination test by specifying the following parameters:

<div align = "center">
<img  src="/assets/files/rag9.png">
</div>

-   `name`: name of the test
-   `model_key`: model key for the generator model tested
-   `datsaet_id`: dataset id containing queries for the RAG
-   `input_column`: column name from the dataset that contains queries for the RAG
-   `prompt_template`: prompt template used to synthesize the retrieved contexts and the query.
-   `vector_db`: configuration of the vector database
-   `rag_hallucination_metrics`: metrics used for the test (Retrieval elevance, Response elevance, Faithfulness)
-   `topic_list`: list of topics that could be used for clustering the input queries for better error analysis. If not provided, it will cluster and automatically detect representative topical keywords from each cluster to show.
-   `grid`: a set of test hyperparameters to be searched (model’s temperature, generated sequence length, and number of top-k contexts to be retrieved)
-   `gpu`: type and number of GPU(s) to be used for the test

‍

## How Dynamo AI can help

At Dynamo AI, we are committed to helping organizations measure and mitigate RAG hallucination effectively. Our comprehensive RAG evaluation offering provides deep insights into model performance, enabling teams to identify and address weaknesses in their RAG pipelines.

We also offer a range of AI privacy and security solutions to help you build trustworthy and responsible AI systems. To learn more about how Dynamo AI can help you evaluate and improve your RAG models, or to explore our AI privacy and security offerings,  [please request a demo](https://dynamo.ai/platform/dynamoeval).

