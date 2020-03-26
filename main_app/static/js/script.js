$(document).ready(function () {
    $('.sidenav').sidenav();

    // Make anything with a data-href attribute a clickable link
    $('.clickable').click(function() {
        window.location.href = this.dataset.href;
    });

    // Show/hide the comment edit form
    $('.edit-form').hide();
    $('body').click(toggleEdit);

    function toggleEdit(evt) {
        if (evt.target.id !== 'edit-btn') return;
        let btnId = evt.target.dataset.id;
        $(`.edit-form[data-id="${btnId}"]`).toggle();
    }
});
