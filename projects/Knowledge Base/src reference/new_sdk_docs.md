# Upgrade the Google GenAI SDK for Python
We released a new SDK (google-genai, v1.0) with the release of Gemini 2. The updated SDK is fully compatible with all Gemini API models and features, including recent additions like the multimodal live API (audio + video streaming), improved tool usage (code execution, function calling and integrated Google search grounding), and media generation (Imagen). This SDK lets you connect to the Gemini API through either Google AI Studio or Vertex AI.

The google-generativeai package will continue to support the original Gemini models. It can also be used with Gemini 2 models, just with a limited feature set. All new features will be developed in the new Google GenAI SDK.





# Authenticate
Authenticate using an API key. You can create your API key in Google AI Studio.

The old SDK handled the API client object implicitly. In the new SDK you create the API client and use it to call the API.

Remember, in either case the SDK will pick up your API key from the GOOGLE_API_KEY environment variable if you don't pass one to configure/Client.


export GOOGLE_API_KEY=...
Before


import google.generativeai as genai

genai.configure(api_key=...)
After


from google import genai

client = genai.Client(api_key=...)
Generate content
The new SDK provides access to all the API methods through the Client object. Except for a few stateful special cases (chat and live-api sessions), these are all stateless functions. For utility and uniformity, objects returned are pydantic classes.

Before


import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(
    'Tell me a story in 300 words'
)
print(response.text)
After


from google import genai
client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='Tell me a story in 300 words.'
)
print(response.text)

print(response.model_dump_json(
    exclude_none=True, indent=4))
Many of the same convenience features exist in the new SDK. For example, PIL.Image objects are automatically converted:

Before


import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content([
    'Tell me a story based on this image',
    Image.open(image_path)
])
print(response.text)
After


from google import genai
from PIL import Image

client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
        'Tell me a story based on this image',
        Image.open(image_path)
    ]
)
print(response.text)


# Function calling
In the new SDK, automatic function calling is the default. Here, you disable it.

Before


import google.generativeai as genai
from enum import Enum 

def get_current_weather(location: str) -> str:
    """Get the current whether in a given location.

    Args:
        location: required, The city and state, e.g. San Franciso, CA
        unit: celsius or fahrenheit
    """
    print(f'Called with: {location=}')
    return "23C"

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[get_current_weather]
)

response = model.generate_content("What is the weather in San Francisco?")
function_call = response.candidates[0].parts[0].function_call
After


from google import genai
from google.genai import types

client = genai.Client()

def get_current_weather(location: str) -> str:
    """Get the current whether in a given location.

    Args:
        location: required, The city and state, e.g. San Franciso, CA
        unit: celsius or fahrenheit
    """
    print(f'Called with: {location=}')
    return "23C"

response = client.models.generate_content(
   model='gemini-2.0-flash',
   contents="What is the weather like in Boston?",
   config=types.GenerateContentConfig(
       tools=[get_current_weather],
       automatic_function_calling={'disable': True},
   ),
)

function_call = response.candidates[0].content.parts[0].function_call
Automatic function calling
The old SDK only supports automatic function calling in chat. In the new SDK this is the default behavior in generate_content.

Before


import google.generativeai as genai

def get_current_weather(city: str) -> str:
    return "23C"

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[get_current_weather]
)

chat = model.start_chat(
    enable_automatic_function_calling=True)
result = chat.send_message("What is the weather in San Francisco?")
After


from google import genai
from google.genai import types
client = genai.Client()

def get_current_weather(city: str) -> str:
    return "23C"

response = client.models.generate_content(
   model='gemini-2.0-flash',
   contents="What is the weather like in Boston?",
   config=types.GenerateContentConfig(
       tools=[get_current_weather] 
   ),
)





# JSON response
Generate answers in JSON format.

By specifying a response_schema and setting response_mime_type="application/json" users can constrain the model to produce a JSON response following a given structure. The new SDK uses pydantic classes to provide the schema (although you can pass a genai.types.Schema, or equivalent dict). When possible, the SDK will parse the returned JSON, and return the result in response.parsed. If you provided a pydantic class as the schema the SDK will convert that JSON to an instance of the class.

