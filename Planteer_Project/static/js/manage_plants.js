document.addEventListener("DOMContentLoaded", function () {
    const modalElement = document.getElementById(
        "plantModal"
    );

    if (
        modalElement &&
        typeof bootstrap !== "undefined"
    ) {

        const modal = new bootstrap.Modal(
            modalElement
        );

        modal.show();

        modalElement.addEventListener(
            "hidden.bs.modal",
            function () {

                window.location.href =
                    modalElement.dataset.returnUrl;

            }
        );

    }
    const imageInput = document.getElementById(
        "id_image"
    );

    const imagePreview = document.getElementById(
        "plantImagePreview"
    );

    if (!imageInput || !imagePreview) return;


    const originalImage = imagePreview.getAttribute(
        "src"
    );

    let previewUrl = null;

    function resetPreview() {

        if (previewUrl) {

            URL.revokeObjectURL(previewUrl);

            previewUrl = null;

        }

        if (originalImage) {

            imagePreview.src = originalImage;

            imagePreview.hidden = false;

        } else {

            imagePreview.removeAttribute("src");

            imagePreview.hidden = true;

        }

    }

    imageInput.addEventListener("change", function () {

        resetPreview();

        const file = imageInput.files[0];

        if (!file || !imageInput.validity.valid) return;

        previewUrl = URL.createObjectURL(file);

        imagePreview.src = previewUrl;

        imagePreview.hidden = false;

    });

});