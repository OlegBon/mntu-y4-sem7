<?php
require 'db.php';

if (isset($_GET['id'])) {
    $id = intval($_GET['id']);

    $sql = "DELETE FROM requests WHERE id=$id";

    if (mysqli_query($conn, $sql)) {
        header("Location: index.php");
    } else {
        echo "Помилка видалення: " . mysqli_error($conn);
    }
} else {
    header("Location: index.php");
}
?>