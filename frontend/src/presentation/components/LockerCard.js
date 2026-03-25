import React from 'react';
import { Link } from 'react-router-dom';
import { Lock, Unlock, DoorOpen, DoorClosed, AlertTriangle, Eye } from 'lucide-react';

export default function LockerCard({ locker, onToggleBlock, onToggleOpen }) {
    const isBlocked = locker.isBlocked();
    const isOpen = locker.isOpen();
    const isOccupied = locker.isOccupied();

    return (
        <div className={`flex flex-col border-[3px] rounded-2xl p-5 shadow-[4px_4px_0_0_#000] bg-white transition-all 
            ${isBlocked ? 'border-red-600 bg-red-50' : 'border-black hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none'}`}>
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h2 className="text-xl font-black uppercase tracking-tight">Box {locker.id}</h2>
                    <p className="text-xs font-bold text-gray-500 uppercase tracking-widest">{locker.location}</p>
                </div>
                {isBlocked && <AlertTriangle className="text-red-500" size={24} />}
            </div>

            <div className="flex flex-col gap-2 mb-6">
                <div className="flex items-center gap-2 text-sm font-semibold">
                    <span className={`w-3 h-3 rounded-full ${isOccupied ? 'bg-orange-500' : 'bg-green-500'}`}></span>
                    {isOccupied ? 'OCUPADO' : 'LIBRE'}
                </div>
                <div className="flex items-center gap-2 text-sm font-semibold text-gray-700">
                    {isOpen ? <DoorOpen size={16} /> : <DoorClosed size={16}/>}
                    {isOpen ? 'PUERTA ABIERTA' : 'PUERTA CERRADA'}
                </div>
            </div>

            <div className="mt-auto grid grid-cols-1 gap-2">
                <div className="grid grid-cols-2 gap-2">
                    <button onClick={() => onToggleBlock(locker.id)} 
                            className={`py-2 px-3 flex justify-center items-center gap-2 rounded-lg text-[10px] sm:text-xs font-bold uppercase transition-colors border-2
                                ${isBlocked ? 'bg-red-100 text-red-700 border-red-200 hover:bg-red-200' : 'bg-black text-white hover:bg-gray-800'}`}>
                        {isBlocked ? <><Unlock size={14}/> Liberar</> : <><Lock size={14}/> Bloquear</>}
                    </button>
                    <button onClick={() => onToggleOpen(locker.id)} 
                            className="py-2 px-3 flex justify-center items-center gap-2 rounded-lg text-[10px] sm:text-xs font-bold uppercase transition-colors border-2 border-gray-200 text-gray-700 hover:bg-gray-100">
                        {isOpen ? 'Cerrar' : 'Abrir'}
                    </button>
                </div>
                <Link to={`/dashboard/casillero/${locker.id}`} 
                      className="py-2 px-3 flex justify-center items-center gap-2 rounded-lg text-xs font-bold uppercase transition-colors border-[3px] border-black text-black bg-orange-50 hover:bg-orange-100">
                    <Eye size={14}/> Detalles de Reserva
                </Link>
            </div>
        </div>
    );
}
