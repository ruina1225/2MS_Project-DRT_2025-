// import React from "react";

// function Users() {
//   return <h1>👤 사용자 관리 페이지</h1>;
// }

// export default Users;

// import React, { useEffect, useState } from "react";
// import axios from "axios";

// function Users() {
//   const [users, setUsers] = useState([]);
//   const [filteredUsers, setFilteredUsers] = useState([]);
//   const [search, setSearch] = useState("");

//   const apiUrl = "http://localhost:3434"; // FastAPI 백엔드 주소

//   // 사용자 목록 불러오기
//   const fetchUsers = async () => {
//     try {
//       const res = await axios.get(`${apiUrl}/users`);
//       setUsers(res.data.users);
//       setFilteredUsers(res.data.users);
//     } catch (err) {
//       console.error("사용자 조회 실패:", err);
//     }
//   };

//   useEffect(() => {
//     fetchUsers();
//   }, []);

//   // 검색어 변경 시 필터링
//   useEffect(() => {
//     const filtered = users.filter((user) =>
//       user.name.toLowerCase().includes(search.toLowerCase())
//     );
//     setFilteredUsers(filtered);
//   }, [search, users]);

//   // 사용자 삭제
//   const deleteUser = async (userId) => {
//     if (!window.confirm("정말 삭제하시겠습니까?")) return;

//     try {
//       await axios.delete(`${apiUrl}/users/${userId}`);
//       alert("삭제 완료");
//       fetchUsers(); // 목록 다시 불러오기
//     } catch (err) {
//       console.error("삭제 실패:", err);
//       alert("삭제 실패");
//     }
//   };

//   return (
//     <div style={{ padding: "2rem" }}>
//       <h2>사용자 검색</h2>
//       <input
//         type="text"
//         placeholder="이름으로 검색"
//         value={search}
//         onChange={(e) => setSearch(e.target.value)}
//         style={{ marginBottom: "1rem", padding: "0.5rem" }}
//       />

//       <h2>사용자 목록</h2>
//       <table border="1" cellPadding="8">
//         <thead>
//           <tr>
//             <th>ID</th>
//             <th>이름</th>
//             <th>생년월일</th>
//             <th>사진</th>
//             <th>삭제</th>
//           </tr>
//         </thead>
//         <tbody>
//           {filteredUsers.map((user) => (
//             <tr key={user.user_id}>
//               <td>{user.user_id}</td>
//               <td>{user.name}</td>
//               <td>{user.birth_date}</td>
//               <td>
//                 <img
//                   src={`${apiUrl}/users/photo-by-id/${user.user_id}`}
//                   alt="사용자 사진"
//                   width="60"
//                 />
//               </td>
//               <td>
//                 <button onClick={() => deleteUser(user.user_id)}>삭제</button>
//               </td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   );
// }

// export default Users;

import React, { useEffect, useState } from "react";
import axios from "axios";

function Users() {
  const [users, setUsers] = useState([]);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [search, setSearch] = useState("");

  const apiUrl = "http://localhost:3434"; // FastAPI 백엔드 주소

  const fetchUsers = async () => {
    try {
      const res = await axios.get(`${apiUrl}/users`);
      setUsers(res.data.users);
      setFilteredUsers(res.data.users);
    } catch (err) {
      console.error("사용자 조회 실패:", err);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  useEffect(() => {
    const filtered = users.filter((user) =>
      user.name.toLowerCase().includes(search.toLowerCase())
    );
    setFilteredUsers(filtered);
  }, [search, users]);

  const deleteUser = async (userId) => {
    if (!window.confirm("정말 삭제하시겠습니까?")) return;

    try {
      await axios.delete(`${apiUrl}/users/${userId}`);
      alert("삭제 완료");
      fetchUsers();
    } catch (err) {
      console.error("삭제 실패:", err);
      alert("삭제 실패");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>사용자 검색</h2>
      <input
        type="text"
        placeholder="이름으로 검색"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ marginBottom: "1rem", padding: "0.5rem" }}
      />

      <h2>사용자 목록</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>ID</th>
            <th>이름</th>
            <th>생년월일</th>
            <th>식별코드</th>
            <th>사진</th>
            <th>삭제</th>
          </tr>
        </thead>
        <tbody>
          {filteredUsers.map((user) => (
            <tr key={user.user_id}>
              <td>{user.user_id}</td>
              <td>{user.name}</td>
              <td>{user.birth_date}</td>
              <td>{user.identifier_code}</td>
              <td>
                <img
                  src={`${apiUrl}/users/photo-by-id/${user.user_id}`}
                  alt="사용자 사진"
                  width="60"
                />
              </td>
              <td>
                <button onClick={() => deleteUser(user.user_id)}>삭제</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Users;
