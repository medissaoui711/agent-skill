from fastapi import HTTPException

MAX_IDS = 200
BATCH_SIZE = 25


class BatchService:
    def __init__(self, repository):
        self.repository = repository

    async def fetch_many(self, ids: list[int]):
        if len(ids) > MAX_IDS:
            raise HTTPException(status_code=422, detail="Too many identifiers")

        results_by_id = {}
        for start in range(0, len(ids), BATCH_SIZE):
            batch = ids[start : start + BATCH_SIZE]
            rows = await self.repository.fetch_by_ids(batch)
            results_by_id.update({row.id: row for row in rows})

        return [results_by_id[id_] for id_ in ids if id_ in results_by_id]
