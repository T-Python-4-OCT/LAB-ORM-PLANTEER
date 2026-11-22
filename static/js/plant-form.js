
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("plant-editor-form");

    if (!form) return;

    const coverInput = form.querySelector(
        'input[type="file"][name="image"]'
    );

    const coverDropzone = document.getElementById(
        "cover-dropzone"
    );

    const coverPreview = document.getElementById(
        "cover-preview"
    );

    const coverPlaceholder = document.getElementById(
        "cover-placeholder"
    );

    const submitButton = document.getElementById(
        "plant-submit-button"
    );

    const objectUrls = new Map();

    // =========================================
    // IMAGE UTILITIES
    // =========================================

    function isImage(file) {
        return (
            file &&
            (
                file.type.startsWith("image/") ||
                /\.(jpg|jpeg|png|webp)$/i.test(file.name)
            )
        );
    }

    function showPreview(input, image, placeholder) {
        const file = input.files && input.files[0];

        if (!file) return;

        if (!isImage(file)) {
            alert("Please select a valid image file.");
            input.value = "";
            return;
        }

        if (objectUrls.has(image)) {
            URL.revokeObjectURL(objectUrls.get(image));
        }

        const url = URL.createObjectURL(file);

        objectUrls.set(image, url);

        image.src = url;
        image.hidden = false;

        if (placeholder) {
            placeholder.hidden = true;
        }
    }

    function assignDroppedFile(input, file) {
        if (!isImage(file)) {
            alert("Only image files are allowed.");
            return;
        }

        const transfer = new DataTransfer();

        transfer.items.add(file);
        input.files = transfer.files;

        input.dispatchEvent(
            new Event("change", { bubbles: true })
        );
    }

    function enableDropzone(dropzone, input) {
        if (!dropzone || !input) return;

        dropzone.addEventListener("click", event => {
            if (
                event.target.closest(
                    'input, button, a, label'
                )
            ) {
                return;
            }

            input.click();
        });

        ["dragenter", "dragover"].forEach(eventName => {
            dropzone.addEventListener(eventName, event => {
                event.preventDefault();
                event.stopPropagation();

                dropzone.classList.add("is-dragging");
            });
        });

        ["dragleave", "drop"].forEach(eventName => {
            dropzone.addEventListener(eventName, event => {
                event.preventDefault();
                event.stopPropagation();

                dropzone.classList.remove("is-dragging");
            });
        });

        dropzone.addEventListener("drop", event => {
            const file = event.dataTransfer?.files?.[0];

            if (file) {
                assignDroppedFile(input, file);
            }
        });
    }

    // =========================================
    // COVER IMAGE
    // =========================================

    if (coverInput && coverDropzone && coverPreview) {
        coverInput.addEventListener("change", () => {
            showPreview(
                coverInput,
                coverPreview,
                coverPlaceholder
            );
        });

        enableDropzone(
            coverDropzone,
            coverInput
        );
    }

    // =========================================
    // GALLERY IMAGES
    // =========================================

    const galleryCards = document.querySelectorAll(
        ".editor-gallery-item"
    );

    galleryCards.forEach(card => {
        const input = card.querySelector(
            'input[type="file"]'
        );

        const dropzone = card.querySelector(
            "[data-gallery-upload]"
        );

        const preview = card.querySelector(
            "[data-gallery-preview]"
        );

        const placeholder = card.querySelector(
            "[data-gallery-placeholder]"
        );

        const deleteCheckbox = card.querySelector(
            'input[type="checkbox"][name$="-DELETE"]'
        );

        if (input && preview) {
            input.addEventListener("change", () => {
                showPreview(
                    input,
                    preview,
                    placeholder
                );
            });
        }

        enableDropzone(dropzone, input);

        // Existing image deletion preview
        if (deleteCheckbox) {
            const syncDeletion = () => {
                card.classList.toggle(
                    "is-marked-for-deletion",
                    deleteCheckbox.checked
                );
            };

            deleteCheckbox.addEventListener(
                "change",
                syncDeletion
            );

            syncDeletion();
        }
    });

    // =========================================
    // SUBMISSION
    // =========================================

    form.addEventListener("submit", () => {
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = "Saving plant...";
        }
    });

    // =========================================
    // CLEAN UP PREVIEW URLS
    // =========================================

    window.addEventListener("pagehide", () => {
        objectUrls.forEach(url => {
            URL.revokeObjectURL(url);
        });

        objectUrls.clear();
    });
});
