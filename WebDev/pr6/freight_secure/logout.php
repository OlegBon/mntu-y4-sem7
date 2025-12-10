<?php
session_start();
session_destroy(); // Знищуємо всі дані сесії
header("Location: login.php");
exit();
?>