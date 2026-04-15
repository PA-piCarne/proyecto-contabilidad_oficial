<h2>Estado del sistema</h2>
<p><strong>Motor detectado:</strong> PHP <?= e(PHP_VERSION) ?></p>
<p><strong>SAPI:</strong> <?= e(PHP_SAPI) ?></p>

<?php
$dbOk = null;
$dbMessage = '';
if (isset($_GET['check_db']) && $_GET['check_db'] === '1') {
    try {
        $pdo = db();
        $stmt = $pdo->query('SELECT DATABASE() AS db_name, VERSION() AS mysql_version');
        $row = $stmt->fetch();
        $dbOk = true;
        $dbMessage = 'Conexión OK a MySQL. Base actual: ' . ($row['db_name'] ?? 'N/A') . ' | Versión MySQL: ' . ($row['mysql_version'] ?? 'N/A');
    } catch (Throwable $e) {
        $dbOk = false;
        $dbMessage = 'No se pudo conectar a MySQL: ' . $e->getMessage();
    }
}
?>

<p>
  <a href="/?page=status&check_db=1">Probar conexión MySQL ahora</a>
</p>

<?php if ($dbOk === true): ?>
  <div class="flash success"><?= e($dbMessage) ?></div>
<?php elseif ($dbOk === false): ?>
  <div class="flash error"><?= e($dbMessage) ?></div>
<?php endif; ?>

<p>Si esta pantalla carga, el proyecto ya se está ejecutando con PHP.</p>
