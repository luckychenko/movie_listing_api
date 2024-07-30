import time

from fastapi import Request

from logger import logger

async def movie_middleware(request: Request, callnext):
    logger.info("Requesting "+str(request.base_url))
    start_time = time.time()
    response = request
    try:
        response = await callnext(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"Request ended. process_time: {process_time}")
    except Exception as e:
        print('=============', str(e))
        logger.error("An error occurred while processing")
    return response


