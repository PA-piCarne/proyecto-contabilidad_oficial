<?php

declare(strict_types=1);

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/helpers.php';

const SECURITY_QUESTIONS = [
    'mascota' => '¿Cómo se llama tu primera mascota?',
    'madre' => '¿Cuál es el segundo nombre de tu madre?',
    'ciudad' => '¿En qué ciudad naciste?',
];

function handle_register(): void
{
    $username = trim($_POST['username'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $telefono = trim($_POST['telefono'] ?? '');
    $password = $_POST['password'] ?? '';
    $password2 = $_POST['password2'] ?? '';
    $pregunta = $_POST['pregunta_seguridad'] ?? '';
    $respuesta = trim($_POST['respuesta_seguridad'] ?? '');

    set_old($_POST);

    if ($username === '' || $email === '' || $telefono === '' || $password === '' || $password2 === '' || $pregunta === '' || $respuesta === '') {
        flash('error', 'Todos los campos son obligatorios.');
        redirect('/?page=register');
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        flash('error', 'Correo electrónico inválido.');
        redirect('/?page=register');
    }

    if (!preg_match('/^\d{10}$/', $telefono)) {
        flash('error', 'El teléfono debe tener exactamente 10 números.');
        redirect('/?page=register');
    }

    if (!array_key_exists($pregunta, SECURITY_QUESTIONS)) {
        flash('error', 'Pregunta de seguridad inválida.');
        redirect('/?page=register');
    }

    if (strlen($password) < 8) {
        flash('error', 'La contraseña debe tener al menos 8 caracteres.');
        redirect('/?page=register');
    }

    if ($password !== $password2) {
        flash('error', 'Las contraseñas no coinciden.');
        redirect('/?page=register');
    }

    $pdo = db();

    $exists = $pdo->prepare('SELECT id FROM usuarios WHERE username = :username OR email = :email LIMIT 1');
    $exists->execute(['username' => $username, 'email' => $email]);

    if ($exists->fetch()) {
        flash('error', 'El usuario o correo ya está registrado.');
        redirect('/?page=register');
    }

    $stmt = $pdo->prepare(
        'INSERT INTO usuarios (username, email, telefono, password_hash, pregunta_seguridad, respuesta_seguridad) VALUES (:username, :email, :telefono, :password_hash, :pregunta_seguridad, :respuesta_seguridad)'
    );

    $stmt->execute([
        'username' => $username,
        'email' => $email,
        'telefono' => $telefono,
        'password_hash' => password_hash($password, PASSWORD_DEFAULT),
        'pregunta_seguridad' => $pregunta,
        'respuesta_seguridad' => mb_strtolower($respuesta),
    ]);

    clear_old();
    flash('success', 'Usuario registrado correctamente.');
    redirect('/?page=login');
}

function handle_login(): void
{
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';

    if ($username === '' || $password === '') {
        flash('error', 'Todos los campos son obligatorios.');
        redirect('/?page=login');
    }

    $stmt = db()->prepare('SELECT id, username, email, password_hash FROM usuarios WHERE username = :username LIMIT 1');
    $stmt->execute(['username' => $username]);
    $user = $stmt->fetch();

    if (!$user || !password_verify($password, $user['password_hash'])) {
        flash('error', 'Usuario o contraseña incorrectos.');
        redirect('/?page=login');
    }

    $_SESSION['user'] = [
        'id' => (int) $user['id'],
        'username' => $user['username'],
        'email' => $user['email'],
    ];

    flash('success', 'Sesión iniciada correctamente.');
    redirect('/?page=menu');
}

function handle_logout(): void
{
    $_SESSION = [];
    if (ini_get('session.use_cookies')) {
        $params = session_get_cookie_params();
        setcookie(session_name(), '', time() - 42000, $params['path'], $params['domain'], $params['secure'], $params['httponly']);
    }
    session_destroy();
    session_start();
    flash('success', 'Sesión cerrada correctamente.');
    redirect('/?page=login');
}

function handle_password_reset(): void
{
    $step = $_POST['step'] ?? 'email';
    $email = trim($_POST['email'] ?? '');

    if ($step === 'email') {
        if ($email === '') {
            flash('error', 'Debe ingresar un correo.');
            redirect('/?page=password_reset');
        }

        $stmt = db()->prepare('SELECT id, email, pregunta_seguridad FROM usuarios WHERE email = :email LIMIT 1');
        $stmt->execute(['email' => $email]);
        $user = $stmt->fetch();

        if (!$user) {
            flash('error', 'No existe un usuario con ese correo.');
            redirect('/?page=password_reset');
        }

        $_SESSION['reset_email'] = $user['email'];
        redirect('/?page=password_reset&step=question');
    }

    if ($step === 'question') {
        $respuesta = trim($_POST['respuesta_seguridad'] ?? '');
        $newPassword = $_POST['nueva_password'] ?? '';
        $sessionEmail = $_SESSION['reset_email'] ?? '';

        if ($sessionEmail === '') {
            flash('error', 'La sesión de recuperación expiró.');
            redirect('/?page=password_reset');
        }

        if ($respuesta === '' || $newPassword === '') {
            flash('error', 'Todos los campos son obligatorios.');
            redirect('/?page=password_reset&step=question');
        }

        if (strlen($newPassword) < 8) {
            flash('error', 'La nueva contraseña debe tener al menos 8 caracteres.');
            redirect('/?page=password_reset&step=question');
        }

        $stmt = db()->prepare('SELECT id, respuesta_seguridad FROM usuarios WHERE email = :email LIMIT 1');
        $stmt->execute(['email' => $sessionEmail]);
        $user = $stmt->fetch();

        if (!$user || mb_strtolower($respuesta) !== $user['respuesta_seguridad']) {
            flash('error', 'La respuesta no coincide.');
            redirect('/?page=password_reset&step=question');
        }

        $update = db()->prepare('UPDATE usuarios SET password_hash = :password_hash WHERE id = :id');
        $update->execute([
            'password_hash' => password_hash($newPassword, PASSWORD_DEFAULT),
            'id' => $user['id'],
        ]);

        unset($_SESSION['reset_email']);
        flash('success', 'Contraseña cambiada correctamente.');
        redirect('/?page=login');
    }
}
