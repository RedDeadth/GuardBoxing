import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const CasilleroDetalle = () => {
    const { id } = useParams();
    const [casillero, setCasillero] = useState(null);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/casilleros/api/detalle/${id}/`)
            .then(response => response.json())
            .then(data => setCasillero(data))
            .catch(error => console.error('Error al cargar detalles del casillero:', error));
    }, [id]);

    const toggleBlock = () => {
        fetch(`http://127.0.0.1:8000/casilleros/api/bloquear/${id}/`, {
            method: 'GET',
        })
        .then(response => {
            if (response.ok) {
                setCasillero(prev => ({ ...prev, blocked: !prev.blocked }));
            } else {
                console.error('Error al cambiar el estado de bloqueo');
            }
        })
        .catch(error => console.error('Error en la petición:', error));
    };

    const toggleOpen = () => {
        fetch(`http://127.0.0.1:8000/casilleros/api/abrir/${id}/`, {
            method: 'GET',
        })
        .then(response => {
            if (response.ok) {
                setCasillero(prev => ({ ...prev, open: !prev.open }));
            } else {
                console.error('Error al cambiar el estado de apertura');
            }
        })
        .catch(error => console.error('Error en la petición:', error));
    };

    const formatDate = (timestamp) => {
        return new Date(timestamp).toLocaleString();
    };

    const calculateRemainingTime = (endTime) => {
        const now = Date.now();
        const remainingTime = endTime - now;
        if (remainingTime <= 0) return 'Reserva expirada';
        const hours = Math.floor(remainingTime / (1000 * 60 * 60));
        const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
        return `${hours} horas y ${minutes} minutos restantes`;
    };

    if (!casillero) {
        return <p>Cargando detalles del casillero...</p>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Detalle del Casillero Código: {id}</h1>
            <div className="border rounded-lg p-4 bg-white shadow-md">
                <p><strong>Ubicación:</strong> {casillero.location || 'No disponible'}</p>
                <p><strong>Precio:</strong> {casillero.price}</p>
                <p><strong>Descripción:</strong> {casillero.description || 'Sin descripción'}</p>
                <p><strong>Estado de Bloqueo:</strong> {casillero.blocked ? 'Bloqueado' : 'Desbloqueado'}</p>
                <p><strong>Ocupado:</strong> {casillero.occupied ? 'Ocupado' : 'Desocupado'}</p>
                <p><strong>Estado de la Puerta:</strong> {casillero.open ? 'Abierto' : 'Cerrado'}</p>
                <p><strong>Propietario:</strong> {casillero.propietario || 'Sin propietario'}</p>
                <p><strong>Compartido con:</strong> {casillero.sharedwith && casillero.sharedwith.length > 0 ? casillero.sharedwith.join(', ') : 'Nadie'}</p>
                <p><strong>Fecha Fin de Reserva: </strong> 
                    {casillero.reservationEndTime ? formatDate(casillero.reservationEndTime) : 'Sin reserva activa'}
                </p>
                <p><strong>Tiempo Restante de la Reserva:</strong> 
                    {casillero.reservationEndTime ? calculateRemainingTime(casillero.reservationEndTime) : 'No aplica'}
                </p>

                <div className="flex space-x-4 mt-4">
                    <button
                        onClick={toggleBlock}
                        className={`px-4 py-2 text-white rounded ${casillero.blocked ? 'bg-red-500' : 'bg-green-500'}`}
                    >
                        {casillero.blocked ? 'Desbloquear' : 'Bloquear'}
                    </button>
                    <button
                        onClick={toggleOpen}
                        className={`px-4 py-2 text-white rounded ${casillero.open ? 'bg-red-500' : 'bg-green-500'}`}
                    >
                        {casillero.open ? 'Cerrar' : 'Abrir'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default CasilleroDetalle;
