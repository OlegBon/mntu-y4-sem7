$(document).ready(function () {
  // Слайдер зображень
  const totalImages = 7;
  let currentIndex = 1;

  function updateImage() {
    $("#sliderImage").fadeOut(200, function () {
      $(this).attr("src", `img/ship${currentIndex}.jpg`).fadeIn(200);
    });
  }

  $("#nextBtn").click(() => {
    currentIndex = currentIndex < totalImages ? currentIndex + 1 : 1;
    updateImage();
  });

  $("#prevBtn").click(() => {
    currentIndex = currentIndex > 1 ? currentIndex - 1 : totalImages;
    updateImage();
  });

  // Робота з API (PHP + MySQL)

  // Функція для захисту від XSS (перетворює <script> на текст)
  function escapeHtml(text) {
    if (!text) return text;
    return text
      .toString()
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Функція завантаження рейсів (READ + SEARCH)
  function loadVoyages(searchQuery = "") {
    $.ajax({
      url: "api.php",
      method: "GET",
      cache: false,
      data: { action: "read", search: searchQuery },
      dataType: "json",
      success: function (data) {
        const tbody = $("#voyageTable tbody");
        tbody.empty(); // Очищаємо таблицю

        if (data.length === 0) {
          tbody.append('<tr><td colspan="5">Рейсів не знайдено</td></tr>');
          return;
        }

        // Малюємо рядки (з захистом від XSS)
        data.forEach((voyage) => {
          const row = $(`
                <tr data-id="${escapeHtml(voyage.id)}">
                    <td>${escapeHtml(voyage.route)}</td>
                    <td>${escapeHtml(voyage.duration)}</td>
                    <td>${escapeHtml(voyage.crew)}</td>
                    <td>${escapeHtml(voyage.status)}</td>
                    <td><button class="deleteBtn">Видалити</button></td>
                </tr>
            `);
          tbody.append(row);
        });
      },
      error: function (err) {
        console.error("Помилка завантаження:", err);
      },
    });
  }

  // Завантажуємо рейси при старті
  loadVoyages();

  // Пошук (SEARCH)
  $("#searchVoyage").on("input", function () {
    const query = $(this).val();
    loadVoyages(query);
  });

  // Додавання рейсу (CREATE)
  $("#voyageForm").submit((e) => {
    e.preventDefault();

    const route = $("#route").val();
    const duration = $("#duration").val();
    const crew = parseInt($("#crew").val());

    if (!route || !duration || isNaN(crew) || crew <= 0) {
      alert("Будь ласка, заповніть всі поля коректно.");
      return;
    }

    $.ajax({
      url: "api.php?action=create",
      method: "POST",
      data: { route: route, duration: duration, crew: crew },
      dataType: "json",
      success: function (response) {
        if (response.success) {
          $("#voyageForm")[0].reset();
          loadVoyages(); // Оновлюємо таблицю
          alert("Рейс успішно заплановано!");
        } else {
          alert("Помилка: " + response.message);
        }
      },
      error: function () {
        alert("Помилка з'єднання з сервером.");
      },
    });
  });

  // Видалення рейсу (DELETE)
  $("#voyageTable tbody").on("click", ".deleteBtn", function () {
    if (!confirm("Видалити цей рейс?")) return;

    const row = $(this).closest("tr");
    const id = row.data("id");

    $.ajax({
      url: "api.php?action=delete",
      method: "POST",
      data: { id: id },
      dataType: "json",
      success: function (response) {
        if (response.success) {
          row.fadeOut(300, function () {
            $(this).remove();
          });
        } else {
          alert("Не вдалося видалити запис.");
        }
      },
    });
  });

  // Очищення всіх рейсів (CLEAR ALL)
  $("#clearVoyagesBtn").click(() => {
    if (
      !confirm(
        "Ви впевнені, що хочете видалити ВСІ заплановані рейси? Цю дію не можна скасувати."
      )
    ) {
      return;
    }

    $.ajax({
      url: "api.php?action=clear",
      method: "POST",
      dataType: "json",
      success: function (response) {
        if (response.success) {
          loadVoyages(); // Тепер ця функція точно буде знайдена
          alert("Всі рейси видалено.");
        } else {
          alert("Помилка: " + response.message);
        }
      },
      error: function () {
        alert("Помилка з'єднання з сервером.");
      },
    });
  });
});
