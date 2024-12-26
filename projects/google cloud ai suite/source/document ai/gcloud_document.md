# Overview
1. Perform OCR on images using Cloud Vision AI API
2. Perform natural language analysis using Natural Language AI API

# OCR
1. Create and initialize Cloud Vision AI client
2. Open image and send image to client
3. Perform OCR using `.text_detection()`
4. Get text from response

# Natural language analysis
1. Create and initialize Language Service client
2. Send text from OCR to client
3. Use `.analyze_sentiment()`, `.analyze_entities()`, `.analyze_syntax()` to perform appropriate analysis


# `client.text_detection()`
## Basic text
The `client.text_detection()` method from the Google Cloud Vision API performs Optical Character Recognition (OCR) on images, extracting text from them.
The `text_annotations` field in response of this method contains detailed information about the text detected in the image.
  It is a list of `EntityAnnotation` objects, where each object contains information about a piece of detected text.
  `description` attribute of every object within `text_annotations` contains the text.
    `description` attribute of first object contains entire text
    `description` attribute of all subsequent objects contains entities and bounding polygons (locations) of all entities

## Handwriting text
Use `client.document_text_detection()` for handwriting in images

## Remote images
Use:
```
image = vision.Image()
    image.source.image_uri = uri
```
for remote images

## PDFs
https://cloud.google.com/vision/docs/pdf



Consider an example response from `client.text_detection()`:

`json
{
  "text_annotations": [
    {
      "description": "Hello, World!",
      "bounding_poly": {
        "vertices": [
          {"x": 30, "y": 50},
          {"x": 150, "y": 50},
          {"x": 150, "y": 80},
          {"x": 30, "y": 80}
        ]
      }
    },
    {
      "description": "Hello",
      "bounding_poly": {
        "vertices": [
          {"x": 30, "y": 50},
          {"x": 80, "y": 50},
          {"x": 80, "y": 80},
          {"x": 30, "y": 80}
        ]
      }
    },
    {
      "description": "World",
      "bounding_poly": {
        "vertices": [
          {"x": 100, "y": 50},
          {"x": 150, "y": 50},
          {"x": 150, "y": 80},
          {"x": 100, "y": 80}
        ]
      }
    }
  ]
}`