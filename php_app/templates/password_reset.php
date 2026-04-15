<?php
$step = $_GET['step'] ?? 'email';
$email = $_SESSION['reset_email'] ?? '';

if ($step === 'question' && $email !== '') {
    $stmt = db()->prepare('SELECT pregunta_seguridad FROM usuarios WHERE email = :email LIMIT 1');
    $stmt->execute(['email' => $email]);
    $row = $stmt->fetch();
    $pregunta = $row ? (SECURITY_QUESTIONS[$row['pregunta_seguridad']] ?? '') : '';
}
?>

<h2>Recuperar contraseña</h2>

<?php if ($step === 'question' && $email !== ''): ?>
  <p><strong>Correo:</strong> <?= e($email) ?></p>
  <p><strong>Pregunta:</strong> <?= e($pregunta) ?></p>

  <form method="post" action="/?page=password_reset">
    <input type="hidden" name="step" value="question">

    <label>Respuesta de seguridad</label>
    <input type="text" name="respuesta_seguridad" required>

    <label>Nueva contraseña</label>
    <input type="password" name="nueva_password" required>

    <button type="submit">Cambiar contraseña</button>
  </form>
<?php else: ?>
  <form method="post" action="/?page=password_reset">
    <input type="hidden" name="step" value="email">

    <label>Correo registrado</label>
    <input type="email" name="email" required>

    <button type="submit">Validar correo</button>
  </form>
<?php endif; ?>
