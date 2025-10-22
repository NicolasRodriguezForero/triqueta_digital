-- ============================================
-- Script de Creación de Base de Datos
-- Proyecto: Triqueta Digital
-- Versión: 1.0
-- Base de Datos: PostgreSQL 15+
-- Fecha: Octubre 2025
-- ============================================

-- Habilitar extensiones
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "postgis";  -- Opcional, para funciones geoespaciales

-- ============================================
-- TABLA: usuarios
-- ============================================
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    foto_url VARCHAR(500),
    rol VARCHAR(50) DEFAULT 'usuario' CHECK (rol IN ('usuario', 'administrador')),
    estado VARCHAR(50) DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo', 'suspendido')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_rol ON usuarios(rol);
CREATE INDEX idx_usuarios_estado ON usuarios(estado);

COMMENT ON TABLE usuarios IS 'Cuentas de usuarios (ciudadanos y administradores)';
COMMENT ON COLUMN usuarios.id IS 'Identificador único del usuario';
COMMENT ON COLUMN usuarios.email IS 'Email único del usuario';
COMMENT ON COLUMN usuarios.password_hash IS 'Hash bcrypt de la contraseña';
COMMENT ON COLUMN usuarios.rol IS 'Rol del usuario: usuario o administrador';

-- ============================================
-- TABLA: perfiles_usuarios
-- ============================================
CREATE TABLE perfiles_usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    etiquetas_interes TEXT[],
    localidad_preferida VARCHAR(100),
    disponibilidad_horaria JSONB,
    nivel_actividad_preferido VARCHAR(50) CHECK (nivel_actividad_preferido IN ('bajo', 'medio', 'alto') OR nivel_actividad_preferido IS NULL),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_perfiles_user_id ON perfiles_usuarios(user_id);
CREATE INDEX idx_perfiles_etiquetas ON perfiles_usuarios USING GIN(etiquetas_interes);

COMMENT ON TABLE perfiles_usuarios IS 'Preferencias y configuración de usuarios';
COMMENT ON COLUMN perfiles_usuarios.etiquetas_interes IS 'Array de etiquetas de interés del usuario';
COMMENT ON COLUMN perfiles_usuarios.disponibilidad_horaria IS 'Horarios de disponibilidad en formato JSON';

-- ============================================
-- TABLA: actividades
-- ============================================
CREATE TABLE actividades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('cultura', 'deporte', 'recreacion')),
    fecha_inicio TIMESTAMP WITH TIME ZONE NOT NULL,
    fecha_fin TIMESTAMP WITH TIME ZONE,
    ubicacion_direccion VARCHAR(500) NOT NULL,
    ubicacion_lat DECIMAL(10, 8) NOT NULL CHECK (ubicacion_lat >= -90 AND ubicacion_lat <= 90),
    ubicacion_lng DECIMAL(11, 8) NOT NULL CHECK (ubicacion_lng >= -180 AND ubicacion_lng <= 180),
    localidad VARCHAR(100) NOT NULL CHECK (localidad IN ('Chapinero', 'Santa Fe', 'La Candelaria')),
    precio DECIMAL(10, 2) DEFAULT 0 CHECK (precio >= 0),
    es_gratis BOOLEAN DEFAULT TRUE,
    nivel_actividad VARCHAR(50) CHECK (nivel_actividad IN ('bajo', 'medio', 'alto') OR nivel_actividad IS NULL),
    etiquetas TEXT[] NOT NULL,
    contacto VARCHAR(255),
    enlace_externo VARCHAR(500),
    fuente VARCHAR(100) DEFAULT 'manual',
    estado VARCHAR(50) DEFAULT 'activa' CHECK (estado IN ('activa', 'inactiva', 'pendiente_validacion', 'rechazada')),
    popularidad_favoritos INTEGER DEFAULT 0,
    popularidad_vistas DECIMAL(10, 2) DEFAULT 0,
    popularidad_normalizada DECIMAL(5, 4) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fecha_fin_valida CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio)
);

