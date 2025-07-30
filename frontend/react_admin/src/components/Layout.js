import React from "react";
import { Link, Outlet, useNavigate } from "react-router-dom";

function Layout() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const linkStyle = {
    color: "#a29bfe",            // 💜 연보라색
    textDecoration: "none",      // 밑줄 제거
    fontWeight: "bold",          // 강조 (옵션)
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <aside
        style={{
          width: "240px",
          background: "#2f3542",
          color: "white",
          padding: "20px",
          display: "flex",
          flexDirection: "column",
          gap: "12px",
        }}
      >
        <h2 style={{ color: "#70a1ff" }}>관리자 페이지</h2>
        <nav style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          <Link to="/" style={linkStyle}>대시보드</Link>
          <Link to="/reservations" style={linkStyle}>예약 관리</Link>
          <Link to="/users" style={linkStyle}>사용자 관리</Link>
          <Link to="/voice-logs" style={linkStyle}>음성 로그</Link>
          <Link to="/statistics" style={linkStyle}>통계</Link>
          <Link to="/settings" style={linkStyle}>설정</Link>
          <button
            onClick={handleLogout}
            style={{
              marginTop: "20px",
              background: "#ff4757",
              color: "white",
              border: "none",
              padding: "8px",
              cursor: "pointer",
            }}
          >
            로그아웃
          </button>
        </nav>
      </aside>

      <main style={{ flex: 1, padding: "20px", backgroundColor: "#f1f2f6" }}>
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;
