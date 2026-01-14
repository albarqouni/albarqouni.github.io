console.log("mriqt.js loaded");

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("[data-compare]").forEach(function (root) {
    var overlay = root.querySelector(".compare__overlay");
    var range = root.querySelector(".compare__range");
    if (!overlay || !range) return;

    function set(v) { overlay.style.width = v + "%"; }
    set(range.value);

    range.addEventListener("input", function (e) {
      set(e.target.value);
    });
  });
});
