from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from backend.database import get_db
from backend.schemas import ContactRequest, EnquiryResponse
from backend.routers.auth import get_current_user, get_current_user_optional

router = APIRouter(prefix="/api/contact", tags=["contact"])


@router.post("/{listing_id}")
async def contact_landlord(
    listing_id: int,
    data: ContactRequest,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    results = await db.select("listings", filters={"id": f"eq.{listing_id}"})
    if not results:
        raise HTTPException(status_code=404, detail="Listing not found")

    listing = results[0]

    await db.insert("enquiries", {
        "listing_id": listing_id,
        "student_name": data.student_name,
        "student_phone": data.student_phone,
        "message": data.message,
    })

    return {
        "success": True,
        "message": f"Your enquiry has been sent to {listing['landlord_name']}. They will contact you at {data.student_phone}.",
        "landlord_name": listing["landlord_name"],
        "landlord_phone": listing["landlord_phone"],
    }


@router.get("/landlord-enquiries", response_model=list[EnquiryResponse])
async def get_landlord_enquiries(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    if current_user["role"] != "landlord":
        raise HTTPException(status_code=403, detail="Only landlords can view enquiries")

    listings = await db.select("listings", filters={"owner_id": f"eq.{current_user['id']}"})
    if not listings:
        return []

    listing_ids = [str(l["id"]) for l in listings]
    listing_map = {l["id"]: l["title"] for l in listings}

    enquiries = []
    for lid in listing_ids:
        batch = await db.select("enquiries", filters={"listing_id": f"eq.{lid}"}, order="created_at.desc")
        enquiries.extend(batch)

    enquiries.sort(key=lambda e: e["created_at"], reverse=True)

    result = []
    for e in enquiries:
        result.append({
            "id": e["id"],
            "listing_id": e["listing_id"],
            "listing_title": listing_map.get(e["listing_id"], ""),
            "student_name": e["student_name"],
            "student_phone": e["student_phone"],
            "message": e.get("message", ""),
            "created_at": e["created_at"],
        })
    return result
