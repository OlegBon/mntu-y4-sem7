<?php
require 'db.php';
require 'auth_check.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    // Перевірка CSRF-токена
    if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== $_SESSION['csrf_token']) {
        die("Помилка безпеки: Невірний CSRF-токен!");
    }
    
    // Отримуємо дані (mysqli_real_escape_string більше НЕ ПОТРІБЕН для підготовлених виразів)
    $client = $_POST['client_name'];
    $cargo = $_POST['cargo_description'];
    $weight = floatval($_POST['weight']);
    $start = $_POST['route_start'];
    $end = $_POST['route_end'];

    // Формуємо шаблон запиту з плейсхолдерами (?) для підготовленого виразу
    $sql = "INSERT INTO requests (client_name, cargo_description, weight, route_start, route_end) 
            VALUES (?, ?, ?, ?, ?)";

    // Підготовка
    $stmt = mysqli_prepare($conn, $sql);

    if ($stmt) {
        // Прив'язка параметрів
        // "ssdss":
        // s = string (клієнт)
        // s = string (вантаж)
        // d = double (вага, бо float)
        // s = string (звідки)
        // s = string (куди)
        mysqli_stmt_bind_param($stmt, "ssdss", $client, $cargo, $weight, $start, $end);

        // Виконання
        if (mysqli_stmt_execute($stmt)) {
            header("Location: index.php");
            exit();
        } else {
            echo "Помилка: " . mysqli_stmt_error($stmt);
        }
        mysqli_stmt_close($stmt);
    } else {
        echo "Помилка БД: " . mysqli_error($conn);
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
        <input type="hidden" name="csrf_token" value="<?= $_SESSION['csrf_token'] ?>">
        
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