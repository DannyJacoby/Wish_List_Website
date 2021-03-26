/* Make a request to the API (since PUT and DELETE can't
 * sent in a form).
 * route - route to send the request to
 * method - HTTP method to use (PUT or DELETE)
 * target_id - id of the html element to target with the response
 *             message
 * data - the json data to pass to PUT requests
 */
let make_req = async (route, method, target_id, data) => {
    let init =  {method: method};

    if (method === "PUT") {
        init.headers = {'Content-Type': 'application/json'};
        init.body = JSON.stringify(data);
    }

    let json = await fetch(route, init)
        .then(response => response.json())
        .catch(e => alert(e));

    let target = document.getElementById(target_id);
    target.innerText = json["message"];

    setTimeout(() => {
        json.redirect ? window.location.href = json.redirect : window.location.reload();
    }, 1500);
}