/* Make a request to the API (since PUT and DELETE can't
 * sent in a form).
 * id - the id of the resource for the request (user_id or item_id)
 * route - route to send the request to
 * method - HTTP method to use (PUT or DELETE)
 * target_id - id of the html element to target with the response
 *             message
 */
let make_req = async (id, route, method, target_id) => {
    route += id ? id.toString() : "";

    let json = await fetch(route, {method: method}).then(response => response.json());

    if (json.redirect) {
        window.location.href = json.redirect;
    }

    let target = document.getElementById(target_id);
    target.innerText = json["message"];
}