Before


import google.generativeai as genai
import typing_extensions as typing

class CountryInfo(typing.TypedDict):
    name: str
    population: int
    capital: str
    continent: str
    major_cities: list[str]
    gdp: int
    official_language: str
    total_area_sq_mi: int

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
result = model.generate_content(
    "Give me information of the United States",
     generation_config=genai.GenerationConfig(
         response_mime_type="application/json",
         response_schema = CountryInfo
     ),
)

After


from google import genai
from pydantic import BaseModel

client = genai.Client()

class CountryInfo(BaseModel):
    name: str
    population: int
    capital: str
    continent: str
    major_cities: list[str]
    gdp: int
    official_language: str
    total_area_sq_mi: int

response = client.models.generate_content( 
    model='gemini-2.0-flash', 
    contents='Give me information of the United States.', 
    config={ 
        'response_mime_type': 'application/json',
        'response_schema': CountryInfo, 
    }, 
 )

response.parsed




Optional arguments
For all methods in the new SDK, the required arguments are provided as keyword arguments. All optional inputs are provided in the config argument.

Config arguments can be specified as either Python dictionaries or Config classes in the google.genai.types namespace. For utility and uniformity, all definitions within the types module are pydantic classes.

Before


import google.generativeai as genai

model = genai.GenerativeModel(
   'gemini-1.5-flash',
    system_instruction='you are a story teller for kids under 5 years old',
    generation_config=genai.GenerationConfig(
       max_output_tokens=400,
       top_k=2,
       top_p=0.5,
       temperature=0.5,
       response_mime_type='application/json',
       stop_sequences=['\n'],
    )
)
response = model.generate_content('tell me a story in 100 words')

After


from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
  model='gemini-2.0-flash',
  contents='Tell me a story in 100 words.',
  config=types.GenerateContentConfig(
      system_instruction='you are a story teller for kids under 5 years old',
      max_output_tokens= 400,
      top_k= 2,
      top_p= 0.5,
      temperature= 0.5,
      response_mime_type= 'application/json',
      stop_sequences= ['\n'],
      seed=42,
   ),
)






# Generate structured output with the Gemini API

Python Node.js Go Dart (Flutter) Android Swift Web REST



Gemini generates unstructured text by default, but some applications require structured text. For these use cases, you can constrain Gemini to respond with JSON, a structured data format suitable for automated processing. You can also constrain the model to respond with one of the options specified in an enum.

Here are a few use cases that might require structured output from the model:

Build a database of companies by pulling company information out of newspaper articles.
Pull standardized information out of resumes.
Extract ingredients from recipes and display a link to a grocery website for each ingredient.
In your prompt, you can ask Gemini to produce JSON-formatted output, but note that the model is not guaranteed to produce JSON and nothing but JSON. For a more deterministic response, you can pass a specific JSON schema in a responseSchema field so that Gemini always responds with an expected structure. To learn more about working with schemas, see More about JSON schemas.

This guide shows you how to generate JSON using the generateContent method through the SDK of your choice or using the REST API directly. The examples show text-only input, although Gemini can also produce JSON responses to multimodal requests that include images, videos, and audio.

Before you begin: Set up your project and API key
Before calling the Gemini API, you need to set up your project and configure your API key.

 Expand to view how to set up your project and API key

Generate JSON
When the model is configured to output JSON, it responds to any prompt with JSON-formatted output.

You can control the structure of the JSON response by supplying a schema. There are two ways to supply a schema to the model:

As text in the prompt
As a structured schema supplied through model configuration
Supply a schema as text in the prompt
The following example prompts the model to return cookie recipes in a specific JSON format.

Since the model gets the format specification from text in the prompt, you may have some flexibility in how you represent the specification. Any reasonable format for representing a JSON schema may work.


from google import genai

