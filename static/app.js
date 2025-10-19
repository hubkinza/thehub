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
// Logout
async function logout() {
  try {
    await fetch(`${API_URL}/logout`, {
      method: "POST",
      credentials: "include",
    });
    window.location.href = "/logout.html";
  } catch (error) {
    alert("Logout failed");
  }
}
// Get all posts
async function getPosts(page = 1, search = "") {
  try {
    const response = await fetch(
      `${API_URL}/posts?page=${page}&search=${search}`,
      {
        credentials: "include",
      }
    );
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch posts");
    return { posts: [], total: 0 };
  }
}

// Get single post
async function getPost(postId) {
  try {
    const response = await fetch(`${API_URL}/posts/${postId}`, {
      credentials: "include",
    });
    return await response.json();
  } catch (error) {
    console.error("Failed to fetch post");
    return null;
  }
}
