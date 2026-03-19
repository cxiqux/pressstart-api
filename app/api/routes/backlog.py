from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.backlog import BacklogCreate, BacklogUpdate, BacklogResponse, BacklogStatus
from app.services import backlog_service
from app.core.security import get_current_user

router = APIRouter(prefix="/backlog", tags=["Backlog"])


@router.get("", response_model=List[BacklogResponse])
def list_backlog(
    status: Optional[BacklogStatus] = Query(None),
    sort: str = Query("updated_at", pattern="^(updated_at|score|title)$"),
    page: int = Query(1, ge=1),
    current_user=Depends(get_current_user),
):
    return backlog_service.list_backlog(
        str(current_user["id"]),
        status=status.value if status else None,
        sort=sort,
        page=page,
    )


@router.post("", response_model=BacklogResponse, status_code=201)
def add_to_backlog(body: BacklogCreate, current_user=Depends(get_current_user)):
    try:
        return backlog_service.add_to_backlog(
            str(current_user["id"]),
            rawg_id=body.rawg_id,
            status=body.status.value,
            score=body.score,
            notes=body.notes,
            hours_played=body.hours_played,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{entry_id}", response_model=BacklogResponse)
def update_entry(entry_id: str, body: BacklogUpdate, current_user=Depends(get_current_user)):
    try:
        return backlog_service.update_entry(
            str(current_user["id"]),
            entry_id,
            status=body.status.value if body.status else None,
            score=body.score,
            notes=body.notes,
            hours_played=body.hours_played,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{entry_id}", status_code=204)
def delete_entry(entry_id: str, current_user=Depends(get_current_user)):
    try:
        backlog_service.delete_entry(str(current_user["id"]), entry_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
