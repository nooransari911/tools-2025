# Project setup
`mcp1.py` file contains the mcp server. All tools are in this file.

The `settings.json` and `mcp.json` files contain the VS code MCP setup files. Alternatively I have also included equivalent config file or Claude Desktop. The command field in the json files should point to the correct python executable that has dependencies installed.

I have included 3 sample images for PYQs and resume PDF in this folder. Sample input and output are included in this file.

Dependencies:
langchain_google_genai
mcp.server.fastmcp
pydantic
educhain




# Prompts
## Test PYQ Generation
Generate new questions based on provided PYQs. PYQs is in 3 images in this dir. Do OCR them, then analyze them, then synthesize new questions. correct tool to generate questions is generate_new_questions_given_analysis. proactively save information to resources.

## Test Resume interview questions
based on resume (the pdf), generate interview questions for role Python GenAI intern

# Sample outputs:
## Test PYQ Generation
### OCR
Input:
```
{
  "file_paths": [
    "/home/ansarimn/Downloads/tools-2025/projects/edulearn/Screenshot_20250703_172559.png",
    "/home/ansarimn/Downloads/tools-2025/projects/edulearn/Screenshot_20250703_172615.png",
    "/home/ansarimn/Downloads/tools-2025/projects/edulearn/Screenshot_20250703_172642.png"
  ],
  "file_types": [
    "image",
    "image",
    "image"
  ]
}
```

Output:
```
{
  "papers": [
    {
      "Year": "2019",
      "QList": [
        {
          "Major_Q_Number": 1,
          "Sub_Q_Number": 1,
          "question_text": "Explain stride Convolution with example.",
          "image_or_other_info": "[6]"
        },
        {
          "Major_Q_Number": 1,
          "Sub_Q_Number": 2,
          "question_text": "Explain Padding and its types.",
          "image_or_other_info": "[6]"
        },
        {
          "Major_Q_Number": 1,
          "Sub_Q_Number": 3,
          "question_text": "Explain Local response normalization and need of it.",
          "image_or_other_info": "[6]"
        },
        {
          "Major_Q_Number": 2,
          "Sub_Q_Number": 1,
          "question_text": "Explain ReLU Layer and its advantages.",
          "image_or_other_info": "[6]"
        },
        {
          "Major_Q_Number": 2,
          "Sub_Q_Number": 2,
          "question_text": "Explain Pooling layers and its types with examples.",
          "image_or_other_info": "[6]"
        },
        {
          "Major_Q_Number": 2,
          "Sub_Q_Number": 3,
          "question_text": "What are the applications of Convolution with examples?",
          "image_or_other_info": "[6]"
        },
        {
          "Major_Q_Number": 3,
          "Sub_Q_Number": 1,
          "question_text": "Draw CNN architecture and explain its working.",
          "image_or_other_info": "[6]"
        },
        {
          "Major_Q_Number": 3,
          "Sub_Q_Number": 2,
          "question_text": "Explain the types of Recurrent Neural Network",
          "image_or_other_info": "[6]"
        },
        {
          "Major_Q_Number": 3,
          "Sub_Q_Number": 3,
          "question_text": "Justify RNN is better suited to treat sequential data than a feed forward neural network.",
          "image_or_other_info": "[5]"
        }
      ]
    },
    {
      "Year": "2023",
      "QList": [
        {
          "Major_Q_Number": 4,
          "Sub_Q_Number": 1,
          "question_text": "Explain Recurrent Neural Network with its architecture.",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 4,
          "Sub_Q_Number": 2,
          "question_text": "Draw and explain architecture for Long Short-Term Memory (LSTM).",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 4,
          "Sub_Q_Number": 3,
          "question_text": "Explain how the memory cell in the LSTM is implemented computationally?",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 5,
          "Sub_Q_Number": 1,
          "question_text": "Explain Deep generative model with example.",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 5,
          "Sub_Q_Number": 2,
          "question_text": "How does GAN training scale with batch size?",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 5,
          "Sub_Q_Number": 3,
          "question_text": "List the applications of GAN network with description.",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 6,
          "Sub_Q_Number": 1,
          "question_text": "Draw and explain architecture of Boltzmann machine.",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 6,
          "Sub_Q_Number": 2,
          "question_text": "Explain different types of GAN.",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 6,
          "Sub_Q_Number": 3,
          "question_text": "Explain Deep Belief Network with diagram.",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 7,
          "Sub_Q_Number": 1,
          "question_text": "Explain dynamic programming algorithms for reinforcement learning.",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 7,
          "Sub_Q_Number": 2,
          "question_text": "What is deep reinforcement learning? Explain in detail.",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 7,
          "Sub_Q_Number": 3,
          "question_text": "Explain Simple reinforcement learning for Tic-Tac-Toe.",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 8,
          "Sub_Q_Number": 1,
          "question_text": "Explain Markov decision process.",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 8,
          "Sub_Q_Number": 2,
          "question_text": "Write Short Note on Q Learning and Deep Q-Networks.",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 8,
          "Sub_Q_Number": 3,
          "question_text": "What are the challenges of reinforcement learning? Explain any four in detail.",
          "image_or_other_info": ""
        }
      ]
    },
    {
      "Year": "2015",
      "QList": [
        {
          "Major_Q_Number": 1,
          "Sub_Q_Number": 1,
          "question_text": "Explain supervised learning with example.",
          "image_or_other_info": "[5]"
        },
        {
          "Major_Q_Number": 1,
          "Sub_Q_Number": 2,
          "question_text": "Discuss the reinforcement learning and write in brief the applications.",
          "image_or_other_info": "[5]"
        },
        {
          "Major_Q_Number": 2,
          "Sub_Q_Number": 1,
          "question_text": "Describe the role of machine learning in the following applications :",
          "image_or_other_info": "[10]"
        },
        {
          "Major_Q_Number": 2,
          "Sub_Q_Number": 2,
          "question_text": "Google home or Alexa",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 2,
          "Sub_Q_Number": 3,
          "question_text": "Unmanned Vehicles",
          "image_or_other_info": ""
        },
        {
          "Major_Q_Number": 3,
          "Sub_Q_Number": 1,
          "question_text": "Explain in brief the feature selection and discuss in details any suitable feature selection method.",
          "image_or_other_info": "[10]"
        },
        {
          "Major_Q_Number": 4,
          "Sub_Q_Number": 1,
          "question_text": "Write a short note on Kernel PCA?",
          "image_or_other_info": "[5]"
        },
        {
          "Major_Q_Number": 4,
          "Sub_Q_Number": 2,
          "question_text": "Discuss in brief the dictionary learning.",
          "image_or_other_info": "[5]"
        },
        {
          "Major_Q_Number": 5,
          "Sub_Q_Number": 1,
          "question_text": "Explain isotonic regression and write the applications in brief.",
          "image_or_other_info": "[5]"
        },
        {
          "Major_Q_Number": 5,
          "Sub_Q_Number": 2,
          "question_text": "What do you mean by linearly separable data and non-linearly separable data?",
          "image_or_other_info": "[5]"
        },
        {
          "Major_Q_Number": 6,
          "Sub_Q_Number": 1,
          "question_text": "Explain in detail the Ridge regression and the Lasso regression.",
          "image_or_other_info": "[10]"
        }
      ]
    }
  ]
}

```

