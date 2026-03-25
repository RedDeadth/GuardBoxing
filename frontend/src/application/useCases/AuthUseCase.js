import { auth, googleProvider } from '../../infrastructure/config/firebase';
import { signInWithPopup, signOut } from 'firebase/auth';

export const loginMockAdmin = (user, pass) => {
    if (user === 'admin' && pass === 'admin') {
        localStorage.setItem('guardbox_token', 'mock_admin_token_123');
        return true;
    }
    return false;
};

export const loginWithGoogle = async () => {
    try {
        const result = await signInWithPopup(auth, googleProvider);
        localStorage.setItem('guardbox_token', result.user.accessToken);
        return true;
    } catch (e) {
        console.error('Google Auth Error:', e);
        return false;
    }
};

export const logout = async () => {
    try {
        await signOut(auth);
    } catch (e) {
        console.error('SignOut Error', e);
    }
    localStorage.removeItem('guardbox_token');
};

export const isAuthenticated = () => {
    return !!localStorage.getItem('guardbox_token');
};
