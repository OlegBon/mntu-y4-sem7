<?php
session_start(); // Відновлюємо сесію

// Якщо в сесії немає user_id — значить користувач не увійшов
if (!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit();
}

// CSRF токен для захисту форм
if (empty($_SESSION['csrf_token'])) {
    // Створюємо випадковий рядок із 32 байт
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}
?>
?>