async function api(url, options = {}) {

    options.headers =
        options.headers || {};


    if (
        options.body &&
        !(options.body instanceof FormData)
    ) {

        options.headers[
            "Content-Type"
        ] = "application/json";

    }


    return fetch(
        url,
        options
    );
}


async function errorText(response) {

    try {

        const data =
            await response.json();


        if (
            Array.isArray(
                data.detail
            )
        ) {

            return data.detail
                .map(
                    error => error.msg
                )
                .join(", ");
        }


        return (
            data.detail ||
            "Something went wrong."
        );

    } catch {

        return "Something went wrong.";
    }
}


function showMessage(message) {

    const element =
        document.getElementById(
            "form-message"
        );


    if (!element) {
        return;
    }


    element.textContent =
        message;


    element.className =
        "message error";
}


async function logout() {

    await api(
        "/api/auth/logout",
        {
            method: "POST"
        }
    );


    window.location.href =
        "/";
}