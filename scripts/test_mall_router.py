from app.database.session import SessionLocal
from app.repositories.mall_repository import MallRepository
from app.repositories.router_repository import RouterRepository

db = SessionLocal()

mall_repo = MallRepository(db)
router_repo = RouterRepository(db)

mall = mall_repo.create("Main Mall")
print("Mall:", mall.id, mall.name)

router = router_repo.create(
    mall_id=mall.id,
    name="Main Mall Router",
    host="192.168.88.1",
    username="admin",
    password="31R-cx70_90",
)
print("Router:", router.id, router.host)
