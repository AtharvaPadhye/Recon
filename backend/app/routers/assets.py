from fastapi import APIRouter, HTTPException
from ..models import Asset
from .. import database

router = APIRouter(prefix="/v1/assets", tags=["assets"])


@router.post("", response_model=Asset)
def create_asset(asset: Asset):
    return database.add_asset(asset)


@router.get("", response_model=list[Asset])
def list_assets():
    return database.list_assets()


@router.get("/{asset_id}", response_model=Asset)
def read_asset(asset_id: str):
    asset = database.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="asset not found")
    return asset


@router.put("/{asset_id}", response_model=Asset)
def update_asset(asset_id: str, asset_update: Asset):
    if not database.get_asset(asset_id):
        raise HTTPException(status_code=404, detail="asset not found")
    asset_update.id = asset_id
    return database.update_asset(asset_id, asset_update)


@router.delete("/{asset_id}")
def delete_asset(asset_id: str):
    if not database.get_asset(asset_id):
        raise HTTPException(status_code=404, detail="asset not found")
    database.delete_asset(asset_id)
    return {"detail": "deleted"}


@router.put("/{asset_id}/location", response_model=Asset)
def update_asset_location(asset_id: str, loc: dict):
    asset = database.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="asset not found")
    asset.location = loc
    return database.update_asset(asset_id, asset)
