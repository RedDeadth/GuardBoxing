import React, { useEffect, useState } from 'react';

const CasillerosList = () => {
    const [casilleros, setCasilleros] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/casilleros/api/lista/')
            .then((response) => response.json())
            .then((data) => {
                console.log(data); // Verifica los datos aquí
                setCasilleros(data); // Asigna los datos al estado
            })
            .catch((error) => console.error('Error fetching casilleros:', error));
    }, []);

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Lista de Casilleros</h1>
            <div className="grid grid-cols-5 gap-4">
                {casilleros.map((casillero) => (
                    <div key={casillero.id} className="border rounded-lg p-4 bg-white shadow-md">
                        <h2 className="text-xl font-semibold text-xl">Codigo Casillero: {casillero.id}</h2>
                        <p className="text-gray-600">Ubicación: {casillero.location}</p>
                        <p className="text-gray-600">Estado de bloqueo: {casillero.blocked ? 'Bloqueado' : 'No bloqueado'}</p>
                        <p className="text-gray-600">Ocupado: {casillero.occupied ? 'Ocupado' : 'Desocupado'}</p>
                        <p className="text-gray-600">Estado de la Puerta: {casillero.open ? 'Abierto' : 'Cerrado'}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};


export default CasillerosList;
