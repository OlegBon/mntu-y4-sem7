<?php
// Параметри підключення до бази даних (стандартні для XAMPP)
$servername = "localhost";
$username = "root";
$password = ""; // У XAMPP за замовчуванням пароль порожній
$dbname = "freight_transport"; // Ім'я бази

// Створення підключення
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Перевірка підключення
if (!$conn) {
    die("Помилка підключення: " . mysqli_connect_error());
}

// Встановлення кодування (щоб кирилиця відображалася коректно)
mysqli_set_charset($conn, "utf8");
?>