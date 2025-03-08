-- Tabla de usuarios del banco
CREATE TABLE users (
    dni VARCHAR(255) PRIMARY KEY,         -- Identificador único del usuario
    nombre VARCHAR(255) NOT NULL,         -- Nombre del usuario
    apellidos VARCHAR(255) NOT NULL,      -- Apellidos del usuario
    email VARCHAR(255) UNIQUE NOT NULL,   -- Correo electrónico único del usuario
    telefono VARCHAR(255),                -- Número de teléfono del usuario
    fecha_registro DATETIME DEFAULT (CURRENT_TIMESTAMP)  -- Fecha de registro del usuario
);

-- Tabla de cuentas bancarias
CREATE TABLE accounts (
    iban VARCHAR(255) PRIMARY KEY,        -- Identificador único de la cuenta bancaria
    usuario_id VARCHAR(255) NOT NULL,     -- Usuario propietario de la cuenta (clave foránea a users)
    tipo VARCHAR(255) NOT NULL,           -- Tipo de cuenta (ej. corriente, ahorro)
    saldo REAL NOT NULL DEFAULT 0.0,      -- Saldo disponible en la cuenta
    moneda VARCHAR(255) NOT NULL,         -- Moneda de la cuenta
    fecha_creacion DATETIME DEFAULT (CURRENT_TIMESTAMP),  -- Fecha de apertura de la cuenta
    FOREIGN KEY (usuario_id) REFERENCES users(dni)  -- Relación con la tabla users
);

-- Tabla de transacciones bancarias
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único de la transacción
    cuenta_id VARCHAR(255) NOT NULL,       -- Cuenta asociada a la transacción (clave foránea a accounts)
    monto REAL NOT NULL,                   -- Monto de la transacción
    tipo VARCHAR(255) NOT NULL,            -- Tipo de transacción (ej. depósito, retiro)
    descripcion VARCHAR(255),              -- Descripción opcional de la transacción
    fecha DATETIME DEFAULT (CURRENT_TIMESTAMP),  -- Fecha de la transacción
    FOREIGN KEY (cuenta_id) REFERENCES accounts(iban)  -- Relación con la tabla accounts
);

-- Tabla de tarjetas bancarias
CREATE TABLE cards (
    numero VARCHAR(255) PRIMARY KEY,       -- Número único de la tarjeta
    account_id VARCHAR(255) NOT NULL,      -- Cuenta asociada a la tarjeta (clave foránea a accounts)
    tipo VARCHAR(255) NOT NULL,            -- Tipo de tarjeta (ej. débito, crédito)
    fecha_vencimiento DATETIME NOT NULL,   -- Fecha de vencimiento de la tarjeta
    cvv VARCHAR(255) NOT NULL,             -- Código de seguridad de la tarjeta
    FOREIGN KEY (account_id) REFERENCES accounts(iban)  -- Relación con la tabla accounts
);

-- Tabla de suscripciones de pago
CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único de la suscripción
    descripcion VARCHAR(255) NOT NULL,     -- Nombre o descripción de la suscripción (ej. Netflix)
    account_id VARCHAR(255) NOT NULL,      -- Cuenta bancaria asociada (clave foránea a accounts)
    monto REAL NOT NULL,                   -- Monto de pago por la suscripción
    fecha_renovacion INT NOT NULL,         -- Fecha de renovación (timestamp)
    renovar BOOLEAN NOT NULL,              -- Indica si se renueva automáticamente
    FOREIGN KEY (account_id) REFERENCES accounts(iban)  -- Relación con la tabla accounts
);

-- Tabla de préstamos bancarios
CREATE TABLE loans (
    id VARCHAR(255) PRIMARY KEY,           -- Identificador único del préstamo
    usuario_id VARCHAR(255) NOT NULL,      -- Usuario que solicitó el préstamo (clave foránea a users)
    monto REAL NOT NULL,                    -- Monto prestado
    tasa_interes REAL NOT NULL,            -- Tasa de interés aplicada
    plazo_meses INTEGER NOT NULL,          -- Plazo de pago en meses
    estado VARCHAR(255) NOT NULL,          -- Estado del préstamo (ej. pendiente, pagado)
    fecha_solicitud DATETIME DEFAULT (CURRENT_TIMESTAMP),  -- Fecha de solicitud
    FOREIGN KEY (usuario_id) REFERENCES users(dni)  -- Relación con la tabla users
);
