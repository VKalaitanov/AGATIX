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

$('form[name=form_new_source]').on('submit', async function (e) {
    console.log("aga")
    e.preventDefault();
    let fd = new FormData(form_new_source)
    let object = convert_fd_to_json(fd)
    console.log(object)
    console.log(fd)
	let response = await sendData('/admin/sources/create', fd)
    let data = await response.json();
    if (data.message === "ok") {
        location.reload()
    }
    else {
        handle_errors_on_form("form_new_source", data.errors)
    }
})

$('form[name=form_new_price]').on('submit', async function (e) {
    e.preventDefault();
    let fd = new FormData(form_new_price)
    let object = convert_fd_to_json(fd)
    let form_url = document.getElementsByName("form_new_price")[0].action

    fd.append("geo", _modalGeoSelect.value)
    fd.append("source", _modalSourceSelect.value)
    fd.append("type", _modalTypeSelect.value)
    fd.append("format", _modalFormatSelect.value)
	let response = await sendData(form_url, fd)
    let data = await response.json();
    if (data.message === "ok") {
        location.reload()
    }
    else {
        handle_errors_on_form("form_new_price", data.errors)
    }
})
$('form[name=form_account_edit]').on('submit', async function (e) {
    e.preventDefault();
    let account_id = document.getElementById("edit_id").value
    let fd = new FormData(form_account_edit)
    let object = convert_fd_to_json(fd)
    let form_url = "/"
    console.log(object)
    fd.append("manager", _managerModalfulSelect.value)
	let response = await sendData("/admin/accounts/" + account_id, fd)
    let data = await response.json();
    if (data.message === "ok") {
        location.reload()
    }
    else {
        handle_errors_on_form("form_account_edit", data.errors)
    }
})
$('form[name=form_new_campaign_admin]').on('submit', async function (e) {
    e.preventDefault();
    let fd = new FormData(form_new_campaign_admin)
    let object = convert_fd_to_json(fd)
    let form_url = "/"
    fd.append("type", _modalTypeSelect.value)
    fd.append("format", _modalFormatSelect.value)
    fd.append("geo", _modalGeoSelect.value)
    fd.append("user", _adminModalCampaignSelect.value)
    fd.append("source", _modalSourceSelect.value)
	let response = await sendData("/admin/campaigns/", fd)
    let data = await response.json();
    if (data.message === "ok") {
        location.reload()
    }
    else {
        handle_errors_on_form("form_new_campaign_admin", data.errors)
    }
})
$('form[name=form_edit_source]').on('submit', async function (e) {
    e.preventDefault();
    let source_id = document.getElementById("edit_source_id").value
    let fd = new FormData(form_edit_source)
    let object = convert_fd_to_json(fd)
	let response = await sendData("/admin/sources/" + source_id + "/edit", fd)
    let data = await response.json();
    if (data.message === "ok") {
        location.reload()
    }
    else {
        handle_errors_on_form("form_edit_source", data.errors, "edit-modal__label")
    }
})
$('form[name=form_edit_campaign]').on('submit', async function (e) {
    e.preventDefault();
    let fd = new FormData(form_edit_campaign)
    let campaign_id = document.getElementById("edit_id").value
    let object = convert_fd_to_json(fd)
	let response = await sendData(`/admin/campaigns/${campaign_id}/update`, fd)
    let data = await response.json();
        if (data.message === "ok") {
        location.reload()
    }
    else {
        handle_errors_on_form("form_edit_campaign", data.errors, "edit-modal__label")
    }
})