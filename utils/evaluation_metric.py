from datasets import Dataset 
from ragas import evaluate
from ragas.metrics import answer_correctness, faithfulness, context_recall, context_precision
from ragas.cost import get_token_usage_for_openai
from dotenv import load_dotenv, find_dotenv
from ragas.llms.base import OpenAI
from ragas.cost import get_token_usage_for_openai
import os
import pandas as pd

from services.cosmos_service import update_score_list

load_dotenv(find_dotenv())
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY"),
    max_tokens= 512, 
    base_url = "https://oai.helicone.ai/v1",  
    default_headers= {
        "Helicone-Auth": "Bearer sk-helicone-h6bsaui-m2ouiyy-xb7ndxa-gdobjsq"
})
def evaluate_all(user_input: str, response: str, reference: str, retrieved_contexts: list):
    sample = {
            "question":[user_input],
            "answer":[response],
            "ground_truth":[reference],
            "contexts": [retrieved_contexts]
    }
    raga_dataset = Dataset.from_dict(sample)
    score_0998 = evaluate(
        dataset=raga_dataset,
        llm = llm,
        metrics=[answer_correctness, faithfulness, context_precision, context_recall],
        token_usage_parser=get_token_usage_for_openai,
    )
    # score_0998.
    print(f"token used in answer correctness = {score_0998.total_tokens()}")
    # print(f"token used in answer correctness = {score_0998.total_cost(cost_per_input_token=score_0998.total_cost, )}")
    print(score_0998)
    return score_0998
    # if score_0998:
    #     score = {"metric":"answer_correctness","score":replace_nan_with_zero(score_0998["answer_correctness"][0])}
    # print(score)
    # # queue.put(score)

async def run_metric_calculator(df: pd.DataFrame, fileID):
    print("Trying to run all metrices with the testset!!")
    for index, row in df.iterrows():
        if pd.isna(row["response"]) or row["response"] == "":  # Skip if response is NaN or empty string
            print(f"Skipping row {index} due to missing response: {row['response']}")
            continue

        print("trying to retrive reference_contexts!!")
        retrieved_contexts = row["reference_contexts"]  # Safer than eval()
        print("Context Retrived!!")
        print("response present!!")
        print(row["response"])
        qID = row["questionID"]
        scorelist = evaluate_all(
            user_input=row["user_input"],
            response=row["response"],
            reference=row["reference"],
            retrieved_contexts=retrieved_contexts
        )
        # print(f"---------------------{type(scorelist)}---------------------")
        scorelist = scorelist.to_pandas().to_dict(orient="records")
        # print("Score list is ", scorelist)
        only_score = {}
        for score in scorelist:
            # print("score is ", score)
            only_score['answer_correctness'] = score["answer_correctness"]
            only_score['faithfulness'] = score["faithfulness"]
            only_score['context_precision'] = score["context_precision"]
            only_score['context_recall'] = score["context_recall"]
        print("only score is ", only_score)
        print("final score is ", scorelist, "and questionId is ", qID)
        res = update_score_list(fileID=fileID, questionID=qID, score_list=only_score)
        print(res)
    return "Metrics score stored sucessfully!!"