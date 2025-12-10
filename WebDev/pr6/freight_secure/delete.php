<?php
require 'auth_check.php';
require 'db.php';

// Приймаємо ТІЛЬКИ POST запити (захист від випадкових переходів по посиланню)
if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    // Перевірка CSRF
    if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== $_SESSION['csrf_token']) {
        die("Помилка безпеки: Невірний CSRF-токен!");
    }

    // Отримання ID
    $id = intval($_POST['id']);

    // Видалення (Prepared Statement)
    $sql = "DELETE FROM requests WHERE id = ?";
    $stmt = mysqli_prepare($conn, $sql);
    
    if ($stmt) {
        mysqli_stmt_bind_param($stmt, "i", $id);
        if (mysqli_stmt_execute($stmt)) {
            header("Location: index.php");
        } else {
            echo "Помилка видалення: " . mysqli_stmt_error($stmt);
        }
        mysqli_stmt_close($stmt);
    }
} else {
    // Якщо хтось спробує відкрити delete.php у браузері -> на головну
    header("Location: index.php");
}
?>