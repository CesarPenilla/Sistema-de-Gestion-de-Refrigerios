import { useState, useEffect, useRef } from 'react';
import { Html5QrcodeScanner } from 'html5-qrcode';
import { validarCodigoQR } from '../services/api';
import '../styles/QRScanner.css';

function QRScanner() {
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [scanner, setScanner] = useState(null);
  const inputRef = useRef(null);

  useEffect(() => {
    // Auto-focus en el campo de entrada cuando se monta el componente
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  useEffect(() => {
    // Re-focus después de mostrar resultado o error
    if (result || error) {
      const timer = setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.focus();
        }
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [result, error]);

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
    const codigo = e.target.codigo.value.trim();
    
    if (!codigo) {
      return;
    }

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
      
      // Limpiar el campo inmediatamente
      e.target.reset();
      
      // Volver a hacer foco en el campo después de un breve delay
      setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.focus();
        }
      }, 100);

      // Auto-limpiar el mensaje de éxito después de 3 segundos
      setTimeout(() => {
        setResult(null);
      }, 3000);

    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Error al validar el código QR';
      setError(errorMsg);
      setResult(null);
      
      // Limpiar el campo también en caso de error
      e.target.reset();
      
      // Volver a hacer foco
      setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.focus();
        }
      }, 100);

      // Auto-limpiar el mensaje de error después de 3 segundos
      setTimeout(() => {
        setError(null);
      }, 3000);
    }
  };

  return (
    <div className="card">
      <h2>Escanear Código QR</h2>

      {error && (
        <div className="alert alert-error" style={{ 
          fontSize: '1.2rem', 
          padding: '1.5rem',
          animation: 'shake 0.5s'
        }}>
          ❌ <strong>{error}</strong>
        </div>
      )}
      
      {result && (
        <div className="alert alert-success" style={{ 
          fontSize: '1.2rem', 
          padding: '1.5rem',
          animation: 'fadeIn 0.3s'
        }}>
          <h3 style={{ margin: '0 0 1rem 0', fontSize: '1.5rem' }}>
            ✅ {result.mensaje}
          </h3>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: '1fr 1fr', 
            gap: '1rem',
            fontSize: '1rem'
          }}>
            <div>
              <strong>👤 Estudiante:</strong><br/>
              {result.estudiante}
            </div>
            <div>
              <strong>🍽️ Comida:</strong><br/>
              {result.tipo_comida}
            </div>
          </div>
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
        <h3>📝 Escaneo Rápido Manual</h3>
        <p style={{ color: '#aaa', marginBottom: '1rem' }}>
          Escanea el código QR con el lector y presiona Enter. El campo se limpiará automáticamente.
        </p>
        <form onSubmit={handleManualInput}>
          <div className="form-group">
            <label htmlFor="codigo">Código QR</label>
            <input
              ref={inputRef}
              type="text"
              id="codigo"
              name="codigo"
              placeholder="Escanea o pega el código aquí..."
              autoFocus
              autoComplete="off"
              style={{
                fontSize: '1.1rem',
                padding: '0.8rem',
                textAlign: 'center',
                fontFamily: 'monospace'
              }}
            />
          </div>
          <button type="submit" className="btn btn-success" style={{ width: '100%' }}>
            ✅ Validar Código (o presiona Enter)
          </button>
        </form>
        <div style={{ 
          marginTop: '1rem', 
          padding: '0.8rem', 
          backgroundColor: '#1a1a1a', 
          borderRadius: '4px',
          fontSize: '0.9rem',
          color: '#888'
        }}>
          💡 <strong>Tip:</strong> Mantén el cursor en el campo de entrada. Después de cada escaneo, 
          el campo se limpiará automáticamente y estará listo para el siguiente código.
        </div>
      </div>
    </div>
  );
}

export default QRScanner;
