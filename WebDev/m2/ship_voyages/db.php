<?php

$host = 'localhost';
$user = 'root';
$pass = '';
$db_name = 'ship_voyages_db';

$conn = mysqli_connect($host, $user, $pass, $db_name);

// Перевірка з'єднання
if (!$conn) {
    // Якщо помилка, повертаємо JSON з помилкою і зупиняємо скрипт
    die(json_encode(['error' => 'Помилка підключення до БД: ' . mysqli_connect_error()]));
}

// Встановлюємо кодування UTF-8, щоб кирилиця відображалася коректно
mysqli_set_charset($conn, "utf8mb4");
?>