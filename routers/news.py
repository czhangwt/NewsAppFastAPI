from fastapi import APIRouter, Depends, Query
from crud import news
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

# create router for news endpoints
# prefix: /api/news
# tags: news
router = APIRouter(prefix="/api/news", tags=["news"])


# Process of implementing API endpoints
# 1. Modulize the endpoints into different files (APIRouter)
# 2. Define the request parameters (Query, Path, Body)
# 3. Define the response parameters (Response Model)
# 4. Implement the endpoint

# get news categories
@router.get("/categories")
async def get_categories( db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100,):
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "get categories success",
        "data": categories
    }

# get news list by category
@router.get("/list")
async def get_news_list(
        db: AsyncSession = Depends(get_db), 
        category_id: int = Query(..., alias="categoryId"), 
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", le=100),
    ):

    offset = (page - 1) * page_size

    news_list = await news.get_news_list(db, category_id, offset, page_size)

    total = await news.get_news_count(db, category_id)

    # check if has more news: skipped + page_size < total
    has_more = total > offset + page_size

    return{
        "code": 200,
        "message": "get news list success",
        "data": {
            "list": news_list,
            "total": total, 
            "hasMore": has_more
        }
    }


# get news detail by id
@router.get("/detail")
async def get_news_detail(
    db: AsyncSession = Depends(get_db), 
    news_id: int = Query(..., alias="newsId")):
    # get news detail by id -> news view + 1 -> get related news

    news_detail = await news.get_news_detail(db, news_id)

    if news_detail is None:
        raise HTTPException(status_code=404, detail="News not found")

    views_result = await news.increase_news_views(db, news_id)

    if not views_result:
        raise HTTPException(status_code=500, detail="Failed to increase news views")

    related_news = await news.get_related_news(db, news_detail.category_id, news_id)
    return {
        "code": 200,
        "message": "get news detail success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
        }
    }

# get related news by category id
@router.get("/related")
async def get_related_news(
    db: AsyncSession = Depends(get_db), 
    category_id: int = Query(..., alias="categoryId"), 
    news_id: int = Query(..., alias="newsId")):
    # get related news by category id and news id
    related_news = await news.get_related_news(db, category_id, news_id)
    return {
        "code": 200,
        "message": "get related news success",
        "data": related_news
    }
