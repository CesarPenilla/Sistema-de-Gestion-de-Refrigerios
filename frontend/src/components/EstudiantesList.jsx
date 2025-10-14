import { useState, useEffect } from 'react';
import { getEstudiantes, deleteEstudiante } from '../services/api';
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

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar este estudiante?')) {
      try {
        await deleteEstudiante(id);
        fetchEstudiantes();
      } catch (err) {
        alert('Error al eliminar el estudiante');
        console.error(err);
      }
    }
  };

  if (loading) return <div className="loading">Cargando estudiantes...</div>;
  if (error) return <div className="alert alert-error">{error}</div>;

  return (
    <div className="card">
      <div className="estudiantes-header">
        <h2>Lista de Estudiantes</h2>
        <button
          className={`btn ${mostrarTodos ? 'btn-primary' : 'btn-success'}`}
          onClick={() => setMostrarTodos(!mostrarTodos)}
        >
          {mostrarTodos ? '✅ Ver Solo Activos' : '👥 Ver Todos'}
        </button>
      </div>
      
      <div className="alert alert-info" style={{ marginBottom: '1rem' }}>
        Mostrando: <strong>{mostrarTodos ? 'Todos los estudiantes' : 'Solo estudiantes activos'}</strong>
        {' '}({estudiantes.length} {estudiantes.length === 1 ? 'estudiante' : 'estudiantes'})
      </div>

      {estudiantes.length === 0 ? (
        <p>No hay estudiantes {!mostrarTodos && 'activos'} registrados.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Identificación</th>
              <th>Email</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {estudiantes.map((estudiante) => (
              <tr key={estudiante.id}>
                <td>{estudiante.nombre}</td>
                <td>{estudiante.identificacion}</td>
                <td>{estudiante.email}</td>
                <td>{estudiante.activo ? '✅ Activo' : '❌ Inactivo'}</td>
                <td>
                  <button
                    className="btn btn-danger"
                    onClick={() => handleDelete(estudiante.id)}
                  >
                    Eliminar
                  </button>
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
