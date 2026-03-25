import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search } from 'lucide-react';
import LockerCard from '../components/LockerCard';
import { getLockers, handleBlockToggle, handleOpenToggle } from '../../application/useCases/LockerUseCase';
import { logout } from '../../application/useCases/AuthUseCase';

export default function Dashboard() {
    const [lockers, setLockers] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const navigate = useNavigate();

    const loadData = () => {
        getLockers().then(setLockers).catch(e => console.error(e));
    };

    useEffect(() => {
        loadData();
    }, []);

    const onBlock = async (id) => {
        await handleBlockToggle(id);
        loadData();
    };

    const onOpen = async (id) => {
        await handleOpenToggle(id);
        loadData();
    };

    const handleLogout = async () => {
        await logout();
        navigate('/login');
    };

    const filteredLockers = lockers.filter(l => {
        const query = searchQuery.toLowerCase();
        const matchId = l.id.toString().includes(query);
        const matchUser = l.userId ? l.userId.toLowerCase().includes(query) : false;
        const matchEmail = l.userEmail ? l.userEmail.toLowerCase().includes(query) : false;
        const matchName = l.userName ? l.userName.toLowerCase().includes(query) : false;
        return matchId || matchUser || matchEmail || matchName;
    });

    return (
        <div className="min-h-screen bg-gray-50 text-black font-sans">
            <header className="bg-white border-b-[3px] border-black p-4 flex justify-between items-center shadow-sm">
                <div className="flex items-center gap-3">
                    <img src="/logo.jpg" alt="Wasabi Logo" className="w-10 h-10 rounded-lg shadow-sm border border-gray-200 object-cover" />
                    <h1 className="text-2xl font-black uppercase tracking-tighter hidden sm:block">GuardBoxing Admin</h1>
                </div>
                <div className="flex-1 max-w-md mx-4 relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                    <input 
                        type="text" 
                        placeholder="Buscar por ID, Usuario, Correo o Nombre..." 
                        value={searchQuery}
                        onChange={e => setSearchQuery(e.target.value)}
                        className="w-full bg-gray-100 border-[2px] border-black rounded-lg py-2 pl-10 pr-4 text-sm font-bold outline-none focus:bg-white transition-colors"
                    />
                </div>
                <button onClick={handleLogout} className="text-sm font-bold uppercase text-red-600 hover:underline flex-shrink-0">Salir</button>
            </header>
            <main className="container mx-auto p-8">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                    {filteredLockers.map(l => (
                        <LockerCard key={l.id} locker={l} onToggleBlock={onBlock} onToggleOpen={onOpen} />
                    ))}
                </div>
                {filteredLockers.length === 0 && <p className="text-center font-bold text-gray-400 mt-20">No se encontraron casilleros.</p>}
            </main>
        </div>
    );
}
