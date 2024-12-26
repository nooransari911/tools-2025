# Why Gemini
## Context window
The basic way you use the Gemini 1.5 models is by passing information (context) to the model, which will subsequently generate a response. An analogy for the context window is short term memory. There is a limited amount of information that can be stored in someone's short term memory, and the same is true for generative models.


## Long context window
Gemini 1.5 Flash comes standard with a 1-million-token context window, and Gemini 1.5 Pro comes with a 2-million-token context window. Historically, large language models (LLMs) were significantly limited by the amount of text (or tokens) that could be passed to the model at one time. The Gemini 1.5 long context window, with near-perfect retrieval (>99%), unlocks many new use cases and developer paradigms.

Most generative models created in the last few years were only capable of processing 8,000 tokens at a time. Newer models pushed this further by accepting 32,000 tokens or 128,000 tokens. Gemini 1.5 is the first model capable of accepting 1 million tokens, and now 2 million tokens with Gemini 1.5 Pro.


## Applications for large context window
While the standard use case for most generative models is still text input, the Gemini 1.5 model family enables a new paradigm of multimodal use cases. These models can natively understand text, video, audio, and images. They are accompanied by the Gemini API that takes in multimodal file types for convenience.

### Long form text
Text has proved to be the layer of intelligence underpinning much of the momentum around LLMs. As mentioned earlier, much of the practical limitation of LLMs was because of not having a large enough context window to do certain tasks. This led to the rapid adoption of retrieval augmented generation (RAG) and other techniques which dynamically provide the model with relevant contextual information. Now, with larger and larger context windows (currently up to 2 million on Gemini 1.5 Pro), there are new techniques becoming available which unlock new use cases.


#### Applications for long form text
Some emerging and standard use cases for text based long context include:

- Summarizing large corpuses of text
    - Previous summarization options with smaller context models would require a sliding window or another technique to keep state of previous sections as new tokens are passed to the model
- Question and answering
    - Historically this was only possible with RAG given the limited amount of context and models' factual recall being low
- Agentic workflows
    - Text is the underpinning of how agents keep state of what they have done and what they need to do; not having enough information about the world and the agent's goal is a limitation on the reliability of agents

Many-shot in-context learning is one of the most unique capabilities unlocked by long context models. Research has shown that taking the common "single shot" or "multi-shot" example paradigm, where the model is presented with one or a few examples of a task, and scaling that up to hundreds, thousands, or even hundreds of thousands of examples, can lead to novel model capabilities. This many-shot approach has also been shown to perform similarly to models which were fine-tuned for a specific task. For use cases where a Gemini model's performance is not yet sufficient for a production rollout, you can try the many-shot approach. As you might explore later in the long context optimization section, context caching makes this type of high input token workload much more economically feasible and even lower latency in some cases.

### Long form video
Video content's utility has long been constrained by the lack of accessibility of the medium itself. It was hard to skim the content, transcripts often failed to capture the nuance of a video, and most tools don't process image, text, and audio together. With Gemini 1.5, the long-context text capabilities translate to the ability to reason and answer questions about multimodal inputs with sustained performance. Gemini 1.5 Flash, when tested on the needle in a video haystack problem with 1M tokens, obtained >99.8% recall of the video in the context window, and 1.5 Pro reached state of the art performance on the Video-MME benchmark.


#### Applications for long form video

Some emerging and standard use cases for video long context include:

- Video question and answering
- Video memory, as shown with Google's Project Astra
- Video captioning
- Video recommendation systems, by enriching existing metadata with new multimodal understanding
- Video customization, by looking at a corpus of data and associated video metadata and then removing parts of videos that are not relevant to the viewer
- Video content moderation
- Real-time video processing

When working with videos, it is important to consider how the videos are processed into tokens, which affects billing and usage limits. You can learn more about prompting with video files in the Prompting guide.


### Long form audio
The Gemini 1.5 models were the first natively multimodal large language models that could understand audio. Historically, the typical developer workflow would involve stringing together multiple domain specific models, like a speech-to-text model and a text-to-text model, in order to process audio. This led to additional latency required by performing multiple round-trip requests and decreased performance usually attributed to disconnected architectures of the multiple model setup.