prompt = """List a few popular cookie recipes in JSON format.

Use this JSON schema:

Recipe = {'recipe_name': str, 'ingredients': list[str]}
Return: list[Recipe]"""

client = genai.Client(api_key="GEMINI_API_KEY")
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=prompt,
)

# Use the response as a JSON string.
print(response.text)
The output might look like this:


[
  {
    "recipe_name": "Chocolate Chip Cookies",
    "ingredients": [
      "2 1/4 cups all-purpose flour",
      "1 teaspoon baking soda",
      "1 teaspoon salt",
      "1 cup (2 sticks) unsalted butter, softened",
      "3/4 cup granulated sugar",
      "3/4 cup packed brown sugar",
      "1 teaspoon vanilla extract",
      "2 large eggs",
      "2 cups chocolate chips"
    ]
  },
  ...
]
Supply a schema through model configuration
The following example does the following:

Instantiates a model configured through a schema to respond with JSON.
Prompts the model to return cookie recipes.
This more formal method for declaring the JSON schema gives you more precise control than relying just on text in the prompt.

Important: When you're working with JSON schemas in the Gemini API, the order of properties matters. For more information, see Property ordering.

from google import genai
from pydantic import BaseModel


class Recipe(BaseModel):
  recipe_name: str
  ingredients: list[str]


client = genai.Client(api_key="GEMINI_API_KEY")
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='List a few popular cookie recipes. Be sure to include the amounts of ingredients.',
    config={
        'response_mime_type': 'application/json',
        'response_schema': list[Recipe],
    },
)
# Use the response as a JSON string.
print(response.text)

# Use instantiated objects.
my_recipes: list[Recipe] = response.parsed
The output might look like this:


[
  {
    "recipe_name": "Chocolate Chip Cookies",
    "ingredients": [
      "1 cup (2 sticks) unsalted butter, softened",
      "3/4 cup granulated sugar",
      "3/4 cup packed brown sugar",
      "1 teaspoon vanilla extract",
      "2 large eggs",
      "2 1/4 cups all-purpose flour",
      "1 teaspoon baking soda",
      "1 teaspoon salt",
      "2 cups chocolate chips"
    ]
  },
  ...
]
Note: Pydantic validators are not yet supported. If a pydantic.ValidationError occurs, it is suppressed, and .parsed may be empty/null.
Schema Definition Syntax
Specify the schema for the JSON response in the response_schema property of your model configuration. The value of response_schema must be a either:

A type, as you would use in a type annotation. See the Python typing module.
An instance of genai.types.Schema.
The dict equivalent of genai.types.Schema.
Define a Schema with a Type
The easiest way to define a schema is with a direct type. This is the approach used in the preceding example:


config={'response_mime_type': 'application/json',
        'response_schema': list[Recipe]}
The Gemini API Python client library supports schemas defined with the following types (where AllowedType is any allowed type):

int
float
bool
str
list[AllowedType]
For structured types:
dict[str, AllowedType]. This annotation declares all dict values to be the same type, but doesn't specify what keys should be included.
User-defined Pydantic models. This approach lets you specify the key names and define different types for the values associated with each of the keys, including nested structures.
Use an enum to constrain output
In some cases you might want the model to choose a single option from a list of options. To implement this behavior, you can pass an enum in your schema. You can use an enum option anywhere you could use a str in the response_schema, because an enum is a list of strings. Like a JSON schema, an enum lets you constrain model output to meet the requirements of your application.

For example, assume that you're developing an application to classify musical instruments into one of five categories: "Percussion", "String", "Woodwind", "Brass", or ""Keyboard"". You could create an enum to help with this task.

In the following example, you pass the enum class Instrument as the response_schema, and the model should choose the most appropriate enum option.


from google import genai
import enum

class Instrument(enum.Enum):
  PERCUSSION = "Percussion"
  STRING = "String"
  WOODWIND = "Woodwind"
  BRASS = "Brass"
  KEYBOARD = "Keyboard"

