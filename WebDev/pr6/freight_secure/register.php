<?php
require 'db.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = mysqli_real_escape_string($conn, $_POST['username']);
    $password = $_POST['password'];
    $password_hash = password_hash($password, PASSWORD_DEFAULT);

    $sql = "INSERT INTO users (username, password) VALUES ('$username', '$password_hash')";

    try {
        if (mysqli_query($conn, $sql)) {
            echo "<div style='color:green; text-align:center; margin-top:20px;'>
                    Користувач створений! <a href='login.php'>Увійти</a>
                  </div>";
        }
    } catch (mysqli_sql_exception $e) {
        // Код помилки 1062 означає Duplicate entry (Дублікат)
        if ($e->getCode() == 1062) {
            echo "<div style='color:red; text-align:center; margin-top:20px;'>
                    Користувач з таким логіном вже існує!
                  </div>";
        } else {
            echo "Помилка: " . $e->getMessage();
        }
    }
}
?>

<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Реєстрація</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container-small">
        <h1>Реєстрація адміна</h1>
        <form method="POST">
            <div class="form-group">
                <label>Логін:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Пароль:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Зареєструвати</button>
        </form>
    </div>
</body>
</html>