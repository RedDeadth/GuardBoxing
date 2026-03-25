import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, User, Clock, AlertTriangle, DoorClosed, DollarSign } from 'lucide-react';
import { getLockerById } from '../../application/useCases/LockerUseCase';

export default function LockerDetail() {
    const { id } = useParams();
    const [locker, setLocker] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        getLockerById(id)
            .then(setLocker)
            .catch(e => setError('No se pudo cargar el casillero o no existe.'));
    }, [id]);

    if (error) return <div className="p-10 text-center text-red-600 font-bold">{error}</div>;
    if (!locker) return <div className="p-10 text-center font-bold">Cargando detalles...</div>;

    const isBlocked = locker.isBlocked();
    const isOccupied = locker.isOccupied();
    const reservedTime = locker.reservedAt || 'Sin registro en Firebase';

    return (
        <div className="min-h-screen bg-gray-50 text-black font-sans p-4 sm:p-10">
            <Link to="/dashboard" className="inline-flex items-center gap-2 mb-6 font-bold uppercase text-xs hover:underline bg-white border-[3px] border-black p-3 rounded-xl shadow-[4px_4px_0_0_#000]">
                <ArrowLeft size={16} /> Volver al Dashboard
            </Link>

            <div className="max-w-3xl mx-auto bg-white border-[4px] border-black rounded-3xl p-8 shadow-[8px_8px_0_0_#000]">
                <div className="flex justify-between items-start border-b-[3px] border-black pb-6 mb-6">
                    <div>
                        <h1 className="text-4xl font-black uppercase tracking-tighter">Box {locker.id}</h1>
                        <p className="text-lg font-bold text-gray-500 uppercase tracking-widest">{locker.location}</p>
                    </div>
                    <div className="flex flex-col gap-2 items-end">
                        <span className={`px-4 py-2 font-black uppercase text-xs rounded-full border-2 ${isBlocked ? 'bg-red-100 text-red-700 border-red-700' : 'bg-green-100 text-green-700 border-green-700'}`}>
                            {isBlocked ? 'Bajo Bloqueo' : 'Desbloqueado'}
                        </span>
                        <span className={`px-4 py-2 font-black uppercase text-xs rounded-full border-2 ${isOccupied ? 'bg-orange-100 text-orange-700 border-orange-700' : 'bg-blue-100 text-blue-700 border-blue-700'}`}>
                            {isOccupied ? 'Arrendado' : 'Disponible'}
                        </span>
                    </div>
                </div>

                <h2 className="text-xl font-black uppercase mb-4">Registro Operativo de IoT</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-gray-50 border-[3px] border-black rounded-xl p-5">
                        <div className="flex items-center gap-3 mb-2 text-gray-500">
                            <User size={20} /> <span className="font-black uppercase text-xs tracking-widest">Arrendatario</span>
                        </div>
                        <p className="font-bold text-base break-all">
                            {locker.userName ? `${locker.userName} (${locker.userEmail})` : (locker.userId || 'Ninguno (Libre)')}
                        </p>
                    </div>

                    <div className="bg-gray-50 border-[3px] border-black rounded-xl p-5">
                        <div className="flex items-center gap-3 mb-2 text-gray-500">
                            <Clock size={20} /> <span className="font-black uppercase text-xs tracking-widest">Tiempo de Reserva</span>
                        </div>
                        <p className="font-bold text-lg">{reservedTime}</p>
                    </div>

                    <div className="bg-gray-50 border-[3px] border-black rounded-xl p-5">
                        <div className="flex items-center gap-3 mb-2 text-gray-500">
                            <DoorClosed size={20} /> <span className="font-black uppercase text-xs tracking-widest">Estado de Puerta</span>
                        </div>
                        <p className="font-bold text-lg">{locker.isOpen() ? 'Se encuentra Abierta' : 'Asegurada Físicamente'}</p>
                    </div>
                    
                    <div className="bg-orange-50 border-[3px] border-orange-300 rounded-xl p-5 flex items-center justify-center">
                        <p className="font-black text-center text-orange-700 uppercase p-2 border-2 border-dashed border-orange-700 rounded-lg w-full">
                            El pago y los tiempos provienen de la tarifa pactada en WasabiDefinitive vía Firebase.
                        </p>
                    </div>
                </div>

            </div>
        </div>
    );
}
