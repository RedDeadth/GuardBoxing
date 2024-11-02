import React from 'react';

const Layout = ({ children, currentUser }) => {
    // Función para determinar si la ruta actual coincide con la ruta del enlace
    const isCurrentPath = (path) => {
        return window.location.pathname === path;
    };

    // Función para manejar la navegación
    const handleNavigation = (path) => {
        window.location.href = path;
    };

    return (
        <div className="flex h-screen">
            {/* Barra lateral */}
            <div className="bg-blue-700 w-64 p-4 text-white flex flex-col justify-between">
                <div>
                    <h1 className="text-2xl font-bold mb-8">Panel de Control</h1>
                    <nav>
                        <button 
                            onClick={() => handleNavigation('/casilleros')}
                            className={`block w-full text-left py-2 px-4 rounded ${isCurrentPath('/casilleros') ? 'bg-blue-500' : 'hover:bg-blue-600'}`}
                        >
                            Casilleros
                        </button>
                        <button 
                            onClick={() => handleNavigation('/usuarios')}
                            className={`block w-full text-left py-2 px-4 rounded ${isCurrentPath('/usuarios') ? 'bg-blue-500' : 'hover:bg-blue-600'}`}
                        >
                            Usuarios
                        </button>
                        <button 
                            onClick={() => handleNavigation('/configuracion')}
                            className={`block w-full text-left py-2 px-4 rounded ${isCurrentPath('/configuracion') ? 'bg-blue-500' : 'hover:bg-blue-600'}`}
                        >
                            Configuración
                        </button>
                    </nav>
                </div>
            </div>

            {/* Contenedor principal */}
            <div className="flex-1 flex flex-col">
                {/* Barra superior */}
                <header className="bg-white p-4 shadow flex items-center justify-between">
                    <div className="text-gray-700 font-bold text-lg">
                        Bienvenido, {currentUser || 'Usuario'}
                    </div>
                    <div className="flex items-center space-x-4">
                        <input
                            type="text"
                            placeholder="Buscar..."
                            className="border rounded px-3 py-2 text-gray-600"
                        />
                        <button
                            onClick={() => handleNavigation('/usuarios/logout')}
                            className="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded text-sm font-medium"
                        >
                            Cerrar Sesión
                        </button>
                    </div>
                </header>

                {/* Contenido dinámico */}
                <main className="flex-1 bg-gray-100 p-6 overflow-auto">
                    {children}
                </main>
            </div>
        </div>
    );
};

export default Layout;