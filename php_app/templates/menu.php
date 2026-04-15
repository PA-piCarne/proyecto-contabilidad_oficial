<?php $user = current_user(); ?>
<h2>Menú principal</h2>
<p>Bienvenido, <strong><?= e($user['username'] ?? '') ?></strong>.</p>
<ul class="clean">
  <li>Módulo empleados (pendiente de migración completa)</li>
  <li>Módulo rol de pagos (pendiente de migración completa)</li>
  <li>Módulo facturación (pendiente de migración completa)</li>
</ul>