CREATE INDEX idx_actividades_localidad ON actividades(localidad);
CREATE INDEX idx_actividades_tipo ON actividades(tipo);
CREATE INDEX idx_actividades_fecha_inicio ON actividades(fecha_inicio);
CREATE INDEX idx_actividades_estado ON actividades(estado);
CREATE INDEX idx_actividades_etiquetas ON actividades USING GIN(etiquetas);
CREATE INDEX idx_actividades_popularidad ON actividades(popularidad_normalizada DESC);

COMMENT ON TABLE actividades IS 'Catálogo de actividades culturales, deportivas y recreativas';
COMMENT ON COLUMN actividades.tipo IS 'Tipo: cultura, deporte, recreacion';
COMMENT ON COLUMN actividades.estado IS 'Estado: activa, inactiva, pendiente_validacion, rechazada';

-- ============================================
-- TABLA: favoritos
-- ============================================
CREATE TABLE favoritos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    actividad_id UUID NOT NULL REFERENCES actividades(id) ON DELETE CASCADE,
    fecha_guardado TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, actividad_id)
);

CREATE INDEX idx_favoritos_user_id ON favoritos(user_id);
CREATE INDEX idx_favoritos_actividad_id ON favoritos(actividad_id);
CREATE UNIQUE INDEX idx_favoritos_unique ON favoritos(user_id, actividad_id);

COMMENT ON TABLE favoritos IS 'Relación muchos-a-muchos entre usuarios y actividades favoritas';

-- ============================================
-- TABLA: refresh_tokens
-- ============================================
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_token_hash ON refresh_tokens(token_hash);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);

COMMENT ON TABLE refresh_tokens IS 'Refresh tokens para autenticación OAuth2';

-- ============================================
-- TABLA: etl_executions
-- ============================================
CREATE TABLE etl_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    finished_at TIMESTAMP WITH TIME ZONE,
    estado VARCHAR(50) DEFAULT 'corriendo' CHECK (estado IN ('corriendo', 'exitoso', 'error')),
    actividades_procesadas INTEGER DEFAULT 0,
    actividades_exitosas INTEGER DEFAULT 0,
    actividades_errores INTEGER DEFAULT 0,
    error_log TEXT,
    triggered_by UUID REFERENCES usuarios(id) ON DELETE SET NULL
);

CREATE INDEX idx_etl_started_at ON etl_executions(started_at DESC);
CREATE INDEX idx_etl_estado ON etl_executions(estado);

COMMENT ON TABLE etl_executions IS 'Logs de ejecuciones del proceso ETL';

-- ============================================
-- TABLA: dispositivos (Post-MVP)
-- ============================================
CREATE TABLE dispositivos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_code VARCHAR(50) UNIQUE NOT NULL,
    tipo VARCHAR(50) DEFAULT 'cubo',
    estado VARCHAR(50) DEFAULT 'disponible' CHECK (estado IN ('disponible', 'vinculado', 'inactivo')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_dispositivos_device_code ON dispositivos(device_code);

COMMENT ON TABLE dispositivos IS 'Catálogo de dispositivos IoT (cubos físicos)';

-- ============================================
-- TABLA: usuarios_dispositivos (Post-MVP)
-- ============================================
CREATE TABLE usuarios_dispositivos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    device_id UUID NOT NULL REFERENCES dispositivos(id) ON DELETE CASCADE,
    device_token TEXT,
    vinculado_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    desvinculado_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_usuarios_dispositivos_user_id ON usuarios_dispositivos(user_id);
CREATE INDEX idx_usuarios_dispositivos_device_id ON usuarios_dispositivos(device_id);
CREATE INDEX idx_usuarios_dispositivos_vinculado_at ON usuarios_dispositivos(vinculado_at);

COMMENT ON TABLE usuarios_dispositivos IS 'Vinculación entre usuarios y dispositivos IoT';

-- ============================================
-- TRIGGERS
-- ============================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a tablas
CREATE TRIGGER update_usuarios_updated_at 
    BEFORE UPDATE ON usuarios
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_perfiles_updated_at 
    BEFORE UPDATE ON perfiles_usuarios
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_actividades_updated_at 
    BEFORE UPDATE ON actividades
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- FIN DEL SCRIPT
-- ============================================

-- Verificar tablas creadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
