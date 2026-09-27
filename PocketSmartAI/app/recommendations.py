import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Recommendation
from app.models import User

from app.schemas import HomeRequest
from app.schemas import JewelryRequest
from app.schemas import PartyRequest

from app.services.recommendation_service import (
    home_recommendations,
    party_recommendations,
    jewelry_recommendations,
)


router = APIRouter(
    tags=["Recommendations"]
)


def save_recommendation(
    db: Session,
    user: User,
    planner_type: str,
    request_data,
    response_data,
):
    row = Recommendation(
        user_id=user.id,
        planner_type=planner_type,
        request_json=json.dumps(
            request_data.model_dump(),
            ensure_ascii=False,
        ),
        response_json=response_data.model_dump_json(),
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return row


@router.post("/api/generate-home")
def generate_home(
    data: HomeRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = home_recommendations(data)

    row = save_recommendation(
        db=db,
        user=user,
        planner_type="home",
        request_data=data,
        response_data=result,
    )

    return {
        "id": row.id,
        "result": result.model_dump(),
    }


@router.post("/api/generate-party")
def generate_party(
    data: PartyRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = party_recommendations(data)

    row = save_recommendation(
        db=db,
        user=user,
        planner_type="party",
        request_data=data,
        response_data=result,
    )

    return {
        "id": row.id,
        "result": result.model_dump(),
    }


@router.post("/api/generate-jewelry")
async def generate_jewelry(
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form("elegant"),
    outfit_description: str = Form(""),
    metal_preference: str = Form("any"),
    outfit_image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    data = JewelryRequest(
        budget=budget,
        occasion=occasion,
        style=style,
        outfit_description=outfit_description,
        metal_preference=metal_preference,
    )

    image_bytes = None

    # Outfit image is OPTIONAL.
    # Ignore an empty upload field.
    if (
        outfit_image is not None
        and outfit_image.filename
        and outfit_image.filename.strip()
    ):
        content_type = outfit_image.content_type or ""

        if not content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Outfit upload must be an image.",
            )

        image_bytes = await outfit_image.read()

        if not image_bytes:
            image_bytes = None

        else:
            settings = get_settings()

            maximum_size = (
                settings.max_upload_mb
                * 1024
                * 1024
            )

            if len(image_bytes) > maximum_size:
                raise HTTPException(
                    status_code=413,
                    detail=(
                        f"Image must be smaller than "
                        f"{settings.max_upload_mb} MB."
                    ),
                )

    result = jewelry_recommendations(
        data=data,
        image_bytes=image_bytes,
    )

    row = save_recommendation(
        db=db,
        user=user,
        planner_type="jewelry",
        request_data=data,
        response_data=result,
    )

    return {
        "id": row.id,
        "result": result.model_dump(),
    }


@router.get("/api/history")
def history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = db.scalars(
        select(Recommendation)
        .where(
            Recommendation.user_id == user.id
        )
        .order_by(
            desc(Recommendation.created_at)
        )
    ).all()

    return [
        {
            "id": row.id,
            "planner_type": row.planner_type,
            "created_at": row.created_at.isoformat(),
            "response": json.loads(
                row.response_json
            ),
        }
        for row in rows
    ]


@router.get(
    "/api/recommendations-details/{recommendation_id}"
)
def recommendation_details(
    recommendation_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    row = db.scalar(
        select(Recommendation)
        .where(
            Recommendation.id == recommendation_id,
            Recommendation.user_id == user.id,
        )
    )

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found.",
        )

    return {
        "id": row.id,
        "planner_type": row.planner_type,
        "created_at": row.created_at.isoformat(),
        "result": json.loads(
            row.response_json
        ),
    }


@router.get("/api/session-info")
def session_info(
    user: User = Depends(get_current_user),
):
    return {
        "logged_in": True,
        "user_id": user.id,
        "email": user.email,
    }


@router.get("/api/session-data")
def session_data(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = db.scalars(
        select(Recommendation)
        .where(
            Recommendation.user_id == user.id
        )
        .order_by(
            desc(Recommendation.created_at)
        )
        .limit(5)
    ).all()

    return {
        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
        },
        "recent_recommendations": [
            row.id
            for row in rows
        ],
    }


@router.post("/api/startup")
def startup():
    return {
        "status": "ready"
    }