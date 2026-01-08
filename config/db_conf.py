from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "mysql+aiomysql://root:1992Carl%40%2A@127.0.0.1:3306/news_app?charset=utf8"

engine = create_async_engine(DATABASE_URL)

async_engine = create_async_engine(
    DATABASE_URL, 
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    echo=True
)

# create async session
AsyncSessionLocal = async_sessionmaker(
    bind = async_engine, #bind the engine to the session
    class_ = AsyncSession,
    expire_on_commit = False # do not expire the session on commit
)


# create dependency function for database session then inject it into the path operation function
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session # yield the session to the path operation function
            await session.commit() # commit the transaction
        except Exception:
            await session.rollback() # rollback the transaction
            raise
        finally:
            await session.close() # close the session
