import React, { useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import { loginWithGoogle, loginMockAdmin, isAuthenticated } from '../../application/useCases/AuthUseCase';

export default function Login() {
    const [user, setUser] = useState('');
    const [pass, setPass] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    if (isAuthenticated()) {
        return <Navigate to="/dashboard" replace />;
    }

    const handleMockLogin = (e) => {
        e.preventDefault();
        if (loginMockAdmin(user, pass)) {
            navigate('/dashboard');
        } else {
            setError('Credenciales inválidas. Usa admin / admin');
        }
    };

    const handleGoogleLogin = async () => {
        const success = await loginWithGoogle();
        if (success) {
            navigate('/dashboard');
        } else {
            setError('Fallo de Autenticación con Google (Token / Consola).');
        }
    };

    return (
        <div className="min-h-screen bg-orange-50 flex items-center justify-center font-sans p-4">
            <div className="bg-white w-full max-w-md rounded-3xl p-8 border-[3px] border-black shadow-[8px_8px_0_0_#000]">
                <div className="flex flex-col items-center mb-8">
                    <img src="/logo.jpg" alt="Logo" className="w-20 h-20 rounded-2xl shadow-sm border border-gray-200 mb-4 object-cover" />
                    <h2 className="text-3xl font-black uppercase tracking-tighter text-center">Admin Access</h2>
                    <p className="text-sm font-semibold text-gray-500 uppercase tracking-widest mt-1">GuardBoxing System</p>
                </div>
                
                {error && <div className="bg-red-100 text-red-700 text-xs font-bold uppercase p-3 rounded-lg border-2 border-red-200 mb-6 text-center">{error}</div>}

                <form onSubmit={handleMockLogin} className="flex flex-col gap-5">
                    <div>
                        <label className="block text-xs font-black uppercase tracking-widest mb-2">Usuario</label>
                        <input type="text" value={user} onChange={e=>setUser(e.target.value)} required 
                            className="w-full bg-gray-50 border-[3px] border-black p-4 text-sm font-bold outline-none focus:bg-white transition-colors" placeholder="admin" />
                    </div>
                    <div>
                        <label className="block text-xs font-black uppercase tracking-widest mb-2">Contraseña</label>
                        <input type="password" value={pass} onChange={e=>setPass(e.target.value)} required 
                            className="w-full bg-gray-50 border-[3px] border-black p-4 text-sm font-bold outline-none focus:bg-white transition-colors" placeholder="•••••" />
                    </div>
                    <button type="submit" className="mt-2 w-full py-4 bg-[#FF6A00] text-white border-[3px] border-black font-black text-lg uppercase tracking-wider transition-all shadow-[4px_4px_0_0_#000] hover:shadow-none hover:translate-x-[4px] hover:translate-y-[4px]">
                        Iniciar Sesión
                    </button>
                    
                    <div className="relative flex items-center my-1">
                        <div className="flex-grow border-t-2 border-dashed border-gray-300"></div>
                        <span className="flex-shrink-0 mx-4 text-gray-300 text-[10px] font-black uppercase">Ó</span>
                        <div className="flex-grow border-t-2 border-dashed border-gray-300"></div>
                    </div>

                    <button 
                        type="button"
                        onClick={handleGoogleLogin} 
                        className="w-full py-4 bg-white text-black border-[3px] border-black font-black text-sm uppercase tracking-wider transition-all shadow-[4px_4px_0_0_#000] hover:shadow-none hover:translate-x-[4px] hover:translate-y-[4px] flex justify-center items-center gap-3"
                    >
                        <img src="https://www.svgrepo.com/show/475656/google-color.svg" alt="Google" className="w-5 h-5" />
                        Auth de Google
                    </button>
                    
                    <p className="text-[10px] text-center font-bold text-gray-400 mt-2 uppercase">Protegido por IoT Locker Tech</p>
                </form>
            </div>
        </div>
    );
}
