import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CrearCasilleroModal from './CrearCasilleroModal';

const CasillerosList = () => {
    const [casilleros, setCasilleros] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [newCasillero, setNewCasillero] = useState({
        id: '',
        location: '',
        price: '',
        description: '',
    });
    const navigate = useNavigate();

    const verDetalles = (id) => {
        navigate(`/casilleros/${id}`); // Usar navigate en lugar de history.push
    };

    useEffect(() => {
        fetch('http://127.0.0.1:8000/casilleros/api/lista/')
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                setCasilleros(data);
            })
            .catch((error) => console.error('Error fetching casilleros:', error));
    }, []);

    const toggleBlock = (id, isBlocked) => {
        const action = isBlocked ? 'desbloquear' : 'bloquear'; // Cambia según la acción
        fetch(`http://127.0.0.1:8000/casilleros/api/bloquear/${id}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                // Actualiza la lista de casilleros después de la acción
                setCasilleros(prevCasilleros =>
                    prevCasilleros.map(casillero =>
                        casillero.id === id ? { ...casillero, blocked: !isBlocked } : casillero
                    )
                );
            } else {
                console.error('Error al cambiar estado del casillero');
            }
        })
        .catch(error => console.error('Error en la petición:', error));
    };

    const toggleOpen = (id, isOpen) => {
        const action = isOpen ? 'cerrar' : 'abrir'; // Cambia según la acción
        fetch(`http://127.0.0.1:8000/casilleros/api/abrir/${id}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                // Actualiza la lista de casilleros después de la acción
                setCasilleros(prevCasilleros =>
                    prevCasilleros.map(casillero =>
                        casillero.id === id ? { ...casillero, open: !isOpen } : casillero
                    )
                );
            } else {
                console.error('Error al cambiar el estado de apertura del casillero');
            }
        })
        .catch(error => console.error('Error en la petición:', error));
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewCasillero((prev) => ({ ...prev, [name]: value }));
    };

    const handleAddCasillero = () => {
        fetch('http://127.0.0.1:8000/casilleros/api/crear/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCasillero),
        })
        .then(response => response.json())
        .then(data => {
            setCasilleros([...casilleros, data]);
            setShowModal(false);
            setNewCasillero({ id: '', location: '', price: '', description: '' });
        })
        .catch(error => console.error('Error creando casillero:', error));
    };

    return (
        
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Lista de Casilleros</h1>
            <div className="grid grid-cols-5 gap-4">
                {casilleros.map((casillero) => (
                    <div key={casillero.id} className="border rounded-lg p-4 bg-white shadow-md relative">
                        <h2 className="text-xl font-semibold">Código Casillero: {casillero.id}</h2>
                        <p className="text-gray-600">Ubicación: {casillero.location}</p>
                        <p className="text-gray-600">Estado de bloqueo: {casillero.blocked ? 'Bloqueado' : 'Desbloqueado'}</p>
                        <p className="text-gray-600">Ocupado: {casillero.occupied ? 'Ocupado' : 'Desocupado'}</p>
                        <p className="text-gray-600">Estado de la Puerta: {casillero.open ? 'Abierto' : 'Cerrado'}</p>

                        <button 
                            onClick={() => verDetalles(casillero.id)} 
                            className="absolute top-2 right-2 w-5 h-5 flex items-center justify-center rounded-full bg-blue-500 text-white hover:bg-blue-600 focus:outline-none"
                            aria-label="Ver detalles"
                        >
                            <span className="text-lg font-bold">i</span> {/* Letra "i" dentro del círculo */}
                        </button>

                        <div className="flex space-x-2 mt-4">
                            
                        
                            <button
                                onClick={() => toggleBlock(casillero.id, casillero.blocked)}
                                className={`px-4 py-2 text-white rounded ${casillero.blocked ? 'bg-red-500' : 'bg-green-500'}`}
                            >
                                {casillero.blocked ? 'Desbloquear' : 'Bloquear'}
                            </button>
                            <button
                                onClick={() => toggleOpen(casillero.id, casillero.open)}
                                className={`px-4 py-2 text-white rounded ${casillero.open ? 'bg-red-500' : 'bg-green-500'}`}
                            >
                                {casillero.open ? 'Cerrar' : 'Abrir'}
                            </button>
                        </div>

                    </div>
                ))}
            </div>
            {/* Botón flotante para abrir el modal */}
        <button
            onClick={() => setShowModal(true)}
            className="fixed bottom-4 right-4 bg-blue-500 text-white px-4 py-2 rounded-full"
        >
            + Crear un nuevo casillero
        </button>

        {/* Modal para crear un nuevo casillero */}
        <CrearCasilleroModal
            isVisible={showModal}
            onClose={() => setShowModal(false)}
            onAdd={handleAddCasillero}
            newCasillero={newCasillero}
            handleInputChange={handleInputChange}
        />
    </div>
);
}
            

export default CasillerosList;
