import { fetchLockers, fetchLockerById, toggleLockerBlock, toggleLockerOpen } from '../../infrastructure/api/ApiService';
import Locker from '../../domain/models/Locker';

export const getLockers = async () => {
    const data = await fetchLockers();
    return data.map(item => new Locker(item));
};

export const getLockerById = async (id) => {
    const data = await fetchLockerById(id);
    return new Locker(data);
};

export const handleBlockToggle = async (id) => {
    return await toggleLockerBlock(id);
};

export const handleOpenToggle = async (id) => {
    return await toggleLockerOpen(id);
};
