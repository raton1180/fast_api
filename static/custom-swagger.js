window.onload = function () {
  const ui = SwaggerUIBundle({
    url: "/openapi.json",
    dom_id: "#swagger-ui",
    presets: [SwaggerUIBundle.presets.apis],
    layout: "BaseLayout",
    requestInterceptor: (req) => {
      const token = localStorage.getItem("access_token");
      if (token) {
        req.headers["Authorization"] = "Bearer " + token;
      }
      return req;
    },
    onComplete: () => {
      const authWrapper = document.querySelector(".auth-wrapper");
      if (!authWrapper) return;

      if (!document.getElementById("login-btn")) {
        const loginBtn = document.createElement("button");
        loginBtn.id = "login-btn";
        loginBtn.style.marginLeft = "10px";
        loginBtn.textContent = "Login";
        loginBtn.onclick = async () => {
          const email = prompt("Email:");
          const password = prompt("Password:");
          if (!email || !password) return alert("Email and password required");

          const resp = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
          });

          if (resp.ok) {
            const data = await resp.json();
            localStorage.setItem("access_token", data.data.access_token);
            alert("Logged in!");
          } else {
            alert("Login failed");
          }
        };
        authWrapper.appendChild(loginBtn);

        const logoutBtn = document.createElement("button");
        logoutBtn.id = "logout-btn";
        logoutBtn.style.marginLeft = "5px";
        logoutBtn.textContent = "Logout";
        logoutBtn.onclick = () => {
          localStorage.removeItem("access_token");
          alert("Logged out");
        };
        authWrapper.appendChild(logoutBtn);
      }
    },
  });
};
