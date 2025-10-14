import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createEstudiante } from '../services/api';
import '../styles/EstudianteForm.css';

function EstudianteForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    nombre: '',
    identificacion: '',
    email: '',
    activo: true,
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createEstudiante(formData);
      setSuccess(true);
      setError(null);
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (err) {
      setError('Error al crear el estudiante. Verifica que la identificación y el email sean únicos.');
      setSuccess(false);
      console.error(err);
    }
  };

  return (
    <div className="card">
      <h2>Nuevo Estudiante</h2>
      
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">¡Estudiante creado exitosamente!</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="nombre">Nombre Completo *</label>
          <input
            type="text"
            id="nombre"
            name="nombre"
            value={formData.nombre}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="identificacion">Número de Identificación *</label>
          <input
            type="text"
            id="identificacion"
            name="identificacion"
            value={formData.identificacion}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Correo Electrónico *</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              name="activo"
              checked={formData.activo}
              onChange={handleChange}
            />
            {' '}Activo
          </label>
        </div>

        <button type="submit" className="btn btn-primary">
          Crear Estudiante
        </button>
      </form>
    </div>
  );
}

export default EstudianteForm;
