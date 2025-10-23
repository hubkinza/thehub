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
      alert("Registration successful! Welcome to The Hub!");
      window.location.href = "/discussions.html";
    } else {
      alert(data.error || "Registration failed. Please try again.");
    }
  } catch (error) {
    console.error("Registration error:", error);
    alert("An error occurred during registration. Please try again.");
  }
}

// Login
async function login(email, password, remember = false) {
  try {
    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password, remember }),
    });
    const data = await response.json();
    if (response.ok) {
      alert("Login successful! Welcome back!");
      window.location.href = "/discussions.html";
    } else {
      alert(data.error || "Login failed. Please try again.");
    }
  } catch (error) {
    console.error("Login error:", error);
    alert("An error occurred during login. Please try again.");
  }
}

// Logout
async function logout() {
  // Ask for confirmation before logging out
  if (!confirm("Are you sure you want to logout?")) {
    return; // User clicked "Cancel", do nothing
  }

  try {
    const response = await fetch(`${API_URL}/logout`, {
      method: "POST",
      credentials: "include",
    });
    if (response.ok) {
      alert("You have been logged out successfully!");
      window.location.href = "/login.html";
    } else {
      alert("Logout failed. Please try again.");
    }
  } catch (error) {
    console.error("Logout error:", error);
    alert("An error occurred during logout.");
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

// Create post
async function createPost(title, content, tags) {
  try {
    const response = await fetch(`${API_URL}/posts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ title, content, tags }),
    });
    const data = await response.json();
    if (response.ok) {
      alert("Post created successfully!");
      window.location.href = "/discussions.html";
    } else {
      alert(data.error || "Failed to create post.");
    }
  } catch (error) {
    alert("Failed to create post");
  }
}

// Delete post
async function deletePost(postId) {
  if (!confirm("Are you sure you want to delete this post?")) return;

  try {
    const response = await fetch(`${API_URL}/posts/${postId}`, {
      method: "DELETE",
      credentials: "include",
    });
    const data = await response.json();
    if (response.ok) {
      alert("Post deleted successfully");
      window.location.href = "/discussions.html";
    } else {
      alert(data.error || "Failed to delete post.");
    }
  } catch (error) {
    alert("Failed to delete post");
  }
}

// Get comments
async function getComments(postId) {
  try {
    const response = await fetch(`${API_URL}/posts/${postId}/comments`, {
      credentials: "include",
    });
    return await response.json();
  } catch (error) {
    return [];
  }
}

// Add comment
async function addComment(postId, content) {
  try {
    const response = await fetch(`${API_URL}/posts/${postId}/comments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ content }),
    });
    const data = await response.json();
    if (response.ok) {
      return data.comment;
    } else {
      alert(data.error || "Failed to add comment.");
      return null;
    }
  } catch (error) {
    alert("Failed to add comment");
    return null;
  }
}

// Toggle like
async function toggleLike(postId) {
  try {
    const response = await fetch(`${API_URL}/posts/${postId}/like`, {
      method: "POST",
      credentials: "include",
    });
    return await response.json();
  } catch (error) {
    return null;
  }
}
