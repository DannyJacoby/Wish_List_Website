document.getElementById("account-btn").addEventListener("click", (event) => {
    let form = new FormData(document.forms["account-form"]);

    for (let pair of form.entries()) {
        if (pair[1].length === 0) {
            alert(pair[0] + " can't be empty!");

            event.preventDefault();
            return false;
        }
    }

    const re = new RegExp('^(?=.*?[\\w])(?=.*?[\\W]).{6,}$');
    let pass = form.get("pass");

    if (!pass.match(re)) {
        alert("Password must be at least 6 characters long, alphanumeric with at least one special character.");

        event.preventDefault();
        return false;
    }

    return true;
});