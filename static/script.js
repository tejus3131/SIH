function validateAndSubmitForm(api) {
    const form = document.getElementById("authorizationForm");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        const formData = new FormData(form);
        try {
            const response = await fetch(api, {
                method: "POST",
                body: formData,
            });
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const data = await response.json();
            window.location.href = data.redirect;
        } catch (error) {
            console.error("Error:", error);
            const responseElement = document.getElementById("response");
            responseElement.textContent = "An error occurred while authorizing.";
        }
    });
}