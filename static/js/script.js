// Recargar la página cada 20 segundos para actualizar fotos nuevas
setInterval(() => {
    location.reload();
}, 20000);

// Función para eliminar una foto
function deletePhoto(photoName) {
    if (confirm("¿Estás seguro de que quieres eliminar esta foto?")) {
        fetch(`/delete/${photoName}`, {
            method: "DELETE"
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Foto eliminada correctamente.");
                location.reload();
            } else {
                alert("Error al eliminar la foto.");
            }
        })
        .catch(error => console.error("Error:", error));
    }
}
document.addEventListener("DOMContentLoaded", () => {
    const gallery = document.getElementById("gallery");
    const modal = document.getElementById("modal");
    const modalImg = document.getElementById("modal-img");
    const closeModal = document.getElementById("close-modal");

    gallery.addEventListener("click", (event) => {
        if (event.target.tagName === "IMG") {
            modal.style.display = "flex";
            modalImg.src = event.target.src;
        }
    });

    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });
});