-- ============================================
-- Script de Datos de Prueba (Seed)
-- Proyecto: Triqueta Digital
-- ============================================

-- Limpiar datos existentes (solo para desarrollo)
TRUNCATE TABLE usuarios_dispositivos, dispositivos, favoritos, refresh_tokens, etl_executions, actividades, perfiles_usuarios, usuarios CASCADE;

-- ============================================
-- USUARIOS DE PRUEBA
-- ============================================

-- Usuario ciudadano
INSERT INTO usuarios (id, email, password_hash, nombre, rol, estado) VALUES
('11111111-1111-1111-1111-111111111111', 'maria.rodriguez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILSvU7JYq', 'María Rodríguez', 'usuario', 'activo'),
('22222222-2222-2222-2222-222222222222', 'carlos.gonzalez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILSvU7JYq', 'Carlos González', 'usuario', 'activo'),
('33333333-3333-3333-3333-333333333333', 'lucia.martinez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILSvU7JYq', 'Lucía Martínez', 'usuario', 'activo');

-- Usuario administrador
INSERT INTO usuarios (id, email, password_hash, nombre, rol, estado) VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'admin@triqueta.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILSvU7JYq', 'Administrador Triqueta', 'administrador', 'activo');

-- Nota: password_hash corresponde a "password123" - SOLO PARA DESARROLLO

-- ============================================
-- PERFILES DE USUARIOS
-- ============================================

INSERT INTO perfiles_usuarios (user_id, etiquetas_interes, localidad_preferida, nivel_actividad_preferido) VALUES
('11111111-1111-1111-1111-111111111111', ARRAY['arte', 'música', 'teatro'], 'Chapinero', 'medio'),
('22222222-2222-2222-2222-222222222222', ARRAY['deporte', 'ciclismo', 'running'], 'Santa Fe', 'alto'),
('33333333-3333-3333-3333-333333333333', ARRAY['cultura', 'cine', 'literatura'], 'La Candelaria', 'bajo');

-- ============================================
-- ACTIVIDADES DE PRUEBA
-- ============================================

-- Actividades Culturales en Chapinero
INSERT INTO actividades (id, titulo, descripcion, tipo, fecha_inicio, fecha_fin, ubicacion_direccion, ubicacion_lat, ubicacion_lng, localidad, precio, es_gratis, nivel_actividad, etiquetas, fuente, estado) VALUES
('a1111111-1111-1111-1111-111111111111', 
 'Concierto de Jazz en el Parque', 
 'Concierto gratuito de jazz al aire libre con bandas locales e internacionales. Evento familiar con zona de picnic.',
 'cultura',
 NOW() + INTERVAL '7 days',
 NOW() + INTERVAL '7 days' + INTERVAL '3 hours',
 'Parque El Virrey, Carrera 15 con Calle 88',
 4.665278,
 -74.056389,
 'Chapinero',
 0,
 TRUE,
 'bajo',
 ARRAY['música', 'jazz', 'aire libre', 'familia'],
 'manual',
 'activa');

INSERT INTO actividades (id, titulo, descripcion, tipo, fecha_inicio, fecha_fin, ubicacion_direccion, ubicacion_lat, ubicacion_lng, localidad, precio, es_gratis, nivel_actividad, etiquetas, fuente, estado) VALUES
('a2222222-2222-2222-2222-222222222222',
 'Exposición de Arte Contemporáneo',
 'Muestra de artistas colombianos emergentes. Entrada libre.',
 'cultura',
 NOW() + INTERVAL '3 days',
 NOW() + INTERVAL '30 days',
 'Casa Cultural Javeriana, Carrera 7 No. 40-62',
 4.630556,
 -74.065278,
 'Chapinero',
 0,
 TRUE,
 'bajo',
 ARRAY['arte', 'pintura', 'cultura', 'exposición'],
 'manual',
 'activa');

-- Actividades Deportivas en Santa Fe
INSERT INTO actividades (id, titulo, descripcion, tipo, fecha_inicio, fecha_fin, ubicacion_direccion, ubicacion_lat, ubicacion_lng, localidad, precio, es_gratis, nivel_actividad, etiquetas, fuente, estado) VALUES
('a3333333-3333-3333-3333-333333333333',
 'Ciclopaseo Nocturno',
 'Recorrido en bicicleta por las principales calles del centro histórico. Incluye refrigerio y guía.',
 'deporte',
 NOW() + INTERVAL '5 days',
 NOW() + INTERVAL '5 days' + INTERVAL '2 hours',
 'Plaza de Bolívar',
 4.598056,
 -74.075833,
 'Santa Fe',
 15000,
 FALSE,
 'medio',
 ARRAY['ciclismo', 'deporte', 'nocturno', 'centro'],
 'IDRD',
 'activa');

