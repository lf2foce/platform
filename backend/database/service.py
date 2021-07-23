import logging
import json
from typing import List
from sqlalchemy.orm import Session
from .core import get_db
from fastapi import Depends, Query

# Use Query as the default value
# read_items(q: Optional[str] = Query(None, max_length=50))

def common_parameters(
    db: Session = Depends(get_db),
    page: int = 1,
    items_per_page: int = Query(5, alias="itemsPerPage"),
    query_str: str = Query(None, alias="q"),
    filter_spec: str = Query([], alias="filter"),
    sort_by: List[str] = Query([], alias="sortBy[]"),
    descending: List[bool] = Query([], alias="descending[]"),
    #current_user: DispatchUser = Depends(get_current_user),
    #role: UserRoles = Depends(get_current_role),
):
    if filter_spec:
        filter_spec = json.loads(filter_spec)

    return {
        "db": db,
        "page": page,
        "items_per_page": items_per_page,
        "query_str": query_str, 
        "sort_by": sort_by,
        "descending": descending,
        #"filter_spec": filter_spec,
        #"current_user": current_user,
        #"role": role,
    }