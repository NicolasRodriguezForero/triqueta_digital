"""Update actividades and favoritos to use UUID and new schema

Revision ID: update_actividades_uuid
Revises: 3ff96ba0ec7a
Create Date: 2025-10-21 17:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = 'update_actividades_uuid'
down_revision = '3ff96ba0ec7a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade actividades and favoritos tables to use UUID and new schema."""
    
    # Drop existing tables to recreate with new schema
    # In production, you would migrate data, but for development we can drop
    op.drop_table('favoritos')
    op.drop_table('actividades')
    
    # Drop old enum types
    op.execute("DROP TYPE IF EXISTS tipoactividad CASCADE")
    op.execute("DROP TYPE IF EXISTS estadoactividad CASCADE")
    
    # Create actividades table with new schema
    op.create_table('actividades',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
        sa.Column('titulo', sa.String(length=255), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=False),
        sa.Column('tipo', sa.String(length=50), nullable=False),
        sa.Column('fecha_inicio', sa.DateTime(timezone=True), nullable=False),
        sa.Column('fecha_fin', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ubicacion_direccion', sa.String(length=500), nullable=False),
        sa.Column('ubicacion_lat', sa.DECIMAL(precision=10, scale=8), nullable=False),
        sa.Column('ubicacion_lng', sa.DECIMAL(precision=11, scale=8), nullable=False),
        sa.Column('localidad', sa.String(length=100), nullable=False),
        sa.Column('precio', sa.DECIMAL(precision=10, scale=2), nullable=False, server_default='0'),
        sa.Column('es_gratis', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('nivel_actividad', sa.String(length=50), nullable=True),
        sa.Column('etiquetas', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('contacto', sa.String(length=255), nullable=True),
        sa.Column('enlace_externo', sa.String(length=500), nullable=True),
        sa.Column('imagen_url', sa.String(length=500), nullable=True),
        sa.Column('fuente', sa.String(length=100), nullable=False, server_default='manual'),
        sa.Column('estado', sa.String(length=50), nullable=False, server_default='activa'),
        sa.Column('popularidad_favoritos', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('popularidad_vistas', sa.DECIMAL(precision=10, scale=2), nullable=False, server_default='0'),
        sa.Column('popularidad_normalizada', sa.DECIMAL(precision=5, scale=4), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for actividades
    op.create_index('idx_actividades_localidad', 'actividades', ['localidad'])
    op.create_index('idx_actividades_tipo', 'actividades', ['tipo'])
    op.create_index('idx_actividades_fecha_inicio', 'actividades', ['fecha_inicio'])
    op.create_index('idx_actividades_estado', 'actividades', ['estado'])
    op.create_index('idx_actividades_etiquetas', 'actividades', ['etiquetas'], postgresql_using='gin')
    op.create_index('idx_actividades_popularidad', 'actividades', ['popularidad_normalizada'])
    op.create_index(op.f('ix_actividades_id'), 'actividades', ['id'], unique=False)
    
    # Create favoritos table with new schema
    op.create_table('favoritos',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('actividad_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('fecha_guardado', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['actividad_id'], ['actividades.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('usuario_id', 'actividad_id', name='uq_usuario_actividad')
    )
    
    # Create indexes for favoritos
    op.create_index(op.f('ix_favoritos_id'), 'favoritos', ['id'], unique=False)
    op.create_index(op.f('ix_favoritos_usuario_id'), 'favoritos', ['usuario_id'], unique=False)
    op.create_index(op.f('ix_favoritos_actividad_id'), 'favoritos', ['actividad_id'], unique=False)


def downgrade() -> None:
    """Downgrade actividades and favoritos tables to previous schema."""
    
    # Drop new tables
    op.drop_table('favoritos')
    op.drop_table('actividades')
    
    # Recreate old enum types
    tipoactividad = postgresql.ENUM('CULTURAL', 'DEPORTIVA', 'RECREATIVA', 'EDUCATIVA', 'SOCIAL', name='tipoactividad')
    tipoactividad.create(op.get_bind())
    
    estadoactividad = postgresql.ENUM('ACTIVA', 'PENDIENTE', 'FINALIZADA', 'CANCELADA', name='estadoactividad')
    estadoactividad.create(op.get_bind())
    
    # Recreate old actividades table
    op.create_table('actividades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(length=255), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=False),
        sa.Column('tipo', tipoactividad, nullable=False),
        sa.Column('localidad', sa.String(length=100), nullable=False),
        sa.Column('direccion', sa.String(length=500), nullable=True),
        sa.Column('latitud', sa.Float(), nullable=True),
        sa.Column('longitud', sa.Float(), nullable=True),
        sa.Column('fecha_inicio', sa.Date(), nullable=False),
        sa.Column('fecha_fin', sa.Date(), nullable=True),
        sa.Column('hora_inicio', sa.Time(), nullable=True),
        sa.Column('hora_fin', sa.Time(), nullable=True),
        sa.Column('precio', sa.Float(), nullable=False),
        sa.Column('capacidad_maxima', sa.Integer(), nullable=True),
        sa.Column('etiquetas', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('estado', estadoactividad, nullable=False),
        sa.Column('organizador', sa.String(length=255), nullable=True),
        sa.Column('contacto_email', sa.String(length=255), nullable=True),
        sa.Column('contacto_telefono', sa.String(length=20), nullable=True),
        sa.Column('url_externa', sa.String(length=500), nullable=True),
        sa.Column('imagen_url', sa.String(length=500), nullable=True),
        sa.Column('popularidad', sa.Float(), nullable=False),
        sa.Column('vistas', sa.Integer(), nullable=False),
        sa.Column('fuente', sa.String(length=50), nullable=False),
        sa.Column('validado', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Recreate old favoritos table
    op.create_table('favoritos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('actividad_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['actividad_id'], ['actividades.id'], ),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('usuario_id', 'actividad_id', name='uq_usuario_actividad')
    )
