<?php

declare(strict_types=1);

require_once __DIR__ . '/../config/session.php';
require_once __DIR__ . '/../src/helpers.php';
require_once __DIR__ . '/../src/auth.php';

$page = $_GET['page'] ?? 'home';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if ($page === 'register') {
        handle_register();
    }

    if ($page === 'login') {
        handle_login();
    }

    if ($page === 'password_reset') {
        handle_password_reset();
    }
}

if ($page === 'logout') {
    handle_logout();
}

$viewPath = __DIR__ . '/../templates/' . $page . '.php';
$protected = ['menu'];

if (in_array($page, $protected, true)) {
    require_auth();
}

if (!is_file($viewPath)) {
    http_response_code(404);
    $viewPath = __DIR__ . '/../templates/404.php';
}

$flashes = get_flashes();

require __DIR__ . '/../templates/layout_header.php';
require $viewPath;
require __DIR__ . '/../templates/layout_footer.php';
