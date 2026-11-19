document.addEventListener("DOMContentLoaded", function () {

    const forms = document.querySelectorAll(
        "form[data-validate]"
    );

    function validateField(field) {

        const value = field.value.trim();
        const minLength = field.minLength;
        const maxLength = field.maxLength;

        field.setCustomValidity("");

        if (field.required && value.length === 0) {

            field.setCustomValidity(
                "This field is required."
            );

        } else if (
            value.length > 0 &&
            minLength > 0 &&
            value.length < minLength
        ) {

            field.setCustomValidity(
                `Please enter at least ${minLength} characters.`
            );

        } else if (
            maxLength > 0 &&
            value.length > maxLength
        ) {

            field.setCustomValidity(
                `Maximum ${maxLength} characters allowed.`
            );

        } else if (
            field.hasAttribute("data-name") &&
            value.length > 0
        ) {

            const validName = /^[\p{L}\p{M} '’-]+$/u;

            if (
                !validName.test(value) ||
                !/\p{L}/u.test(value)
            ) {

                field.setCustomValidity(
                    "Please enter a valid name."
                );

            }

        }

        return field.validity.valid;

    }


    function showFieldError(field) {

        const isValid = validateField(field);

        field.classList.toggle(
            "is-invalid",
            !isValid
        );

        field.setAttribute(
            "aria-invalid",
            String(!isValid)
        );

        const container = field.closest(".contact-field");

        const errorElement = container?.querySelector(
            "[data-client-error]"
        );

        if (errorElement) {

            errorElement.textContent = isValid
                ? ""
                : field.validationMessage;

        }

    }


    forms.forEach(form => {

        const fields = form.querySelectorAll(
            "[data-trim]"
        );

        fields.forEach(field => {

            field.addEventListener("input", function () {

                showFieldError(field);

            });

            field.addEventListener("blur", function () {

                showFieldError(field);

            });

            field.addEventListener("invalid", function () {

                showFieldError(field);

            });

        });

        form.addEventListener("submit", function (event) {

            fields.forEach(field => {

                field.value = field.value.trim();

                showFieldError(field);

            });

            if (!form.checkValidity()) {

                event.preventDefault();

                form.reportValidity();

            }

        });

    });

});