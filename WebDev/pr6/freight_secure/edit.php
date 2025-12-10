<?php
require 'auth_check.php';
require 'db.php';

if (!isset($_GET['id'])) {
    die("ID заявки не вказано!");
}

$id = intval($_GET['id']);

// Оновлення (UPDATE) заявки
if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    // Перевірка CSRF-токена
    if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== $_SESSION['csrf_token']) {
        die("Помилка безпеки: Невірний CSRF-токен!");
    }

    $client = $_POST['client_name'];
    $cargo = $_POST['cargo_description'];
    $weight = floatval($_POST['weight']);
    $start = $_POST['route_start'];
    $end = $_POST['route_end'];
    $status = $_POST['status'];

    // Підготовлений запит UPDATE
    $sql = "UPDATE requests SET 
            client_name=?, 
            cargo_description=?, 
            weight=?, 
            route_start=?, 
            route_end=?, 
            status=? 
            WHERE id=?";

    $stmt = mysqli_prepare($conn, $sql);

    if ($stmt) {
        // Типи: s(string), s(string), d(double), s(string), s(string), s(string), i(int - це ID)
        // Тому виходить "ssdsssi"
        mysqli_stmt_bind_param($stmt, "ssdsssi", $client, $cargo, $weight, $start, $end, $status, $id);

        if (mysqli_stmt_execute($stmt)) {
            header("Location: index.php");
            exit();
        } else {
            echo "Помилка оновлення: " . mysqli_stmt_error($stmt);
        }
        mysqli_stmt_close($stmt);
    } else {
        echo "Помилка підготовки: " . mysqli_error($conn);
    }
}

// Отримання даних (SELECT) заявки для заповнення форми
$sql = "SELECT * FROM requests WHERE id = ?";
$stmt = mysqli_prepare($conn, $sql);

if ($stmt) {
    mysqli_stmt_bind_param($stmt, "i", $id);
    mysqli_stmt_execute($stmt);
    
    // Отримуємо результат у зручному форматі
    $result = mysqli_stmt_get_result($stmt);
    $row = mysqli_fetch_assoc($result);
    
    mysqli_stmt_close($stmt);
} else {
    die("Помилка БД");
}

if (!$row) {
    die("Заявку не знайдено!");
}
?>

<!DOCTYPE html>
<html lang="uk">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Редагування заявки</title>
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>

        <div class="container-small">
            <h1>Редагувати заявку #<?= $row['id'] ?></h1>

            <form action="edit.php?id=<?= $id ?>" method="POST" id="editForm">
                <input type="hidden" name="csrf_token" value="<?= $_SESSION['csrf_token'] ?>">
                
                <div class="form-group">
                    <label>Замовник:</label>
                    <input type="text" name="client_name" value="<?= htmlspecialchars($row['client_name']) ?>" required>
                </div>

                <div class="form-group">
                    <label>Опис вантажу:</label>
                    <textarea name="cargo_description" required><?= htmlspecialchars($row['cargo_description']) ?></textarea>
                </div>

                <div class="form-group">
                    <label>Вага (тонн):</label>
                    <input type="number" step="0.1" name="weight" value="<?= $row['weight'] ?>" required>
                </div>

                <div class="form-group">
                    <label>Маршрут (Звідки):</label>
                    <input type="text" name="route_start" value="<?= htmlspecialchars($row['route_start']) ?>" required>
                </div>

                <div class="form-group">
                    <label>Маршрут (Куди):</label>
                    <input type="text" name="route_end" value="<?= htmlspecialchars($row['route_end']) ?>" required>
                </div>

                <div class="form-group">
                    <label>Статус:</label>
                    <select name="status">
                        <option value="Нова" <?= $row['status'] == 'Нова' ? 'selected' : '' ?>>Нова</option>
                        <option value="В дорозі" <?= $row['status'] == 'В дорозі' ? 'selected' : '' ?>>В дорозі</option>
                        <option value="Виконана" <?= $row['status'] == 'Виконана' ? 'selected' : '' ?>>Виконана</option>
                    </select>
                </div>

                <button type="submit" id="saveBtn" class="btn btn-primary" disabled>Оновити</button>
                <a href="index.php" class="btn btn-warning pull-right">Скасувати</a>
            </form>
        </div>

        <script src="js/form.js"></script>

    </body>
</html>