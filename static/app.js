// API Base URL
const API_URL = "/api";

// Check if user is logged in
async function checkAuth() {
  try {
    const response = await fetch(`${API_URL}/current-user`, {
      credentials: "include",
    });
    if (response.ok) {
      const data = await response.json();
      return data;
    }
    return null;
  } catch (error) {
    return null;
  }
}

// Register
async function register(username, email, password) {
  try {
    const response = await fetch(`${API_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ username, email, password }),
    });
    const data = await response.json();
    if (response.ok) {
      window.location.href = "/discussions.html";
    } else {
      alert(data.error);
    }
  } catch (error) {
    alert("Registration failed");
  }
}

// Login
async function login(email, password, remember) {
  try {
    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password, remember }),
    });
    const data = await response.json();
    if (response.ok) {
      window.location.href = "/discussions.html";
    } else {
      alert(data.error);
    }
  } catch (error) {
    alert("Login failed");
  }
}
