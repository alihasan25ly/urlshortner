import uvicorn
if __name__ == "__main__":
    uvicorn.run("index:app", host="0.0.0.0", port=3000, reload=True)