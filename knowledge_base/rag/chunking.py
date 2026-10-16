import re


def fixed_size_chunking(text, chunk_size=300, overlap=50):
    """
    Split text into fixed-size chunks with overlap.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def sentence_based_chunking(text):
    """
    Split text into sentence-based chunks.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    chunks = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    return chunks


if __name__ == "__main__":

    sample_text = (
        "Candidates must meet the minimum qualifications "
        "specified in the job description. "
        "Required qualifications may include education, "
        "technical skills, or relevant experience. "
        "Applicants should provide accurate information."
    )

    print("=" * 60)
    print("CHUNKING TEST")
    print("=" * 60)

    # Fixed-size chunking
    fixed_chunks = fixed_size_chunking(
        sample_text,
        chunk_size=100,
        overlap=20
    )

    print("\nFIXED-SIZE CHUNKS")
    print("-" * 60)

    for i, chunk in enumerate(fixed_chunks, start=1):
        print(f"\nChunk {i}:")
        print(chunk)

    # Sentence-based chunking
    sentence_chunks = sentence_based_chunking(
        sample_text
    )

    print("\nSENTENCE-BASED CHUNKS")
    print("-" * 60)

    for i, chunk in enumerate(sentence_chunks, start=1):
        print(f"\nChunk {i}:")
        print(chunk)