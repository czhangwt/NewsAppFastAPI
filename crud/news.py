from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.news import Category, News
from sqlalchemy import func

# get categories from database
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_news_list(
    db: AsyncSession, 
    category_id: int, 
    skip: int = 0, 
    limit: int = 10
    ):
    # select news by category id
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# check news count by category id
async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count()).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one() #only one value, else raise error
    
# get news detail by id
async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# increate news views by id
async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # after increase views, check if the database update is successful and return True
    return result.rowcount > 0


# get related news by category id and news id
async def get_related_news(db: AsyncSession, category_id: int, news_id: int):
    # recommended news by category id and top views/publish time
    stmt = select(News).where(
        News.category_id == category_id
        ).where(
            News.id != news_id
        ).order_by(
            News.views.desc(),
            News.publish_time.desc()
        ).limit(5)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    # get core information of related news 
    return [
        {"id": news.id,
        "title": news.title, 
        "image": news.image, 
        "views": news.views, 
        "publish_time": news.publish_time
        } 
    for news in related_news
    ]
    