On standard audio-haystack evaluations, Gemini 1.5 Pro is able to find the hidden audio in 100% of the tests and Gemini 1.5 Flash is able to find it in 98.7% of the tests. Gemini 1.5 Flash accepts up to 9.5 hours of audio in a single request and Gemini 1.5 Pro can accept up to 19 hours of audio using the 2-million-token context window. Further, on a test set of 15-minute audio clips, Gemini 1.5 Pro archives a word error rate (WER) of ~5.5%, much lower than even specialized speech-to-text models, without the added complexity of extra input segmentation and pre-processing.

#### Applications for long form audio

Some emerging and standard use cases for audio context include:

- Real-time transcription and translation
- Podcast / video question and answering
- Meeting transcription and summarization
- Voice assistants

You can learn more about prompting with audio files in the Prompting guide.



## Long context optimizations
The primary optimization when working with long context and the Gemini 1.5 models is to use context caching. Beyond the previous impossibility of processing lots of tokens in a single request, the other main constraint was the cost. If you have a "chat with your data" app where a user uploads 10 PDFs, a video, and some work documents, you would historically have to work with a more complex retrieval augmented generation (RAG) tool / framework in order to process these requests and pay a significant amount for tokens moved into the context window. Now, you can cache the files the user uploads and pay to store them on a per hour basis. The input / output cost per request with Gemini 1.5 Flash for example is ~4x less than the standard input / output cost, so if the user chats with their data enough, it becomes a huge cost saving for you as the developer.


## Long context limitations
In various sections of this guide, we talked about how Gemini 1.5 models achieve high performance across various needle-in-a-haystack retrieval evals. These tests consider the most basic setup, where you have a single needle you are looking for. In cases where you might have multiple "needles" or specific pieces of information you are looking for, the model does not perform with the same accuracy. Performance can vary to a wide degree depending on the context. This is important to consider as there is an inherent tradeoff between getting the right information retrieved and cost. You can get ~99% on a single query, but you have to pay the input token cost every time you send that query. So for 100 pieces of information to be retrieved, if you needed 99% performance, you would likely need to send 100 requests. This is a good example of where context caching can significantly reduce the cost associated with using Gemini models while keeping the performance high


---


# Prompt
Text prompt entered by user
`prompt = "Briefly describe this image`

---

# Primitive text
`response = model.generate_content(prompt)`

Use `stream=True` in `generate_content()` to enable streaming of output

## Applications

- Creative writing
- Describing or interpreting media assets
- Text completion
- Summarizing free-form text
- Translating between languages
- Chatbots
- Your own novel use cases

---

# Model
## Configurations
```
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(
    "Tell me a story about a magic backpack.",
    generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        stop_sequences=["x"],
        max_output_tokens=20,
        temperature=1.0,
    ),
)

print(response.text)
```

Various parameters:

- `candidateCount` specifies the number of generated responses to return. Currently, this value can only be set to 1. If unset, this will default to 1.

- `stopSequences` specifies the set of character sequences (up to 5) that will stop output generation. If specified, the API will stop at the first appearance of a `stop_sequence`. The stop sequence won't be included as part of the response.

- `maxOutputTokens` sets the maximum number of tokens to include in a candidate.

- `temperature` controls the randomness of the output. Use higher values for more creative responses, and lower values for more deterministic responses. Values can range from [0.0, 2.0].

## Tokens
```
model.count_tokens ([file])
```

---

# Document processing
Gemini 1.5 Pro and 1.5 Flash support a maximum of 3,600 document pages. Document pages must be in the application/pdf MIME type.

Each document page is equivalent to 258 tokens.

While there are no specific limits to the number of pixels in a document besides the model's context window, larger pages are scaled down to a maximum resolution of 3072x3072 while preserving their original aspect ratio, while smaller pages are scaled up to 768x768 pixels. There is no cost reduction for pages at lower sizes, other than bandwidth, or performance improvement for pages at higher resolution.


## File API
File API lets you store up to 20 GB of files per project, with a per-file maximum size of 2 GB. Files are stored for 48 hours. They can be accessed in that period with your API key, but cannot be downloaded from the API. It is available at no cost in all regions where the Gemini API is available.

### Upload a file
`path` contains path to file

```
sample_file = genai.upload_file(path="gemini.pdf",
                                display_name="Gemini 1.5 PDF")

print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
```

### Verify uploaded file and get metadata
```
file = genai.get_file(name=sample_file.name)
print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")
```

