import { useState } from 'react';
import { Html5QrcodeScanner } from 'html5-qrcode';
import { validarCodigoQR } from '../services/api';
import { useEffect } from 'react';
import '../styles/QRScanner.css';

function QRScanner() {
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [scanner, setScanner] = useState(null);

  useEffect(() => {
    return () => {
      // Cleanup al desmontar el componente
      if (scanner) {
        scanner.clear().catch(err => console.error('Error clearing scanner:', err));
      }
    };
  }, [scanner]);

  const startScanning = () => {
    setScanning(true);
    setResult(null);
    setError(null);

    const qrScanner = new Html5QrcodeScanner(
      'qr-reader',
      { 
        fps: 10, 
        qrbox: { width: 250, height: 250 },
        aspectRatio: 1.0
      },
      false
    );

    qrScanner.render(onScanSuccess, onScanError);
    setScanner(qrScanner);
  };

  const stopScanning = () => {
    if (scanner) {
      scanner.clear().then(() => {
        setScanning(false);
        setScanner(null);
      }).catch(err => {
        console.error('Error al detener el escáner:', err);
      });
    }
  };

  const onScanSuccess = async (decodedText) => {
    console.log('QR escaneado:', decodedText);
    
    // Detener el escáner
    stopScanning();

    try {
      const response = await validarCodigoQR(decodedText);
      setResult({
        success: true,
        mensaje: response.data.mensaje,
        estudiante: response.data.estudiante,
        tipo_comida: response.data.tipo_comida,
        fecha_uso: response.data.fecha_uso
      });
      setError(null);
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Error al validar el código QR';
      setError(errorMsg);
      setResult(null);
    }
  };

  const onScanError = (err) => {
    // Ignorar errores de escaneo continuos
    if (err.includes('NotFoundException')) {
      return;
    }
    console.warn('Error de escaneo:', err);
  };

  const handleManualInput = async (e) => {
    e.preventDefault();
    const codigo = e.target.codigo.value;
    
    try {
      const response = await validarCodigoQR(codigo);
      setResult({
        success: true,
        mensaje: response.data.mensaje,
        estudiante: response.data.estudiante,
        tipo_comida: response.data.tipo_comida,
        fecha_uso: response.data.fecha_uso
      });
      setError(null);
      e.target.reset();
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Error al validar el código QR';
      setError(errorMsg);
      setResult(null);
    }
  };

  return (
    <div className="card">
      <h2>Escanear Código QR</h2>

      {error && <div className="alert alert-error">{error}</div>}
      {result && (
        <div className="alert alert-success">
          <h3>✅ {result.mensaje}</h3>
          <p><strong>Estudiante:</strong> {result.estudiante}</p>
          <p><strong>Tipo de comida:</strong> {result.tipo_comida}</p>
          <p><strong>Fecha de uso:</strong> {new Date(result.fecha_uso).toLocaleString()}</p>
        </div>
      )}

      <div style={{ marginBottom: '2rem' }}>
        {!scanning ? (
          <button className="btn btn-primary" onClick={startScanning}>
            Iniciar Escáner de Cámara
          </button>
        ) : (
          <button className="btn btn-danger" onClick={stopScanning}>
            Detener Escáner
          </button>
        )}
      </div>

      <div id="qr-reader" style={{ marginBottom: '2rem' }}></div>

      <div className="card" style={{ marginTop: '2rem' }}>
        <h3>O ingresar código manualmente</h3>
        <form onSubmit={handleManualInput}>
          <div className="form-group">
            <label htmlFor="codigo">Código UUID</label>
            <input
              type="text"
              id="codigo"
              name="codigo"
              placeholder="Ej: 550e8400-e29b-41d4-a716-446655440000"
              required
            />
          </div>
          <button type="submit" className="btn btn-success">
            Validar Código
          </button>
        </form>
      </div>
    </div>
  );
}

export default QRScanner;
