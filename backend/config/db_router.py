"""
Database Router para dirigir modelos a sus bases de datos correspondientes.
- Visitante → rica_univalle (BD externa, solo lectura)
- CodigoQR, Estudiante y modelos de Django → default (refrigerio_local)
"""


class DatabaseRouter:
    """
    Router que dirige las operaciones de base de datos según el modelo
    """
    
    def db_for_read(self, model, **hints):
        """Dirigir operaciones de lectura"""
        if model._meta.app_label == 'event_management' and model.__name__ == 'Visitante':
            return 'rica_univalle'
        return 'default'
    
    def db_for_write(self, model, **hints):
        """Dirigir operaciones de escritura"""
        if model._meta.app_label == 'event_management' and model.__name__ == 'Visitante':
            # Visitante es solo lectura desde Django (se gestiona en el otro software)
            return 'rica_univalle'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Permitir relaciones si ambos modelos están en la misma BD
        """
        db_set = {'default', 'rica_univalle'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Controlar en qué BD se aplican migraciones
        """
        # Visitante no debe migrar (tabla ya existe en rica_univalle)
        if model_name == 'visitante':
            return db == 'rica_univalle'
        
        # Otros modelos de event_management migran en default
        if app_label == 'event_management':
            return db == 'default'
        
        # Modelos de Django (auth, sessions, etc.) van a default
        return db == 'default'
