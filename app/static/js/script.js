document.querySelectorAll("[data-storage-percent]").forEach((storageFill) => {
    const percent = Number(storageFill.dataset.storagePercent);
    storageFill.style.width = `${Math.min(100, Math.max(0, percent))}%`;
});
