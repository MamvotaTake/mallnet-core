from app.database.session import SessionLocal
from app.repositories.internet_package_repository import InternetPackageRepository

db = SessionLocal()
repo = InternetPackageRepository(db)

# Create packages
repo.create("Daily", 1.0, 1, "daily_1usd")
repo.create("Weekly", 3.0, 7, "weekly_3usd")
repo.create("Monthly", 10.0, 30, "monthly_10usd")

# Fetch all
packages = repo.get_all()
for p in packages:
    print(p)
