<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sistema Contable (PHP + MySQL)</title>
  <style>
    body{font-family:Arial,sans-serif;background:#f3f4f6;margin:0}
    .container{max-width:900px;margin:2rem auto;background:white;padding:1.5rem;border-radius:8px}
    .nav a{margin-right:12px}
    .flash{padding:.7rem;border-radius:6px;margin:.6rem 0}
    .error{background:#fee2e2}
    .success{background:#dcfce7}
    input,select{display:block;width:100%;max-width:440px;padding:.5rem;margin:.25rem 0 .85rem}
    button{padding:.6rem 1rem;cursor:pointer}
  </style>
</head>
<body>
<div class="container">
  <div class="nav">
    <a href="/?page=home">Inicio</a>
    <?php if (current_user()): ?>
      <a href="/?page=menu">Menú</a>
      <a href="/?page=logout">Salir</a>
    <?php else: ?>
      <a href="/?page=login">Login</a>
      <a href="/?page=register">Registro</a>
    <?php endif; ?>
  </div>

  <?php foreach ($flashes as $flash): ?>
    <div class="flash <?= e($flash['type']) ?>"><?= e($flash['message']) ?></div>
  <?php endforeach; ?>
