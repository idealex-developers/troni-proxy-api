from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

TARGET_BASE_URL = "https://google.com/"  # Change this to your target base URL

@app.get("/docs")
async def proxy_docs(request: Request):
    return await proxy_request("docs", request)


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_request(full_path: str, request: Request):
    target_url = f"{TARGET_BASE_URL}/{full_path}"
    
    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=request.query_params
        )
    
    # return {"data": response.json(), "headers": response.headers}
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type", "text/plain")  # Default to text/plain
    )