Then this was saved to file



### Analysis Report
Input:
```
{
  "questions": {
    "papers": [
      {
        "Year": "2019",
        "QList": [
          {
            "Major_Q_Number": 1,
            "Sub_Q_Number": 1,
            "question_text": "Explain stride Convolution with example.",
            "image_or_other_info": "[6]"
          },
          {
            "Major_Q_Number": 1,
            "Sub_Q_Number": 2,
            "question_text": "Explain Padding and its types.",
            "image_or_other_info": "[6]"
          },
          {
            "Major_Q_Number": 1,
            "Sub_Q_Number": 3,
            "question_text": "Explain Local response normalization and need of it.",
            "image_or_other_info": "[6]"
          },
          {
            "Major_Q_Number": 2,
            "Sub_Q_Number": 1,
            "question_text": "Explain ReLU Layer and its advantages.",
            "image_or_other_info": "[6]"
          },
          {
            "Major_Q_Number": 2,
            "Sub_Q_Number": 2,
            "question_text": "Explain Pooling layers and its types with examples.",
            "image_or_other_info": "[6]"
          },
          {
            "Major_Q_Number": 2,
            "Sub_Q_Number": 3,
            "question_text": "What are the applications of Convolution with examples?",
            "image_or_other_info": "[6]"
          },
          {
            "Major_Q_Number": 3,
            "Sub_Q_Number": 1,
            "question_text": "Draw CNN architecture and explain its working.",
            "image_or_other_info": "[6]"
          },
          {
            "Major_Q_Number": 3,
            "Sub_Q_Number": 2,
            "question_text": "Explain the types of Recurrent Neural Network",
            "image_or_other_info": "[6]"
          },
          {
            "Major_Q_Number": 3,
            "Sub_Q_Number": 3,
            "question_text": "Justify RNN is better suited to treat sequential data than a feed forward neural network.",
            "image_or_other_info": "[5]"
          }
        ]
      },
      {
        "Year": "2023",
        "QList": [
          {
            "Major_Q_Number": 4,
            "Sub_Q_Number": 1,
            "question_text": "Explain Recurrent Neural Network with its architecture.",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 4,
            "Sub_Q_Number": 2,
            "question_text": "Draw and explain architecture for Long Short-Term Memory (LSTM).",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 4,
            "Sub_Q_Number": 3,
            "question_text": "Explain how the memory cell in the LSTM is implemented computationally?",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 5,
            "Sub_Q_Number": 1,
            "question_text": "Explain Deep generative model with example.",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 5,
            "Sub_Q_Number": 2,
            "question_text": "How does GAN training scale with batch size?",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 5,
            "Sub_Q_Number": 3,
            "question_text": "List the applications of GAN network with description.",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 6,
            "Sub_Q_Number": 1,
            "question_text": "Draw and explain architecture of Boltzmann machine.",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 6,
            "Sub_Q_Number": 2,
            "question_text": "Explain different types of GAN.",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 6,
            "Sub_Q_Number": 3,
            "question_text": "Explain Deep Belief Network with diagram.",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 7,
            "Sub_Q_Number": 1,
            "question_text": "Explain dynamic programming algorithms for reinforcement learning.",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 7,
            "Sub_Q_Number": 2,
            "question_text": "What is deep reinforcement learning? Explain in detail.",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 7,
            "Sub_Q_Number": 3,
            "question_text": "Explain Simple reinforcement learning for Tic-Tac-Toe.",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 8,
            "Sub_Q_Number": 1,
            "question_text": "Explain Markov decision process.",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 8,
            "Sub_Q_Number": 2,
            "question_text": "Write Short Note on Q Learning and Deep Q-Networks.",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 8,
            "Sub_Q_Number": 3,
            "question_text": "What are the challenges of reinforcement learning? Explain any four in detail.",
            "image_or_other_info": ""
          }
        ]
      },
      {
        "Year": "2015",
        "QList": [
          {
            "Major_Q_Number": 1,
            "Sub_Q_Number": 1,
            "question_text": "Explain supervised learning with example.",
            "image_or_other_info": "[5]"
          },
          {
            "Major_Q_Number": 1,
            "Sub_Q_Number": 2,
            "question_text": "Discuss the reinforcement learning and write in brief the applications.",
            "image_or_other_info": "[5]"
          },
          {
            "Major_Q_Number": 2,
            "Sub_Q_Number": 1,
            "question_text": "Describe the role of machine learning in the following applications :",
            "image_or_other_info": "[10]"
          },
          {
            "Major_Q_Number": 2,
            "Sub_Q_Number": 2,
            "question_text": "Google home or Alexa",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 2,
            "Sub_Q_Number": 3,
            "question_text": "Unmanned Vehicles",
            "image_or_other_info": ""
          },
          {
            "Major_Q_Number": 3,
            "Sub_Q_Number": 1,
            "question_text": "Explain in brief the feature selection and discuss in details any suitable feature selection method.",
            "image_or_other_info": "[10]"
          },
          {
            "Major_Q_Number": 4,
            "Sub_Q_Number": 1,
            "question_text": "Write a short note on Kernel PCA?",
            "image_or_other_info": "[5]"
          },
          {
            "Major_Q_Number": 4,
            "Sub_Q_Number": 2,
            "question_text": "Discuss in brief the dictionary learning.",
            "image_or_other_info": "[5]"
          },
          {
            "Major_Q_Number": 5,
            "Sub_Q_Number": 1,
            "question_text": "Explain isotonic regression and write the applications in brief.",
            "image_or_other_info": "[5]"
          },
          {
            "Major_Q_Number": 5,
            "Sub_Q_Number": 2,
            "question_text": "What do you mean by linearly separable data and non-linearly separable data?",
            "image_or_other_info": "[5]"
          },
          {
            "Major_Q_Number": 6,
            "Sub_Q_Number": 1,
            "question_text": "Explain in detail the Ridge regression and the Lasso regression.",
            "image_or_other_info": "[10]"
          }
        ]
      },
      {
        "Year": "2015",
        "QList": []
      }
    ]
  }
}
```

