<?php
session_start(); // Починаємо сесію
require 'db.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = mysqli_real_escape_string($conn, $_POST['username']);
    $password = $_POST['password'];

    // Шукаємо користувача
    $sql = "SELECT * FROM users WHERE username='$username'";
    $result = mysqli_query($conn, $sql);
    $user = mysqli_fetch_assoc($result);

    // Перевіряємо пароль
    if ($user && password_verify($password, $user['password'])) {
        // Успішний вхід!
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['username'] = $user['username'];
        
        header("Location: index.php");
        exit();
    } else {
        // Невірний логін або пароль
        $error = "Невірний логін або пароль";
    }
}
?>

<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вхід</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container-small">
        <h1>Вхід у систему</h1>
        
        <?php if (isset($error)): ?>
            <p style="color: red; text-align: center;"><?= $error ?></p>
        <?php endif; ?>

        <form method="POST">
            <div class="form-group">
                <label>Логін:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Пароль:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Увійти</button>
        </form>
    </div>
</body>
</html>