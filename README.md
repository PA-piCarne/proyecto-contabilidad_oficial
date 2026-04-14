# Migración parcial a PHP + MySQL

Se agregó una versión en **PHP puro** del sistema para cubrir lo solicitado en la tarea: migrar autenticación (login, register y recuperación de contraseña) y cambiar de SQLite/DB Browser a **MySQL**.

## Lo migrado
- Registro de usuario con validaciones (correo, teléfono de 10 dígitos, contraseña, pregunta/respuesta de seguridad).
- Login con sesión PHP y contraseñas hasheadas.
- Logout.
- Recuperación de contraseña por correo + pregunta de seguridad.
- Conexión MySQL por PDO usando variables de entorno.
- Esquema SQL base para usuarios, empleados, rol de pagos, facturas y detalle de facturas.

## Estructura
- `php_app/public/index.php`: Front controller y rutas.
- `php_app/src/auth.php`: Lógica de autenticación.
- `php_app/config/database.php`: conexión a MySQL.
- `php_app/sql/schema.sql`: script de base de datos.

## Requisitos
- PHP 8.1+
- MySQL 8+

## Configuración
1. Crear la base y tablas:
   ```bash
   mysql -u root -p < php_app/sql/schema.sql
   ```
2. Exportar variables de conexión (si no usas valores por defecto):
   ```bash
   export DB_HOST=127.0.0.1
   export DB_PORT=3306
   export DB_NAME=contabilidad
   export DB_USER=root
   export DB_PASS=tu_password
   ```
3. Ejecutar el servidor:
   ```bash
   php -S 0.0.0.0:8000 -t php_app/public
   ```
4. Abrir en navegador:
   - `http://localhost:8000/?page=register`
   - `http://localhost:8000/?page=login`

## Nota
La base Django original se mantuvo en el repositorio para referencia, pero la nueva implementación PHP es funcional para el flujo de autenticación solicitado.