Output:
```
## Analysis of Previous Year Questions (PYQs) in Machine Learning

This analysis examines the provided PYQs from 2015, 2019, and 2023, focusing on frequency, concept coverage, difficulty, question types, and educational value to provide actionable insights for future study.

**1. High-Value Questions (Top 20-30%):**  Given the small sample size (19 unique questions across three years), defining the top 20-30% is challenging.  Instead, we'll highlight the most conceptually significant and frequently recurring themes.  These are weighted more heavily in the Category Analysis.

* **2019 Q3.S3:** "Justify RNN is better suited to treat sequential data than a feed forward neural network."  (Difficulty: Medium-High; Topic: RNN vs. Feedforward NN; Value: Tests deep understanding of sequential data processing).
* **2023 Q4.S1, Q4.S2, Q4.S3:** These three questions on RNNs, LSTMs, and LSTM memory cell implementation represent a high-value cluster, highlighting the importance of recurrent networks. (Difficulty: Medium-High; Topic: RNNs and LSTMs; Value: Covers the core architecture and computational details of LSTMs).
* **2023 Q5.S1, Q5.S2, Q5.S3:** These three questions on GANs (Generative Adversarial Networks) represent another high-value cluster. (Difficulty: Medium-High; Topic: GANs; Value: Covers the core concepts, training aspects, and applications of GANs).
* **2023 Q7.S1, Q7.S2, Q7.S3:**  These three questions on Reinforcement Learning (RL) show the increasing emphasis on this topic. (Difficulty: Medium-High; Topic: Reinforcement Learning; Value: Covers various aspects of RL, including dynamic programming, deep RL, and its challenges).
* **2015 Q3.S1:** "Explain in brief the feature selection and discuss in details any suitable feature selection method." (Difficulty: Medium; Topic: Feature Selection; Value: Fundamental to machine learning model building).
* **2015 Q6.S1:** "Explain in detail the Ridge regression and the Lasso regression." (Difficulty: Medium; Topic: Regularization; Value: Important for model building and preventing overfitting).

**2. Category Analysis with Importance Weights:**

| Category                     | Importance Weight | Frequency | 2015 | 2019 | 2023 |
|------------------------------|--------------------|------------|------|------|------|
| Recurrent Neural Networks (RNNs, LSTMs) | **High (4)**       | 4          | 0    | 1    | 3    |
| Convolutional Neural Networks (CNNs) | **High (3)**       | 7          | 0    | 7    | 0    |
| Generative Adversarial Networks (GANs) | **High (3)**       | 3          | 0    | 0    | 3    |
| Reinforcement Learning          | **High (4)**       | 6          | 2    | 0    | 4    |
| Supervised Learning           | Medium (2)        | 1          | 1    | 0    | 0    |
| Feature Selection/Engineering | Medium (2)        | 1          | 1    | 0    | 0    |
| Regularization                | Medium (2)        | 1          | 1    | 0    | 0    |
| Other (Boltzmann Machines, Deep Belief Networks, etc.) | Low (1)         | 3          | 0    | 0    | 3    |


**3. Difficulty Mapping:**

* **Easy:**  Questions requiring simple definitions or basic explanations (few in this dataset).
* **Medium:** Questions requiring understanding of concepts and application to simple examples.  (Majority of questions fall here).
* **Medium-High:** Questions requiring in-depth understanding, justification, or detailed explanations (RNN, LSTM, GAN, RL questions).
* **High:**  Questions requiring advanced problem-solving or synthesis of multiple concepts (none in this dataset, likely due to the limited scope).

**4. Trend Analysis:**

* **Shift towards Deep Learning:** A clear trend shows an increased focus on deep learning architectures (RNNs, CNNs, GANs) in recent years (2019 and 2023) compared to 2015, which focuses more on fundamental machine learning concepts.
* **Emphasis on Reinforcement Learning:**  Reinforcement learning has gained significant attention, becoming a major topic in 2023.
* **Generative Models:** The emergence of GANs as a significant topic reflects the growth of generative models in the field.

**5. Study Recommendations:**

* **Prioritize Deep Learning Architectures:**  Focus on a strong understanding of RNNs (especially LSTMs), CNNs, and GANs, as these are clearly high-value topics.
* **Master Reinforcement Learning:**  Deeply understand the core concepts of reinforcement learning, including Markov Decision Processes, dynamic programming, Q-learning, and deep Q-networks, and be prepared to address challenges within the field.
* **Fundamentals Remain Crucial:**  While deep learning is important, don't neglect the fundamentals: feature selection/engineering, regularization techniques (Ridge and Lasso regression), and basic supervised learning concepts.
* **Practice Explanations and Justifications:**  The PYQs often demand explanations and justifications, not just definitions. Practice explaining concepts in detail and comparing different approaches.
* **Diagrammatic Representation:**  The ability to draw and explain the architecture of neural networks is highly valued. Practice drawing diagrams for major architectures.
* **Broaden Knowledge:** While the provided dataset focuses on specific areas, a broader understanding of various machine learning algorithms and applications is beneficial.


This analysis provides a structured overview of the PYQs.  A larger dataset would allow for a more statistically robust trend analysis and identification of high-value questions.  However, this analysis provides valuable insights for focusing study efforts effectively.
```

