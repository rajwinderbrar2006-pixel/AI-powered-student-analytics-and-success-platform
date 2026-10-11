import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";

import {
  getAuth,
  GoogleAuthProvider
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyB0TZPCXnF4UpxNNm6OEQx99Sx629jfAy8",
  authDomain: "nexora-b18da.firebaseapp.com",
  projectId: "nexora-b18da",
  storageBucket: "nexora-b18da.firebasestorage.app",
  messagingSenderId: "158481730076",
  appId: "1:158481730076:web:0a1719a57c61b210b86dd9",
  measurementId: "G-XFJNP8EZQL"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
