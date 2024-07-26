async function sendData(url, body) {
	const response = await fetch(url, {
		method: 'POST',
		headers: {
			'X-CSRFToken': getCookie('csrftoken'),
			// 'Content-Type': 'application/json'
		},
		body: body
	});
    if (!response.ok) {
        const message = `An error has occured: ${response.status}`;
        alert('error')
    }
	return response
}
function convert_fd_to_json(form_data) {
	var object = {};
	form_data.forEach((value, key) => {
		if(!Reflect.has(object, key)){
			object[key] = value;
			return;
		}
		if(!Array.isArray(object[key])){
			object[key] = [object[key]];
		}
		object[key].push(value);
	});
	return object
}
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