Then this was saved to file


### New Questions
Input:
```
{
  "analysis": "## Analysis of Previous Year Questions (PYQs) in Machine Learning\n\nThis analysis examines the provided PYQs from 2015, 2019, and 2023, focusing on frequency, concept coverage, difficulty, question types, and educational value to provide actionable insights for future study.\n\n**1. High-Value Questions (Top 20-30%):**  Given the small sample size (19 unique questions across three years), defining the top 20-30% is challenging.  Instead, we'll highlight the most conceptually significant and frequently recurring themes.  These are weighted more heavily in the Category Analysis.\n\n* **2019 Q3.S3:** \"Justify RNN is better suited to treat sequential data than a feed forward neural network.\"  (Difficulty: Medium-High; Topic: RNN vs. Feedforward NN; Value: Tests deep understanding of sequential data processing).\n* **2023 Q4.S1, Q4.S2, Q4.S3:** These three questions on RNNs, LSTMs, and LSTM memory cell implementation represent a high-value cluster, highlighting the importance of recurrent networks. (Difficulty: Medium-High; Topic: RNNs and LSTMs; Value: Covers the core architecture and computational details of LSTMs).\n* **2023 Q5.S1, Q5.S2, Q5.S3:** These three questions on GANs (Generative Adversarial Networks) represent another high-value cluster. (Difficulty: Medium-High; Topic: GANs; Value: Covers the core concepts, training aspects, and applications of GANs).\n* **2023 Q7.S1, Q7.S2, Q7.S3:**  These three questions on Reinforcement Learning (RL) show the increasing emphasis on this topic. (Difficulty: Medium-High; Topic: Reinforcement Learning; Value: Covers various aspects of RL, including dynamic programming, deep RL, and its challenges).\n* **2015 Q3.S1:** \"Explain in brief the feature selection and discuss in details any suitable feature selection method.\" (Difficulty: Medium; Topic: Feature Selection; Value: Fundamental to machine learning model building).\n* **2015 Q6.S1:** \"Explain in detail the Ridge regression and the Lasso regression.\" (Difficulty: Medium; Topic: Regularization; Value: Important for model building and preventing overfitting).\n\n**2. Category Analysis with Importance Weights:**\n\n| Category                     | Importance Weight | Frequency | 2015 | 2019 | 2023 |\n|------------------------------|--------------------|------------|------|------|------|\n| Recurrent Neural Networks (RNNs, LSTMs) | **High (4)**       | 4          | 0    | 1    | 3    |\n| Convolutional Neural Networks (CNNs) | **High (3)**       | 7          | 0    | 7    | 0    |\n| Generative Adversarial Networks (GANs) | **High (3)**       | 3          | 0    | 0    | 3    |\n| Reinforcement Learning          | **High (4)**       | 6          | 2    | 0    | 4    |\n| Supervised Learning           | Medium (2)        | 1          | 1    | 0    | 0    |\n| Feature Selection/Engineering | Medium (2)        | 1          | 1    | 0    | 0    |\n| Regularization                | Medium (2)        | 1          | 1    | 0    | 0    |\n| Other (Boltzmann Machines, Deep Belief Networks, etc.) | Low (1)         | 3          | 0    | 0    | 3    |\n\n\n**3. Difficulty Mapping:**\n\n* **Easy:**  Questions requiring simple definitions or basic explanations (few in this dataset).\n* **Medium:** Questions requiring understanding of concepts and application to simple examples.  (Majority of questions fall here).\n* **Medium-High:** Questions requiring in-depth understanding, justification, or detailed explanations (RNN, LSTM, GAN, RL questions).\n* **High:**  Questions requiring advanced problem-solving or synthesis of multiple concepts (none in this dataset, likely due to the limited scope).\n\n**4. Trend Analysis:**\n\n* **Shift towards Deep Learning:** A clear trend shows an increased focus on deep learning architectures (RNNs, CNNs, GANs) in recent years (2019 and 2023) compared to 2015, which focuses more on fundamental machine learning concepts.\n* **Emphasis on Reinforcement Learning:**  Reinforcement learning has gained significant attention, becoming a major topic in 2023.\n* **Generative Models:** The emergence of GANs as a significant topic reflects the growth of generative models in the field.\n\n**5. Study Recommendations:**\n\n* **Prioritize Deep Learning Architectures:**  Focus on a strong understanding of RNNs (especially LSTMs), CNNs, and GANs, as these are clearly high-value topics.\n* **Master Reinforcement Learning:**  Deeply understand the core concepts of reinforcement learning, including Markov Decision Processes, dynamic programming, Q-learning, and deep Q-networks, and be prepared to address challenges within the field.\n* **Fundamentals Remain Crucial:**  While deep learning is important, don't neglect the fundamentals: feature selection/engineering, regularization techniques (Ridge and Lasso regression), and basic supervised learning concepts.\n* **Practice Explanations and Justifications:**  The PYQs often demand explanations and justifications, not just definitions. Practice explaining concepts in detail and comparing different approaches.\n* **Diagrammatic Representation:**  The ability to draw and explain the architecture of neural networks is highly valued. Practice drawing diagrams for major architectures.\n* **Broaden Knowledge:** While the provided dataset focuses on specific areas, a broader understanding of various machine learning algorithms and applications is beneficial.\n\n\nThis analysis provides a structured overview of the PYQs.  A larger dataset would allow for a more statistically robust trend analysis and identification of high-value questions.  However, this analysis provides valuable insights for focusing study efforts effectively.",
  "num": 10
}
```

