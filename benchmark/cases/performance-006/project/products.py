from fastapi import HTTPException


class ProductService:
    def __init__(self, repository, cache):
        self.repository = repository
        self.cache = cache

    async def get_product(self, product_id: int):
        cached = self.cache.get(product_id)
        if cached is not None:
            return cached
        product = await self.repository.get(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Not found")
        self.cache.set(product_id, product, ttl=300)
        return product

    async def update_product(self, product_id: int, changes: dict):
        product = await self.repository.update(product_id, changes)
        if product is None:
            raise HTTPException(status_code=404, detail="Not found")
        return product
