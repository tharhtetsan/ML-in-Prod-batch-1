from fastapi  import FastAPI,Request, Response
from typing import Callable
from uuid import uuid1
import time
import torch
from datetime import datetime
import uvicorn

app = FastAPI()





@app.middleware("http")
async def monitor_service(req: Request, call_next : Callable ) -> Response:
    start_time = time.time()

    response : Response  =  await call_next(req)
    response_time = round(start_time - time.time(),4) #duration to 4 decimal places.
    request_id = uuid1().hex
    response.headers["X-Process-Time"] = str(response_time)
    response.headers["X-API-Request-ID"] = request_id 

    print("Middleware is working now ....")

    with open("usage.log", "a") as file: 
        file.write(
            f"Request ID: {request_id}"
            f"\nDatetime: {datetime.utcnow().isoformat()}"
            f"\nEndpoint triggered: {req.url}"
            f"\nClient IP Address: {req.client.host}"
            f"\nResponse time: {response_time} seconds"
            f"\nStatus Code: {response.status_code}"
            f"\nSuccessful: {response.status_code < 400}\n\n"
        )
    return response
    


@app.get("/check_gpu")
async def check_gpu():
    device_name  = None
    if torch.backends.mps.is_available():
        device_name = "mps"
    else:
        device_name = "cpu"
        

    mps_device = torch.device(device_name)
    x = torch.ones(1, device=mps_device)
    print("GPU Type: ", mps_device)
    return {"device": device_name}


if __name__ == "__main__":
    uvicorn.run("middleware_logging:app", port=8000, reload=True)