Output:
```
{
  "questions": [
    {
      "question": "Which of the following best describes the primary advantage of using Recurrent Neural Networks (RNNs) over feedforward neural networks for sequential data?",
      "answer": "RNNs maintain an internal state that allows them to process sequential data with temporal dependencies.",
      "explanation": "Feedforward networks process each input independently, ignoring the order. RNNs, however, use their hidden state to incorporate information from previous inputs, making them suitable for sequences.",
      "options": [
        "RNNs are computationally faster than feedforward networks.",
        "RNNs require less training data than feedforward networks.",
        "RNNs maintain an internal state that allows them to process sequential data with temporal dependencies.",
        "RNNs are less prone to overfitting than feedforward networks."
      ]
    },
    {
      "question": "What is the primary function of the memory cell in an LSTM (Long Short-Term Memory) network?",
      "answer": "To regulate the flow of information into and out of the cell state, allowing the network to learn long-range dependencies.",
      "explanation": "The gates (input, output, and forget) within the memory cell control the information that is stored and retrieved, enabling LSTMs to handle long sequences effectively.",
      "options": [
        "To perform backpropagation through time.",
        "To generate random numbers for the network.",
        "To regulate the flow of information into and out of the cell state, allowing the network to learn long-range dependencies.",
        "To speed up the training process."
      ]
    },
    {
      "question": "In Generative Adversarial Networks (GANs), what is the role of the discriminator?",
      "answer": "To distinguish between real data and data generated by the generator.",
      "explanation": "The discriminator acts as a critic, evaluating the quality of the generator's output. This adversarial process drives both networks to improve.",
      "options": [
        "To generate new data samples.",
        "To preprocess the input data.",
        "To distinguish between real data and data generated by the generator.",
        "To regularize the weights of the generator."
      ]
    },
    {
      "question": "Which of the following is NOT a common challenge in Reinforcement Learning?",
      "answer": "Lack of labeled data",
      "explanation": "Reinforcement learning does not require labeled data; instead, it relies on rewards and penalties to guide the learning process.",
      "options": [
        "Reward sparsity",
        "Exploration-exploitation dilemma",
        "Credit assignment problem",
        "Lack of labeled data"
      ]
    },
    {
      "question": "What is the primary purpose of regularization techniques like Ridge and Lasso regression?",
      "answer": "To prevent overfitting by adding a penalty term to the loss function.",
      "explanation": "Overfitting occurs when a model learns the training data too well, performing poorly on unseen data.  Regularization helps to reduce this by constraining the model's complexity.",
      "options": [
        "To increase the speed of training.",
        "To reduce the bias of the model.",
        "To prevent overfitting by adding a penalty term to the loss function.",
        "To improve the interpretability of the model."
      ]
    },
    {
      "question": "Explain the difference between L1 and L2 regularization.",
      "answer": "L1 regularization (Lasso) adds a penalty proportional to the absolute value of the weights, leading to sparse solutions (some weights become zero). L2 regularization (Ridge) adds a penalty proportional to the square of the weights, leading to smaller weights but not necessarily zero.",
      "explanation": "This difference impacts feature selection; L1 tends to select fewer features while L2 shrinks all features.",
      "options": [
        "L1 is faster, L2 is more accurate.",
        "L1 handles outliers better, L2 is more sensitive.",
        "L1 adds a penalty proportional to the absolute value of the weights, leading to sparse solutions; L2 adds a penalty proportional to the square of the weights, leading to smaller weights but not necessarily zero.",
        "They are essentially the same."
      ]
    },
    {
      "question": "What is a common application of Convolutional Neural Networks (CNNs)?",
      "answer": "Image recognition and classification",
      "explanation": "CNNs excel at processing grid-like data such as images due to their use of convolutional layers which are designed to detect features in a spatial context.",
      "options": [
        "Natural language processing",
        "Time series forecasting",
        "Image recognition and classification",
        "Recommender systems"
      ]
    },
    {
      "question": "What is the key difference between supervised and unsupervised learning?",
      "answer": "Supervised learning uses labeled data, while unsupervised learning uses unlabeled data.",
      "explanation": "Supervised learning aims to predict a target variable based on labeled examples, while unsupervised learning aims to discover patterns and structures in unlabeled data.",
      "options": [
        "Supervised learning is faster, unsupervised learning is more accurate.",
        "Supervised learning uses labeled data, while unsupervised learning uses unlabeled data.",
        "Supervised learning requires more data, unsupervised learning requires less data.",
        "They are essentially the same."
      ]
    },
    {
      "question": "Describe a scenario where feature selection would be beneficial.",
      "answer": "High-dimensional data with many irrelevant or redundant features, leading to overfitting and decreased model performance.",
      "explanation": "Feature selection helps to reduce the dimensionality of the data by selecting the most relevant features, resulting in a more efficient and accurate model.",
      "options": [
        "When the dataset is very small.",
        "When the dataset has only a few features.",
        "When the target variable is categorical.",
        "High-dimensional data with many irrelevant or redundant features, leading to overfitting and decreased model performance."
      ]
    },
    {
      "question": "What is a Markov Decision Process (MDP) and why is it important in Reinforcement Learning?",
      "answer": "An MDP is a mathematical framework for modeling decision-making in situations where outcomes are partly random and partly under the control of a decision maker. It's crucial in RL as it provides a formal structure for defining the environment and agent's interaction.",
      "explanation": "MDPs are the foundation of many RL algorithms, providing a way to define states, actions, rewards, and transition probabilities.",
      "options": [
        "A type of neural network architecture.",
        "A regularization technique.",
        "A mathematical framework for modeling decision-making in situations where outcomes are partly random and partly under the control of a decision maker.",
        "A type of generative model."
      ]
    }
  ]
}
```