INSERT INTO actividades (id, titulo, descripcion, tipo, fecha_inicio, fecha_fin, ubicacion_direccion, ubicacion_lat, ubicacion_lng, localidad, precio, es_gratis, nivel_actividad, etiquetas, fuente, estado) VALUES
('a4444444-4444-4444-4444-444444444444',
 'Yoga en el Parque',
 'Clase de yoga para todos los niveles. Trae tu mat.',
 'deporte',
 NOW() + INTERVAL '2 days',
 NOW() + INTERVAL '2 days' + INTERVAL '1 hour',
 'Parque Nacional Olaya Herrera',
 4.630000,
 -74.062000,
 'Santa Fe',
 0,
 TRUE,
 'bajo',
 ARRAY['yoga', 'bienestar', 'meditación', 'aire libre'],
 'manual',
 'activa');

-- Actividades Recreativas en La Candelaria
INSERT INTO actividades (id, titulo, descripcion, tipo, fecha_inicio, fecha_fin, ubicacion_direccion, ubicacion_lat, ubicacion_lng, localidad, precio, es_gratis, nivel_actividad, etiquetas, fuente, estado) VALUES
('a5555555-5555-5555-5555-555555555555',
 'Tour Gastronómico del Centro',
 'Recorrido por restaurantes tradicionales con degustación incluida.',
 'recreacion',
 NOW() + INTERVAL '10 days',
 NOW() + INTERVAL '10 days' + INTERVAL '3 hours',
 'Plaza del Chorro de Quevedo',
 4.599167,
 -74.069167,
 'La Candelaria',
 35000,
 FALSE,
 'bajo',
 ARRAY['gastronomía', 'tour', 'comida', 'tradición'],
 'manual',
 'activa');

INSERT INTO actividades (id, titulo, descripcion, tipo, fecha_inicio, fecha_fin, ubicacion_direccion, ubicacion_lat, ubicacion_lng, localidad, precio, es_gratis, nivel_actividad, etiquetas, fuente, estado) VALUES
('a6666666-6666-6666-6666-666666666666',
 'Taller de Fotografía Urbana',
 'Aprende técnicas de fotografía callejera con fotógrafo profesional.',
 'recreacion',
 NOW() + INTERVAL '14 days',
 NOW() + INTERVAL '14 days' + INTERVAL '4 hours',
 'Museo Botero, Calle 11 No. 4-41',
 4.596389,
 -74.074167,
 'La Candelaria',
 25000,
 FALSE,
 'medio',
 ARRAY['fotografía', 'arte', 'taller', 'urbano'],
 'manual',
 'activa');

-- Actividad pendiente de validación
INSERT INTO actividades (id, titulo, descripcion, tipo, fecha_inicio, fecha_fin, ubicacion_direccion, ubicacion_lat, ubicacion_lng, localidad, precio, es_gratis, nivel_actividad, etiquetas, fuente, estado) VALUES
('a7777777-7777-7777-7777-777777777777',
 'Festival de Comida Asiática',
 'Evento gastronómico con restaurantes de comida asiática.',
 'recreacion',
 NOW() + INTERVAL '20 days',
 NOW() + INTERVAL '22 days',
 'Parque de los Hippies, Carrera 7 con Calle 60',
 4.653056,
 -74.059722,
 'Chapinero',
 0,
 TRUE,
 'bajo',
 ARRAY['gastronomía', 'comida', 'festival', 'asiática'],
 'importacion_csv',
 'pendiente_validacion');

-- ============================================
-- FAVORITOS
-- ============================================

-- María marca como favoritas actividades culturales
INSERT INTO favoritos (user_id, actividad_id) VALUES
('11111111-1111-1111-1111-111111111111', 'a1111111-1111-1111-1111-111111111111'),
('11111111-1111-1111-1111-111111111111', 'a2222222-2222-2222-2222-222222222222'),
('11111111-1111-1111-1111-111111111111', 'a6666666-6666-6666-6666-666666666666');

