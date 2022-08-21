import os
import uvicorn
import random
import json
from typing import Optional, Union
from fastapi import FastAPI, BackgroundTasks, Header
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List, Dict, Any
from dotenv import load_dotenv
load_dotenv('token.env')
TOKEN = os.getenv('TOKEN')

class newReview(BaseModel):
    title: str
    content: str
    rating: float | None = None 

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Define origins for CORS

origins = [
    "http://yourorigin.domain",
    "https://yourorigin.domain"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse("/docs")

# get random number between min(default:0) and max(default:300)
@app.get("/random")
def get_random_value(min: Optional[int] = 0, max: Optional[int] = 300):
    rval = random.randint(min, max)
    return { "value": rval }


@app.get("/reviews")
def get_reviews_json():
    return JSONResponse(status_code=200,content=json.load(open('data.json')))

@app.post("/reviews/add")
def add_a_review(review: newReview, token: str = Header(convert_underscores=False)):
    if token != TOKEN:

        return JSONResponse(status_code=401,content="Wrong access token!")

    elif token == TOKEN:

        oldReviews = json.load(open('data.json'))["reviews"]
		
        if oldReviews[-1]:
            newID = oldReviews[-1]["id"] + 1
        else:
            newID = 0
        
        if review.dict().get("rating"):
            newObj = {"title": review.dict().get("title"),"content": review.dict().get("content"),"rating": review.dict().get("rating"),"id": newID}
        else:
            newObj = {"title": review.dict().get("title"),"content": review.dict().get("content"),"id": newID}

        oldReviews.append(newObj)

        newReviews = {
            "reviews": oldReviews
        }

        json.dump(newReviews,open('data.json', "w"), indent = 4)
        
        return JSONResponse(status_code=200,content="Added movie!")

    elif token == None or token == "":

        return JSONResponse(status_code=401,content="An access token is required!")

    else:

        return JSONResponse(status_code=401,content="An access token is required!")


@app.delete("/reviews/remove")
def delete_a_review(id: int, token: str = Header(convert_underscores=False)):
    if token != TOKEN:

        return JSONResponse(status_code=401,content="Wrong access token!")

    elif token == TOKEN:

        oldReviews = json.load(open('data.json'))["reviews"]
		
        for review in oldReviews:
            try:
                if review["id"] == id:
                    del oldReviews[oldReviews.index(review)]
                    newReviews = {
            "reviews": oldReviews
        }
                    for review in newReviews["reviews"]:
                        if review["id"] > id:
                            review["id"] -= 1
                        

                    json.dump(newReviews,open('data.json', "w"), indent = 4)
                    return JSONResponse(status_code=200,content="Deleted review!")
            except:
                    return JSONResponse(status_code=406,content="A movie with that review does not exit!")
    elif token == None or token == "":

        return JSONResponse(status_code=401,content="An access token is required!")

    else:

        return JSONResponse(status_code=401,content="An access token is required!")

@app.put("/reviews/update")
def update_a_review(updatedReview: newReview, id: int, token: str = Header(convert_underscores=False)):
    
    if token != TOKEN:

        return JSONResponse(status_code=401,content="Wrong access token!")

    if token == TOKEN:
        
        if updatedReview.dict().get("title") == " ":
            
            return JSONResponse(status_code=400,content="A valid title is required!")
        
        if updatedReview.dict().get("content") == " ":
            
            return JSONResponse(status_code=400,content="A valid piece of review content is required!")
        
        if not isinstance(updatedReview.dict().get("rating"), float):
            
            return JSONResponse(status_code=400,content="A valid rating is required!")
        
        reviews = json.load(open('data.json'))["reviews"]
        
        for review in reviews:
            
            if review["id"] == id:
                
                try:
                    
                    if 'rating' in updatedReview.dict():
                        
                        if updatedReview.dict().get("rating") > 5 or updatedReview.dict().get("rating") < 0:
                            
                            review.pop('rating', None)
                            
                        else:
                            
                            review["rating"] = updatedReview.dict().get("rating")
                            
                    review["title"] = updatedReview.dict().get("title")
                    
                    review["content"] = updatedReview.dict().get("content")
                    
                    newObjReviews = {
                        "reviews": reviews
                    }
                    
                    json.dump(newObjReviews,open('data.json', "w"), indent = 4)
                    
                    return JSONResponse(status_code=200,content="Updated review!" + " (" + updatedReview.dict().get("title") + ")")
                
                except:
                
                    return JSONResponse(status_code=406,content="Server error, contact api owner.")
                
    if token == None or token == "":

        return JSONResponse(status_code=400,content="An access token is required!")

    else:

        return JSONResponse(status_code=400,content="An access token is required!")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", default=25570)), log_level="info", reload=True, forwarded_allow_ips='*')
