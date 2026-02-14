const API_URL = "http://127.0.0.1:5000/api";

async function apiRequest(endpoint, method="GET", data=null) {
  const token = localStorage.getItem("token");

  const res = await fetch(`${API_URL}${endpoint}`, {
    method,
    headers: {
      "Content-Type":"application/json",
      "Authorization": token || ""
    },
    body: data ? JSON.stringify(data) : null
  });

  return res.json();
}
