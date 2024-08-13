import redis
from .models import CoffeeProducts,ProcessedProducts

def large_coffee_products_view(request):
    redis_cache = redis.StrictRedis(host='localhost', port=6379, db=0)
    data = redis_cache.get(f"{request.user.username}'s coffee products")
    
    if not data:
        # Retrieve large data from database or any source
        coffee_products = CoffeeProducts.objects.select_related('producer').filter(producer=request.user)
        # Store the data in Redis
        redis_cache.set(f"{request.user.username}'s coffee products", coffee_products)
        data = redis_cache.get(f"{request.user.username}'s coffee products")

    return data

def large_processed_products_view():
    redis_cache = redis.StrictRedis(host='localhost', port=6379, db=0)
    data = redis_cache.get("processed coffee products")
    print(data)
    
    if not data:
        # Retrieve large data from database or any source
        processed_products = ProcessedProducts.objects.prefetch_related('rating').select_related('product').all()
        print(processed_products)
        # Store the data in Redis
        redis_cache.set("processed coffee products", processed_products)
        data = redis_cache.get("processed coffee products")

    return data