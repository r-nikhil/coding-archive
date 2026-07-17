---
layout: post
title:  Unlocking Differential Privacy for >7B Parameter LLMs
categories: [ai, security]
---

------------------------

This post was cowritten by me and was originally published on [Dynamo AI's blog](https://dynamo.ai/blog/unlocking-differential-privacy-for-llms).


<div align = "center">
<img  src="/assets/files/dpmain.png">
</div>


Recent research shows that large language models (LLMs) are often prone to memorizing their training and fine-tuning datasets. This is a vulnerability that can be exploited by adversarial attacks, where malicious actors craft specific prompts to  [extract sensitive information](https://arxiv.org/abs/2311.17035)  from these models.

For organizations developing and deploying LLMs, this presents a significant risk to data security and privacy. Differential privacy (DP) helps mitigate this risk by strategically injecting statistical noise during the training process. This technique controls the risk of data memorization, while balancing privacy and performance.

Given its effectiveness, differential privacy is being closely examined by federal agencies as a key defense against adversarial attacks and data leakage in LLMs. The National Institute of Standards and Technology (NIST), which developed the widely used NIST AI Risk Management Framework, endorsed  [differential privacy](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.ipd.pdf)  as the most reliable method for ensuring robust privacy protection against both known and future attacks, even with multiple data releases.

Other government organizations, like the  [U.S. Census Bureau](https://www.census.gov/programs-surveys/decennial-census/decade/2020/planning-management/process/disclosure-avoidance/differential-privacy.html), are starting to adopt differential privacy as core component of their data protection strategies. To expand the use of privacy-preserving machine learning, it's crucial to develop differential privacy solutions that can efficiently handle large datasets and complex applications.

‍

> “Differential privacy is currently the best known method for providing robust privacy protection against known and future attacks, even in the face of multiple data releases.” — The National Institute of Standards and Technology (NIST)


<div align = "center">
<img  src="/assets/files/dynaproc.png">
</div>

## **Challenges in adopting differential privacy for LLMs**

Despite its promise for safeguarding LLMs, differential privacy adoption has faced significant challenges. The sheer magnitude of LLMs, some of which have trillions of parameters, poses significant hurdles for engineers.

The traditional Differentially-Private Stochastic Gradient Descent ([DP-SGD](https://arxiv.org/abs/1607.00133)), which  [computes individual, per-sample gradients](https://arxiv.org/pdf/2010.09063), significantly slows down training compared to standard neural network methods. This is because DP-SGD loses the parallel processing benefits of GPUs, resulting in longer training times and higher GPU memory requirements.

The previous state-of-the-art in differentially private fine-tuning struggled with models exceeding approximately 1.5 billion parameters. Practitioners faced challenges with limited throughput and extremely long training durations. The memory constraints of these methods made it challenging to train on anything other than high-end GPUs, like the A100 (40GB, 80GB), resulting in costly and complex implementation.

Moreover, current differential privacy frameworks, such as the Opacus library, aren't well-stuied for large LLM workloads. While Opacus supports Distributed Data Parallel (DDP) training, it lacks model sharding capabilities.

DDP replicates the entire model on each GPU, which can lead to memory constraints when handling large models. This limitation made it difficult or nearly impossible to train LLMs with billions of parameters efficiently across multiple GPUs. As a result, the lack of model sharding in Opacus has hindered the scalability and practicality of differentially private training for large-scale deep learning models.


<div align = "center">
<img  src="/assets/files/dp1.png">
</div>
<div align = "center">
<img  src="/assets/files/dp2.png">
</div>



## **Apply differential privacy at scale with DynamoEnhance**

[Bu  _et al._](https://arxiv.org/abs/2311.11822)  developed a new approach called DP-ZeRO to enable large-scale differentially private deep learning using the DeepSpeed library. DeepSpeed, known for its Zero Redundancy Optimizer (ZeRO), enhances training speed and reduces memory usage when working with large models across multiple GPUs. The researchers have extended DeepSpeed to support differentially private training, proving that effective privacy injection is achievable with the right techniques.

DP-ZeRO opens up exciting opportunities for Dynamo AI to build upon the work and integrate scalable differential privacy in  [DynamoEnhance](https://dynamo.ai/platform/dynamoenhance). By leveraging DeepSpeed's multi-GPU model sharding capabilities and incorporating differential privacy into the distributed training process, DynamoEnhance offers enhanced data protection and privacy without sacrificing the power of large-scale models.

This is where we come in. DynamoEnhance’s MultiGPU privacy framework, built on the DeepSpeed library, seamlessly integrates differential privacy. It features user-friendly Trainers inspired by popular transformers and TRL (Transformer Reinforcement library) libraries, making advanced privacy protection accessible while optimizing model performance.

```python
from dynamofl.privacy import DPTrainer, PrivacyArguments

# model, tokenizer = ...
# train_dataset, eval_dataset = ...

privacy_args = PrivacyArguments(target_epsilon=1.0)
trainer = DPTrainer(
    model=model,
    tokenizer=tokenizer,
    args=train_args,
    privacy_args=privacy_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)
trainer.train()
```

In the above example, we set the target epsilon value in our  `PrivacyArguments`, where  `Epsilon`  represents the “privacy budget.” A lower epsilon value indicates less privacy expenditure, resulting in more noise being added to the gradients. Conversely, a higher epsilon value means a larger privacy budget and less noice to the gradients, offering reduced privacy protection.

By leveraging DeepSpeed and incorporating innovative techniques, DynamoEnhance enables efficient, scalable training of LLMs while maintaining robust privacy guarantees and accommodating larger batch sizes.

This cutting-edge approach differentiates our solution by providing enterprise customers with an effective and easy-to-use approach to safeguarding sensitive data with differential privacy, while harnessing the power of LLMs.

Our technology supports MultiGPU model sharding in ways not previously achievable with existing differential privacy libraries. The DynamoEnhance MultiGPU Differential Privacy SDK is compatible with popular training libraries and methods, including Hugging Face, mixed precision, quantized training like BitsAndBytes, Mixture of Quantization (MoQ), LoRA fine-tuning, flash attention, and accelerate. We support leading LLMs such as Llama-70B, Mistral-8x7B, and more.

## **Empowering enterprise customers with differential privacy**

At Dynamo AI, our mission is to empower enterprise customers with the tools and knowledge necessary to unlock the potential of differential privacy. We offer comprehensive documentation and QuickStart guides that enable users to effortlessly experiment with differential privacy fine-tuning of LLMs, regardless of their technical expertise.

By prioritizing accessibility and usability, we aim to make privacy-enhancing technologies available to a broader audience, beyond just those with a formal background in privacy-preserving machine learning.

As LLMs become more powerful and prevalent, the risk of exposing sensitive information from training datasets increases.  [Dynamo AI](https://dynamo.ai/)  provides comprehensive privacy solutions that help teams effectively measure, address, and prevent data leakage, ensuring the responsible deployment and use of LLMs while protecting sensitive information.

We also offer a range of AI privacy and security solutions to help you build trustworthy and responsible AI systems. To learn more about Dynamo AI and to explore our privacy and security offerings,  [request a demo today.](https://dynamo.ai/request-a-demo)

