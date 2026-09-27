def register_and_login(client):

    register_response = client.post(

        "/api/auth/register",

        json={

            "email":
                "test@example.com",

            "full_name":
                "Test User",

            "password":
                "password123",
        },
    )


    assert register_response.status_code in {
        201,
        409,
    }


    login_response = client.post(

        "/api/auth/login",

        json={

            "email":
                "test@example.com",

            "password":
                "password123",
        },
    )


    assert (
        login_response.status_code
        == 200
    )


def test_health(client):

    response =
        client.get(
            "/api/health"
        )

    assert (
        response.status_code
        == 200
    )

    assert (
        response.json()["status"]
        == "ok"
    )


def test_home_flow(client):

    register_and_login(client)


    response = client.post(

        "/api/generate-home",

        json={

            "budget":
                100000,

            "room_type":
                "Living Room",

            "style":
                "Modern",

            "city":
                "Chennai",

            "items": [

                {
                    "category":
                        "Furniture",

                    "quantity":
                        1,
                },

                {
                    "category":
                        "Lighting",

                    "quantity":
                        2,
                },

            ],
        },
    )


    assert (
        response.status_code
        == 200
    )


    data = response.json()


    assert data["id"]


    assert (
        data["result"]["planner_type"]
        == "home"
    )


def test_party_flow(client):

    register_and_login(client)


    response = client.post(

        "/api/generate-party",

        json={

            "budget":
                50000,

            "guests":
                30,

            "event_type":
                "Birthday",

            "venue":
                "Cafe",

            "city":
                "Chennai",

            "food_preference":
                "Vegetarian",
        },
    )


    assert (
        response.status_code
        == 200
    )


    assert (
        response.json()
        ["result"]
        ["within_budget"]
        is True
    )


def test_history(client):

    register_and_login(client)


    response =
        client.get(
            "/api/history"
        )


    assert (
        response.status_code
        == 200
    )


    assert isinstance(
        response.json(),
        list,
    )