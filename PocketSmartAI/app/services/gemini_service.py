from app.schemas import BudgetAllocation
from app.schemas import HomeRequest
from app.schemas import JewelryRequest
from app.schemas import PartyRequest
from app.schemas import RecommendationItem
from app.schemas import RecommendationResponse

from app.services.catalog_service import choose_platform
from app.services.catalog_service import search_url


def create_item(
    title: str,
    category: str,
    price: float,
    reason: str,
    planner: str,
) -> RecommendationItem:

    platform = choose_platform(
        category,
        planner,
    )

    return RecommendationItem(
        title=title,
        category=category,
        platform=platform,
        estimated_price=round(price, 2),
        reason=reason,
        url=search_url(
            platform,
            title,
        ),
        confidence=0.72,
    )


def fallback_home(
    data: HomeRequest,
) -> RecommendationResponse:

    weights = {
        "lighting": 0.18,
        "furniture": 0.38,
        "decor": 0.18,
        "ceiling fan": 0.12,
        "dining table": 0.14,
    }

    recommendations = []
    allocation = []

    for item in data.items:

        category_key = item.category.lower()

        percentage = weights.get(
            category_key,
            0.15,
        )

        amount = data.budget * percentage

        allocation.append(
            BudgetAllocation(
                category=item.category,
                amount=round(
                    amount,
                    2,
                ),
                percentage=round(
                    percentage * 100,
                    2,
                ),
            )
        )

        recommendations.append(
            create_item(
                title=(
                    f"{data.style.title()} "
                    f"{item.category}"
                ),
                category=item.category,
                price=amount,
                reason=(
                    f"Budget-oriented "
                    f"{data.style} option for "
                    f"a {data.room_type}. "
                    f"Quantity requested: "
                    f"{item.quantity}."
                ),
                planner="home",
            )
        )

    total = sum(
        item.estimated_price
        for item in recommendations
    )

    return RecommendationResponse(
        planner_type="home",
        budget=data.budget,
        total_estimated=round(
            total,
            2,
        ),
        within_budget=(
            total <= data.budget
        ),
        summary=(
            f"A practical "
            f"{data.style} "
            f"{data.room_type} plan "
            f"focused on staying near "
            f"the ₹{data.budget:,.0f} budget."
        ),
        budget_allocation=allocation,
        recommendations=recommendations,
        tips=[
            "Compare dimensions and warranty before purchasing.",
            "Treat listed prices as estimates until the platform confirms them.",
        ],
    )


def fallback_party(
    data: PartyRequest,
) -> RecommendationResponse:

    splits = [
        ("Food", 0.50),
        ("Decoration", 0.20),
        ("Venue", 0.20),
        ("Entertainment", 0.10),
    ]

    recommendations = []
    allocation = []

    for category, percentage in splits:

        amount = (
            data.budget * percentage
        )

        allocation.append(
            BudgetAllocation(
                category=category,
                amount=round(
                    amount,
                    2,
                ),
                percentage=percentage * 100,
            )
        )

        if category == "Food":
            platform = "Zomato"
        elif category == "Venue":
            platform = "OYO"
        else:
            platform = "Amazon"

        title = (
            f"{data.event_type.title()} "
            f"{category.lower()} package "
            f"for {data.guests} guests"
        )

        recommendations.append(
            RecommendationItem(
                title=title,
                category=category,
                platform=platform,
                estimated_price=round(
                    amount,
                    2,
                ),
                reason=(
                    f"Allocated "
                    f"{percentage:.0%} "
                    f"of the budget for a "
                    f"{data.event_type} "
                    f"with {data.guests} guests."
                ),
                url=search_url(
                    platform,
                    title,
                ),
                confidence=0.70,
            )
        )

    return RecommendationResponse(
        planner_type="party",
        budget=data.budget,
        total_estimated=data.budget,
        within_budget=True,
        summary=(
            f"A balanced starter budget "
            f"for a {data.event_type} "
            f"for {data.guests} guests."
        ),
        budget_allocation=allocation,
        recommendations=recommendations,
        tips=[
            "Get final per-person catering quotes before booking.",
            "Keep a small contingency if your venue has variable fees.",
        ],
    )


def fallback_jewelry(
    data: JewelryRequest,
) -> RecommendationResponse:

    allocation = [

        BudgetAllocation(
            category="Primary jewelry",
            amount=round(
                data.budget * 0.65,
                2,
            ),
            percentage=65,
        ),

        BudgetAllocation(
            category="Secondary piece",
            amount=round(
                data.budget * 0.25,
                2,
            ),
            percentage=25,
        ),

        BudgetAllocation(
            category="Contingency",
            amount=round(
                data.budget * 0.10,
                2,
            ),
            percentage=10,
        ),
    ]

    recommendations = [

        create_item(
            title=(
                f"{data.style.title()} "
                f"necklace for {data.occasion}"
            ),
            category="necklace",
            price=data.budget * 0.65,
            reason=(
                "A versatile focal piece "
                "selected around the "
                "requested occasion and style."
            ),
            planner="jewelry",
        ),

        create_item(
            title=(
                f"Matching "
                f"{data.style.lower()} earrings"
            ),
            category="earrings",
            price=data.budget * 0.25,
            reason=(
                "A coordinating secondary "
                "piece that keeps the "
                "overall plan within budget."
            ),
            planner="jewelry",
        ),
    ]

    total = sum(
        item.estimated_price
        for item in recommendations
    )

    return RecommendationResponse(
        planner_type="jewelry",
        budget=data.budget,
        total_estimated=round(
            total,
            2,
        ),
        within_budget=(
            total <= data.budget
        ),
        summary=(
            f"Jewelry ideas for "
            f"{data.occasion}, emphasizing "
            f"a {data.style} look and your "
            f"{data.metal_preference} "
            f"metal preference."
        ),
        budget_allocation=allocation,
        recommendations=recommendations,
        tips=[
            "Use the outfit image as a broad style/color reference.",
            "Verify material, size, return policy and final price on the seller page.",
        ],
    )