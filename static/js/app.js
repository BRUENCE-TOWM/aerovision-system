document.body.addEventListener("htmx:afterSwap", function (event) {
    const target = event.target;
    if (target instanceof HTMLElement) {
        target.classList.add("htmx-swapped");
        window.setTimeout(function () {
            target.classList.remove("htmx-swapped");
        }, 700);
    }
});

document.body.addEventListener("htmx:beforeRequest", function (event) {
    const trigger = event.target;
    if (trigger instanceof HTMLElement) {
        trigger.classList.add("is-loading");
    }
});

document.body.addEventListener("htmx:afterRequest", function (event) {
    const trigger = event.target;
    if (trigger instanceof HTMLElement) {
        trigger.classList.remove("is-loading");
    }
});
