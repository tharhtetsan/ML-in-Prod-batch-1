from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None

    model_config  = {
        "json_schema_extra" : {
            "examples" : [
                {
                    "name" : "Foo",
                    "description" : "A very nice Item",
                    "price" : 35.4,
                    "tax" : 3.2
                }
            ]
        }
    }

@app.put("/items/{item_id}")
async def update_item(item_id : int, item : Item):
    print("item : ",item)
    results = {"item_id" : item_id}

    return results



if __name__ == "__main__":
    uvicorn.run("test_pydantic:app", port=8000, reload=True)