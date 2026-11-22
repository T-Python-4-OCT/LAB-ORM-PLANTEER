/* Planteer — small helpers: mobile menu, closing messages, filter auto-submit, image preview */
(function () {
  "use strict";

  /* mobile menu */
  var toggle = document.querySelector("[data-nav-toggle]");
  var links = document.getElementById("nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* close success messages */
  document.querySelectorAll("[data-dismiss]").forEach(function (btn) {
    btn.addEventListener("click", function () { btn.closest(".toast").remove(); });
  });

  /* all-plants filters: apply as soon as a select changes */
  document.querySelectorAll("form[data-autosubmit] select").forEach(function (select) {
    select.addEventListener("change", function () { select.form.submit(); });
  });

  /* plant photo: preview the chosen image before saving */
  var upload = document.querySelector("[data-upload]");
  if (upload) {
    var input = upload.querySelector("input[type=file]");
    var preview = upload.querySelector("[data-upload-preview]");
    var empty = upload.querySelector("[data-upload-empty]");
    var nameEl = document.querySelector("[data-upload-name]");
    var initialSrc = preview.getAttribute("src");
    var initialName = nameEl.textContent;

    input.addEventListener("change", function () {
      var file = input.files && input.files[0];
      if (preview.src && preview.src.indexOf("blob:") === 0) URL.revokeObjectURL(preview.src);
      var src = file ? URL.createObjectURL(file) : initialSrc;
      if (src) { preview.src = src; } else { preview.removeAttribute("src"); }
      preview.hidden = !src;
      empty.hidden = !!src;
      upload.classList.toggle("has-file", !!src);
      nameEl.textContent = file ? file.name : initialName;
    });
    ["dragenter", "dragover"].forEach(function (e) { upload.addEventListener(e, function () { upload.classList.add("is-drag"); }); });
    ["dragleave", "drop"].forEach(function (e) { upload.addEventListener(e, function () { upload.classList.remove("is-drag"); }); });
  }
})();
