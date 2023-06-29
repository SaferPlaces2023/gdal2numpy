import httpx
import asyncio


# create a fetch function that will download multiple urls
async def mfetch(urls):
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(*[client.get(url) for url in urls])





if __name__ == "__main__":
    responses = asyncio.run(mfetch(["https://s3.amazonaws.com/saferplaces.co/lidar-rer-100m.tif", 
                        "https://s3.amazonaws.com/saferplaces.co/lidar-rer-100m(1).tif"
                        ]))
    
    for response in responses:
        print(response.status_code)