import math
from ragas.metrics import (
    Faithfulness,
    ResponseRelevancy,
    LLMContextPrecisionWithReference,
    LLMContextRecall
)
from ragas.dataset_schema import SingleTurnSample
from ragas.llms import LlamaIndexLLMWrapper
from llama_index.llms.openai import OpenAI
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import OpenAIEmbeddings
import pandas as pd
import multiprocessing as mp
import ast  # Safe alternative to eval()
from datasets import Dataset 
from ragas import evaluate
from ragas.metrics import answer_correctness

# load .env file
from dotenv import load_dotenv, find_dotenv
import os

from services.cosmos_service import update_score_list
load_dotenv(find_dotenv())
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Init metrics with evaluator LLM
evaluator_llm = LlamaIndexLLMWrapper(OpenAI(model="gpt-4o"))
evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())

def replace_nan_with_zero(value):
    return 0 if isinstance(value, float) and math.isnan(value) else value
# ---------------- Synchronous Multiprocessing Functions ----------------
def calculate_faithfulness(user_input: str, response: str, retrieved_contexts: list, queue):
    sample = SingleTurnSample(
            user_input=user_input,
            response=response,
            retrieved_contexts=retrieved_contexts
        )
    scorer = Faithfulness(llm=evaluator_llm)
    # queue.put("faithfulness", scorer.single_turn_score(sample))  # Removed 'await' since it's synchronous
    score = {"metric":"faithfulness","score":replace_nan_with_zero(scorer.single_turn_score(sample))}
    print(score)
    queue.put(score)

def calculate_response_relevancy(user_input: str, response: str, retrieved_contexts: list, queue):
    sample = SingleTurnSample(
        user_input=user_input,
        response=response,
        retrieved_contexts=retrieved_contexts
    )
    scorer = ResponseRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings)
    # queue.put("res_relevency", scorer.single_turn_score(sample))  # Removed 'await'
    score = {"metric":"res_relevency","score":replace_nan_with_zero(scorer.single_turn_score(sample))}
    print(score)
    queue.put(score)  
    
def calculate_answer_correctness(user_input: str, response: str, reference: str, queue):
    sample = {
            "question":[user_input],
            "answer":[response],
            "ground_truth":[reference],
    }
    raga_dataset = Dataset.from_dict(sample)
    score_0998 = evaluate(raga_dataset,metrics=[answer_correctness])
    if score_0998:
        score = {"metric":"answer_correctness","score":replace_nan_with_zero(score_0998["answer_correctness"][0])}
    print(score)
    queue.put(score)

def calculate_context_precision(user_input: str, response: str, retrieved_contexts: list,reference: str, queue):
    context_precision = LLMContextPrecisionWithReference(llm=evaluator_llm)
    sample = SingleTurnSample(
        user_input=user_input,
        response=response,
        reference=reference,
        retrieved_contexts=retrieved_contexts, 
    )
    # queue.put("context_precision", context_precision.single_turn_score(sample))  # Removed 'await'
    score = {"metric":"context_precision","score":replace_nan_with_zero(context_precision.single_turn_score(sample))}
    print(score)
    queue.put(score) 

def calculate_context_recall(user_input: str, response: str, retrieved_contexts: list, reference: str, queue):
    sample = SingleTurnSample(
        user_input=user_input,
        response=response,
        reference=reference,
        retrieved_contexts=retrieved_contexts, 
    )
    context_recall = LLMContextRecall(llm=evaluator_llm)
    # queue.put("context_recall", context_recall.single_turn_score(sample))  # Removed 'await'
    score = {"metric":"context_recall","score":replace_nan_with_zero(context_recall.single_turn_score(sample))}
    print(score)
    queue.put(score) 

# ---------------- Running All Metrics ----------------
def run_all_metrics(df: pd.DataFrame, fileID):
    queue = mp.Queue()
    print("Trying to run all metrices with the testset!!")
    for index, row in df.iterrows():
        if pd.isna(row["response"]) or row["response"] == "":  # Skip if response is NaN or empty string
            print(f"Skipping row {index} due to missing response: {row['response']}")
            continue

        print("trying to retrive reference_contexts!!")
        # retrieved_contexts = ast.literal_eval(row["reference_contexts"])  # Safer than eval()
        retrieved_contexts = row["reference_contexts"]  # Safer than eval()
        print("Context Retrived!!")
        print("response present!!")
        print(row["response"])
        qID = row["questionID"]
        p1 = mp.Process(target=calculate_faithfulness, args=(row["user_input"], row["response"], retrieved_contexts, queue))
        p2 = mp.Process(target=calculate_response_relevancy, args=(row["user_input"], row["response"], retrieved_contexts, queue))
        p3 = mp.Process(target=calculate_context_precision, args=(row["user_input"], row["response"], retrieved_contexts,row["reference"], queue))
        p4 = mp.Process(target=calculate_context_recall, args=(row["user_input"], row["response"], retrieved_contexts, row["reference"], queue))
        p5 = mp.Process(target=calculate_answer_correctness, args=(row["user_input"], row["response"], row["reference"], queue))
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        print("Processes started")

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        print("Processes joined")
        score1 = queue.get()
        score2 = queue.get()
        score3 = queue.get()
        score4 = queue.get()
        score5 = queue.get()
        scorelist = []
        scorelist.append(score1)
        scorelist.append(score2)
        scorelist.append(score3)
        scorelist.append(score4)
        scorelist.append(score5)
        print("Evaluation Sucess!!")
        print("Updating Cosmos!!")
        res = update_score_list(fileID=fileID, questionID=qID, score_list=scorelist)
        print(res)
    return "Metrics score stored sucessfully!!"
# if __name__ == "__main__":
#     mp.set_start_method("spawn", force=True)  # Set at the beginning
#     df = read_testset(file_name="testset_response_(WCF)_9.csv")
#     run_all_metrics(df)