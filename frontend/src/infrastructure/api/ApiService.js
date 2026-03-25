export const fetchLockers = async () => {
    const res = await fetch('http://127.0.0.1:8000/casilleros/api/lista/');
    if (!res.ok) throw new Error('API Error');
    return res.json();
};

export const fetchLockerById = async (id) => {
    const res = await fetch(`http://127.0.0.1:8000/casilleros/api/detalle/${id}/`);
    if (!res.ok) throw new Error('API Error');
    return res.json();
};

export const toggleLockerBlock = async (id) => {
    const res = await fetch(`http://127.0.0.1:8000/casilleros/api/bloquear/${id}/`);
    if (!res.ok) throw new Error('Action failed');
    return res.json();
};

export const toggleLockerOpen = async (id) => {
    const res = await fetch(`http://127.0.0.1:8000/casilleros/api/abrir/${id}/`);
    if (!res.ok) throw new Error('Action failed');
    return res.json();
};