Then this was saved to file


### Final response
The workflow is complete:

1. OCR was performed on the 3 images to extract PYQs.
2. The extracted PYQs were saved as `pyqs_from_images.md` in the resources.
3. A comprehensive analysis report was generated and saved as `pyq_analysis_report.md.md`.
4. Based on the analysis, 10 new questions were synthesized using the correct tool and saved as `new_questions_from_pyq_analysis.md`.

All key information and results are now available in the resources directory for further use. If you want to view or use any of these outputs, let me know!


## Generate questions from resume

Input:
```
{
  "source_path": "/home/ansarimn/Downloads/tools-2025/projects/edulearn/Resume S 01 July 2025 AI.pdf",
  "source_type": "pdf",
  "num": 10,
  "target_role": "Python GenAI intern"
}
```

Output:
```
{
  "questions": [
    {
      "question": "Describe your experience using Claude and Gemini models in your AI document processing application. What were some of the challenges you encountered, and how did you overcome them?",
      "answer": "I utilized Claude and Gemini for natural language understanding and processing within my document processing application. Challenges included handling variations in document formats and ensuring accurate extraction of information despite inconsistencies.  I addressed these by implementing robust error handling, comprehensive logging, and dynamic configuration to adapt to different input types and model behaviors.",
      "explanation": "This question assesses the candidate's practical experience with large language models and their ability to troubleshoot real-world problems.",
      "options": [
        "I used them for basic text analysis.",
        "I utilized Claude and Gemini for natural language understanding and processing, overcoming challenges like inconsistent document formats through robust error handling and dynamic configuration.",
        "I had no challenges using these models.",
        "I only used Claude; Gemini was not implemented."
      ]
    },
    {
      "question": "Your AI document processing application features parallel processing. Explain the benefits of this approach and how you implemented it in your project.",
      "answer": "Parallel processing significantly improved processing speed by distributing the workload across multiple cores.  I implemented it using Python's multiprocessing library, dividing the documents into smaller chunks for concurrent processing.",
      "explanation": "This probes the candidate's understanding of parallel processing and their ability to apply it in a practical context.",
      "options": [
        "Parallel processing was not used.",
        "It improved processing speed, implemented using Python's threading library.",
        "It improved processing speed, implemented using Python's multiprocessing library.",
        "I am unfamiliar with parallel processing."
      ]
    },
    {
      "question": "Explain your experience with DynamoDB integration in your AI document processing application. Why did you choose DynamoDB for logging?",
      "answer": "I used DynamoDB for its scalability and speed in handling high volumes of log data. It's a NoSQL database ideal for storing and retrieving log entries efficiently, supporting the application's dynamic nature.",
      "explanation": "This tests the candidate's knowledge of database choices and their justification for specific technologies.",
      "options": [
        "I used a relational database for logging.",
        "I used DynamoDB for its scalability and speed in handling high-volume log data.",
        "I did not integrate a database for logging.",
        "DynamoDB was chosen for its ease of use, regardless of efficiency."
      ]
    },
    {
      "question": "In your personal website project, you utilized Hugo (SSG). What are the advantages of using a Static Site Generator like Hugo compared to a traditional CMS?",
      "answer": "Hugo offers advantages such as improved performance, enhanced security, and easier deployment compared to traditional CMS.  Static sites are faster to load and generally more secure due to the absence of dynamic content generation.",
      "explanation": "This evaluates the candidate's understanding of web development technologies and their ability to compare different approaches.",
      "options": [
        "There are no significant advantages.",
        "Hugo is slower but easier to use.",
        "Hugo offers improved performance, security, and easier deployment.",
        "Hugo is only suitable for small websites."
      ]
    },
    {
      "question": "How did you implement automated search indexing and cache refresh/invalidation in your personal website?",
      "answer": "I used [mention specific tools/techniques, e.g.,  a combination of serverless functions and AWS services like CloudFront] to trigger automated indexing and cache invalidation upon website updates. This ensured search engines always had access to the latest content.",
      "explanation": "This question assesses practical implementation skills and knowledge of web optimization techniques.",
      "options": [
        "Manual updates were required.",
        "I used a third-party service.",
        "I used a combination of serverless functions and AWS services to automate this process.",
        "Search indexing and cache management were not implemented."
      ]
    },
    {
      "question": "Your automated backup solution uses AWS S3. Explain the importance of incremental backups and how you implemented them.",
      "answer": "Incremental backups only store the changes since the last backup, saving storage space and transfer time. I implemented this by comparing file checksums or timestamps and only uploading the modified files.",
      "explanation": "This tests the candidate's understanding of efficient backup strategies.",
      "options": [
        "Full backups were used for simplicity.",
        "Incremental backups were used, but I'm unsure of the specific implementation.",
        "Incremental backups were implemented by comparing file checksums or timestamps.",
        "Incremental backups were not implemented."
      ]
    },
    {
      "question": "Describe your experience extracting and parsing data from CSV bank statements. What challenges did you face, and how did you address them?",
      "answer": "I used Python libraries like pandas to parse the CSV data. Challenges included handling inconsistent formatting and missing data. I addressed these using data cleaning and validation techniques.",
      "explanation": "This assesses data handling and problem-solving skills.",
      "options": [
        "I manually processed the data.",
        "I used Python libraries to parse the data, handling inconsistencies through data cleaning and validation.",
        "I encountered no challenges.",
        "I am unfamiliar with data parsing."
      ]
    },
    {
      "question": "You mention using GCP BigQuery for data migration in your bank statement visualization project.  Why did you choose BigQuery over other cloud-based data warehousing solutions?",
      "answer": "BigQuery's serverless architecture and scalability made it suitable for handling large datasets and generating interactive visualizations efficiently.  Its SQL-based query language also simplified data analysis.",
      "explanation": "This explores the candidate's knowledge of cloud-based data warehousing and their ability to justify technology choices.",
      "options": [
        "I chose it arbitrarily.",
        "BigQuery's serverless architecture and scalability were key factors.",
        "I preferred its user interface.",
        "Other solutions were not considered."
      ]
    },
    {
      "question": "Explain your understanding of the concept of 'robust error handling' and how it's crucial in building reliable AI applications.",
      "answer": "Robust error handling involves anticipating potential issues, implementing mechanisms to detect and handle them gracefully, and preventing application crashes.  It's crucial for AI applications because unexpected inputs or model failures can lead to incorrect results or service disruptions.  Proper error handling ensures the application continues to function correctly even under adverse conditions.",
      "explanation": "This evaluates the candidate's understanding of software engineering best practices.",
      "options": [
        "Error handling is not important for AI applications.",
        "Robust error handling involves simply using try-except blocks.",
        "Robust error handling involves anticipating potential issues, implementing mechanisms to detect and handle them gracefully, and preventing application crashes.",
        "I am unfamiliar with robust error handling."
      ]
    },
    {
      "question": "Considering your experience with both AWS and GCP, what are the key differences between these two cloud platforms, and which would you prefer for a new GenAI project and why?",
      "answer": "AWS and GCP offer similar services but differ in pricing models, specific service strengths (e.g., AWS for serverless, GCP for Big Data), and overall ecosystem. For a new GenAI project, I would likely lean towards [AWS or GCP, justify the choice based on specific needs like serverless capabilities for model deployment, cost optimization, or specific AI/ML services offered by the platform].",
      "explanation": "This assesses the candidate's understanding of cloud platforms and their ability to make informed technology choices based on project requirements.",
      "options": [
        "There are no significant differences.",
        "AWS is always superior to GCP.",
        "GCP is always superior to AWS.",
        "AWS and GCP offer similar services but differ in pricing models, specific service strengths, and overall ecosystem;  the best choice depends on the project's specific needs."
      ]
    }
  ]
}
```

Then this was saved to file

10 interview questions for the "Python GenAI intern" role have been generated based on the provided resume PDF and saved as resume_python_genai_intern_questions.md in the resources directory.

Let me know if you want to view or use these questions!

