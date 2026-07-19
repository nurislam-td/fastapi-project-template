from typing import Annotated

from fastapi.params import Query
from pydantic import BaseModel


class PaginationParamsSchema(BaseModel):
    limit: Annotated[int, Query(...)]
    offset: Annotated[int, Query(...)]


PaginationParamsSchemaType = Annotated[PaginationParamsSchema, Query(...)]
