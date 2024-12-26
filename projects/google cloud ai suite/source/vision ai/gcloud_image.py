import os
from google.cloud import vision
from google.cloud import language_v1

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/ansarimn/Downloads/optimum-task-411411-3f4dc520069f.json"


def extract_text_from_image(image_path):
    """
    Extracts text from an image using Google Cloud Vision OCR.
    """

    """
    
    """
    client = vision.ImageAnnotatorClient()
    #  with open(image_path, 'rb') as image_file:
    #      content = image_file.read()
    #  image = vision.Image(content=content)

    image = vision.Image ()
    image.source.gcs_image_uri = "gs://gcloud_image_intelligence/sample_image.png"

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f"{response.error.message}")

    # The first text annotation contains the full text detected
    if texts:
        return texts[0].description
    return ""

def analyze_text(text):
    """
    Analyzes text using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )


    '''
    # Perform sentiment analysis
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    print(f"Sentiment score: {sentiment.score}, magnitude: {sentiment.magnitude}")

    # Perform entity recognition
    entities = client.analyze_entities(document=document).entities
    for entity in entities:
        print(f"Entity: {entity.name}, Type: {language_v1.Entity.Type(entity.type_).name}, Salience: {entity.salience}")

    # Perform syntax analysis
    syntax = client.analyze_syntax(document=document)
    for token in syntax.tokens:
        print(f"Token: {token.text.content}, Part of Speech: {language_v1.PartOfSpeech.Tag(token.part_of_speech.tag).name}")
    '''



def main(image_path):
    # Extract text from the scanned document
    text = extract_text_from_image(image_path)
    print(f"Extracted Text:\n{text}")

    # Analyze the extracted text
    analyze_text(text)

if __name__ == "__main__":
    # Replace with the path to your scanned document image
    scanned_image_path = "/google cloud intelligence/gc.jpeg"
    main(scanned_image_path)