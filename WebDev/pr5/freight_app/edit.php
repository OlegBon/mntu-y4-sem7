<?php
require 'db.php';

// Перевіряємо, чи переданий ID в URL
if (!isset($_GET['id'])) {
    die("ID заявки не вказано!");
}

$id = intval($_GET['id']); // Захист - перетворюємо в число

// 1. Оновлення даних (якщо натиснули кнопку)
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $client = mysqli_real_escape_string($conn, $_POST['client_name']);
    $cargo = mysqli_real_escape_string($conn, $_POST['cargo_description']);
    $weight = floatval($_POST['weight']);
    $start = mysqli_real_escape_string($conn, $_POST['route_start']);
    $end = mysqli_real_escape_string($conn, $_POST['route_end']);
    $status = mysqli_real_escape_string($conn, $_POST['status']); // Додали статус

    $sql = "UPDATE requests SET 
            client_name='$client', 
            cargo_description='$cargo', 
            weight='$weight', 
            route_start='$start', 
            route_end='$end', 
            status='$status' 
            WHERE id=$id";

    if (mysqli_query($conn, $sql)) {
        header("Location: index.php");
        exit();
    } else {
        echo "Помилка оновлення: " . mysqli_error($conn);
    }
}

// 2. Отримання старих даних для форми
$sql = "SELECT * FROM requests WHERE id=$id";
$result = mysqli_query($conn, $sql);
$row = mysqli_fetch_assoc($result);

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