client = genai.Client(api_key="GEMINI_API_KEY")
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='What type of instrument is an oboe?',
    config={
        'response_mime_type': 'text/x.enum',
        'response_schema': Instrument,
    },
)

print(response.text)
# Woodwind
The Python SDK will translate the type declarations for the API. However, the API accepts a subset of the OpenAPI 3.0 schema (Schema). You can also pass the schema as JSON:


from google import genai

client = genai.Client(api_key="GEMINI_API_KEY")
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='What type of instrument is an oboe?',
    config={
        'response_mime_type': 'text/x.enum',
        'response_schema': {
            "type": "STRING",
            "enum": ["Percussion", "String", "Woodwind", "Brass", "Keyboard"],
        },
    },
)

print(response.text)
# Woodwind
Beyond basic multiple choice problems, you can use an enum anywhere in a schema for JSON or function calling. For example, you could ask the model for a list of recipe titles and use a Grade enum to give each title a popularity grade:


from google import genai

import enum
from pydantic import BaseModel

class Grade(enum.Enum):
    A_PLUS = "a+"
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    F = "f"

class Recipe(BaseModel):
  recipe_name: str
  rating: Grade

client = genai.Client(api_key="GEMINI_API_KEY")
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='List 10 home-baked cookies and give them grades based on tastiness.',
    config={
        'response_mime_type': 'application/json',
        'response_schema': list[Recipe],
    },
)

print(response.text)
# [{"rating": "a+", "recipe_name": "Classic Chocolate Chip Cookies"}, ...]
More about JSON schemas
When you configure the model to return a JSON response, you can use a Schema object to define the shape of the JSON data. The Schema represents a select subset of the OpenAPI 3.0 Schema object.

Here's a pseudo-JSON representation of all the Schema fields:


{
  "type": enum (Type),
  "format": string,
  "description": string,
  "nullable": boolean,
  "enum": [
    string
  ],
  "maxItems": string,
  "minItems": string,
  "properties": {
    string: {
      object (Schema)
    },
    ...
  },
  "required": [
    string
  ],
  "propertyOrdering": [
    string
  ],
  "items": {
    object (Schema)
  }
}
The Type of the schema must be one of the OpenAPI Data Types. Only a subset of fields is valid for each Type. The following list maps each Type to valid fields for that type:

string -> enum, format
integer -> format
number -> format
boolean
array -> minItems, maxItems, items
object -> properties, required, propertyOrdering, nullable
Here are some example schemas showing valid type-and-field combinations:


{ "type": "string", "enum": ["a", "b", "c"] }

{ "type": "string", "format": "date-time" }

{ "type": "integer", "format": "int64" }

{ "type": "number", "format": "double" }

{ "type": "boolean" }

{ "type": "array", "minItems": 3, "maxItems": 3, "items": { "type": ... } }

{ "type": "object",
  "properties": {
    "a": { "type": ... },
    "b": { "type": ... },
    "c": { "type": ... }
  },
  "nullable": true,
  "required": ["c"],
  "propertyOrdering": ["c", "b", "a"]
}
For complete documentation of the Schema fields as they're used in the Gemini API, see the Schema reference.

Property ordering
When you're working with JSON schemas in the Gemini API, the order of properties is important. By default, the API orders properties alphabetically and does not preserve the order in which the properties are defined (although the Google Gen AI SDKs may preserve this order). If you're providing examples to the model with a schema configured, and the property ordering of the examples is not consistent with the property ordering of the schema, the output could be rambling or unexpected.

To ensure a consistent, predictable ordering of properties, you can use the optional propertyOrdering[] field.


"propertyOrdering": ["recipe_name", "ingredients"]
propertyOrdering[] – not a standard field in the OpenAPI specification – is an array of strings used to determine the order of properties in the response. By specifying the order of properties and then providing examples with properties in that same order, you can potentially improve the quality of results.

Key Point: To improve results when you're using a JSON schema, set propertyOrdering[] and provide examples with a matching property ordering.
Was this helpful?

Send feedback



