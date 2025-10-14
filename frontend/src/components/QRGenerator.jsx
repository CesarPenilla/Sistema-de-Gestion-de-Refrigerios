import { useState, useEffect } from 'react';
import { 
  getEstudiantes, 
  generarCodigosQR, 
  generarCodigosMasivo,
  getCodigosPorEstudiante, 
  getCodigoQRBase64 
} from '../services/api';
import '../styles/QRGenerator.css';

function QRGenerator() {
  const [estudiantes, setEstudiantes] = useState([]);
  const [selectedEstudiante, setSelectedEstudiante] = useState('');
  const [codigos, setCodigos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    fetchEstudiantes();
  }, []);

  const fetchEstudiantes = async () => {
    try {
      // Obtener solo estudiantes activos
      const response = await getEstudiantes(true);
      setEstudiantes(response.data.results || response.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleGenerar = async () => {
    if (!selectedEstudiante) {
      setError('Por favor selecciona un estudiante');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await generarCodigosQR(selectedEstudiante);
      setSuccess(response.data.mensaje);
      await handleVerCodigos();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al generar códigos QR');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerarMasivo = async () => {
    if (!window.confirm('¿Estás seguro de generar códigos QR para TODOS los estudiantes activos sin códigos?')) {
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setCodigos([]);
      const response = await generarCodigosMasivo();
      setSuccess(
        `${response.data.mensaje}\n` +
        `Total de códigos generados: ${response.data.total_codigos_generados}\n` +
        `Estudiantes procesados: ${response.data.estudiantes_procesados.length}`
      );
      // Recargar la lista de estudiantes
      await fetchEstudiantes();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al generar códigos masivos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleVerCodigos = async () => {
    if (!selectedEstudiante) {
      setError('Por favor selecciona un estudiante');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await getCodigosPorEstudiante(selectedEstudiante);
      
      // Obtener las imágenes en base64 para cada código
      const codigosConImagenes = await Promise.all(
        response.data.map(async (codigo) => {
          try {
            const imgResponse = await getCodigoQRBase64(codigo.id);
            return {
              ...codigo,
              imagen: imgResponse.data.imagen_base64
            };
          } catch (err) {
            console.error('Error al obtener imagen:', err);
            return codigo;
          }
        })
      );
      
      setCodigos(codigosConImagenes);
      setSuccess(null);
    } catch (err) {
      setError('Error al cargar códigos QR');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEstudianteChange = (e) => {
    setSelectedEstudiante(e.target.value);
    setCodigos([]);
    setError(null);
    setSuccess(null);
  };

  return (
    <div className="card">
      <h2>Generar Códigos QR</h2>

      {error && <div className="alert alert-error" style={{whiteSpace: 'pre-line'}}>{error}</div>}
      {success && <div className="alert alert-success" style={{whiteSpace: 'pre-line'}}>{success}</div>}

      {/* Sección de Generación Masiva */}
      <div className="card" style={{ marginBottom: '2rem', padding: '1.5rem' }}>
        <h3>🚀 Generación Masiva</h3>
        <p style={{ marginBottom: '1rem', color: '#aaa' }}>
          Genera códigos QR para <strong>todos los estudiantes activos</strong> que aún no tienen códigos.
        </p>
        <button
          className="btn btn-primary"
          onClick={handleGenerarMasivo}
          disabled={loading}
          style={{ width: '100%', padding: '1rem', fontSize: '1.1rem' }}
        >
          {loading ? '⏳ Generando...' : '🎫 Generar Códigos para Todos los Estudiantes Activos'}
        </button>
      </div>

      <hr style={{ margin: '2rem 0', borderColor: '#444' }} />

      {/* Sección de Generación Individual */}
      <h3>Generar para un Estudiante Específico</h3>
      
      <div className="form-group">
        <label htmlFor="estudiante">Seleccionar Estudiante Activo</label>
        <select
          id="estudiante"
          value={selectedEstudiante}
          onChange={handleEstudianteChange}
        >
          <option value="">-- Seleccionar --</option>
          {estudiantes.map((est) => (
            <option key={est.id} value={est.id}>
              {est.nombre} - {est.identificacion}
            </option>
          ))}
        </select>
        {estudiantes.length === 0 && (
          <p style={{ color: '#888', marginTop: '0.5rem' }}>
            No hay estudiantes activos disponibles
          </p>
        )}
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem', flexWrap: 'wrap' }}>
        <button
          className="btn btn-primary"
          onClick={handleGenerar}
          disabled={loading || !selectedEstudiante}
        >
          {loading ? 'Generando...' : 'Generar Códigos QR'}
        </button>

        <button
          className="btn btn-success"
          onClick={handleVerCodigos}
          disabled={loading || !selectedEstudiante}
        >
          Ver Códigos Existentes
        </button>
      </div>

      {codigos.length > 0 && (
        <div className="qr-grid">
          {codigos.map((codigo) => (
            <div key={codigo.id} className="qr-container card">
              <h3>{codigo.tipo_comida}</h3>
              {codigo.imagen ? (
                <img
                  src={codigo.imagen}
                  alt={`QR ${codigo.tipo_comida}`}
                  className="qr-image"
                />
              ) : (
                <p>Imagen no disponible</p>
              )}
              <p>Estado: {codigo.usado ? '❌ Usado' : '✅ Disponible'}</p>
              {codigo.fecha_uso && (
                <p>Usado el: {new Date(codigo.fecha_uso).toLocaleString()}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default QRGenerator;
