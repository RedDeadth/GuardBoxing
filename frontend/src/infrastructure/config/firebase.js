import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyAeXeBoiWk0jJr5-7Eico4ZHKaZutPXFg0",
  authDomain: "guardianbox-2636d.firebaseapp.com",
  databaseURL: "https://guardianbox-2636d-default-rtdb.firebaseio.com",
  projectId: "guardianbox-2636d",
  storageBucket: "guardianbox-2636d.firebasestorage.app",
  messagingSenderId: "391140718969",
  appId: "1:391140718969:web:425e4de6d7c7b54d4fd7a8",
  measurementId: "G-WKNGWB0DRQ"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
