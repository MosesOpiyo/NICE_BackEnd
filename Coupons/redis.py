import redis
from .models import Coupon

def coupons_view():
    redis_cache = redis.StrictRedis(host='localhost', port=6379, db=0)
    data = redis_cache.get("Coupons")
    
    if not data:
        # Retrieve large data from database or any source
        coupons = Coupon.objects.all()
        # Store the data in Redis
        redis_cache.set("Coupons", coupons)
        data = redis_cache.get("Coupons")

    return data