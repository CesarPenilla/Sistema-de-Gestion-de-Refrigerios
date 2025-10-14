import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Estudiantes
export const getEstudiantes = (soloActivos = false) => {
  const params = soloActivos ? '?activos=true' : '';
  return api.get(`/estudiantes/${params}`);
};
export const getEstudiante = (id) => api.get(`/estudiantes/${id}/`);
export const createEstudiante = (data) => api.post('/estudiantes/', data);
export const updateEstudiante = (id, data) => api.put(`/estudiantes/${id}/`, data);
export const deleteEstudiante = (id) => api.delete(`/estudiantes/${id}/`);
export const getEstudianteConCodigos = (id) => api.get(`/estudiantes/${id}/con_codigos/`);
export const generarCodigosQR = (id) => api.post(`/estudiantes/${id}/generar_codigos/`);
export const generarCodigosMasivo = () => api.post('/estudiantes/generar_codigos_masivo/');

// Códigos QR
export const getCodigosQR = () => api.get('/codigos-qr/');
export const getCodigoQR = (id) => api.get(`/codigos-qr/${id}/`);
export const validarCodigoQR = (codigo) => api.post('/codigos-qr/validar/', { codigo });
export const getCodigoQRImagen = (id) => `${API_URL}/codigos-qr/${id}/generar_imagen/`;
export const getCodigoQRBase64 = (id) => api.get(`/codigos-qr/${id}/generar_base64/`);
export const getCodigosPorEstudiante = (estudianteId) => 
  api.get(`/codigos-qr/por_estudiante/?estudiante_id=${estudianteId}`);

export default api;