### Prompt with uploaded file
```
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content([sample_file, "Can you summarize this document as a bulleted list?"])
print(response.text)
```

### Prompt with multiple files
```
response = model.generate_content([prompt, sample_file, sample_file_2, sample_file_3])
```

### List all files uploaded
```
for file in genai.list_files():
    print(f"{file.display_name}, URI: {file.uri}")

```

### Delete uploaded file
```
genai.delete_file(document_file.name)
```

---

# Vision
## Image
Gemini 1.5 Pro and 1.5 Flash support a maximum of 3,600 image files.

Images must be in one of the following image data MIME types:

- PNG - image/png
- JPEG - image/jpeg
- WEBP - image/webp
- HEIC - image/heic
- HEIF - image/heif

Each image is equivalent to 258 tokens.

While there are no specific limits to the number of pixels in an image besides the model's context window, larger images are scaled down to a maximum resolution of 3072x3072 while preserving their original aspect ratio, while smaller images are scaled up to 768x768 pixels. There is no cost reduction for images at lower sizes, other than bandwidth, or performance improvement for images at higher resolution.

For best results:

- Rotate images to the correct orientation before uploading.
- Avoid blurry images.
- If using a single image, place the text prompt after the image.

## Video
Gemini 1.5 Pro and Flash support up to approximately an hour of video data.

Video must be in one of the following video format MIME types:

- video/mp4
- video/mpeg
- video/mov
- video/avi
- video/x-flv
- video/mpg
- video/webm
- video/wmv
- video/3gpp

The File API service extracts image frames from videos at 1 frame per second (FPS) and audio at 1Kbps, single channel, adding timestamps every second. These rates are subject to change in the future for improvements in inference.
Note: The details of fast action sequences may be lost at the 1 FPS frame sampling rate. Consider slowing down high-speed clips for improved inference quality.

Individual frames are 258 tokens, and audio is 32 tokens per second. With metadata, each second of video becomes ~300 tokens, which means a 1M context window can fit slightly less than an hour of video.

To ask questions about time-stamped locations, use the format MM:SS, where the first two digits represent minutes and the last two digits represent seconds.

For best results:

- Use one video per prompt.
- If using a single video, place the text prompt after the video.


## Working with File API
Same as above

---

# Code execution
The Gemini API code execution feature enables the model to generate and run Python code and learn iteratively from the results until it arrives at a final output. You can use this code execution capability to build applications that benefit from code-based reasoning and that produce text output. For example, you could use code execution in an application that solves equations or processes text.

Code execution is available in both AI Studio and the Gemini API. In AI Studio, you can enable code execution under Advanced settings. The Gemini API provides code execution as a tool, similar to function calling. After you add code execution as a tool, the model decides when to use it.


## Using code execution
```
response = model.generate_content(
    ('What is the sum of the first 50 prime numbers? '
    'Generate and run code for the calculation, and make sure you get all 50.'),
    tools='code_execution')

```


## Billing
There's no additional charge for enabling code execution from the Gemini API. You'll be billed at the current rate of input and output tokens.

- You're only billed once for the input tokens you pass to the model, and you're billed for the final output tokens returned to you by the model.
- Tokens representing generated code are counted as output tokens.
- Code execution results are also counted as output tokens.

## Limitations
- The model can only generate and execute code. It can't return other artifacts like media files.
- The feature doesn't support file I/O or use cases that involve non-text output (for example, data plots or a CSV file upload).
- Code execution can run for a maximum of 30 seconds before timing out.
- In some cases, enabling code execution can lead to regressions in other areas of model output (for example, writing a story).
- There is some variation in the ability of the different models to use code execution successfully. Gemini 1.5 Pro is the best performing model, based on our testing.

---

# JSON mode
Gemini generates unstructured text by default, but some applications require structured text. For these use cases, you can constrain Gemini to respond with JSON, a structured data format suitable for automated processing.

In your prompt, you can ask Gemini to produce JSON-formatted output, but note that Google can't guarantee that it will produce JSON and nothing but JSON. However, if you use Gemini 1.5 Pro, you can pass a specific JSON schema in a responseSchema field so that Gemini always responds with an expected structure.

Gemini can produce JSON responses to multimodal requests that include text, images, videos, and audio.


