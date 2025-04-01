from typing import Dict, List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import tempfile
import os

from pydantic import BaseModel
from services.cosmos_service import get_item, get_score_item, insert_items, update_item, get_item_for_evaluation
from utils.create_testset import generate_testset
from utils.evaluation import run_all_metrics
from utils.refactor import transform_data, transform_to_df

file_router = APIRouter()

# Define Pydantic model for request body
class ResponseDetails(BaseModel):
    response: str
    reference: Optional[str] = None
    reference_contexts: Optional[List[str]] = []

class QuestionResponse(BaseModel):
    responses: Dict[str, ResponseDetails]

@file_router.get("/")
def welcome():
    print("This API is Live!!")
    return "This API is Live!!"

@file_router.post("/upload") # API 1
async def process_file(file: UploadFile = File(...), testset_size: int = Form(1)):
    if file.content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file_path = os.path.join(tmp_dir, file.filename)

        # Write file content to the temp file
        with open(tmp_file_path, "wb") as tmp_file:
            tmp_file.write(await file.read())

        print(f"File saved temporarily at {tmp_file_path}")

        # Generate testset using the temporary file path
        df = generate_testset(tmp_file_path, testset_size)

    # return df.to_dict(orient="records")
    res = df.to_dict(orient = "records")
    response =  transform_data(res)
    fileID = insert_items(response)
    return {"fileID": fileID, "message": f"Item stored with file id {fileID}", "response": response}
    
@file_router.get("/get_testset") #API 2
def getitem(fileID):
    try:
        res = get_item(fileID=fileID)
        return res[0]["testset"]
    except Exception as e:
        raise HTTPException (status_code= 500, detail=str(e))
    
@file_router.post("/submit") # API 3
def submit(fileID, request_body: QuestionResponse = None):
    if not request_body:
        raise HTTPException(status_code=400, detail="Invalid request body.")

    response = update_item(fileID, request_body.responses)
    return response

@file_router.post("/evaluate") # API 4
def evaluate(fileID):
    items = get_item_for_evaluation(fileID)
    # print(items)
    ragas_df = transform_to_df(items["testset"])
    # ragas_df.to_csv("eval.csv", index=False)
    return run_all_metrics(df=ragas_df, fileID=fileID)

@file_router.get("/get_scores") # API 5
def scores(fileID):
    return get_score_item(fileID)
