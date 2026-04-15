<h2>Registro</h2>
<form method="post" action="/?page=register">
  <label>Usuario</label>
  <input type="text" name="username" required value="<?= old('username') ?>">

  <label>Correo</label>
  <input type="email" name="email" required value="<?= old('email') ?>">

  <label>Teléfono (10 dígitos)</label>
  <input type="text" name="telefono" pattern="[0-9]{10}" maxlength="10" required value="<?= old('telefono') ?>">

  <label>Pregunta de seguridad</label>
  <select name="pregunta_seguridad" required>
    <option value="">Seleccione…</option>
    <?php foreach (SECURITY_QUESTIONS as $key => $question): ?>
      <option value="<?= e($key) ?>" <?= old('pregunta_seguridad') === $key ? 'selected' : '' ?>><?= e($question) ?></option>
    <?php endforeach; ?>
  </select>

  <label>Respuesta de seguridad</label>
  <input type="text" name="respuesta_seguridad" required value="<?= old('respuesta_seguridad') ?>">

  <label>Contraseña</label>
  <input type="password" name="password" required>

  <label>Confirmar contraseña</label>
  <input type="password" name="password2" required>

  <button type="submit">Crear cuenta</button>
</form>
