# Contains functions that deal with the extraction of documents from a text file (see PR01)

import json

from document import Document
import re


def extract_collection(source_file_path: str) -> list[Document]:
    """
    Loads a text file (aesopa10.txt) and extracts each of the listed fables/stories from the file.
    :param source_file_name: File name of the file that contains the fables
    :return: List of Document objects
    """
    with open(source_file_path, "r") as file:
        text = file.read()

    # Split the text into sections based on three blank lines
    fables = re.split(r"\n\s*\n\s*\n", text.strip())

    catalog = []

    for index, fable in enumerate(fables):
        if not fable.strip():
            continue  # Skip any empty sections

        # Extract the title and the body of the fable
        parts = fable.strip().split("\n\n", 1)
        if len(parts) < 2:
            continue  # Skip sections that do not have both title and body

        title = parts[0].strip()
        body = parts[1].strip()

        # Remove line breaks in the body
        body_text = " ".join(body.splitlines())

        # Tokenize the body into terms (keeping duplicates)
        terms = body_text.split()

        # Create a Document object and add to the catalog
        document = Document()
        document.document_id = (index,)
        document.title = (title,)
        document.raw_text = (body_text,)
        document.terms = terms
        catalog.append(document)

    return catalog


def save_collection_as_json(collection: list[Document], file_path: str) -> None:
    """
    Saves the collection to a JSON file.
    :param collection: The collection to store (= a list of Document objects)
    :param file_path: Path of the JSON file
    """

    serializable_collection = []
    for document in collection:
        serializable_collection += [
            {
                "document_id": document.document_id,
                "title": document.title,
                "raw_text": document.raw_text,
                "terms": document.terms,
                "filtered_terms": document.filtered_terms,
                "stemmed_terms": document.stemmed_terms,
            }
        ]

    with open(file_path, "w") as json_file:
        json.dump(serializable_collection, json_file)


def load_collection_from_json(file_path: str) -> list[Document]:
    """
    Loads the collection from a JSON file.
    :param file_path: Path of the JSON file
    :return: list of Document objects
    """
    try:
        with open(file_path, "r") as json_file:
            json_collection = json.load(json_file)

        collection = []
        for doc_dict in json_collection:
            document = Document()
            document.document_id = doc_dict.get("document_id")
            document.title = doc_dict.get("title")
            document.raw_text = doc_dict.get("raw_text")
            document.terms = doc_dict.get("terms")
            document.filtered_terms = doc_dict.get("filtered_terms")
            document.stemmed_terms = doc_dict.get("stemmed_terms")
            collection += [document]

        return collection
    except FileNotFoundError:
        print("No collection was found. Creating empty one.")
        return []
