from llama_index.readers.file import PDFReader
from ragas.testset import TestsetGenerator
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def generate_testset(file_stream, testset_size: int):
    print("Trying to read the document")

    # Read the PDF content from bytes
    reader = PDFReader()
    documents = reader.load_data(file_stream)

    print("Document loaded successfully!!!")

    # Generative model setup
    # generator_llm = OpenAI(model="gpt-4o")
    # embeddings = OpenAIEmbedding(dimensions=256, model="text-embedding-3-small")
    
    generator_llm = OpenAI(
        # model="gpt-4o",
        model="gpt-4o-mini",
        api_key= os.getenv("OPENAI_API_KEY"),
        max_tokens= 512, 
        api_base = "https://oai.helicone.ai/v1",  
        default_headers= {
            "Helicone-Auth": os.getenv("HELICONE_API_KEY")
        }
    )

    embeddings = OpenAIEmbedding(
        dimensions=256, 
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
        api_base="https://oai.helicone.ai/v1",
        default_headers={
            "Helicone-Auth": os.getenv("HELICONE_API_KEY")
        }
    )

    generator = TestsetGenerator.from_llama_index(
        llm=generator_llm,
        embedding_model=embeddings,
    )
    print("Testset generator created successfully!!!")
    testset = generator.generate_with_llamaindex_docs(
        documents,
        testset_size=testset_size,
    )
    print("Testset generated successfully!!!")
    print(f"len(testset) = {len(testset)} and given testest_size = {testset_size}")
    df = testset.to_pandas()
    if len(df) == testset_size:
        return df
    else:
        return df.head(testset_size)
