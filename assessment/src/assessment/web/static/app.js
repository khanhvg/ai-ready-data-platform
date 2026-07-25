(() => {
  "use strict";

  const errorSummary = document.querySelector("[data-error-summary]");
  if (errorSummary) {
    errorSummary.focus();
  }

  const status = document.querySelector("#autosave-status");
  let queue = Promise.resolve();

  document.querySelectorAll("form[data-autosave]").forEach((form) => {
    form.addEventListener("change", (event) => {
      const statusControl = form.querySelector('select[name="evidence_status"]');
      const noRating = form.querySelector('input[name="rating"][value=""]');
      if (statusControl && noRating) {
        if (event.target === statusControl && statusControl.value === "Not assessed") {
          noRating.checked = true;
        } else if (event.target === noRating && noRating.checked) {
          statusControl.value = "Not assessed";
        } else if (
          event.target === statusControl
          && statusControl.value !== "Not assessed"
          && noRating.checked
        ) {
          noRating.checked = false;
        } else if (
          event.target.matches?.('input[name="rating"]')
          && event.target.value !== ""
          && statusControl.value === "Not assessed"
        ) {
          statusControl.value = "Self-reported";
        }
      }
      if (!status || !form.reportValidity()) return;
      status.textContent = "Saving…";
      queue = queue.then(async () => {
        try {
          const response = await fetch(form.action, {
            method: "POST",
            body: new FormData(form),
            credentials: "same-origin",
            headers: { "X-Assessment-Autosave": "1" },
          });
          const text = await response.text();
          if (!response.ok) {
            status.textContent = response.status === 409
              ? "A newer revision exists. Reload before saving."
              : "Save failed—use the Save button to retry.";
            return;
          }
          const parsed = new DOMParser().parseFromString(text, "text/html");
          const revision = parsed.querySelector('input[name="revision"]')?.value;
          if (revision) {
            document.querySelectorAll('input[name="revision"]').forEach((input) => {
              input.value = revision;
            });
          }
          status.textContent = `Saved · revision ${revision || "updated"}`;
        } catch {
          status.textContent = "Save failed—use the Save button to retry.";
        }
      });
    });
  });
})();
