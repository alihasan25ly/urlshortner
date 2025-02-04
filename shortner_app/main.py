import uvicorn
if __name__ == "__main__":
    uvicorn.run("shortner_app.index:app", host="0.0.0.0", port=8000, reload=True)