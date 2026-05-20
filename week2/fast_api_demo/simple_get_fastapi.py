from fastapi import FastAPI

# this is instance of FastAPI class
app = FastAPI()

#defining a route for my api endpoint, / is root endpoint
# defining route via a decorator, @app.get() 
# means this route will respond to GET requests

@app.get("/")
def hello():
    return {"message": "Hello World"}

@app.get("/about")
def about():
    return {"message": "This is a FastAPI demo application"}
# we take help of uvicorn to run our app, 
# uvicorn is an ASGI server implementation, 
#  --it is used to run FastAPI applications