<h2>Registro</h2>
<p>Crea tu cuenta para acceder al sistema.</p>
<form method="post" action="/?page=register" class="form-grid">
  <div class="field">
    <label>Usuario</label>
    <input type="text" name="username" required value="<?= old('username') ?>">
  </div>

  <div class="field">
    <label>Correo</label>
    <input type="email" name="email" required value="<?= old('email') ?>">
  </div>

  <div class="field">
    <label>Teléfono (10 dígitos)</label>
    <input type="text" name="telefono" pattern="[0-9]{10}" maxlength="10" required value="<?= old('telefono') ?>">
  </div>

  <div class="field">
    <label>Pregunta de seguridad</label>
    <select name="pregunta_seguridad" required>
      <option value="">Seleccione…</option>
      <?php foreach (SECURITY_QUESTIONS as $key => $question): ?>
        <option value="<?= e($key) ?>" <?= old('pregunta_seguridad') === $key ? 'selected' : '' ?>><?= e($question) ?></option>
      <?php endforeach; ?>
    </select>
  </div>

  <div class="field full">
    <label>Respuesta de seguridad</label>
    <input type="text" name="respuesta_seguridad" required value="<?= old('respuesta_seguridad') ?>">
  </div>

  <div class="field">
    <label>Contraseña</label>
    <input type="password" name="password" required>
  </div>

  <div class="field">
    <label>Confirmar contraseña</label>
    <input type="password" name="password2" required>
  </div>

  <div class="field full mt">
    <button class="btn" type="submit">Crear cuenta</button>
  </div>
</form>
