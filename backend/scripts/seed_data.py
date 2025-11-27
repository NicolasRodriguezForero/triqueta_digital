"""
Seed data script for Triqueta Digital MVP.
Creates initial data for testing and demo purposes.
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Usuario, Actividad, PerfilUsuario
from app.core.security import get_password_hash
import os
from datetime import datetime, timedelta


async def seed_database():
    """Seed database with initial data."""
    
    # Database URL
    database_url = os.getenv(
        'DATABASE_URL',
        'postgresql+asyncpg://triqueta_user:triqueta_pass@localhost:5432/triqueta_db'
    )
    
    print(f"🌱 Seeding database: {database_url}")
    
    engine = create_async_engine(database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # 1. Create admin user
        print("Creating admin user...")
        admin = Usuario(
            email="admin@triqueta.digital",
            hashed_password=get_password_hash("admin123"),
            is_admin=True
        )
        session.add(admin)
        await session.flush()
        
        admin_profile = PerfilUsuario(
            usuario_id=admin.id,
            nombre_completo="Admin Triqueta",
            localidad_preferida="Chapinero",
            nivel_actividad="medio"
        )
        session.add(admin_profile)
        
        # 2. Create regular users
        print("Creating regular users...")
        users_data = [
            {
                "email": "maria@example.com",
                "nombre": "María González",
                "password": "password123"
            },
            {
                "email": "carlos@example.com",
                "nombre": "Carlos Rodríguez",
                "password": "password123"
            },
            {
                "email": "ana@example.com",
                "nombre": "Ana Martínez",
                "password": "password123"
            }
        ]
        
        users = []
        for user_data in users_data:
            user = Usuario(
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                is_admin=False
            )
            session.add(user)
            await session.flush()
            
            profile = PerfilUsuario(
                usuario_id=user.id,
                nombre_completo=user_data["nombre"],
                localidad_preferida="Santa Fe",
                nivel_actividad="bajo"
            )
            session.add(profile)
            users.append(user)

        # 3. Create sample activities
        print("Creating sample activities...")
        activities = [
            Actividad(
                titulo="Ciclovía Chapinero",
                descripcion="Espacio recreativo para ciclistas todos los domingos en Chapinero. Horario: Domingos 7:00 AM - 2:00 PM",
                tipo="deporte",
                localidad="Chapinero",
                ubicacion_direccion="Carrera 7 desde Calle 72 hasta Calle 100",
                ubicacion_lat=4.6560663,
                ubicacion_lng=-74.0595918,
                fecha_inicio=datetime.now(),
                fecha_fin=datetime.now() + timedelta(days=365),
                precio=0.0,
                es_gratis=True,
                contacto="60112345678 - ciclovia@bogota.gov.co",
                etiquetas=["ciclismo", "deporte", "recreación", "familias"],
                fuente="Manual",
                estado="activa"
            ),
            Actividad(
                titulo="Cine al Parque",
                descripcion="Proyección gratuita de cine colombiano en parques de la ciudad. Horario: 19:00 - 21:00",
                tipo="cultura",
                localidad="Chapinero",
                ubicacion_direccion="Parque El Virrey",
                ubicacion_lat=4.672222,
                ubicacion_lng=-74.055556,
                fecha_inicio=datetime.now() + timedelta(days=7),
                fecha_fin=datetime.now() + timedelta(days=7),
                precio=0.0,
                es_gratis=True,
                contacto="60112345679 - cultura@bogota.gov.co",
                etiquetas=["cine", "cultura", "entretenimiento"],
                fuente="Manual",
                estado="activa"
            ),
            Actividad(
                titulo="Yoga en el Parque",
                descripcion="Clases gratuitas de yoga para todos los niveles. Horario: Sábados y domingos 8:00 AM - 10:00 AM",
                tipo="recreacion",
                localidad="Santa Fe",
                ubicacion_direccion="Parque de los Periodistas",
                ubicacion_lat=4.6019,
                ubicacion_lng=-74.0705,
                fecha_inicio=datetime.now(),
                fecha_fin=datetime.now() + timedelta(days=90),
                precio=0.0,
                es_gratis=True,
                contacto="60112345680 - recreacion@bogota.gov.co",
                etiquetas=["yoga", "bienestar", "salud"],
                fuente="Manual",
                estado="activa"
            ),
            Actividad(
                titulo="Concierto Sinfónica",
                descripcion="Concierto de la Orquesta Filarmónica de Bogotá. Horario: 20:00 - 22:00",
                tipo="cultura",
                localidad="La Candelaria",
                ubicacion_direccion="Teatro Colón - Calle 10",
                ubicacion_lat=4.5968,
                ubicacion_lng=-74.0746,
                fecha_inicio=datetime.now() + timedelta(days=14),
                fecha_fin=datetime.now() + timedelta(days=14),
                precio=30000.0,
                es_gratis=False,
                contacto="60112345681 - teatro@bogota.gov.co",
                enlace_externo="https://teatrocolon.gov.co",
                etiquetas=["música", "clásica", "orquesta"],
                fuente="Manual",
                estado="activa"
            ),
            Actividad(
                titulo="Taller de Pintura Comunitario",
                descripcion="Taller gratuito de pintura para todas las edades. Horario: Martes y jueves 10:00 AM - 12:00 PM",
                tipo="cultura",
                localidad="Santa Fe",
                ubicacion_direccion="Casa de la Cultura Santa Fe",
                ubicacion_lat=4.6100,
                ubicacion_lng=-74.0700,
                fecha_inicio=datetime.now() + timedelta(days=5),
                fecha_fin=datetime.now() + timedelta(days=60),
                precio=0.0,
                es_gratis=True,
                contacto="60112345682 - cultura@santafe.gov.co",
                etiquetas=["arte", "pintura", "taller"],
                fuente="Manual",
                estado="activa"
            ),
        ]
        
        for activity in activities:
            session.add(activity)
        await session.commit()
        
        print("✅ Database seeded successfully!")
        print(f"   - Created 1 admin user (admin@triqueta.digital / admin123)")
        print(f"   - Created {len(users)} regular users")
        print(f"   - Created {len(activities)} sample activities")
    
    await engine.dispose()


if __name__ == '__main__':
    print("🌱 Starting seed process...")
    asyncio.run(seed_database())
