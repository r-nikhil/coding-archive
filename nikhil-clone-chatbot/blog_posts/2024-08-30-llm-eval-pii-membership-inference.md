---
layout: post
title:  Integrating Explainable LLM Data Leakage Testing into your CI/CD Pipeline 
categories: [ai, security]
---
---------------------

This post was cowritten by me and was originally published on [Dynamo AI's blog](https://dynamo.ai/blog/integrate-explainable-llm-data-leakage-testing-into-your-ci-cd-pipeline-with-dynamoeval).

<div align = "center">
<img  src="/assets/files/piimain.png">
</div>

Generative AI (GenAI) introduces new challenges in data privacy, including the potential risk of large language models (LLMs) memorizing and leaking personally identifiable information (PII) or copyrighted data in training datasets. Although this technology is still emerging, enterprises using or deploying GenAI still need to meet the existing laws and regulations on data privacy.

[Research in machine learning](https://arxiv.org/abs/2202.07646) has long highlighted privacy vulnerabilities associated with model training, such as data leakage in LLMs. These vulnerabilities can lead to significant compliance, financial, and reputational consequences. Regulators stress the importance of using explainable red-teaming techniques and implementing effective controls to manage these risks.

[DynamoEval](https://dynamo.ai/platform/dynamoeval)’s privacy testing suite goes beyond simple PII detection. It generates reports detailing the conditions that make applications susceptible to data leakage. This post will show how to integrate DynamoEval’s tests into a CI/CD pipeline with [DynamoEnhance](https://dynamo.ai/platform/dynamoenhance), facilitating rapid deployment and testing of compensating controls and risk mitigation strategies like differential privacy.

At Dynamo AI, we lead in [privacy research](https://arxiv.org/abs/2307.16382), quickly integrating the latest techniques into DynamoEval. Our tool red-teams models for vulnerabilities, employing attacks such as Membership Inference, PII Extraction, and Data Extraction. It also provides automated reports, dashboards, and detailed analyses to identify and address these risks.

Below, we explore how DynamoEval uses explainable testing to address PII extraction and membership inference vulnerabilities in LLMs. This walkthrough includes simulating a privacy attack as described by [Lukas et al](https://arxiv.org/abs/2302.00539). from Microsoft Research, demonstrating how enterprises can enhance data privacy in their machine learning applications.


## Evaluating model vulnerability to PII extraction and membership inference



**PII extraction attacks**  and  **membership Inference attacks**  are two types of privacy attacks that can expose sensitive information in machine learning models. We demonstrate how to evaluate models against these attacks and interpret the results.

-   In a  **PII extraction attack** setting**,**  an adversary attempts to extract sensitive pieces of information (e.g., names, addresses, phone numbers) that the model might have memorized during fine-tuning or training.
-   In a  **membership inference attack** setting, the adversary tries to infer whether or not an already-known data point was used for training.

With DynamoEval, we evaluate our models against these attacks by simulating an adversary with access to the model and a set of data records. DynamoEval runs multiple iterations of an attack using different splits of the data and hyperparameter settings. We then provide detailed metrics, like ROC curves, AUC scores, PII extraction, Precision, and Recall to quantify the model's vulnerability to these attacks.

## Evaluating PII extraction attacks

A PII extraction attack assesses the risk of PII being extracted by attackers who have various levels of knowledge about the training dataset. This attack involves prompting the model with a series of inputs and analyzing whether PII is present in the model's outputs.

During a PII extraction attack, three key metrics are reported:**‍**

-   **PII Extracted:** The number of PII successfully extracted from the model responses
-   **Recall**: The percentage of actual PII that was successfully extracted (out of the training dataset)
-   **Precision**: The proportion of identified PII instances that are true positives

<div align = "center">
<img  src="/assets/files/piiextract.png">
</div>

## Membership inference attacks


The goal of a membership inference attack is to determine whether specific data records can be inferred as part of the model’s training dataset. It is conducted by simulating an attacker with access to the model and a dataset, with some records being part of the training data.

We simulate the attacker building a classifier that predicts whether a data record was part of the training dataset. The performance of this classifier indicates how much information about the training data is exposed, revealing its susceptibility to membership inference attacks.

-   **True positive rate (TPR):**  In this attack, the true positive rate (TPR) represents the percentage of data records correctly predicted to be members of the training dataset. We evaluate the TPR at various low false positive rates (FPRs) to determine the attacker’s success in high-confidence scenarios.
-   **ROC-AUC**: In this attack, the Receiver Operating Characteristic (ROC) curve can also be used to to define vulnerability, which demonstrates the performance of the attack as a tradeoff between the TPR and FPR at various thresholds. We can then use the Area Under the ROC Curve (AUC) to measure the aggregate performance across all thresholds.  [Recent research](https://arxiv.org/abs/2112.03570)  also suggests evaluating the attack’s TPR in the low FPR regime (the three percentages shown at the top) to characterize whether the attack can confidently identify members of the training set.

<div align = "center">
<img  src="/assets/files/meminf.png">
</div>


## DynamoEval UI walkthrough

In this section, we provide a step-by-step guide to using the DynamoEval product:

#### 1. Curate a train/test dataset

First, select the training and test datasets for evaluating the model’s privacy vulnerabilities. Specify which column contains the text data. Datasets are uploaded in CSV format.

For PII extraction and membership inference attacks, this dataset is usually the one used for fine-tuning the model.

#### 2. Upload model and dataset to Dynamo AI

Upload both your trained model and the dataset to the Dynamo AI platform. Make sure to specify any relevant files, such as LoRA adapter configurations, if applicable.

<div align = "center">
<img  src="/assets/files/upload.png">
</div>


#### 3. Choose tests

Select the specific attack you want to run, such as PII Extraction or Membership Inference. The screenshot below displays the range of privacy attacks available on our platform.

<div align = "center">
<img  src="/assets/files/testcat.png">
</div>


#### 4. Analyze results

After the tests are complete, we analyze the results to understand the model's vulnerability to the attacks.

In the ROC curve example below, the straight, gray line where X = Y indicates a random guessing baseline. The AUC is a measure of the performance of a binary classifier, ranging from 0 to 1. An AUC of 1.0 indicates perfect classification, while an AUC of 0.5 would indicate random guessing.

In this case, the AUC is 0.77, revealing that the attacker was able to differentiate between members and non-members of the dataset with a high success rate.

<div align = "center">
<img  src="/assets/files/miipii.png">
</div>
Below, the FPR represents the percentage of records falsely identified as being members of the training dataset, and the TPR represents the percentage of records correctly identified as being members of the training dataset.

We provide three different TPR rates for clarity. You can also review the prompts and responses used in the attack in our deep dive section. Additionally, any PII extracted from the model during the attack is tagged and included in the response.

<div align = "center">
<img  src="/assets/files/deepdive.png">
</div>


We can also review the loss distribution plots to gain insights into the model's behavior on both training and testing data. [Research](https://arxiv.org/abs/1906.00389) shows that a high degree of separation in these distributions suggests the model is less generalized and more vulnerable to membership inference and data leakage.

<div align = "center">
<img  src="/assets/files/plotmii.png">
</div>

#### 5. Generate test reports

After the tests are completed, we generate PDF reports that provide detailed information on the attack methodology, results, and recommendations for improving the models.

<div align = "center">
<img  src="/assets/files/testreport.png">
</div>


## DynamoEval SDK walkthrough

#### 1. Initiation

Start by installing the public Dynamo AI SDK. import the required libraries and specify the required environment variables. Create a Dynamo AI instance using your API token and host.

If you do not have an API token, log into  [app.dynamofl.com](http://app.dynamofl.com/)  with your credentials to generate one. This API token will enable you to programmatically connect to the DynamoFL server, create projects, and evaluate models. (Note that if you generate multiple API tokens, only your most recent one will be valid.)

```

from dynamofl import DynamoFL, GPUConfig, GPUType

API_KEY = "" # Add your API key here
API_HOST = "https://api.dynamofl.com" # DFL or custom API host here

dfl = DynamoFL(API_KEY, host=API_HOST)

```


#### 2. Create a model and dataset object

Next, create a local model object. This object specifies the model on which privacy tests will be run using the 'create_test' method. Dynamo AI currently supports two types of model objects: local models and remote model API endpoints. In this example, we will focus on local models.

A local model object can be used to upload a custom model and run penetration tests. Creating a local model object requires specifying the model file path and architecture. Currently, Dynamo AI supports penetration testing on uploaded models with '.pt' and '.bin' file formats. (Please confirm that your provided model file fits this formatting.) For model architectures, provide any valid HuggingFaceHub model id.

In this example, we use a local model that has been fine-tuned using Low-Rank Adaptation (LoRA). LoRA is a technique that "freezes" the majority of parameters in a pre-trained LLM, while fine-tuning a small subset of additional parameters. This reduces training time, compute usage, and storage costs.

When working with a model fine-tuned with LoRA or parameter-efficient fine-tuning (PEFT), you must also provide the file path to the PEFT adapter configuration.

To run a privacy evaluation test, specify the dataset used for fine-tuning the model. Create a dataset object by providing the dataset file path and assign it a unique key and identifying name.

```

model_path_dir = "<path_to_your_trained_model_file>"

# using a PEFT LoRA adapter for a lightweight model upload

model_file_path = os.path.join(model_path_dir, "adapter_model.bin")
peft_config_path = os.path.join(model_path_dir, "adapter_config.json")
model_architecture = "dynamofl-sandbox/sheared-llama-1b3"

# Creating a local model referring to a fine-tuned LLaMA 1.3B
model = dfl.create_model(
    name="Sheared LLama DP", 
    model_file_path=model_file_path,
    architecture=model_architecture,
    peft_config_path=peft_config_path,
    architecture_hf_token="hf_***",
)
print(f"Model successfully uploaded with key {model.key}.")

# Upload dataset
dataset = dfl.create_dataset(
    key="dataset_pii_extraction",
    file_path="<path_to_your_training_dataset_file>",
    name="Finetuning Dataset"
)
# dataset id
print(f"Dataset successfully uploaded with key {dataset.key}.")

```


#### 3. Test parameters

When configuring a test, you can configure various parameters to customize the test to your needs. Key parameters include:

-   The column name from the dataset to create prompts
-   The types of PII to detect for leakage
-   The model temperature for running tests

These test configuration parameters should be provided to the  `create_pii_extraction_test`  method. Additionally, it's required to provide the dataset column names in the test parameters when creating a test.

##### PII classes and entities

When configuring a PII extraction or inference attack, one of the most important hyperparameters is the  `pii_classes`  parameter. This parameter defines which types of PII the extraction attack will target.

In addition to the predefined PII classes, you can also detect leakage for custom-defined regex entities. To do this, define a dictionary mapping entity names to the valid Python regex expression in the  `regex_expressions`  parameter.

```
pii_entities = ["PERSON", "DATE_TIME", "ORGANIZATION", "EMAIL_ADDRESS"]
regex_expressions = {
    "USERNAME": r"([a-zA-Z]+_[a-zA-Z0-9]+)",
}

test_info = dfl.create_pii_extraction_test(
    name="privacy_test_pii_extraction",
    model_key=model.key, # previously created model identifier key
    dataset_id=dataset._id, # previously created dataset id
    pii_ref_column="text", # column name containing text to be evaluated
    gpu=GPUConfig(gpu_type=GPUType.V100, gpu_count=1), # default GPU parameters
    sampling_rate=1024,
    pii_classes=pii_entities,
    regex_expressions=regex_expressions,
    grid=[{
        "temperature": [0.5, 1.0, 1.5]
    }], # test configurations
)

attack_info = dfl.get_attack_info(attack_id)
print("Attack status: {}.".format(attack_info))
```

#### 4. Run the test

To run a membership inference privacy evaluation test, call the  `create_membership_inference_test`  method. This will submit the test to your cloud machine-learning platform, where it will be run.

Dynamo AI currently has four types of privacy tests to assess whether a fine-tuned model has memorized data from the training set.

-   **PII Extraction:**  Checks if PII can be extracted by prompting the model naively, simulating an attacker with no knowledge of the training dataset
-   **PII Inference:**  Tests whether a model can re-fill PII into sentences from a fine-tuned dataset, where PII has been redacted, assuming an attacker with knowledge of the concepts and potential PII in the dataset
-   **Data Extraction:**  Evaluates whether the model can be prompted to reveal training data verbatim in its responses
-   **Membership Inference:**  Determines whether specific data records can be identified as part of the model's training dataset

After creating your tests, go to the model dashboard page in the Dynamo AI UI. You will see that your model and dataset have been created and your test is running.

Once the test is complete, a report file will be generated which you can download for a detailed analysis of the results.

```
# Upload dataset
dataset_mia = dfl.create_dataset(
    key="dataset_mia",
    file_path="<path_to_your_training_dataset_file>",
    test_file_path="<path_to_your_test_dataset_file>",
    name="Finetuning Dataset"
)

# dataset id
print(f"Dataset successfully uploaded with key {dataset_mia.key}.")

test_info_mia = dfl.create_membership_inference_test(
    name="privacy_test_mia",
    model_key=model.key, # previously created model identifier key
    dataset_id=dataset_mia._id, # previously created dataset id
    input_column="text",
    gpu=GPUConfig(gpu_type=GPUType.A10G, gpu_count=1), # another GPU configuration
    pii_classes=pii_entities,
    regex_expressions=regex_expressions,
    base_model=model_args.model_name_or_path,
)
```


#### Integrating DynamoEval into your CI/CD pipelines

Ensuring data privacy and security in machine learning models is critical, and real-time monitoring plays an important role in the process.

By integrating DynamoEval into your development and deployment process, you can conduct comprehensive testing for privacy and security vulnerabilities.

**Integration areas:**

-   **Post-training checks:** Incorporating DynamoEval in your post-training checks allows you to scan models after training or fine-tuning to detect any privacy leaks or compliance issues that may have arisen during the training phase.
-   **Scans in CI/CD pipeline:**  Automate DynamoEval scans within your CI/CD pipeline to include them in the release phase, ensuring that models are evaluated for vulnerabilities before they are staged for deployment.
-   **Final privacy check:**  Conduct a final privacy check during the deployment phase to safeguard against deploying models with vulnerabilities.

Making DynamoEval scans a routine part of the CI/CD pipelines enables you to proactively safeguard your models against privacy risks, ensuring trust and compliance throughout your operations.

#### Actionable insights and mitigation strategies

DynamoEval not only identifies potential privacy vulnerabilities, it also provides actionable insights to mitigate these risks. Based on the evaluation results, the platform offers recommendations for improving the model's privacy protection.

For instance, given the AUC score of 0.77 in our example, which indicates a significant vulnerability to membership inference attacks, the next step would be to remediate this risk. Implementing techniques such as  [differential privacy](https://arxiv.org/abs/1607.00133)  during model training can effectively reduc this vulnerability. Our evaluation shows that applying differential private effectively lowers the AUC, underscoring its effectiveness in improving privacy protection.

In addition, employing non-aggressive PII scrubbing techniques that preserve data relationships and uniqueness while minimizing leakage risk can further strengthen privacy protection efforts.  
  
Finally, leveraging  [DynamoGuard](https://dynamo.ai/platform/dynamoguard), our privacy guardrail product, can provide additional security by detecting and redacting PII in real time. Combining both model-level and infrastructure-level privacy measures can substantially enhance the overall privacy posture of machine learning applications.

As LLMs become more powerful and prevalent, the risk of exposing sensitive information from training datasets increases. With Dynamo AI's comprehensive privacy solutions, teams can effectively measure, address, and prevent data leakage, ensuring the responsible deployment and use of LLMs while protecting sensitive information.

**Learn more about Dynamo AI and our AI privacy and security solutions by** [**scheduling a demo.**](https://dynamo.ai/request-a-demo)


