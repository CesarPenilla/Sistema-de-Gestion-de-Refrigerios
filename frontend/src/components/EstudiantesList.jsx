import { useState, useEffect } from 'react';
import { getEstudiantes } from '../services/api';
import '../styles/EstudiantesList.css';

function EstudiantesList() {
  const [estudiantes, setEstudiantes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [mostrarTodos, setMostrarTodos] = useState(false);

  useEffect(() => {
    fetchEstudiantes();
  }, [mostrarTodos]);

  const fetchEstudiantes = async () => {
    try {
      setLoading(true);
      // Mostrar solo activos por defecto, o todos si se solicita
      const response = await getEstudiantes(!mostrarTodos);
      setEstudiantes(response.data.results || response.data);
      setError(null);
    } catch (err) {
      setError('Error al cargar los estudiantes');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Cargando estudiantes...</div>;
  if (error) return <div className="alert alert-error">{error}</div>;

  return (
    <div className="card">
      <div className="estudiantes-header">
        <h2>Lista de Invitados</h2>
        <button
          className={`btn ${mostrarTodos ? 'btn-primary' : 'btn-success'}`}
          onClick={() => setMostrarTodos(!mostrarTodos)}
        >
          {mostrarTodos ? '✅ Ver Solo Activos' : '👥 Ver Todos'}
        </button>
      </div>
      
      <div className="alert alert-info" style={{ marginBottom: '1rem' }}>
        📋 Mostrando: <strong>{mostrarTodos ? 'Todos los visitantes' : 'Solo visitantes activos'}</strong>
        {' '}({estudiantes.length} {estudiantes.length === 1 ? 'visitante' : 'visitantes'})
      </div>

      <div className="alert" style={{ 
        marginBottom: '1rem', 
        backgroundColor: '#2a2a2a', 
        border: '1px solid #555',
        padding: '1rem'
      }}>
        <p style={{ margin: 0, color: '#aaa' }}>
          ℹ️ <strong>Nota:</strong> Los datos de visitantes provienen del sistema RICA y son de <strong>solo lectura</strong>. 
          Para modificar o eliminar visitantes, utiliza el software RICA en el puerto 8000.
        </p>
      </div>

      {estudiantes.length === 0 ? (
        <p>No hay visitantes {!mostrarTodos && 'activos'} registrados.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Identificación</th>
              <th>Email</th>
              <th>Estado</th>
              <th>Origen</th>
            </tr>
          </thead>
          <tbody>
            {estudiantes.map((estudiante) => (
              <tr key={estudiante.id}>
                <td>{estudiante.nombre}</td>
                <td>{estudiante.identificacion}</td>
                <td>{estudiante.email || <span style={{ color: '#888' }}>Sin email</span>}</td>
                <td>
                  <span style={{ 
                    padding: '0.3rem 0.6rem', 
                    borderRadius: '4px',
                    backgroundColor: estudiante.activo ? '#4CAF50' : '#888',
                    color: 'white',
                    fontSize: '0.85rem',
                    fontWeight: 'bold'
                  }}>
                    {estudiante.activo ? '✅ Activo' : '❌ Inactivo'}
                  </span>
                </td>
                <td>
                  <span style={{ 
                    color: '#888', 
                    fontSize: '0.85rem',
                    fontStyle: 'italic'
                  }}>
                    📡 RICA (Solo lectura)
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default EstudiantesList;