## Applications
For example, these use cases require structured output from the model:
- Build a database of companies by pulling company information out of newspaper articles.
- Pull standardized information out of resumes.
- Extract ingredients from recipes and display a link to a grocery website for each ingredient.



## JSON Mode
When the model is configured to output JSON, it responds to any prompt with JSON-formatted output.

Control the structure of the JSON response by supplying a schema. There are two ways to supply a schema to the model:
- As text in the prompt. This approach works with both Gemini 1.5 Flash and Gemini 1.5 Pro.
- As a structured schema supplied through model configuration. This approach works with Gemini 1.5 Pro but not Gemini 1.5 Flash.


### Schema in prompt
```
model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})
prompt = """
    List 5 popular cookie recipes.
    Using this JSON schema:
        Recipe = {"recipe_name": str}
    Return a `list[Recipe]`
"""
response = model.generate_content(prompt)
print(response.text)
```

### Schema in model configuration
Note: works with only 1.5 Pro, not with 1.5 Flash

```
import google.generativeai as genai
import typing_extensions as typing

class Recipe(typing.TypedDict):
  recipe_name: str

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro',
                                # Set the `response_mime_type` to output JSON
                                # Pass the schema object to the `response_schema` field
                                generation_config=
                                {"response_mime_type": "application/json",
                                "response_schema": list[Recipe]})


prompt = "List 5 popular cookie recipes"
response = model.generate_content(prompt)
print(response.text)
```

---

# Pricing
## Overview
| Model Name    | Maximum Token Size | Token Type                          | Pricing                   |
|---------------|---------------------|-------------------------------------|---------------------------|
| Gemini 1.5 Pro| Up to 128k tokens  | Input Pricing                       | $3.50 / 1 million tokens  |
|               |                     | Output Pricing                      | $10.50 / 1 million tokens |
|               |                     | Context Caching                     | $0.875 / 1 million tokens |
|               | Longer than 128k    | Input Pricing                       | $7.00 / 1 million tokens  |
|               |                     | Output Pricing                      | $21.00 / 1 million tokens |
|               |                     | Context Caching                     | $1.75 / 1 million tokens  |
| Gemini 1.5 Flash | Up to 128k tokens  | Input Pricing                       | $0.075 / 1 million tokens  |
|                  |                     | Output Pricing                      | $0.30 / 1 million tokens   |
|                  |                     | Context Caching                     | $0.01875 / 1 million tokens|
|                  | Longer than 128k    | Input Pricing                       | $0.15 / 1 million tokens   |
|                  |                     | Output Pricing                      | $0.60 / 1 million tokens   |
|                  |                     | Context Caching                     | $0.0375 / 1 million tokens |



## Example: lesser evil video
~20 minutes,
351,640, 0.3 million tokens
roughly $2.46 @ ($3.5/1 million tokens)
roughly Rs 211.687 @ (Rs86/$1)


## Rate limiting

| Model Name            | Requests Per Minute (RPM) | Tokens Per Minute (TPM) | Requests Per Day (RPD) |
|-----------------------|---------------------------|-------------------------|------------------------|
| Gemini 1.5 Flash (Free)  | 15 RPM                    | 1 million TPM            | 1,500 RPD              |
| Gemini 1.5 Flash (Paid)  | 1,000 RPM                 | 4 million TPM            | -                      |
| Gemini 1.5 Pro (Free)    | 2 RPM                     | 32,000 TPM               | 50 RPD                 |
| Gemini 1.5 Pro (Paid)    | 360 RPM                   | 4 million TPM            | -                      |


## Detailed pricing
### Gemini

