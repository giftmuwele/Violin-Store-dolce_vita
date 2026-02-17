const API_URL = "http://127.0.0.1:5000/api";

/* ----------------------------------------
   Check if user is logged in
-----------------------------------------*/
function isLoggedIn() {
    return localStorage.getItem("token") !== null;
}

/* ----------------------------------------
   Get current user role
-----------------------------------------*/
function getUserRole() {
    return localStorage.getItem("role");
}

/* ----------------------------------------
   Protect page (redirect if not logged in)
-----------------------------------------*/
function requireLogin() {
    if (!isLoggedIn()) {
        alert("Please login first.");
        window.location.href = "login.html";
    }
}

/* ----------------------------------------
   Protect admin page
-----------------------------------------*/
function requireAdmin() {
    if (!isLoggedIn() || getUserRole() !== "admin") {
        alert("Admin access only.");
        window.location.href = "index.html";
    }
}

/* ----------------------------------------
   Logout
-----------------------------------------*/
function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}
