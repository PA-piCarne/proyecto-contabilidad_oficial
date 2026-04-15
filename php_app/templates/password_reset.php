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

  <form method="post" action="/?page=password_reset" class="form-grid">
    <input type="hidden" name="step" value="question">

    <div class="field full">
      <label>Respuesta de seguridad</label>
      <input type="text" name="respuesta_seguridad" required>
    </div>

    <div class="field full">
      <label>Nueva contraseña</label>
      <input type="password" name="nueva_password" required>
    </div>

    <div class="field full mt">
      <button class="btn" type="submit">Cambiar contraseña</button>
    </div>
  </form>
<?php else: ?>
  <p>Ingresa tu correo para validar tu identidad.</p>
  <form method="post" action="/?page=password_reset" class="form-grid">
    <input type="hidden" name="step" value="email">

    <div class="field full">
      <label>Correo registrado</label>
      <input type="email" name="email" required>
    </div>

    <div class="field full mt">
      <button class="btn" type="submit">Validar correo</button>
    </div>
  </form>
<?php endif; ?>
