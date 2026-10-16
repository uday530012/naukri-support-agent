from pathlib import Path


# Find the knowledge_base folder
KNOWLEDGE_BASE_DIR = (
    Path(__file__).resolve().parent.parent / "knowledge_base"
)


def load_documents():
    """
    Load all TXT files from the knowledge_base folder.
    """

    documents = []

    txt_files = sorted(
        KNOWLEDGE_BASE_DIR.glob("*.txt")
    )

    if not txt_files:
        raise FileNotFoundError(
            f"No .txt files found in: {KNOWLEDGE_BASE_DIR}"
        )

    for file_path in txt_files:

        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            print(
                f"Warning: {file_path.name} is empty."
            )
            continue

        documents.append({
            "document_id": file_path.stem,
            "filename": file_path.name,
            "text": text
        })

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print("=" * 60)
    print("KNOWLEDGE BASE DOCUMENT LOADER")
    print("=" * 60)

    print(
        f"\nKnowledge base path:"
    )
    print(KNOWLEDGE_BASE_DIR)

    print(
        f"\nDocuments loaded: {len(documents)}"
    )

    print("\nDocuments:")

    for document in documents:
        print(
            f"- {document['filename']} "
            f"({len(document['text'])} characters)"
        )

    print(
        "\nDocument loading completed successfully."
    )