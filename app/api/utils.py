import httpx
from fastapi import HTTPException


async def external_api_get(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            return response

        except httpx.RequestError as exc:
            # network error
            raise HTTPException(
                status_code=400, detail=f"Error response from external API: {exc}"
            )
        except httpx.HTTPStatusError as exc:
            # 4xx 5xx status code
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error response from external API: {exc.response.text}",
            )
