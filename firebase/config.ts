// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyAHGhfnYf-RYDOdaOtCrGDKG5covOigdCI",
    authDomain: "gasolean-2c897.firebaseapp.com",
    projectId: "gasolean-2c897",
    storageBucket: "gasolean-2c897.firebasestorage.app",
    messagingSenderId: "796230442248",
    appId: "1:796230442248:web:183b91790f19da3a1560bd",
    measurementId: "G-V8LYMSVP2W"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getFirestore(app);

export { db };
