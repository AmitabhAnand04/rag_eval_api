from llama_index.readers.file import PDFReader
from ragas.testset import TestsetGenerator
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

def generate_testset(file_stream, testset_size: int):
    print("Trying to read the document")

    # Read the PDF content from bytes
    reader = PDFReader()
    documents = reader.load_data(file_stream)

    print("Document loaded successfully!!!")

    # Generative model setup
    generator_llm = OpenAI(model="gpt-4o")
    embeddings = OpenAIEmbedding()

    generator = TestsetGenerator.from_llama_index(
        llm=generator_llm,
        embedding_model=embeddings,
    )

    testset = generator.generate_with_llamaindex_docs(
        documents,
        testset_size=testset_size,
    )

    df = testset.to_pandas()
    return df