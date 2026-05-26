// Firebase initialization - shared across all Kodarase pages
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js";
import { getAuth, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyA5ol4Pm3N9GPBqMFsYoC7A5BtkmwkLs-Q",
  authDomain: "kodarase.firebaseapp.com",
  projectId: "kodarase",
  storageBucket: "kodarase.firebasestorage.app",
  messagingSenderId: "724443029569",
  appId: "1:724443029569:web:d013fd1684e172685ce6c0",
  measurementId: "G-4WL8JNNJCG"
};

export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
export const googleProvider = new GoogleAuthProvider();
