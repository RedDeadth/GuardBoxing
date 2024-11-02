// CrearCasilleroModal.js
import React from 'react';

const CrearCasilleroModal = ({ isVisible, onClose, onAdd, newCasillero, handleInputChange }) => {
    if (!isVisible) return null;

    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center">
            <div className="bg-white p-8 rounded-lg shadow-lg max-w-sm w-full">
                <h2 className="text-2xl font-semibold mb-4">Nuevo Casillero</h2>
                <input
                    type="text"
                    name="id"
                    placeholder="ID"
                    value={newCasillero.id}
                    onChange={handleInputChange}
                    className="w-full p-2 mb-2 border rounded"
                />
                <input
                    type="text"
                    name="location"
                    placeholder="Ubicación"
                    value={newCasillero.location}
                    onChange={handleInputChange}
                    className="w-full p-2 mb-2 border rounded"
                />
                <input
                    type="text"
                    name="price"
                    placeholder="Precio"
                    value={newCasillero.price}
                    onChange={handleInputChange}
                    className="w-full p-2 mb-2 border rounded"
                />
                <input
                    type="text"
                    name="description"
                    placeholder="Descripción"
                    value={newCasillero.description}
                    onChange={handleInputChange}
                    className="w-full p-2 mb-2 border rounded"
                />
                <div className="flex justify-end space-x-2 mt-4">
                    <button onClick={onClose} className="px-4 py-2 bg-red-500 text-white rounded">
                        Cancelar
                    </button>
                    <button onClick={onAdd} className="px-4 py-2 bg-green-500 text-white rounded">
                        Añadir
                    </button>
                </div>
            </div>
        </div>
    );
};

export default CrearCasilleroModal;
