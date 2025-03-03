import json
from azure.cosmos import CosmosClient, exceptions
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
connection_string = os.getenv("AZURE_COSMOS_CONN_STR")

# Initialize the Cosmos client

DATABASE_NAME = "rag_score_db"
CONTAINER_NAME = "rag_eval_dataset"

# Initialize Cosmos client
client = CosmosClient.from_connection_string(connection_string)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def insert_items(body_item):
    try:
        container.create_item(body_item)
        return body_item["id"]
    except exceptions.CosmosHttpResponseError as e:
        return f"Failure: An error occurred - {e.message}"
    except exceptions.CosmosResourceExistsError:
        return "Failure: A conversation log with the same ID already exists."
    
def get_item(fileID):
    try:
        query = f'SELECT * FROM c where c.id = "{fileID}"'
        res = container.query_items(query=query, enable_cross_partition_query=True)
        # res2 = json.dumps(list(res))
        # print(list(res))
        return list(res)
    except exceptions.CosmosHttpResponseError as e:
        return f"Failure: An error occurred - {e.message}"

# Old code which updates only response in the test set.

# def update_item(fileID, question_responses):
#     """
#     Update multiple responses for given questionIDs in the Cosmos DB item.

#     :param fileID: str - The ID of the item to update.
#     :param question_responses: dict - A dictionary where keys are questionIDs and values are their responses.
#     EXAMPLE: question_responses = {
#     "21c08461-192a-45d4-b83c-e894bd7b34d9": "Response for cerebrovascular disease",
#     "615429a9-3e7f-4f19-92af-2410bd4b784c": "Response for pulmonary embolism"
#     }

#     """
#     try:
#         # Query the item
#         query = f"SELECT * FROM c WHERE c.id = '{fileID}'"
#         items = list(container.query_items(query=query, enable_cross_partition_query=True))

#         if not items:
#             print("❌ Item not found.")
#             return "Item not found."

#         item = items[0]  # Retrieve the first matching item

#         # Update the response for the matching questionIDs
#         updated = False
#         for question in item.get("testset", []):
#             if question["questionID"] in question_responses:
#                 question["response"] = question_responses[question["questionID"]]
#                 updated = True

#         # Replace the item in Cosmos DB if updates were made
#         if updated:
#             container.replace_item(item=item["id"], body=item)
#             print(f"✅ Updated item with ID: {fileID} for questionIDs: {list(question_responses.keys())}")
#             return f"Updated item with ID: {fileID} for questionIDs: {list(question_responses.keys())}"
#         else:
#             print("ℹ️ No updates made.")
#             return "No matching questionIDs found."
    
#     except exceptions.CosmosHttpResponseError as e:
#         return f"Failure: An error occurred - {e.message}"

def update_item(fileID, question_responses):
    """
    Update multiple fields (response, reference_contexts, reference) for given questionIDs in the Cosmos DB item.

    :param fileID: str - The ID of the item to update.
    :param question_responses: dict - A dictionary where keys are questionIDs and values are dictionaries containing response, reference_contexts, and reference.
    
    EXAMPLE:
    question_responses = {
        "21c08461-192a-45d4-b83c-e894bd7b34d9": {
            "response": "Response for cerebrovascular disease",
            "reference_contexts": ["Context 1", "Context 2"],
            "reference": "Reference 1"
        },
        "615429a9-3e7f-4f19-92af-2410bd4b784c": {
            "response": "Response for pulmonary embolism"
        }
    }
    """
    try:
        # Query the item
        query = f"SELECT * FROM c WHERE c.id = '{fileID}'"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))

        if not items:
            print("❌ Item not found.")
            return "Item not found."

        item = items[0]  # Retrieve the first matching item

        # Update the fields for the matching questionIDs
        updated = False
        for question in item.get("testset", []):
            if question["questionID"] in question_responses:
                question_data = question_responses[question["questionID"]]
                
                # question["response"] = question_data.get("response", question.get("response"))
                # question["reference_contexts"] = question_data.get("reference_contexts", question.get("reference_contexts", []))
                # question["reference"] = question_data.get("reference", question.get("reference"))
                question["response"] = question_data.response if question_data.response is not None else question.get("response")
                if len(question_data.reference_contexts) > 0:
                    print("reference context is not none so adding its value.")
                    print(question_data.reference_contexts)
                    question["reference_contexts"] = question_data.reference_contexts
                
                if question_data.reference is not None:
                    print("reference context is not none so adding its value.")
                    print(question_data.reference)
                    question["reference"] = question_data.reference

                updated = True

        # Replace the item in Cosmos DB if updates were made
        if updated:
            container.replace_item(item=item["id"], body=item)
            print(f"✅ Updated item with ID: {fileID} for questionIDs: {list(question_responses.keys())}")
            return f"Updated item with ID: {fileID} for questionIDs: {list(question_responses.keys())}"
        else:
            print("ℹ️ No updates made.")
            return "No matching questionIDs found."
    
    except exceptions.CosmosHttpResponseError as e:
        return f"Failure: An error occurred - {e.message}"


def get_item_for_evaluation(fileID):
    query = f'SELECT c.testset FROM c where c.id = "{fileID}"'
    res = list(container.query_items(query=query, enable_cross_partition_query=True))
    return res[0]

def update_score_list(fileID, questionID, score_list):
    query = f"""
    SELECT * FROM c 
    WHERE c.id = @fileID
    """
    params = [
        {"name": "@fileID", "value": fileID}
    ]
    
    items = list(container.query_items(query=query, parameters=params, enable_cross_partition_query=True))
    revised_score_list = {}
    for score in score_list:
        revised_score_list[score["metric"]] = score["score"]
    if items:
        for item in items:
            updated = False
            for test in item.get("testset", []):
                if test.get("questionID") == questionID:
                    test["metrics_score"] = revised_score_list
                    updated = True
                    break
            
            if updated:
                container.upsert_item(item)
                print("Score list updated successfully.")
                return "Item with score updated sucessfully!!"
            else:
                print("Question ID not found in testset.")
                return "Question ID not found in testset."
    else:
        print("No matching fileID found.")
        return "No matching fileID found."

def get_score_item(fileID):
    try:
        # Query the item by id
        query = f"SELECT * FROM c WHERE c.id = '{fileID}'"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        
        if not items:
            return {"error": "Item not found"}
        
        item = items[0]
        
        # Extract relevant fields
        extracted_data = []
        for test in item.get("testset", []):
            extracted_data.append({
                "questionID": test.get("questionID"),
                "user_input": test.get("user_input"),
                "response": test.get("response"),
                "context_precision": test.get("metrics_score", {}).get("context_precision"),
                "context_recall": test.get("metrics_score", {}).get("context_recall"),
                "res_relevency": test.get("metrics_score", {}).get("res_relevency"),
                "faithfulness": test.get("metrics_score", {}).get("faithfulness"),
                "answer_correctness": test.get("metrics_score", {}).get("answer_correctness")
            })
        
        return {"fileID": fileID, "scores": extracted_data}
    except Exception as e:
        return {"error": str(e)}

