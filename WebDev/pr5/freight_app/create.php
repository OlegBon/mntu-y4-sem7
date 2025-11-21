<?php
require 'db.php';

// Перевіряємо, чи прийшли дані методом POST (чи натиснув користувач кнопку)
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    
    // Отримуємо дані та екрануємо їх (захист від злому SQL Injection)
    $client = mysqli_real_escape_string($conn, $_POST['client_name']);
    $cargo = mysqli_real_escape_string($conn, $_POST['cargo_description']);
    $weight = floatval($_POST['weight']); // Перетворюємо в число
    $start = mysqli_real_escape_string($conn, $_POST['route_start']);
    $end = mysqli_real_escape_string($conn, $_POST['route_end']);

    // Формуємо SQL запит
    // Status не передаємо - в базі він за замовчуванням 'Нова'
    $sql = "INSERT INTO requests (client_name, cargo_description, weight, route_start, route_end) 
            VALUES ('$client', '$cargo', '$weight', '$start', '$end')";

    // Виконуємо запит
    if (mysqli_query($conn, $sql)) {
        // Якщо успішно - перекидаємо користувача на головну
        header("Location: index.php"); // або index.html
        echo "<script>window.location.href='index.php';</script>"; 
        exit();
    } else {
        echo "Помилка: " . mysqli_error($conn);
    }
}
?>

<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Нова заявка</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

<div class="container-small">
    <h1>Створити заявку</h1>

    <form action="create.php" method="POST" id="editForm">
        
        <div class="form-group">
            <label>Замовник (Клієнт):</label>
            <input type="text" name="client_name" required placeholder="ТОВ Ромашка">
        </div>

        <div class="form-group">
            <label>Опис вантажу:</label>
            <textarea name="cargo_description" required placeholder="Що веземо?"></textarea>
        </div>

        <div class="form-group">
            <label>Вага (тонн):</label>
            <input type="number" step="0.1" name="weight" required placeholder="0.0">
        </div>

        <div class="form-group">
            <label>Маршрут (Звідки):</label>
            <input type="text" name="route_start" required placeholder="Місто відправлення">
        </div>

        <div class="form-group">
            <label>Маршрут (Куди):</label>
            <input type="text" name="route_end" required placeholder="Місто призначення">
        </div>

        <button type="submit" id="saveBtn" class="btn btn-primary" disabled>Зберегти</button>
        <a href="index.php" class="btn btn-warning pull-right">Скасувати</a>
    </form>
</div>

<script src="js/form.js"></script>

</body>
</html>