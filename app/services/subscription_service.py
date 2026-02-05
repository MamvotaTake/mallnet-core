import datetime
import logging
from fastapi import HTTPException

from app.mikrotik.client import MikroTikClient
from app.mikrotik.hotspot import HotspotService
from app.repositories.internet_package_repository import InternetPackageRepository
from app.repositories.router_repository import RouterRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.user_repository import UserRepository


class SubscriptionService:
    def __init__(self, db):
        self.db = db
        self.subscription_repo = SubscriptionRepository(db)
        self.package_repo = InternetPackageRepository(db)
        self.user_repo = UserRepository(db)
        self.router_repo = RouterRepository(db)
        self.logger = logging.getLogger(__name__)

    # -------------------------
    # Core public method
    # -------------------------
    def create_subscription(
            self,
            mall_id: int,
            package_id: int,
            mac_address: str,
    ):
        # 1️⃣ Get or create user
        user = self.user_repo.get_or_create(
            mall_id=mall_id,
            mac_address=mac_address,
        )

        # 2️⃣ Get package
        package = self.package_repo.get_by_id(package_id)
        if not package:
            raise HTTPException(status_code=404, detail="Internet package not found")

        # 3️⃣ Deactivate existing subscription
        active = self.subscription_repo.get_active_by_user(user.id)
        if active:
            self.deactivate_subscription(active)

        # 4️⃣ Create new subscription
        end_date = datetime.datetime.utcnow() + datetime.timedelta(
            days=package.duration_days
        )

        subscription = self.subscription_repo.create(
            user_id=user.id,
            package_id=package.id,
            end_date=end_date,
        )

        # 5️⃣ Enable internet on MikroTik
        router = self._get_router_for_user(user)
        self._enable_hotspot_user(
            router=router,
            mac_address=user.mac_address,
            profile=package.mikrotik_profile,
        )

        return subscription

    def deactivate_subscription(self, subscription):
        self.subscription_repo.deactivate(subscription)
        user = self.user_repo.get_by_id(subscription.user_id)
        if not user or not user.mac_address:
            return
        router = self._get_router_for_user(user)
        self._disable_hotspot_user(router, user.mac_address)

    def expire_subscriptions(self):
        expired = self.subscription_repo.get_expired_active()
        for subscription in expired:
            self.deactivate_subscription(subscription)
        return len(expired)

    # -------------------------
    # Router resolution
    # -------------------------
    def _get_router_for_user(self, user):
        router = self.router_repo.get_by_mall(user.mall_id)
        if not router:
            raise HTTPException(status_code=404, detail="No router configured for mall")
        return router

    # -------------------------
    # MikroTik operations
    # -------------------------
    def _enable_hotspot_user(self, router, mac_address: str, profile: str):
        try:
            mikrotik = MikroTikClient(
                host=router.host,
                username=router.username,
                password=router.password,
                port=router.api_port,
            )
            api = mikrotik.connect()

            hotspot = HotspotService(api)
            hotspot.create_mac_user(
                mac_address=mac_address,
                profile=profile,
            )
        except Exception as exc:
            self.logger.exception("Failed to enable hotspot user for %s", mac_address)
            raise HTTPException(
                status_code=502,
                detail="Failed to enable hotspot user",
            ) from exc

    def _disable_hotspot_user(self, router, mac_address: str):
        try:
            mikrotik = MikroTikClient(
                host=router.host,
                username=router.username,
                password=router.password,
                port=router.api_port,
            )
            api = mikrotik.connect()

            hotspot = HotspotService(api)
            hotspot.disable_mac_user(mac_address)
        except Exception:
            self.logger.exception("Failed to disable hotspot user for %s", mac_address)
