# Diseño del Sistema de Recomendación con Inteligencia Artificial

## Triqueta Digital

**Fecha:** Noviembre 2024  
**Estado:** Diseño Conceptual  
**Versión:** 1.0

---

## 📋 Tabla de Contenidos

1. [Análisis del Estado Actual](#1-análisis-del-estado-actual)
2. [Enfoques de Machine Learning para Recomendaciones](#2-enfoques-de-machine-learning-para-recomendaciones)
3. [Arquitectura del Sistema](#3-arquitectura-del-sistema)
4. [Datos Necesarios](#4-datos-necesarios)
5. [Estrategia de Recopilación de Datos](#5-estrategia-de-recopilación-de-datos)
6. [Modelos Propuestos](#6-modelos-propuestos)
7. [Pipeline de Entrenamiento](#7-pipeline-de-entrenamiento)
8. [Evaluación y Métricas](#8-evaluación-y-métricas)
9. [Estrategia de Despliegue](#9-estrategia-de-despliegue)
10. [Roadmap de Implementación](#10-roadmap-de-implementación)

---

## 1. Análisis del Estado Actual

### 1.1 Datos Disponibles Actualmente

#### **Datos de Usuarios:**

- ✅ **Perfil básico**: email, nombre, teléfono, biografía
- ✅ **Preferencias explícitas**:
  - `etiquetas_interes` (array de strings)
  - `localidad_preferida` (Chapinero, Santa Fe, La Candelaria)
  - `disponibilidad_horaria` (mañana, tarde, noche, fin_de_semana)
  - `nivel_actividad` (bajo, medio, alto)
- ✅ **Relaciones**: favoritos con timestamps

#### **Datos de Actividades:**

- ✅ **Contenido**: título, descripción, tipo, etiquetas
- ✅ **Ubicación**: dirección, coordenadas GPS, localidad
- ✅ **Temporal**: fecha_inicio, fecha_fin
- ✅ **Precio**: precio, es_gratis
- ✅ **Metadatos**: nivel_actividad, contacto, imagen_url, fuente
- ✅ **Métricas agregadas**: popularidad_favoritos, popularidad_vistas, popularidad_normalizada

#### **Interacciones Actuales:**

- ✅ **Favoritos**: usuario_id, actividad_id, fecha_guardado
- ✅ **Vistas**: registradas pero sin tracking individual (solo contador agregado)
- ❌ **No hay**: ratings explícitos, tiempo de visualización, clics, búsquedas guardadas

### 1.2 Limitaciones Actuales

1. **Datos de interacción limitados**: Solo favoritos explícitos, sin señales implícitas detalladas
2. **Sin tracking de comportamiento**: No se registra tiempo en página, scroll, clics en enlaces externos
3. **Sin feedback negativo**: No sabemos qué actividades NO le gustaron al usuario
4. **Cold start problem**: Usuarios nuevos sin historial
5. **Sparsity**: Muchos usuarios, muchas actividades, pocas interacciones

---

## 2. Enfoques de Machine Learning para Recomendaciones

### 2.1 Tipos de Sistemas de Recomendación

#### **A. Collaborative Filtering (CF)**

**Ventajas:**

- No requiere características de contenido
- Descubre patrones ocultos en interacciones
- Funciona bien con datos suficientes

**Desventajas:**

- Cold start problem (nuevos usuarios/actividades)
- Sparsity problem (matriz usuario-actividad muy dispersa)
- No explica por qué se recomienda

**Aplicabilidad en Triqueta:**

- ⚠️ Limitada inicialmente por falta de datos
- ✅ Útil cuando tengamos suficientes interacciones

#### **B. Content-Based Filtering**

**Ventajas:**

- Funciona con nuevos usuarios/actividades
- Explicable (basado en características)
- No requiere datos de otros usuarios

**Desventajas:**

- Limitado a características conocidas
- No descubre intereses nuevos
- Over-specialization

**Aplicabilidad en Triqueta:**

- ✅ Buena opción inicial (ya tenemos características)
- ✅ Complementa el sistema actual

#### **C. Hybrid Approach (Recomendado)**

**Combinación de:**

- Content-Based (etiquetas, localidad, tipo)
- Collaborative Filtering (similitud entre usuarios)
- Popularity-based (actividades trending)
- Deep Learning (embeddings, representaciones densas)

**Aplicabilidad en Triqueta:**

- ✅ **MEJOR OPCIÓN**: Combina fortalezas de ambos enfoques
- ✅ Mitiga cold start con content-based
- ✅ Mejora con más datos usando CF

### 2.2 Algoritmos Específicos Propuestos

#### **Opción 1: Matrix Factorization (SVD, NMF)**

- **Técnica**: Factorización de matriz usuario-actividad
- **Ventajas**: Simple, interpretable, escalable
- **Requisitos**: Matriz de interacciones densa
- **Uso**: Cuando tengamos ~1000+ interacciones

#### **Opción 2: Deep Learning (Neural Collaborative Filtering)**

- **Técnica**: Red neuronal para aprender embeddings
- **Ventajas**: Captura patrones complejos, no lineales
- **Requisitos**: Más datos, más recursos computacionales
- **Uso**: Fase avanzada con muchos datos

#### **Opción 3: Factorization Machines / Wide & Deep**

- **Técnica**: Combina features categóricas y numéricas
- **Ventajas**: Maneja features mixtas, explicable
- **Requisitos**: Features bien definidas
- **Uso**: **RECOMENDADO para inicio** - aprovecha datos existentes

#### **Opción 4: Two-Tower Architecture (Embeddings)**

- **Técnica**: Dos redes (usuario y actividad) que producen embeddings
- **Ventajas**: Escalable, permite búsqueda rápida (ANN)
- **Requisitos**: Datos de entrenamiento suficientes
- **Uso**: Fase de producción con muchos usuarios

---

## 3. Arquitectura del Sistema

### 3.1 Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND / API                            │
│              (FastAPI - Endpoint actual)                     │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              SERVICIO DE RECOMENDACIONES                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Recommendation Service (Actual)                      │  │
│  │  - Lógica híbrida simple                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ML Recommendation Service (Nuevo)                    │  │
│  │  - Modelo entrenado                                    │  │
│  │  - Predicciones en tiempo real                        │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬───────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   PostgreSQL │ │    Redis     │ │  ML Service  │
│   (Datos)    │ │   (Cache)    │ │  (Modelo)    │
└──────────────┘ └──────────────┘ └──────────────┘
        │                              │
        └──────────────┬───────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │  Feature Store       │
            │  (Features procesadas)│
            └──────────────────────┘
```

### 3.2 Componentes del Sistema ML

#### **A. Feature Engineering Pipeline**

- Extracción de features de usuarios
- Extracción de features de actividades
- Features de interacción (historial, frecuencia)
- Features temporales (día de semana, hora, estación)
- Features geográficas (distancia, densidad de actividades)

#### **B. Model Training Service**

- Entrenamiento offline (batch)
- Validación cruzada
- Selección de hiperparámetros
- Versionado de modelos

#### **C. Model Serving Service**

- API REST para predicciones
- Carga de modelos entrenados
- Preprocesamiento en tiempo real
- Post-procesamiento (filtros, diversidad)

#### **D. Monitoring & Evaluation**

- Métricas en tiempo real
- A/B testing framework
- Logging de predicciones
- Alertas de degradación

---

## 4. Datos Necesarios

### 4.1 Datos Actuales (Ya Disponibles)

#### **Features de Usuario:**

```python
user_features = {
    # Explícitas
    'etiquetas_interes': ['música', 'teatro', 'arte'],
    'localidad_preferida': 'Chapinero',
    'disponibilidad_horaria': 'tarde',
    'nivel_actividad': 'medio',

    # Implícitas (a calcular)
    'total_favoritos': 15,
    'diversidad_tipos': 0.67,  # tipos únicos / total favoritos
    'diversidad_localidades': 0.33,
    'antiguedad_cuenta_dias': 120,
    'frecuencia_actividad': 0.5,  # favoritos por semana
}
```

#### **Features de Actividad:**

```python
activity_features = {
    # Contenido
    'tipo': 'cultura',
    'etiquetas': ['música', 'concierto'],
    'nivel_actividad': 'medio',
    'localidad': 'Chapinero',

    # Temporal
    'fecha_inicio': '2024-11-25 19:00:00',
    'dia_semana': 1,  # lunes
    'hora': 19,
    'es_fin_de_semana': False,
    'dias_hasta_evento': 3,

    # Geográfico
    'lat': 4.6533,
    'lng': -74.0836,
    'precio': 0,
    'es_gratis': True,

    # Popularidad
    'popularidad_favoritos': 45,
    'popularidad_vistas': 12.5,
    'popularidad_normalizada': 0.75,

    # Texto (para NLP)
    'titulo': 'Concierto de Jazz',
    'descripcion': '...',
}
```

### 4.2 Datos que Necesitamos Recopilar

#### **A. Interacciones Explícitas (Alta Prioridad)**

1. **Ratings/Calificaciones**

   ```python
   class Rating(Base):
       usuario_id: int
       actividad_id: UUID
       rating: int  # 1-5 estrellas
       fecha: datetime
       comentario: Optional[str]
   ```

   - **Por qué**: Feedback directo de preferencia
   - **Cuándo**: Después de asistir a actividad o ver detalle

2. **Feedback Explícito**
   ```python
   class Feedback(Base):
       usuario_id: int
       actividad_id: UUID
       tipo: str  # 'like', 'dislike', 'maybe'
       fecha: datetime
   ```
   - **Por qué**: Señales positivas y negativas
   - **Cuándo**: En lista de recomendaciones o búsqueda

#### **B. Interacciones Implícitas (Alta Prioridad)**

1. **Eventos de Visualización Detallados**

   ```python
   class ActivityView(Base):
       usuario_id: Optional[int]  # null si anónimo
       actividad_id: UUID
       timestamp: datetime
       tiempo_en_pagina: int  # segundos
       scroll_depth: float  # 0-1
       clicks_enlace_externo: bool
       origen: str  # 'busqueda', 'recomendacion', 'favoritos', 'lista'
   ```

   - **Por qué**: Señal implícita de interés
   - **Cuándo**: Cada vez que se ve detalle de actividad

2. **Eventos de Búsqueda**

   ```python
   class SearchEvent(Base):
       usuario_id: Optional[int]
       query: str
       filtros: dict  # JSON
       resultados_encontrados: int
       actividades_clicked: List[UUID]
       timestamp: datetime
   ```

   - **Por qué**: Intención explícita del usuario
   - **Cuándo**: Cada búsqueda realizada

3. **Eventos de Navegación**
   ```python
   class NavigationEvent(Base):
       usuario_id: Optional[int]
       actividad_id: UUID
       accion: str  # 'view_list', 'apply_filter', 'sort_by'
       parametros: dict  # JSON
       timestamp: datetime
   ```
   - **Por qué**: Patrones de exploración
   - **Cuándo**: Interacciones con listas y filtros

#### **C. Datos Contextuales (Media Prioridad)**

1. **Datos Temporales Mejorados**

   - Día de la semana de interacción
   - Hora del día
   - Estación del año
   - Festivos/eventos especiales

2. **Datos Geográficos Mejorados**

   - Distancia desde ubicación del usuario (si disponible)
   - Densidad de actividades en área
   - Accesibilidad (transporte público)

3. **Datos de Dispositivo**
   ```python
   class UserSession(Base):
       usuario_id: Optional[int]
       device_type: str  # 'mobile', 'desktop', 'tablet'
       browser: str
       ip_address: str  # hasheado
       timestamp: datetime
   ```
   - **Por qué**: Contexto de uso
   - **Cuándo**: Cada sesión

#### **D. Datos de Resultado (Alta Prioridad)**

1. **Asistencia Real**
   ```python
   class Attendance(Base):
       usuario_id: int
       actividad_id: UUID
       asistio: bool
       fecha_asistencia: datetime
       rating_post_evento: Optional[int]
       comentario: Optional[str]
   ```
   - **Por qué**: Ground truth para validar recomendaciones
   - **Cuándo**: Después del evento (encuesta opcional)

---

## 5. Estrategia de Recopilación de Datos

### 5.1 Fase 1: Instrumentación Mínima (Inmediata)

**Objetivo**: Recopilar datos básicos sin cambios mayores en UX

#### **Implementar:**

1. ✅ **Tracking de vistas detalladas** (ya existe parcialmente)

   - Agregar: tiempo en página, scroll depth
   - Agregar: origen de la vista (recomendación vs búsqueda)

2. ✅ **Tracking de búsquedas**

   - Query, filtros aplicados, resultados clickeados

3. ✅ **Sistema de feedback rápido**
   - Botón "Me gusta" / "No me interesa" en recomendaciones
   - Sin requerir rating completo

#### **Métricas objetivo:**

- 1000+ eventos de visualización por semana
- 500+ búsquedas por semana
- 200+ feedbacks por semana

### 5.2 Fase 2: Engagement Mejorado (1-2 meses)

**Objetivo**: Aumentar calidad y cantidad de señales

#### **Implementar:**

1. **Sistema de ratings**

   - Rating 1-5 estrellas después de ver detalle
   - Opcional pero incentivado

2. **Tracking de asistencia**

   - Encuesta post-evento (opcional)
   - "¿Asististe a esta actividad?"

3. **Mejoras en tracking**
   - Tiempo de visualización preciso
   - Clicks en enlaces externos
   - Scroll completo

#### **Métricas objetivo:**

- 5000+ eventos por semana
- 1000+ ratings por semana
- 100+ confirmaciones de asistencia por semana

### 5.3 Fase 3: Datos Ricos (3-6 meses)

**Objetivo**: Datos suficientes para modelos avanzados

#### **Implementar:**

1. **Datos contextuales completos**

   - Ubicación del usuario (opcional, con consentimiento)
   - Historial de navegación completo

2. **A/B testing framework**

   - Comparar diferentes modelos
   - Medir impacto en engagement

3. **Feedback loop cerrado**
   - Recomendaciones → Interacción → Feedback → Mejora

#### **Métricas objetivo:**

- 10,000+ eventos por semana
- 2000+ ratings por semana
- 500+ asistencias confirmadas por semana

---

## 6. Modelos Propuestos

### 6.1 Modelo Inicial: Factorization Machines (FM)

**Justificación**:

- Maneja features categóricas y numéricas
- No requiere muchos datos para empezar
- Explicable y eficiente

**Arquitectura**:

```
Input Features:
├── Usuario Features (one-hot + embeddings)
│   ├── etiquetas_interes (multi-hot)
│   ├── localidad_preferida (categorical)
│   ├── nivel_actividad (categorical)
│   └── estadísticas (numéricas)
│
├── Actividad Features (one-hot + embeddings)
│   ├── tipo (categorical)
│   ├── etiquetas (multi-hot)
│   ├── localidad (categorical)
│   ├── nivel_actividad (categorical)
│   └── popularidad (numérica)
│
└── Interacción Features
    ├── distancia_usuario_actividad (numérica)
    ├── match_etiquetas (numérica)
    ├── match_localidad (binaria)
    └── dias_hasta_evento (numérica)

↓

Factorization Machine Layer
- Aprende interacciones entre features
- Embeddings de dimensión k (e.g., 32)

↓

Output: Probabilidad de interacción (0-1)
```

**Entrenamiento**:

- **Objetivo**: Predecir si usuario interactuará con actividad
- **Etiquetas**: 1 si favorito/rating alto, 0 si no interactuó o rating bajo
- **Algoritmo**: SGD o Adam optimizer
- **Regularización**: L2 para evitar overfitting

### 6.2 Modelo Intermedio: Wide & Deep Learning

**Justificación**:

- Combina memorización (wide) y generalización (deep)
- Mejor para datos mixtos
- Escalable

**Arquitectura**:

```
Wide Component (Memorización):
├── Features cruzadas importantes
│   ├── etiquetas_usuario × etiquetas_actividad
│   ├── localidad_usuario × localidad_actividad
│   └── tipo × nivel_actividad
└── Linear Model

Deep Component (Generalización):
├── Embeddings de features categóricas
├── Features numéricas normalizadas
├── Fully Connected Layers (3-4 capas)
│   ├── 128 → 64 → 32 → 16
│   └── ReLU activations
└── Output Layer

↓

Combinación: Wide + Deep → Probabilidad final
```

### 6.3 Modelo Avanzado: Two-Tower Neural Network

**Justificación**:

- Escalable a millones de usuarios/actividades
- Permite búsqueda rápida con ANN (Approximate Nearest Neighbors)
- State-of-the-art en sistemas de recomendación

**Arquitectura**:

```
User Tower:
├── User ID Embedding (lookup table)
├── User Features
│   ├── etiquetas_interes (embedding)
│   ├── localidad_preferida (embedding)
│   └── estadísticas (dense)
├── Fully Connected Layers
│   └── 64 → 32 → 16
└── User Embedding (16-dim)

Activity Tower:
├── Activity ID Embedding (lookup table)
├── Activity Features
│   ├── tipo (embedding)
│   ├── etiquetas (embedding)
│   ├── localidad (embedding)
│   └── popularidad (dense)
├── Fully Connected Layers
│   └── 64 → 32 → 16
└── Activity Embedding (16-dim)

↓

Similarity: Cosine(User Embedding, Activity Embedding)
```

**Ventajas**:

- Predicción rápida: solo calcular similitud
- Búsqueda eficiente: usar ANN (FAISS, Annoy)
- Escalable: embeddings pre-computados

### 6.4 Modelo Híbrido Final (Recomendado)

**Combinación de múltiples modelos**:

```
┌─────────────────────────────────────────┐
│     Ensemble de Modelos                  │
├─────────────────────────────────────────┤
│                                          │
│  1. Factorization Machine (30%)         │
│     - Features cruzadas                 │
│                                          │
│  2. Two-Tower Neural (50%)              │
│     - Embeddings de usuario/actividad   │
│                                          │
│  3. Content-Based Filter (10%)          │
│     - Similitud de etiquetas            │
│                                          │
│  4. Popularity Boost (10%)              │
│     - Actividades trending              │
│                                          │
└─────────────────────────────────────────┘
              ↓
    Weighted Average / Stacking
              ↓
    Score Final (0-1)
```

**Ventajas**:

- Robustez: múltiples modelos compensan errores
- Flexibilidad: ajustar pesos según performance
- Explicabilidad: cada componente aporta explicación

---

## 7. Pipeline de Entrenamiento

### 7.1 Pipeline Completo

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA COLLECTION                           │
│  PostgreSQL → Raw Events → Feature Store                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  FEATURE ENGINEERING                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ User Features│  │Activity Feat.│  │Interaction   │      │
│  │              │  │              │  │Features      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                       │                                      │
│                       ▼                                      │
│              Feature Store (Parquet/CSV)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  DATA PREPARATION                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Train/Val/   │  │ Negative     │  │ Data         │     │
│  │ Test Split   │  │ Sampling     │  │ Augmentation │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    MODEL TRAINING                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Hyperparameter│ │ Cross-        │  │ Model        │     │
│  │ Tuning        │ │ Validation   │  │ Selection    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    MODEL EVALUATION                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Metrics      │  │ A/B Testing  │  │ Error        │     │
│  │ Calculation  │  │ Framework    │  │ Analysis     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    MODEL DEPLOYMENT                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Model        │  │ Versioning  │  │ Monitoring   │       │
│  │ Serialization│  │ (MLflow)    │  │ (Prometheus)  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Feature Engineering Detallado

#### **A. User Features**

```python
def extract_user_features(user_id, db):
    user = get_user(user_id, db)
    profile = user.perfil
    favorites = get_user_favorites(user_id, db)

    features = {
        # Categóricas (one-hot encoding)
        'localidad_preferida_chapinero': 1 if profile.localidad_preferida == 'Chapinero' else 0,
        'localidad_preferida_santafe': 1 if profile.localidad_preferida == 'Santa Fe' else 0,
        'localidad_preferida_candelaria': 1 if profile.localidad_preferida == 'La Candelaria' else 0,
        'nivel_actividad_bajo': 1 if profile.nivel_actividad == 'bajo' else 0,
        'nivel_actividad_medio': 1 if profile.nivel_actividad == 'medio' else 0,
        'nivel_actividad_alto': 1 if profile.nivel_actividad == 'alto' else 0,

        # Multi-hot encoding para etiquetas
        'etiqueta_musica': 1 if 'música' in profile.etiquetas_interes else 0,
        'etiqueta_teatro': 1 if 'teatro' in profile.etiquetas_interes else 0,
        # ... para cada etiqueta posible

        # Numéricas
        'total_favoritos': len(favorites),
        'diversidad_tipos': len(set(f.tipo for f in favorites)) / max(len(favorites), 1),
        'diversidad_localidades': len(set(f.localidad for f in favorites)) / max(len(favorites), 1),
        'antiguedad_cuenta_dias': (datetime.now() - user.created_at).days,
        'frecuencia_favoritos_semana': len(favorites) / max((datetime.now() - user.created_at).days / 7, 1),

        # Estadísticas de favoritos
        'promedio_precio_favoritos': np.mean([f.precio for f in favorites]) if favorites else 0,
        'ratio_gratis_favoritos': sum(1 for f in favorites if f.es_gratis) / max(len(favorites), 1),
    }

    return features
```

#### **B. Activity Features**

```python
def extract_activity_features(activity_id, db):
    activity = get_activity(activity_id, db)

    features = {
        # Categóricas
        'tipo_cultura': 1 if activity.tipo == 'cultura' else 0,
        'tipo_deporte': 1 if activity.tipo == 'deporte' else 0,
        'tipo_recreacion': 1 if activity.tipo == 'recreacion' else 0,
        'localidad_chapinero': 1 if activity.localidad == 'Chapinero' else 0,
        # ... similar para otras localidades

        # Multi-hot para etiquetas
        'etiqueta_musica': 1 if 'música' in activity.etiquetas else 0,
        # ... para cada etiqueta

        # Numéricas
        'popularidad_favoritos': activity.popularidad_favoritos,
        'popularidad_vistas': float(activity.popularidad_vistas),
        'popularidad_normalizada': float(activity.popularidad_normalizada),
        'precio': float(activity.precio),
        'es_gratis': 1 if activity.es_gratis else 0,

        # Temporales
        'dias_hasta_evento': (activity.fecha_inicio - datetime.now()).days,
        'dia_semana': activity.fecha_inicio.weekday(),
        'hora': activity.fecha_inicio.hour,
        'es_fin_de_semana': 1 if activity.fecha_inicio.weekday() >= 5 else 0,

        # Geográficas
        'lat': float(activity.ubicacion_lat),
        'lng': float(activity.ubicacion_lng),
    }

    return features
```

#### **C. Interaction Features**

```python
def extract_interaction_features(user_id, activity_id, db):
    user = get_user(user_id, db)
    activity = get_activity(activity_id, db)
    user_favorites = get_user_favorites(user_id, db)

    # Match features
    user_tags = set(user.perfil.etiquetas_interes)
    activity_tags = set(activity.etiquetas)
    matching_tags = user_tags & activity_tags

    features = {
        # Match scores
        'match_etiquetas_count': len(matching_tags),
        'match_etiquetas_ratio': len(matching_tags) / max(len(user_tags), 1),
        'match_localidad': 1 if user.perfil.localidad_preferida == activity.localidad else 0,
        'match_nivel_actividad': 1 if user.perfil.nivel_actividad == activity.nivel_actividad else 0,
        'match_tipo': 1 if activity.tipo in [f.tipo for f in user_favorites] else 0,

        # Distancia (si tenemos ubicación del usuario)
        'distancia_km': calculate_distance(user_location, activity_location) if user_location else None,

        # Contexto temporal
        'match_disponibilidad': check_time_match(user.perfil.disponibilidad_horaria, activity.fecha_inicio),
    }

    return features
```

### 7.3 Negative Sampling

**Problema**: Solo tenemos interacciones positivas (favoritos). Necesitamos ejemplos negativos.

**Estrategias**:

1. **Random Negative Sampling**

   - Para cada positivo, muestrear N actividades aleatorias que el usuario NO favoritó
   - Ratio positivo:negativo = 1:4 (típico)

2. **Popularity-based Negative Sampling**

   - Muestrear actividades populares que el usuario NO vio
   - Más realista (es más probable que las haya visto)

3. **Hard Negative Sampling**
   - Actividades similares a favoritos pero que NO fueron favoritadas
   - Más difícil, mejora el modelo

```python
def generate_negative_samples(user_id, positive_interactions, all_activities, ratio=4):
    user_favorited_ids = {fav.actividad_id for fav in positive_interactions}

    # Actividades que el usuario NO favoritó
    negative_candidates = [
        act for act in all_activities
        if act.id not in user_favorited_ids and act.estado == 'activa'
    ]

    # Estrategia: 50% random, 50% popular
    n_negatives = len(positive_interactions) * ratio

    random_negatives = random.sample(negative_candidates, n_negatives // 2)

    popular_negatives = sorted(
        [act for act in negative_candidates if act not in random_negatives],
        key=lambda x: x.popularidad_normalizada,
        reverse=True
    )[:n_negatives // 2]

    return random_negatives + popular_negatives
```

### 7.4 Entrenamiento

```python
# Pseudocódigo de entrenamiento

# 1. Cargar datos
positive_samples = load_favorites()  # (user_id, activity_id, label=1)
all_activities = load_all_activities()

# 2. Generar muestras negativas
negative_samples = generate_negative_samples(positive_samples, all_activities)

# 3. Extraer features
X_train = []
y_train = []

for user_id, activity_id, label in positive_samples + negative_samples:
    user_features = extract_user_features(user_id)
    activity_features = extract_activity_features(activity_id)
    interaction_features = extract_interaction_features(user_id, activity_id)

    features = combine_features(user_features, activity_features, interaction_features)
    X_train.append(features)
    y_train.append(label)

# 4. Entrenar modelo
model = FactorizationMachine(n_features=len(X_train[0]), k=32)
model.fit(X_train, y_train, epochs=50, batch_size=256)

# 5. Evaluar
predictions = model.predict(X_test)
metrics = calculate_metrics(y_test, predictions)
```

---

## 8. Evaluación y Métricas

### 8.1 Métricas Offline

#### **A. Métricas de Clasificación**

- **AUC-ROC**: Área bajo curva ROC (mejor para ranking)
- **Precision@K**: Precisión en top K recomendaciones
- **Recall@K**: Cobertura en top K
- **F1-Score**: Balance entre precisión y recall

#### **B. Métricas de Ranking**

- **NDCG@K** (Normalized Discounted Cumulative Gain)

  - Mide calidad del ranking
  - Penaliza items relevantes en posiciones bajas
  - **Objetivo**: NDCG@10 > 0.5

- **MAP@K** (Mean Average Precision)

  - Promedio de precisión promedio
  - **Objetivo**: MAP@10 > 0.3

- **MRR** (Mean Reciprocal Rank)
  - Posición del primer item relevante
  - **Objetivo**: MRR > 0.4

#### **C. Métricas de Diversidad**

- **Coverage**: % de actividades recomendadas al menos una vez
- **Diversity**: Similitud promedio entre recomendaciones
- **Novelty**: Actividades poco populares recomendadas

### 8.2 Métricas Online (A/B Testing)

#### **A. Métricas de Engagement**

- **CTR** (Click-Through Rate): % de recomendaciones clickeadas
- **Conversion Rate**: % que agrega a favoritos
- **Time to Interaction**: Tiempo hasta primera interacción

#### **B. Métricas de Negocio**

- **Retention Rate**: % de usuarios que regresan
- **Session Length**: Duración promedio de sesión
- **Activities Discovered**: Nuevas actividades descubiertas

### 8.3 Framework de Evaluación

```python
class RecommendationEvaluator:
    def evaluate_offline(self, model, test_data):
        """Evaluación offline con métricas estándar"""
        predictions = model.predict(test_data)

        metrics = {
            'auc_roc': roc_auc_score(test_data.labels, predictions),
            'ndcg@10': ndcg_score(test_data, predictions, k=10),
            'map@10': map_score(test_data, predictions, k=10),
            'precision@10': precision_at_k(test_data, predictions, k=10),
            'recall@10': recall_at_k(test_data, predictions, k=10),
        }

        return metrics

    def evaluate_online(self, experiment_results):
        """Evaluación online de A/B test"""
        control_group = experiment_results['control']
        treatment_group = experiment_results['treatment']

        metrics = {
            'ctr_improvement': (
                treatment_group['ctr'] - control_group['ctr']
            ) / control_group['ctr'],
            'conversion_improvement': (
                treatment_group['conversion_rate'] - control_group['conversion_rate']
            ) / control_group['conversion_rate'],
            'statistical_significance': self.chi_square_test(
                control_group, treatment_group
            ),
        }

        return metrics
```

---

## 9. Estrategia de Despliegue

### 9.1 Arquitectura de Despliegue

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION ENVIRONMENT                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         FastAPI Backend (Actual)                      │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Recommendation Service                        │   │  │
│  │  │  - Fallback al sistema actual                  │   │  │
│  │  │  - Llamada a ML Service si disponible          │   │  │
│  │  └──────────────────────────────────────────────┘   │  │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         ML Serving Service (Nuevo)                     │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Model Loader                                 │   │  │
│  │  │  - Carga modelo entrenado                     │   │  │
│  │  │  - Versionado (MLflow)                        │   │  │
│  │  └──────────────────────────────────────────────┘   │  │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Prediction Service                           │   │  │
│  │  │  - Preprocesamiento                           │   │  │
│  │  │  - Predicción batch/online                    │   │  │
│  │  │  - Post-procesamiento                        │   │  │
│  │  └──────────────────────────────────────────────┘   │  │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Feature Store                                 │  │
│  │  - Features pre-computadas                           │  │
│  │  - Cache de embeddings                               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              TRAINING ENVIRONMENT (Offline)                 │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Data Pipeline                                        │ │
│  │  - ETL de PostgreSQL → Feature Store                 │ │
│  └──────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Training Pipeline                                   │ │
│  │  - Feature Engineering                               │ │
│  │  - Model Training                                    │ │
│  │  - Evaluation                                        │ │
│  └──────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Model Registry (MLflow)                             │ │
│  │  - Versionado de modelos                              │ │
│  │  - Tracking de experimentos                          │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 Estrategia de Rollout

#### **Fase 1: Shadow Mode (1-2 semanas)**

- Modelo ML corre en paralelo con sistema actual
- No afecta recomendaciones mostradas
- Comparar predicciones offline
- Validar latencia y performance

#### **Fase 2: A/B Testing (2-4 semanas)**

- 10% de tráfico al modelo ML
- 90% al sistema actual
- Medir métricas de engagement
- Ajustar según resultados

#### **Fase 3: Canary Deployment (1-2 semanas)**

- 50% de tráfico al modelo ML
- Monitoreo intensivo
- Rollback automático si métricas degradan

#### **Fase 4: Full Rollout**

- 100% de tráfico al modelo ML
- Sistema actual como fallback
- Monitoreo continuo

### 9.3 Monitoreo en Producción

#### **Métricas a Monitorear**:

1. **Latencia**: P95 < 100ms
2. **Throughput**: Requests por segundo
3. **Error Rate**: < 0.1%
4. **Cache Hit Rate**: > 80%
5. **Model Drift**: Cambios en distribución de features

#### **Alertas**:

- Latencia > 200ms
- Error rate > 1%
- Cache hit rate < 50%
- Degradación de métricas de negocio > 10%

---

## 10. Roadmap de Implementación

### 10.1 Fase 1: Preparación (Mes 1-2)

**Objetivos**:

- Instrumentar recopilación de datos
- Establecer infraestructura básica

**Tareas**:

1. ✅ Crear tablas para eventos de interacción
2. ✅ Implementar tracking de vistas detalladas
3. ✅ Implementar tracking de búsquedas
4. ✅ Crear Feature Store básico
5. ✅ Establecer pipeline de datos (ETL)

**Entregables**:

- Base de datos con eventos
- Dashboard de métricas de datos
- 1000+ eventos recopilados

### 10.2 Fase 2: Modelo MVP (Mes 3-4)

**Objetivos**:

- Entrenar primer modelo funcional
- Validar enfoque

**Tareas**:

1. ✅ Feature engineering completo
2. ✅ Implementar Factorization Machine
3. ✅ Pipeline de entrenamiento
4. ✅ Evaluación offline
5. ✅ API de predicción básica

**Entregables**:

- Modelo entrenado con AUC > 0.65
- API de predicción funcionando
- Reporte de evaluación

### 10.3 Fase 3: Integración (Mes 5-6)

**Objetivos**:

- Integrar modelo en producción
- A/B testing

**Tareas**:

1. ✅ Integración con backend FastAPI
2. ✅ Sistema de cache para predicciones
3. ✅ A/B testing framework
4. ✅ Monitoreo y alertas
5. ✅ Documentación

**Entregables**:

- Modelo en producción (shadow mode)
- Dashboard de monitoreo
- Resultados de A/B test

### 10.4 Fase 4: Optimización (Mes 7-12)

**Objetivos**:

- Mejorar modelo con más datos
- Optimizar performance

**Tareas**:

1. ✅ Recopilar más datos (objetivo: 10K+ eventos)
2. ✅ Experimentar con modelos avanzados (Wide & Deep, Two-Tower)
3. ✅ Optimizar features
4. ✅ Tuning de hiperparámetros
5. ✅ Implementar ensemble

**Entregables**:

- Modelo mejorado (AUC > 0.75)
- Sistema de recomendación híbrido
- Mejora medible en engagement

---

## 11. Consideraciones Técnicas

### 11.1 Stack Tecnológico Propuesto

#### **Machine Learning**:

- **Framework**: PyTorch o TensorFlow
- **Librerías**:
  - `scikit-learn` para modelos simples
  - `pytorch-fm` o `xlearn` para Factorization Machines
  - `tensorflow-recommenders` para modelos avanzados

#### **Feature Store**:

- **Opción 1**: PostgreSQL (simple, ya existe)
- **Opción 2**: Redis (rápido, para features frecuentes)
- **Opción 3**: Feast (feature store dedicado, avanzado)

#### **Model Serving**:

- **Opción 1**: FastAPI endpoint (simple, integrado)
- **Opción 2**: TensorFlow Serving (escalable)
- **Opción 3**: TorchServe (si usamos PyTorch)

#### **MLOps**:

- **MLflow**: Tracking de experimentos y versionado
- **Docker**: Contenedores para entrenamiento y serving
- **Kubernetes**: Orquestación (opcional, para escala)

### 11.2 Requisitos de Infraestructura

#### **Desarrollo**:

- CPU: 4+ cores
- RAM: 16GB+
- GPU: Opcional (acelera entrenamiento)

#### **Producción**:

- CPU: 8+ cores (para serving)
- RAM: 32GB+
- Storage: 100GB+ (modelos, features)

### 11.3 Costos Estimados

#### **Desarrollo**:

- Tiempo: 6-12 meses (1 desarrollador ML)
- Infraestructura: $50-200/mes (cloud)

#### **Producción**:

- Servidor ML: $100-500/mes
- Storage: $20-50/mes
- **Total**: ~$200-800/mes

---

## 12. Riesgos y Mitigaciones

### 12.1 Riesgos Identificados

1. **Falta de datos suficientes**

   - **Riesgo**: Modelo no aprende patrones útiles
   - **Mitigación**: Empezar con modelo simple, usar content-based como fallback

2. **Cold start problem**

   - **Riesgo**: Nuevos usuarios sin historial
   - **Mitigación**: Usar features de perfil, popularidad como fallback

3. **Model drift**

   - **Riesgo**: Modelo se vuelve obsoleto con el tiempo
   - **Mitigación**: Re-entrenamiento periódico (semanal/mensual)

4. **Latencia en producción**

   - **Riesgo**: Predicciones muy lentas
   - **Mitigación**: Cache agresivo, pre-computar embeddings

5. **Sesgo en recomendaciones**
   - **Riesgo**: Solo recomendar actividades populares
   - **Mitigación**: Métricas de diversidad, penalización de popularidad

### 12.2 Plan de Contingencia

- **Fallback**: Sistema actual siempre disponible
- **Rollback**: Capacidad de volver a versión anterior del modelo
- **Monitoring**: Alertas tempranas de degradación

---

## 13. Próximos Pasos Inmediatos

### 13.1 Esta Semana

1. ✅ Revisar y aprobar este diseño
2. ✅ Definir prioridades de implementación
3. ✅ Asignar recursos (desarrollador ML)

### 13.2 Este Mes

1. ✅ Crear tablas de eventos en base de datos
2. ✅ Implementar tracking básico
3. ✅ Establecer Feature Store
4. ✅ Recopilar primeros 1000 eventos

### 13.3 Próximos 3 Meses

1. ✅ Entrenar primer modelo MVP
2. ✅ Validar enfoque con datos reales
3. ✅ Preparar integración con backend

---

## 14. Conclusión

Este diseño propone un sistema de recomendación basado en ML que:

1. ✅ **Aprovecha datos existentes**: Usa features ya disponibles
2. ✅ **Escala gradualmente**: De simple a complejo según datos disponibles
3. ✅ **Mitiga riesgos**: Fallback y monitoreo continuo
4. ✅ **Es práctico**: Roadmap realista y alcanzable

**Recomendación**: Empezar con **Factorization Machines** como MVP, evolucionar a **Two-Tower Neural Network** cuando tengamos suficientes datos.

---

**Documento creado por**: AI Assistant  
**Fecha**: Noviembre 2024  
**Versión**: 1.0  
**Estado**: Propuesta - Pendiente de Revisión
