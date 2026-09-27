from app.schemas import HomeRequest
from app.schemas import JewelryRequest
from app.schemas import PartyRequest

from app.services.recommendation_service import (
    fallback_home,
    fallback_jewelry,
    fallback_party,
)


def test_home_fallback():

    result = fallback_home(

        HomeRequest(

            budget=10000,

            room_type="Bedroom",

            style="minimal",

            items=[
                {
                    "category":
                        "Lighting",

                    "quantity":
                        1,
                }
            ],
        )
    )


    assert (
        result.planner_type
        == "home"
    )


    assert (
        result.total_estimated
        <= result.budget
    )


def test_party_fallback():

    result = fallback_party(

        PartyRequest(

            budget=20000,

            guests=20,

            event_type="Birthday",
        )
    )


    assert (
        result.total_estimated
        == 20000
    )


def test_jewelry_fallback():

    result = fallback_jewelry(

        JewelryRequest(

            budget=5000,

            occasion="Wedding",

            style="Elegant",
        )
    )


    assert (
        result.total_estimated
        <= result.budget
    )