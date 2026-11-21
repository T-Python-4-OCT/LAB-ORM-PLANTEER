
document.addEventListener("DOMContentLoaded", function () {
    const mainImage = document.getElementById("mainPlantImage");
    const thumbnails = document.querySelectorAll(".gallery-thumb");

    if (!mainImage || !thumbnails.length) {
        return;
    }

    thumbnails.forEach(function (thumbnail) {
        thumbnail.addEventListener("click", function () {
            const imageUrl = thumbnail.dataset.image;

            if (!imageUrl) {
                return;
            }

            mainImage.src = imageUrl;

            const thumbnailImage = thumbnail.querySelector("img");

            if (thumbnailImage) {
                mainImage.alt = thumbnailImage.alt;
            }

            thumbnails.forEach(function (item) {
                item.classList.remove("active");
            });

            thumbnail.classList.add("active");
        });
    });
});
