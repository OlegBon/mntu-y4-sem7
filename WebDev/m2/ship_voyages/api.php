<?php

// Якщо це просто читання даних (GET), дозволяємо кеш на 60 секунд
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    header('Cache-Control: max-age=60'); 
} else {
    // Для POST/DELETE кеш заборонено
    header('Cache-Control: no-store, no-cache, must-revalidate');
}

// Вказуємо, що відповідь буде у форматі JSON
header('Content-Type: application/json');

// Підключаємо базу
require_once 'db.php';

// Отримуємо "дію" (action) з GET-параметра або POST
$action = $_GET['action'] ?? '';

// Отримуємо дані (READ + SEARCH)
if ($action === 'read') {
    $search = $_GET['search'] ?? ''; // Параметр пошуку

    if ($search) {
        // Реалізація пошуку
        // Захист від SQL Injection через Prepared Statements
        $sql = "SELECT * FROM voyages WHERE route LIKE ? ORDER BY created_at DESC";
        $stmt = mysqli_prepare($conn, $sql);
        $searchTerm = "%" . $search . "%";
        mysqli_stmt_bind_param($stmt, "s", $searchTerm);
        mysqli_stmt_execute($stmt);
        $result = mysqli_stmt_get_result($stmt);
    } else {
        // Якщо пошуку немає, виводимо все
        $sql = "SELECT * FROM voyages ORDER BY created_at DESC";
        $result = mysqli_query($conn, $sql);
    }

    $voyages = mysqli_fetch_all($result, MYSQLI_ASSOC);
    echo json_encode($voyages); // Повертаємо JSON
    exit;
}

// Додавання рейсу (CREATE)
if ($action === 'create' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    // Отримуємо дані
    $route = $_POST['route'] ?? '';
    $duration = $_POST['duration'] ?? '';
    $crew = intval($_POST['crew'] ?? 0);

    // Валідація на сервері
    if (empty($route) || empty($duration) || $crew <= 0) {
        echo json_encode(['success' => false, 'message' => 'Некоректні дані']);
        exit;
    }

    // Збереження в MySQL
    // Prepared Statements (Захист від SQL Injection)
    $sql = "INSERT INTO voyages (route, duration, crew, status) VALUES (?, ?, ?, 'Заплановано')";
    $stmt = mysqli_prepare($conn, $sql);
    mysqli_stmt_bind_param($stmt, "ssi", $route, $duration, $crew);

    if (mysqli_stmt_execute($stmt)) {
        // Повертаємо ID нового запису
        echo json_encode(['success' => true, 'id' => mysqli_insert_id($conn)]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Помилка БД']);
    }
    exit;
}

// Видалення рейсу (DELETE)
if ($action === 'delete' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = intval($_POST['id'] ?? 0);

    if ($id > 0) {
        $sql = "DELETE FROM voyages WHERE id = ?";
        $stmt = mysqli_prepare($conn, $sql);
        mysqli_stmt_bind_param($stmt, "i", $id);
        
        if (mysqli_stmt_execute($stmt)) {
            echo json_encode(['success' => true]);
        } else {
            echo json_encode(['success' => false]);
        }
    }
    exit;
}

// Очищення всіх рейсів (CLEAR ALL)
if ($action === 'clear' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    // Видаляємо всі записи з таблиці
    $sql = "DELETE FROM voyages"; 
    
    if (mysqli_query($conn, $sql)) {
        // Скидаємо лічильник ID (AUTO_INCREMENT), щоб нові рейси починалися з 1 (опціонально)
        mysqli_query($conn, "ALTER TABLE voyages AUTO_INCREMENT = 1");
        
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Помилка очищення']);
    }
    exit;
}

// Якщо дія невідома
echo json_encode(['error' => 'Invalid action']);
?>