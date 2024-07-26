function handle_errors_on_form(form_name, errors, modal_type="add-modal__label") {
    $(".add-modal__error").remove();
    for (const [key, value] of Object.entries(errors)) {
        let inp = $(`form[name=${form_name}] :input[name="${key}"]`)[0]
        if (!inp) {
            inp = $(`form[name=${form_name}] :input[name=${key}_hidden]`)[0]
        }
        if (value[0]) {
            inp.closest("." + modal_type).insertAdjacentHTML("beforeend", `<span class="add-modal__error">${value}</span>`)
        }
        else {
            inp.closest("." + modal_type).insertAdjacentHTML("beforeend", `<span class="add-modal__error">Check input value</span>`)
        }
    }
}

$('form[name=form_new_campaign]').on('submit', async function (e) {

    e.preventDefault();
    let fd = new FormData(form_new_campaign)

    fd.append("geo", _modalGeoSelect.value)
    fd.append("source", _modalUserSourceSelect.value)
    fd.append("type", _modalTypeSelect.value)
    fd.append("format", _formatUserModalSelect.value)
    let object = convert_fd_to_json(fd)
	let response = await sendData('/campaigns/create/', fd)
    let data = await response.json();
    if (data.message === "ok") {
        location.reload()
    }
    else {
        handle_errors_on_form("form_new_campaign", data.errors)
    }
});
$('form[name=form_new_invoice]').on('submit', async function (e) {
    e.preventDefault();
    let fd = new FormData(form_new_invoice)
    let form_url = document.getElementsByName("form_new_invoice")[0].action
    fd.append("type", _userTypeInvoceSelect.value)
    let object = convert_fd_to_json(fd)
	let response = await sendData(form_url, fd)
    let data = await response.json();
    if (data.message === "ok") {
        location.reload()
    }
    else {
        handle_errors_on_form("form_new_invoice", data.errors)
    }
})
$('form[name=form_edit_campaign]').on('submit', async function (e) {
    e.preventDefault();
    let fd = new FormData(form_edit_campaign)
    let campaign_id = document.getElementById("edit_id").value
    let object = convert_fd_to_json(fd)
	let response = await sendData(`/campaigns/${campaign_id}/update`, fd)
    let data = await response.json();
    if (data.message === "ok") {
        location.reload()
    }
    else {
        handle_errors_on_form("form_edit_campaign", data.errors, modal_type="edit-modal__label")
    }
})