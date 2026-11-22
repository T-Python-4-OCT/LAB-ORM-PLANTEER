document.addEventListener("DOMContentLoaded", function () {

    const forms = document.querySelectorAll("form[data-validate]");

    const allowedImageTypes = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ];

    const maxImageSize = 5 * 1024 * 1024;

    const validName = /^[\p{L}\p{M} '’-]+$/u;


    // Validate individual fields

    function validateField(field) {

        field.setCustomValidity("");


        // Image validation

        if (field.type === "file") {

            const file = field.files[0];

            if (file) {

                if (
                    file.type &&
                    !allowedImageTypes.includes(file.type)
                ) {

                    field.setCustomValidity(
                        "Only JPG, PNG and WEBP images are allowed."
                    );

                } else if (file.size > maxImageSize) {

                    field.setCustomValidity(
                        "Image size cannot exceed 5 MB."
                    );

                }

            }

            return field.validity.valid;

        }


        // Text validation

        const value = field.value.trim();

        const length = Array.from(value).length;

        const minLength = field.minLength;

        const maxLength = field.maxLength;


        // Required fields

        if (field.required && !value) {

            field.setCustomValidity(
                "This field is required."
            );

        }
        else if (
            length > 0 &&
            minLength > 0 &&
            length < minLength
        ) {

            field.setCustomValidity(
                `Please enter at least ${minLength} characters.`
            );

        }
        else if (
            maxLength > 0 &&
            length > maxLength
        ) {

            field.setCustomValidity(
                `Maximum ${maxLength} characters allowed.`
            );

        }
        else if (
            field.hasAttribute("data-name") &&
            value &&
            (!validName.test(value) || !/\p{L}/u.test(value))
        ) {

            field.setCustomValidity(
                "Please enter a valid name."
            );

        }

        return field.validity.valid;

    }
    function showFieldError(field) {

        const valid = validateField(field);

        field.classList.toggle(
            "is-invalid",
            !valid
        );

        field.setAttribute(
            "aria-invalid",
            String(!valid)
        );

        const container = field.closest(
            ".contact-field, .mb-3"
        );

        const errorElement = container?.querySelector(
            "[data-client-error]"
        );

        if (errorElement) {

            errorElement.textContent = valid
                ? ""
                : field.validationMessage;

        }

        return valid;

    }
    forms.forEach(form => {

        const fields = Array.from(
            form.querySelectorAll(
                "input[data-trim], textarea[data-trim], select, input[type='file']"
            )
        ).filter(field => field.willValidate);

        form.noValidate = true;

        fields.forEach(field => {

            ["input", "change", "blur"].forEach(event => {

                field.addEventListener(
                    event,
                    () => showFieldError(field)
                );

            });

        });

        form.addEventListener("submit", event => {

            fields.forEach(field => {

                if (field.hasAttribute("data-trim")) {

                    field.value = field.value.trim();

                }

                showFieldError(field);

            });

            if (!form.checkValidity()) {

                event.preventDefault();

                form.reportValidity();

            }

        });

    });

});