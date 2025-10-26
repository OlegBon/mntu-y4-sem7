$(document).ready(function () {
  // Слайдер з кнопками
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

  // Очистка запланованих рейсів
  $("#clearVoyagesBtn").click(() => {
    if (confirm("Ви впевнені, що хочете очистити всі заплановані рейси?")) {
      localStorage.removeItem("voyages");
      $("#voyageTable tbody").fadeOut(300, function () {
        $(this).empty().show();
      });
    }
  });

  // Завантаження з localStorage
  const savedVoyages = JSON.parse(localStorage.getItem("voyages")) || [];
  savedVoyages.forEach((v) => addRow(v));

  // Валідація
  $("#voyageForm").submit((e) => {
    e.preventDefault();

    const route = $("#route").val();
    const duration = $("#duration").val();
    const crew = parseInt($("#crew").val());

    if (!route || !duration || isNaN(crew) || crew <= 0) {
      alert("Будь ласка, заповніть всі поля коректно.");
      return;
    }

    const voyage = {
      route,
      duration,
      crew,
      status: "Заплановано",
    };

    addRow(voyage);
    saveVoyage(voyage);
    $("#voyageForm")[0].reset();
  });

  function saveVoyage(voyage) {
    const voyages = JSON.parse(localStorage.getItem("voyages")) || [];
    voyages.push(voyage);
    localStorage.setItem("voyages", JSON.stringify(voyages));
  }
});

// Функції для додавання та видалення рейсів з анімацією
function addRow(voyage) {
  const row = $(`
    <tr>
      <td>${voyage.route}</td>
      <td>${voyage.duration}</td>
      <td>${voyage.crew}</td>
      <td>${voyage.status}</td>
      <td><button class="deleteBtn">Видалити</button></td>
    </tr>
  `);

  row.find(".deleteBtn").click(function () {
    row.fadeOut(300, function () {
      row.remove();
      removeVoyage(voyage);
    });
  });

  $("#voyageTable tbody").append(row.hide().fadeIn(500));
}

// Видалення рейсу з localStorage
function removeVoyage(voyageToRemove) {
  const voyages = JSON.parse(localStorage.getItem("voyages")) || [];
  const updated = voyages.filter(
    (v) =>
      !(
        v.route === voyageToRemove.route &&
        v.duration === voyageToRemove.duration &&
        v.crew === voyageToRemove.crew
      )
  );
  localStorage.setItem("voyages", JSON.stringify(updated));
}
