$(document).ready(function () {
  // Плавне зникнення при кліку
  $(".fade-img").click(function () {
    $(this).closest(".img-block").fadeOut(1000);
  });

  // Показати всі
  $("#showAll").click(function () {
    $(".img-block").fadeIn(1000);
  });

  // Додавання підписів
  $(".fade-img").each(function () {
    const altText = $(this).attr("alt");
    $(this).parent().append(`<p class="caption">${altText}</p>`);
  });

  // Hover-ефекти через jQuery
  $(".fade-img").hover(
    function () {
      $(this).css("box-shadow", "0 0 20px rgba(0,0,0,0.5)");
    },
    function () {
      $(this).css("box-shadow", "0 4px 8px rgba(0,0,0,0.2)");
    }
  );

  // Анімація появи при завантаженні
  $(".img-block")
    .hide()
    .each(function (index) {
      $(this)
        .delay(200 * index)
        .fadeIn(600);
    });
});