| Model Name        | Feature       | Type     | Unit        | Price (<= 128K context window) | Price (> 128K context window) |
|-------------------|---------------|----------|--------------|---------------------------------|---------------------------------|
| Gemini 1.5 Flash  | Image Input    | Input    | / image     | $0.00002                      | $0.00004                      |
|                   | Video Input    | Input    | / second    | $0.00002                      | $0.00004                      |
|                   | Text Input     | Input    | / 1k characters | $0.00001875                    | $0.0000375                    |
|                   | Audio Input    | Input    | / second    | $0.000002                      | $0.000004                      |
|                   | Text Output    | Output   | / 1k characters | $0.000075                     | $0.00015                     |
| Gemini 1.5 Pro  | Image Input    | Input    | / image     | $0.001315                     | $0.00263                      |
|                   | Video Input    | Input    | / second    | $0.001315                     | $0.00263                      |
|                   | Text Input     | Input    | / 1k characters | $0.00125                     | $0.0025                       |
|                   | Audio Input    | Input    | / second    | $0.000125                     | $0.00025                      |
|                   | Text Output    | Output   | / 1k characters | $0.00375                     | $0.0075                       |
| Gemini 1.0 Pro  | Image Input    | Input    | / image     | $0.0025                      | N/A                          |
|                   | Video Input    | Input    | / second    | $0.002                       | N/A                          |
|                   | Text Input     | Input    | / 1k characters | $0.000125                     | N/A                          |
|                   | Text Output    | Output   | / 1k characters | $0.000375                     | N/A                          |
| Grounding with Google Search | Text Grounding | Input    | / 1k requests | $35                          | N/A                          | 



### Legacy models: PaLM and Codey

| Model Type | Input Price per 1k characters | Output Price per 1k characters |
|---|---|---|
| PaLM 2 for Text (Text Bison) | Online requests: $0.00025; Batch requests: $0.00020 | Online requests: $0.0005; Batch requests: $0.0004 |
| PaLM 2 for Text 32k (Text Bison 32k) | Online requests: $0.00025; Batch requests: $0.00020 | Online requests: $0.0005; Batch requests: $0.0004 |
| PaLM 2 for Text (Text Unicorn) | Online requests: $0.0025; Batch requests: $0.0020 | Online requests: $0.0075; Batch requests: $0.0060 |
| PaLM 2 for Chat (Chat Bison) | Online requests: $0.00025 | Online requests: $0.0005 |
| PaLM 2 for Chat 32k (Chat Bison 32k) | Online requests: $0.00025* | Online requests: $0.0005* |
| Codey for Code Generation | Online requests: $0.00025; Batch requests: $0.00020 | Online requests: $0.0005; Batch requests: $0.0004 |
| Codey for Code Generation 32k | Online requests: $0.00025 | Online requests: $0.0005 |
| Codey for Code Chat | Online requests: $0.00025 | Online requests: $0.0005 |
| Codey for Code Chat 32k | Online requests: $0.00025 | Online requests: $0.0005 | 


## Basic pricing comparison

| Model | Type            | Input (per 1k characters) | Output (per 1k characters) |
|---|-----------------|---|---|
| Gemini 1.5 Flash | <= 128K context | $0.00001875 | $0.000075 |
| Gemini 1.5 Flash | \> 128K context | $0.0000375 | $0.00015 |
| Gemini 1.5 Pro | <= 128K context | $0.00125 | $0.00375 |
| Gemini 1.5 Pro | \> 128K context | $0.0025 | $0.0075 |
| PaLM 2 for Text (Text Bison) | Online          | $0.00025 | $0.0005 |
| PaLM 2 for Text (Text Bison 32k) | Online          | $0.00025 | $0.0005 |
| Codey for Code Generation | Online          | $0.00025 | $0.0005 |
| Codey for Code Generation 32k | Online          | $0.00025 | $0.0005 |


## Models overview
| Model Name | Speed | Context Size | Input Pricing | Output Pricing | Pricing | Type | Dev |
|---|---|---|---|---|---|---|---|
| Gemini 1.5 Flash | Fast | <= 128K context | 1 | 4 | $ | Generic | Easy |
| Gemini 1.5 Flash | Fast | > 128K context | 2 | 8 | $ | Generic | Easy |
| Gemini 1.5 Pro | Slow | <= 128K context | 500 | 1500 | $$$$ | Generic | Easy |
| Gemini 1.5 Pro | Slow | > 128K context | 1000 | 3000 | $$$$ | Generic | Easy |
| PaLM 2 for Text (Text Bison) Online | Medium | - | 10 | 20 | $$ | Generic | Easy |
| PaLM 2 for Text (Text Bison 32k) Online | Medium | - | 10 | 20 | $$ | Generic | Easy |
| Codey for Code Generation Online | Medium | - | 10 | 20 | $$ | Generic | Easy |
| Codey for Code Generation 32k Online | Medium | - | 10 | 20 | $$ | Generic | Easy |

## Services overview