-- Carlos marca actividades deportivas
INSERT INTO favoritos (user_id, actividad_id) VALUES
('22222222-2222-2222-2222-222222222222', 'a3333333-3333-3333-3333-333333333333'),
('22222222-2222-2222-2222-222222222222', 'a4444444-4444-4444-4444-444444444444');

-- Lucía marca actividades recreativas
INSERT INTO favoritos (user_id, actividad_id) VALUES
('33333333-3333-3333-3333-333333333333', 'a5555555-5555-5555-5555-555555555555');

-- ============================================
-- ACTUALIZAR POPULARIDAD
-- ============================================

-- Actualizar contadores de favoritos
UPDATE actividades SET popularidad_favoritos = 3 WHERE id = 'a1111111-1111-1111-1111-111111111111';
UPDATE actividades SET popularidad_favoritos = 2 WHERE id = 'a2222222-2222-2222-2222-222222222222';
UPDATE actividades SET popularidad_favoritos = 2 WHERE id = 'a3333333-3333-3333-3333-333333333333';
UPDATE actividades SET popularidad_favoritos = 2 WHERE id = 'a4444444-4444-4444-4444-444444444444';
UPDATE actividades SET popularidad_favoritos = 1 WHERE id = 'a5555555-5555-5555-5555-555555555555';
UPDATE actividades SET popularidad_favoritos = 1 WHERE id = 'a6666666-6666-6666-6666-666666666666';

-- Simular vistas
UPDATE actividades SET popularidad_vistas = 15.5 WHERE id = 'a1111111-1111-1111-1111-111111111111';
UPDATE actividades SET popularidad_vistas = 12.3 WHERE id = 'a2222222-2222-2222-2222-222222222222';
UPDATE actividades SET popularidad_vistas = 8.7 WHERE id = 'a3333333-3333-3333-3333-333333333333';

-- Calcular popularidad normalizada (simplificado)
UPDATE actividades SET popularidad_normalizada = (popularidad_favoritos * 1.0 + popularidad_vistas * 0.1) / 20.0;

-- ============================================
-- ETL EXECUTIONS (Historial)
-- ============================================

INSERT INTO etl_executions (id, started_at, finished_at, estado, actividades_procesadas, actividades_exitosas, actividades_errores, triggered_by) VALUES
(gen_random_uuid(), NOW() - INTERVAL '7 days', NOW() - INTERVAL '7 days' + INTERVAL '5 minutes', 'exitoso', 50, 48, 2, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'),
(gen_random_uuid(), NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days' + INTERVAL '3 minutes', 'exitoso', 25, 25, 0, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa');

-- ============================================
-- DISPOSITIVOS IoT (Post-MVP)
-- ============================================

INSERT INTO dispositivos (id, device_code, tipo, estado) VALUES
('d1111111-1111-1111-1111-111111111111', 'TRIQ-CUBE-001', 'cubo', 'disponible'),
('d2222222-2222-2222-2222-222222222222', 'TRIQ-CUBE-002', 'cubo', 'vinculado');

-- Vincular dispositivo a María
INSERT INTO usuarios_dispositivos (user_id, device_id, device_token) VALUES
('11111111-1111-1111-1111-111111111111', 'd2222222-2222-2222-2222-222222222222', 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...');

-- Actualizar estado del dispositivo
UPDATE dispositivos SET estado = 'vinculado' WHERE id = 'd2222222-2222-2222-2222-222222222222';

-- ============================================
-- VERIFICACIONES
-- ============================================

-- Contar registros
SELECT 'usuarios' AS tabla, COUNT(*) AS total FROM usuarios
UNION ALL
SELECT 'perfiles_usuarios', COUNT(*) FROM perfiles_usuarios
UNION ALL
SELECT 'actividades', COUNT(*) FROM actividades
UNION ALL
SELECT 'favoritos', COUNT(*) FROM favoritos
UNION ALL
SELECT 'etl_executions', COUNT(*) FROM etl_executions
UNION ALL
SELECT 'dispositivos', COUNT(*) FROM dispositivos
UNION ALL
SELECT 'usuarios_dispositivos', COUNT(*) FROM usuarios_dispositivos;

-- ============================================
-- FIN DEL SCRIPT DE SEED
-- ============================================
