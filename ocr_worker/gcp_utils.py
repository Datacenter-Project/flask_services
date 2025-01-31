import uuid 


# def detect_text(path):
#     """Detects text in the file."""
#     from google.cloud import vision
#     import io
#     client = vision.ImageAnnotatorClient()

#     # [START vision_python_migration_text_detection]
#     with io.open(path, 'rb') as image_file:
#         content = image_file.read()

#     image = vision.Image(content=content)

#     response = client.text_detection(image=image)
#     texts = response.text_annotations
#     print('Text:')
#     print(texts[0].description)

#     full_text = ''

#     for text in texts:
#         # print('\n"{}"'.format(text.description))
#         full_text += text.description+' '

#         vertices = (['({},{})'.format(vertex.x, vertex.y)
#                     for vertex in text.bounding_poly.vertices])

#         # print('bounds: {}'.format(','.join(vertices)))

#     if response.error.message:
#         raise Exception(
#             '{}\nFor more info on error messages, check: '
#             'https://cloud.google.com/apis/design/errors'.format(
#                 response.error.message))
#     # [END vision_python_migration_text_detection]
# # [END vision_text_detection]

def detect_document_from_file(source_file):
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    # with io.open(path, 'rb') as image_file:
    #     content = image_file.read()

    image = vision.Image(content=source_file)

    response = client.document_text_detection(image=image)

    texts = []

    for page in response.full_text_annotation.pages:
        page_text = ''
        for block in page.blocks:
            block_text = ''
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                paragraph_text = ''                
                # print('Paragraph confidence: {}'.format(
                    # paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    paragraph_text += word_text+' '
                    # print('Word text: {} (confidence: {})'.format(
                    #     word_text, word.confidence))

                    # for symbol in word.symbols:
                    #     print('\tSymbol: {} (confidence: {})'.format(
                    #         symbol.text, symbol.confidence))
                # print("Pargraph: ", paragraph_text)
            
                block_text += paragraph_text+' '
            print("Block text:", block_text)
            page_text += block_text+'\n\n'
        texts.append(page_text)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return texts

def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            block_text = ''
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                paragraph_text = ''                
                # print('Paragraph confidence: {}'.format(
                    # paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    paragraph_text += word_text+' '
                    # print('Word text: {} (confidence: {})'.format(
                    #     word_text, word.confidence))

                    # for symbol in word.symbols:
                    #     print('\tSymbol: {} (confidence: {})'.format(
                    #         symbol.text, symbol.confidence))
                # print("Pargraph: ", paragraph_text)
            
                block_text += paragraph_text+' '
            print("Block text:", block_text)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

if __name__ == "__main__":
    # input_image_path = 'sample_input_image.png'
    input_image_path = 'detect_handwriting_OCR-detect-handwriting_SMALL.png'
    
    # detect_text(input_image_path)
    # detect_document(input_image_path)
    destination_blob_name = str(uuid.uuid4())
    print(str(destination_blob_name))
    # upload_blob_from_filename("datacenter_project_bucket", input_image_path, input_image_path)
    # download_blob("datacenter_project_bucket", input_image_path, 'temp.png')
    # with open(input_image_path, 'rb') as fin:
    #     upload_blob_from_file("datacenter_project_bucket", fin, destination_blob_name)