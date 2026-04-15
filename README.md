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
- `php_app/templates/status.php`: verificación de versión PHP y prueba de conexión a MySQL.

## Requisitos
- PHP 8.1+
- MySQL 8+
- MySQL Workbench (opcional para interfaz gráfica)

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
   - `http://localhost:8000/?page=status`

## ¿Cómo conectarlo en MySQL Workbench?
1. Abre MySQL Workbench.
2. Ve a **MySQL Connections** > **+**.
3. Configura:
   - **Connection Name:** `contabilidad_local`
   - **Hostname:** `127.0.0.1`
   - **Port:** `3306`
   - **Username:** `root` (o tu usuario)
4. Clic en **Test Connection** y escribe tu password.
5. Abre la conexión y ejecuta:
   ```sql
   USE contabilidad;
   SHOW TABLES;
   SELECT * FROM usuarios;
   ```

## ¿Cómo saber que está hecho en PHP?
- El servidor se levanta con el comando `php -S ...`.
- El front controller principal es `php_app/public/index.php`.
- La pantalla `/?page=status` muestra versión de PHP activa y permite probar conexión real a MySQL.

## Solución al error en Windows: `php no se reconoce`
Si PowerShell te muestra:
`php : El término 'php' no se reconoce...`
significa que **PHP no está instalado** o **no está agregado al PATH**.

### Opción A (recomendada): instalar PHP con Winget
1. Abre PowerShell como administrador.
2. Instala PHP:
   ```powershell
   winget install PHP.PHP
   ```
3. Cierra y vuelve a abrir PowerShell.
4. Verifica:
   ```powershell
   php -v
   ```
5. Si ya funciona, arranca servidor:
   ```powershell
   php -S 127.0.0.1:8000 -t php_app/public
   ```

### Opción B: usar XAMPP (si ya lo tienes)
1. Revisa si existe `C:\xampp\php\php.exe`.
2. Arranca así, usando ruta completa:
   ```powershell
   C:\xampp\php\php.exe -S 127.0.0.1:8000 -t php_app/public
   ```
3. Si funciona, agrega `C:\xampp\php` al PATH de Windows para poder usar `php` directamente.

### Opción C: instalación manual de PHP
1. Descarga PHP para Windows (zip) desde: https://windows.php.net/download/
2. Descomprime, por ejemplo en `C:\php`.
3. Agrega `C:\php` al PATH del sistema.
4. Abre una nueva consola y ejecuta:
   ```powershell
   php -v
   php -S 127.0.0.1:8000 -t php_app/public
   ```

### Verificación final
Cuando el servidor arranque, abre:
- `http://127.0.0.1:8000/?page=status`

Si ves versión de PHP y el estado del sistema, ya quedó correcto.


## Error: `could not find driver` (PDO MySQL)
Ese mensaje significa que PHP sí está corriendo, pero **no tiene habilitado el driver `pdo_mysql`**.

### Cómo arreglarlo en Windows (XAMPP)
1. Abre el archivo `C:\xampp\php\php.ini`.
2. Busca estas líneas y asegúrate de que estén activas (sin `;` al inicio):
   ```ini
   extension=pdo_mysql
   extension=mysqli
   ```
3. Guarda y reinicia Apache (o reinicia tu `php -S ...` si usas servidor embebido).
4. Verifica en consola:
   ```powershell
   php -m | findstr /I "pdo pdo_mysql mysqli"
   ```
5. Debes ver `PDO`, `pdo_mysql` y/o `mysqli` listados.

### Si usas PHP instalado con Winget
1. Ubica el `php.ini` activo:
   ```powershell
   php --ini
   ```
2. Edita ese `php.ini` y habilita:
   ```ini
   extension=pdo_mysql
   ```
3. Reinicia terminal y vuelve a levantar:
   ```powershell
   php -S 127.0.0.1:8000 -t php_app/public
   ```

## Nota
La base Django original se mantuvo en el repositorio para referencia, pero la nueva implementación PHP es funcional para el flujo de autenticación solicitado.