| Model Name | Speed | Quality | Pricing | Type | Development Difficulty |
|---|---|---|---|---|---|
| Vision AI | Faster | == | $$(?) | Specialized | Hard |
| Document AI | Faster | == | $$(?) | Specialized/Highly specialized | Hard |
| Vertex AI (Gemini Pro) | Same/Slower | ==== | $$$$ | Generic | Easy |

---



# Context caching
In a typical AI workflow, you might pass the same input tokens over and over to a model. Using the Gemini API context caching feature, you can pass some content to the model once, cache the input tokens, and then refer to the cached tokens for subsequent requests. At certain volumes, using cached tokens is lower cost than passing in the same corpus of tokens repeatedly.

When you cache a set of tokens, you can choose how long you want the cache to exist before the tokens are automatically deleted. This caching duration is called the time to live (TTL). If not set, the TTL defaults to 1 hour. The cost for caching depends on the input token size and how long you want the tokens to persist.

Context caching supports both Gemini 1.5 Pro and Gemini 1.5 Flash. Context caching is only available for stable models with fixed versions (for example, `gemini-1.5-pro-001`). You must include the version postfix (for example, the `-001` in `gemini-1.5-pro-001`).

Context caching is particularly well suited to scenarios where a substantial initial context is referenced repeatedly by shorter requests. Consider using context caching for use cases such as:
- Chatbots with extensive system instructions
- Repetitive analysis of lengthy video files
- Recurring queries against large document sets
- Frequent code repository analysis or bug fixing


How caching reduces costs
Context caching is a paid feature designed to reduce overall operational costs. Billing is based on the following factors:

- Cache token count: The number of input tokens cached, billed at a reduced rate when included in subsequent prompts.
- Storage duration: The amount of time cached tokens are stored (TTL), billed based on the TTL duration of cached token count. There are no minimum or maximum bounds on the TTL.
- Other factors: Other charges apply, such as for non-cached input tokens and output tokens.

For up-to-date pricing details, refer to the Gemini API pricing page. To learn how to count tokens, see the Token guide.

## Using context caching
```
import os
import google.generativeai as genai
from google.generativeai import caching
import datetime
import time

# Get your API key from https://aistudio.google.com/app/apikey
# and access your API key as an environment variable.
# To authenticate from a Colab, see
# https://github.com/google-gemini/cookbook/blob/main/quickstarts/Authentication.ipynb
genai.configure(api_key=os.environ['API_KEY'])

# Download video file
# curl -O https://storage.googleapis.com/generativeai-downloads/data/Sherlock_Jr_FullMovie.mp4

path_to_video_file = 'Sherlock_Jr_FullMovie.mp4'

# Upload the video using the Files API
video_file = genai.upload_file(path=path_to_video_file)

# Wait for the file to finish processing
while video_file.state.name == 'PROCESSING':
  print('Waiting for video to be processed.')
  time.sleep(2)
  video_file = genai.get_file(video_file.name)

print(f'Video processing complete: {video_file.uri}')

# Create a cache with a 5 minute TTL
cache = caching.CachedContent.create(
    model='models/gemini-1.5-flash-001',
    display_name='sherlock jr movie', # used to identify the cache
    system_instruction=(
        'You are an expert video analyzer, and your job is to answer '
        'the user\'s query based on the video file you have access to.'
    ),
    contents=[video_file],
    ttl=datetime.timedelta(minutes=5),
)

# Construct a GenerativeModel which uses the created cache.
model = genai.GenerativeModel.from_cached_content(cached_content=cache)

# Query the model
response = model.generate_content([(
    'Introduce different characters in the movie by describing '
    'their personality, looks, and names. Also list the timestamps '
    'they were introduced for the first time.')])

print(response.usage_metadata)

# The output should look something like this:
#
# prompt_token_count: 696219
# cached_content_token_count: 696190
# candidates_token_count: 214
# total_token_count: 696433

print(response.text)

```


### Configuring caching
#### List caching
It's not possible to retrieve or view cached content, but you can retrieve cache metadata (`name`, `model`, `display_name`, `usage_metadata`, `create_time`, `update_time`, and `expire_time`).

```
for c in caching.CachedContent.list():
  print(c)

```
#### Update caching
Update TTL (time to live) for caching
```
import datetime

cache.update(ttl=datetime.timedelta(hours=2))
```

#### Delete caching
```
cache.delete()
```
