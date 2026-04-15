<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sistema Contable (PHP + MySQL)</title>
  <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
  <main class="page">
    <section class="card">
      <nav class="nav">
        <a href="/?page=home">Inicio</a>
        <a href="/?page=status">Estado</a>
        <?php if (current_user()): ?>
          <a href="/?page=menu">Menú</a>
          <a href="/?page=logout">Salir</a>
        <?php else: ?>
          <a href="/?page=login">Login</a>
          <a href="/?page=register">Registro</a>
        <?php endif; ?>
      </nav>

      <?php foreach ($flashes as $flash): ?>
        <div class="flash <?= e($flash['type']) ?>"><?= e($flash['message']) ?></div>
      <?php endforeach; ?>
