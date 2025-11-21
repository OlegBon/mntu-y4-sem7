// Логіка модального вікна видалення
document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("deleteModal");
  const confirmBtn = document.getElementById("confirmDeleteBtn");

  // Робимо функції глобальними, щоб їх бачив HTML (onclick)
  window.openModal = function (id) {
    confirmBtn.href = "delete.php?id=" + id;
    modal.style.display = "flex";
  };

  window.closeModal = function () {
    modal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target == modal) {
      closeModal();
    }
  };
});
