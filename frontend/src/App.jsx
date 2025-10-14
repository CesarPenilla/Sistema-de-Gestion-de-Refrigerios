import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import './styles/global.css'
import EstudiantesList from './components/EstudiantesList'
import EstudianteForm from './components/EstudianteForm'
import QRScanner from './components/QRScanner'
import QRGenerator from './components/QRGenerator'

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <h1>🍽️ Sistema de Gestión de Refrigerios</h1>
          <ul>
            <li><Link to="/">Estudiantes</Link></li>
            <li><Link to="/nuevo">Nuevo Estudiante</Link></li>
            <li><Link to="/generar-qr">Generar QR</Link></li>
            <li><Link to="/escanear">Escanear QR</Link></li>
          </ul>
        </nav>

        <div className="container">
          <Routes>
            <Route path="/" element={<EstudiantesList />} />
            <Route path="/nuevo" element={<EstudianteForm />} />
            <Route path="/generar-qr" element={<QRGenerator />} />
            <Route path="/escanear" element={<QRScanner />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
