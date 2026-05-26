// Auth helpers - login, registro, perfil, direcciones, pedidos
import { auth, db, googleProvider } from './firebase-config.js';
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup,
  signOut as fbSignOut,
  onAuthStateChanged,
  updateProfile,
  sendPasswordResetEmail,
} from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";
import {
  doc, setDoc, getDoc, updateDoc, collection, addDoc,
  query, where, orderBy, getDocs, serverTimestamp,
} from "https://www.gstatic.com/firebasejs/11.0.2/firebase-firestore.js";

// ============ AUTH ============

export async function registerUser(email, password, displayName) {
  const cred = await createUserWithEmailAndPassword(auth, email, password);
  if (displayName) await updateProfile(cred.user, { displayName });
  await createUserDoc(cred.user, displayName);
  return cred.user;
}

export async function loginEmail(email, password) {
  const cred = await signInWithEmailAndPassword(auth, email, password);
  return cred.user;
}

export async function loginGoogle() {
  const cred = await signInWithPopup(auth, googleProvider);
  // crea doc si no existe
  const userRef = doc(db, 'users', cred.user.uid);
  const snap = await getDoc(userRef);
  if (!snap.exists()) {
    await createUserDoc(cred.user, cred.user.displayName);
  }
  return cred.user;
}

export async function signOut() {
  return fbSignOut(auth);
}

export async function resetPassword(email) {
  return sendPasswordResetEmail(auth, email);
}

export function onUserChange(callback) {
  return onAuthStateChanged(auth, callback);
}

export function getCurrentUser() {
  return auth.currentUser;
}

// ============ USER DOC ============

async function createUserDoc(user, displayName) {
  const userRef = doc(db, 'users', user.uid);
  await setDoc(userRef, {
    email: user.email,
    displayName: displayName || user.displayName || '',
    photoURL: user.photoURL || '',
    membershipLevel: 'basic',
    discountPct: 0,
    createdAt: serverTimestamp(),
  });
}

export async function getUserProfile(uid) {
  const snap = await getDoc(doc(db, 'users', uid));
  return snap.exists() ? snap.data() : null;
}

export async function updateUserProfile(uid, data) {
  return updateDoc(doc(db, 'users', uid), data);
}

// ============ DIRECCIONES ============

export async function getAddresses(uid) {
  const q = query(collection(db, 'users', uid, 'addresses'), orderBy('createdAt', 'desc'));
  const snap = await getDocs(q);
  return snap.docs.map(d => ({ id: d.id, ...d.data() }));
}

export async function addAddress(uid, address) {
  return addDoc(collection(db, 'users', uid, 'addresses'), {
    ...address,
    createdAt: serverTimestamp(),
  });
}

export async function deleteAddress(uid, addressId) {
  const { deleteDoc } = await import("https://www.gstatic.com/firebasejs/11.0.2/firebase-firestore.js");
  return deleteDoc(doc(db, 'users', uid, 'addresses', addressId));
}

// ============ PEDIDOS ============

export async function getOrders(uid) {
  const q = query(
    collection(db, 'orders'),
    where('userId', '==', uid),
    orderBy('createdAt', 'desc')
  );
  const snap = await getDocs(q);
  return snap.docs.map(d => ({ id: d.id, ...d.data() }));
}

export async function createOrder(uid, orderData) {
  return addDoc(collection(db, 'orders'), {
    userId: uid,
    ...orderData,
    status: 'pending',
    createdAt: serverTimestamp(),
  });
}
