<!-- <?php
require 'db.php'; // Підключаємо файл з'єднання до бази даних

echo "Супер! Підключення до бази даних успішне!";
?> -->

<?php
// Підключаємо файл з'єднання з БД
require 'db.php';

// Виконуємо запит на отримання всіх заявок
$sql = "SELECT * FROM requests";
$result = mysqli_query($conn, $sql);
?>

<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вантажні перевезення</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

<div class="container">
    <h1>Заявки на перевезення</h1>
    
    <a href="create.php" class="btn btn-primary">Додати заявку</a>
    <div class="table-responsive">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Клієнт</th>
                    <th>Вантаж</th>
                    <th>Вага (т)</th>
                    <th>Маршрут</th>
                    <th>Статус</th>
                    <th>Дії</th>
                </tr>
            </thead>
            <tbody>
                <?php 
                // Перевіряємо, чи є записи
                if (mysqli_num_rows($result) > 0): 
                    // Виводимо кожен рядок
                    while($row = mysqli_fetch_assoc($result)): ?>
                        <tr>
                            <td><?= $row['id'] ?></td>
                            <td><?= htmlspecialchars($row['client_name']) ?></td>
                            <td><?= htmlspecialchars($row['cargo_description']) ?></td>
                            <td><?= $row['weight'] ?></td>
                            <td><?= htmlspecialchars($row['route_start']) . ' -> ' . htmlspecialchars($row['route_end']) ?></td>
                            <td>
                                <span class="status-badge"><?= $row['status'] ?></span>
                            </td>
                            <td>
                                <a href="edit.php?id=<?= $row['id'] ?>" class="btn-small btn-warning">Ред.</a>
                                <button class="btn-small btn-danger" onclick="openModal(<?= $row['id'] ?>)">Вид.</button>
                            </td>
                        </tr>
                    <?php endwhile; 
                else: ?>
                    <tr>
                        <td colspan="7">Заявок поки немає.</td>
                    </tr>
                <?php endif; ?>
            </tbody>
        </table>
    </div>
</div>

<div id="deleteModal" class="modal-overlay">
    <div class="modal-content">
        <h3>Підтвердження</h3>
        <p>Ви дійсно хочете видалити цю заявку?</p>
        <p style="color: #666; font-size: 0.9em;">Цю дію неможливо скасувати.</p>
        
        <div class="modal-actions">
            <button class="btn btn-warning" onclick="closeModal()">Скасувати</button>
            
            <a href="#" id="confirmDeleteBtn" class="btn btn-danger">Так, видалити</a>
        </div>
    </div>
</div>

<script src="js/modal.js"></script>

</body>
</html>