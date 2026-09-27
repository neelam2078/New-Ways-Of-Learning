from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

from fastapi.templating import Jinja2Templates

from app.dependencies import get_current_user
from app.models import User


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/")
def index(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": None,
        },
    )


@router.get("/register")
def register_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "user": None,
        },
    )


@router.get("/login")
def login_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "user": None,
        },
    )


@router.get("/dashboard")
def dashboard(
    request: Request,
    user: User = Depends(
        get_current_user
    ),
):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
        },
    )


@router.get("/history")
def history_page(
    request: Request,
    user: User = Depends(
        get_current_user
    ),
):
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "user": user,
        },
    )


@router.get("/planner/home")
def home_page(
    request: Request,
    user: User = Depends(
        get_current_user
    ),
):
    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context={
            "user": user,
        },
    )


@router.get("/planner/party")
def party_page(
    request: Request,
    user: User = Depends(
        get_current_user
    ),
):
    return templates.TemplateResponse(
        request=request,
        name="party_planner.html",
        context={
            "user": user,
        },
    )


@router.get("/planner/jewelry")
def jewelry_page(
    request: Request,
    user: User = Depends(
        get_current_user
    ),
):
    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html",
        context={
            "user": user,
        },
    )


@router.get(
    "/recommendations/{recommendation_id}"
)
def recommendation_page(
    request: Request,
    recommendation_id: int,
    user: User = Depends(
        get_current_user
    ),
):
    return templates.TemplateResponse(
        request=request,
        name="recommendations.html",
        context={
            "user": user,
            "recommendation_id": recommendation_id,
        },
    )
