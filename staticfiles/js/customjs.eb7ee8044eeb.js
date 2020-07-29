function setupYesOrNoModal(data){
    let thisModal = $('#yesOrNoModal');
    $('#yesOrNoModalLabel').text(data.title);
    $('#yesOrNoModalBody').text(data.message)

    function modalButtonClicked(event) {
        let button = event.target;
        if (button.id === "yesOrNoModalNo") {
            data.no();
        }
        else {
            data.yes();
        }
        thisModal.modal("hide");
    };

    document.getElementById('yesOrNoModalButtons').addEventListener('click', modalButtonClicked, {once: true});
    thisModal.modal('show');
}
// Can be run to show alert on any page
// todo need to improve how alert is dismissed
function showAlertMessage(message, type="info", container="custom_message_alert") {
    let alertContainer = document.getElementById(container);
    let alert = document.createElement("div");
    let closeButton = document.createElement("button");
    let closeIcon = document.createElement("span");

    alert.setAttribute("class", "alert alert-"+ type +" alert-dismissible fade in show");

    alert.setAttribute("role", "alert");

    closeButton.setAttribute("type", "button");
    closeButton.setAttribute("class", "close");
    closeButton.setAttribute("data-dismiss", "alert");
    closeButton.setAttribute("aria-label", "Close");

    closeIcon.setAttribute("aria-hidden", "true");
    closeIcon.appendChild(document.createTextNode("×"));

    message = document.createTextNode(message);

    alert.appendChild(message);
    alert.appendChild(closeButton);
    closeButton.appendChild(closeIcon)

    alertContainer.appendChild(alert);

    // todo this resets timer and all alerts close at same time
    setTimeout(function() {
        $(".alert").alert('close');
    }, 10000);
}
