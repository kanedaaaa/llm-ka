from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse, JSONResponse
import httpx

app = FastAPI()

REAL_OLLAMA_URL = "http://localhost:11435"  # Your real Ollama instance

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy(full_path: str, request: Request):
    method = request.method
    url = f"{REAL_OLLAMA_URL}/{full_path}"
    headers = dict(request.headers)
    headers.pop("host", None)

    try:
        body = await request.body()

        async with httpx.AsyncClient(timeout=60) as client:
            # Stream response if it's event-stream (for things like completions)
            async with client.stream(method, url, headers=headers, content=body) as res:
                if res.headers.get("content-type", "").startswith("text/event-stream"):
                    return StreamingResponse(
                        res.aiter_raw(),
                        status_code=res.status_code,
                        headers=dict(res.headers),
                    )
                else:
                    return Response(
                        content=await res.aread(),
                        status_code=res.status_code,
                        headers=dict(res.headers),
                    )

    except httpx.RequestError as e:
        return JSONResponse(
            status_code=502,
            content={"error": f"Proxy connection error: {str(e)}"},
        )
