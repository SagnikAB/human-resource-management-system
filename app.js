const storageKey = "hrms-static-demo-v2";

const seed = {
  users: [
    {
      id: "u-admin",
      email: "admin@company.test",
      password: "AdminPass123!",
      role: "ADMIN",
      employeeId: "e-admin"
    },
    {
      id: "u-alex",
      email: "alex.employee@company.test",
      password: "EmployeePass123!",
      role: "EMPLOYEE",
      employeeId: "e-alex"
    }
  ],
  employees: [
    {
      id: "e-admin",
      code: "HR-001",
      name: "Morgan Admin",
      email: "admin@company.test",
      role: "ADMIN",
      department: "Human Resources",
      designation: "HR Manager",
      phone: "+91 90000 10001",
      address: "Kolkata, India",
      salary: 128000,
      status: "Active"
    },
    {
      id: "e-alex",
      code: "EMP-1001",
      name: "Alex Rivera",
      email: "alex.employee@company.test",
      role: "EMPLOYEE",
      department: "Engineering",
      designation: "Software Engineer",
      phone: "+91 90000 10002",
      address: "Bengaluru, India",
      salary: 100000,
      status: "Active"
    },
    {
      id: "e-nia",
      code: "EMP-1002",
      name: "Nia Sharma",
      email: "nia.sharma@company.test",
      role: "EMPLOYEE",
      department: "Finance",
      designation: "Payroll Analyst",
      phone: "+91 90000 10003",
      address: "Delhi, India",
      salary: 82000,
      status: "Active"
    },
    {
      id: "e-ravi",
      code: "EMP-1003",
      name: "Ravi Mehta",
      email: "ravi.mehta@company.test",
      role: "EMPLOYEE",
      department: "Operations",
      designation: "Ops Coordinator",
      phone: "+91 90000 10004",
      address: "Mumbai, India",
      salary: 69000,
      status: "On Leave"
    }
  ],
  attendance: [
    { id: "a1", employeeId: "e-alex", date: "2026-07-01", checkIn: "09:12", checkOut: "18:04", status: "Present" },
    { id: "a2", employeeId: "e-alex", date: "2026-07-02", checkIn: "09:26", checkOut: "17:41", status: "Present" },
    { id: "a3", employeeId: "e-nia", date: "2026-07-02", checkIn: "09:05", checkOut: "18:10", status: "Present" },
    { id: "a4", employeeId: "e-ravi", date: "2026-07-03", checkIn: "-", checkOut: "-", status: "Leave" }
  ],
  leaves: [
    { id: "l1", employeeId: "e-ravi", type: "Sick", start: "2026-07-03", end: "2026-07-04", remarks: "Fever and doctor visit", status: "Pending", note: "" },
    { id: "l2", employeeId: "e-alex", type: "Paid", start: "2026-06-24", end: "2026-06-25", remarks: "Family travel", status: "Approved", note: "Approved by HR" }
  ],
  payroll: [
    { id: "p1", employeeId: "e-alex", period: "June 2026", gross: 100000, deductions: 8500, net: 91500, status: "Published" },
    { id: "p2", employeeId: "e-nia", period: "June 2026", gross: 82000, deductions: 6000, net: 76000, status: "Published" },
    { id: "p3", employeeId: "e-ravi", period: "June 2026", gross: 69000, deductions: 5200, net: 63800, status: "Draft" }
  ],
  currentUserId: null
};

let state = loadState();
let view = "dashboard";
let authMode = "signin";
let selectedEmployeeId = "e-alex";
let employeeSearch = "";
let sidebarOpen = false;

function loadState() {
  const saved = localStorage.getItem(storageKey);
  return saved ? JSON.parse(saved) : structuredClone(seed);
}

function saveState() {
  localStorage.setItem(storageKey, JSON.stringify(state));
}

function qs(selector) {
  return document.querySelector(selector);
}

function money(value) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0
  }).format(value);
}

function today() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function currentMonthLabel() {
  return new Date().toLocaleDateString("en-IN", { month: "long", year: "numeric" });
}

function resetDemo() {
  state = structuredClone(seed);
  view = "dashboard";
  employeeSearch = "";
  sidebarOpen = false;
  saveState();
  toast("Demo data reset to defaults.");
  render();
}

function currentUser() {
  return state.users.find((user) => user.id === state.currentUserId);
}

function employeeName(employeeId) {
  return state.employees.find((employee) => employee.id === employeeId)?.name ?? "Unknown";
}

function employeeForUser(user = currentUser()) {
  return state.employees.find((employee) => employee.id === user?.employeeId);
}

function isHr(user = currentUser()) {
  return user?.role === "ADMIN" || user?.role === "HR";
}

function initials(name) {
  return name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function toast(message) {
  const node = document.createElement("div");
  node.className = "toast";
  node.textContent = message;
  document.body.appendChild(node);
  setTimeout(() => node.remove(), 2400);
}

function render() {
  const user = currentUser();
  qs("#app").innerHTML = user ? appShell(user) : authScreen();
  bindEvents();
}

function authScreen() {
  const isSignIn = authMode === "signin";
  return `
    <main class="auth-screen">
      <section class="auth-panel">
        <div class="brand">
          <small>Human Resource Management System</small>
          <h1>Every workday, perfectly aligned.</h1>
          <p class="muted">Use the demo accounts or register a new employee profile for this static GitHub Pages build.</p>
        </div>
        <div class="tabs" aria-label="Authentication mode">
          <button class="${isSignIn ? "active" : ""}" data-auth-mode="signin">Sign In</button>
          <button class="${!isSignIn ? "active" : ""}" data-auth-mode="signup">Sign Up</button>
        </div>
        <form class="form" id="${isSignIn ? "signinForm" : "signupForm"}">
          ${isSignIn ? signinFields() : signupFields()}
          <button class="primary" type="submit">${isSignIn ? "Enter Dashboard" : "Create Account"}</button>
        </form>
      </section>
      <section class="auth-art">
        <div class="feature-strip">
          <div class="metric"><span class="muted">Profiles</span><strong>${state.employees.length}</strong></div>
          <div class="metric"><span class="muted">Leave Requests</span><strong>${state.leaves.length}</strong></div>
          <div class="metric"><span class="muted">Attendance Rows</span><strong>${state.attendance.length}</strong></div>
          <div class="metric"><span class="muted">Payroll Records</span><strong>${state.payroll.length}</strong></div>
        </div>
        <div class="wireframe-card">
          <img src="wireframe-reference.svg" alt="HRMS wireframe reference" />
        </div>
      </section>
    </main>
  `;
}

function signinFields() {
  return `
    <div class="form-row">
      <label for="email">Email</label>
      <input id="email" name="email" type="email" value="admin@company.test" required />
    </div>
    <div class="form-row">
      <label for="password">Password</label>
      <div class="input-group">
        <input id="password" name="password" type="password" value="AdminPass123!" required />
        <button type="button" class="ghost input-addon" data-toggle-password="password" aria-label="Show password">Show</button>
      </div>
    </div>
    <p class="notice">Admin: admin@company.test / AdminPass123!<br />Employee: alex.employee@company.test / EmployeePass123!</p>
  `;
}

function signupFields() {
  return `
    <div class="two">
      <div class="form-row">
        <label for="firstName">First Name</label>
        <input id="firstName" name="firstName" required />
      </div>
      <div class="form-row">
        <label for="lastName">Last Name</label>
        <input id="lastName" name="lastName" required />
      </div>
    </div>
    <div class="form-row">
      <label for="signupEmail">Email</label>
      <input id="signupEmail" name="email" type="email" required />
    </div>
    <div class="two">
      <div class="form-row">
        <label for="employeeCode">Employee ID</label>
        <input id="employeeCode" name="employeeCode" placeholder="EMP-1004" required />
      </div>
      <div class="form-row">
        <label for="role">Role</label>
        <select id="role" name="role">
          <option value="EMPLOYEE">Employee</option>
          <option value="HR">HR</option>
        </select>
      </div>
    </div>
    <div class="form-row">
      <label for="signupPassword">Password</label>
      <input id="signupPassword" name="password" type="password" minlength="8" required />
    </div>
  `;
}

function appShell(user) {
  const employee = employeeForUser(user);
  const nav = isHr(user)
    ? ["dashboard", "employees", "attendance", "leave", "payroll", "wireframe"]
    : ["dashboard", "profile", "attendance", "leave", "payroll", "wireframe"];

  return `
    <main class="shell">
      <button class="menu-toggle" data-action="toggle-sidebar" aria-label="Toggle navigation">${sidebarOpen ? "✕" : "☰"}</button>
      ${sidebarOpen ? `<button class="sidebar-backdrop" data-action="toggle-sidebar" aria-label="Close navigation"></button>` : ""}
      <aside class="sidebar ${sidebarOpen ? "open" : ""}">
        <div class="profile-chip">
          <div class="avatar">${initials(employee?.name ?? "HR")}</div>
          <div>
            <strong>${employee?.name ?? "HRMS User"}</strong>
            <div class="muted">${user.role}</div>
          </div>
        </div>
        <nav class="nav">
          ${nav.map((item) => `<button class="${view === item ? "active" : ""}" data-view="${item}">${label(item)}</button>`).join("")}
        </nav>
        <div class="sidebar-footer">
          <button class="ghost" data-action="reset-demo">Reset Demo</button>
          <button class="ghost" data-action="logout">Log Out</button>
        </div>
      </aside>
      <section class="main">
        ${contentFor(view, user)}
      </section>
    </main>
  `;
}

function label(key) {
  return {
    dashboard: "Dashboard",
    employees: "Employees",
    profile: "My Profile",
    attendance: "Attendance",
    leave: "Leave",
    payroll: "Payroll",
    wireframe: "Wireframe"
  }[key];
}

function pageHeader(title, subtitle, actions = "") {
  return `
    <header class="topbar">
      <div class="page-title">
        <span class="eyebrow">Human Resource Management System</span>
        <h1>${title}</h1>
        <span class="muted">${subtitle}</span>
      </div>
      <div class="actions">${actions}</div>
    </header>
  `;
}

function contentFor(page, user) {
  if (page === "employees") return employeesView();
  if (page === "profile") return profileView(employeeForUser(user));
  if (page === "attendance") return attendanceView(user);
  if (page === "leave") return leaveView(user);
  if (page === "payroll") return payrollView(user);
  if (page === "wireframe") return wireframeView();
  return dashboardView(user);
}

function dashboardView(user) {
  const pending = state.leaves.filter((leave) => leave.status === "Pending").length;
  const presentToday = state.attendance.filter((row) => row.date === today() && row.status === "Present").length;
  return `
    ${pageHeader(isHr(user) ? "Admin Dashboard" : "Employee Dashboard", "Quick access to the HR workflows from the design.")}
    <section class="grid dashboard-grid">
      <div class="metric"><span class="muted">Employees</span><strong>${state.employees.length}</strong></div>
      <div class="metric"><span class="muted">Present Today</span><strong>${presentToday}</strong></div>
      <div class="metric"><span class="muted">Pending Leave</span><strong>${pending}</strong></div>
      <div class="metric"><span class="muted">Payroll Items</span><strong>${state.payroll.length}</strong></div>
    </section>
    <section class="grid content-grid" style="margin-top:16px">
      <div class="panel">
        <div class="panel-head"><h2>Recent Activity</h2><span class="pill">Live Demo</span></div>
        <div class="list">
          ${state.leaves.slice(0, 4).map((leave) => `
            <article class="card employee-card">
              <div class="avatar">${initials(employeeName(leave.employeeId))}</div>
              <div><strong>${employeeName(leave.employeeId)}</strong><div class="muted">${leave.type} leave from ${leave.start} to ${leave.end}</div></div>
              <span class="pill ${leave.status.toLowerCase()}">${leave.status}</span>
            </article>
          `).join("")}
        </div>
      </div>
      <div class="panel">
        <div class="panel-head"><h2>Core Features</h2></div>
        <div class="list">
          <div class="notice">Role-based access separates Admin/HR controls from employee self-service.</div>
          <div class="notice">Attendance, leave, profile, and payroll screens are wired with editable demo data.</div>
          <div class="notice">This static build is ready for GitHub Pages deployment from the repository root.</div>
        </div>
      </div>
    </section>
  `;
}

function filteredEmployees() {
  const query = employeeSearch.trim().toLowerCase();
  if (!query) return state.employees;
  return state.employees.filter(
    (employee) =>
      employee.name.toLowerCase().includes(query) ||
      employee.code.toLowerCase().includes(query) ||
      employee.department.toLowerCase().includes(query) ||
      employee.email.toLowerCase().includes(query)
  );
}

function employeesView() {
  const rows = filteredEmployees();
  return `
    ${pageHeader("Employee Directory", "Search, switch between employees, and manage staff records.")}
    <section class="grid content-grid">
      <div class="panel">
        <div class="panel-head">
          <h2>All Employees</h2>
          <span class="pill">${rows.length} shown</span>
        </div>
        <div class="form-row search-row">
          <input id="employeeSearch" type="search" placeholder="Search by name, ID, department, or email…" value="${employeeSearch}" />
        </div>
        <div class="list">
          ${rows.length ? rows.map((employee) => `
            <article class="card employee-card ${employee.id === selectedEmployeeId ? "selected" : ""}">
              <div class="avatar">${initials(employee.name)}</div>
              <div>
                <strong>${employee.name}</strong>
                <div class="muted">${employee.code} · ${employee.department} · ${employee.designation}</div>
              </div>
              <button data-select-employee="${employee.id}">${employee.id === selectedEmployeeId ? "Selected" : "Open"}</button>
            </article>
          `).join("") : `<div class="empty">No employees match your search.</div>`}
        </div>
      </div>
      ${profileView(state.employees.find((employee) => employee.id === selectedEmployeeId), true)}
    </section>
  `;
}

function profileView(employee, compact = false) {
  if (!employee) return `<div class="empty">No profile selected.</div>`;
  return `
    ${compact ? "" : pageHeader("My Profile", "View and update limited employee details.")}
    <section class="panel">
      <div class="panel-head"><h2>${employee.name}</h2><span class="pill">${employee.status}</span></div>
      <form class="form" id="profileForm" data-profile-id="${employee.id}">
        <div class="two">
          <div class="form-row"><label>Employee ID</label><input value="${employee.code}" disabled /></div>
          <div class="form-row"><label>Role</label><input value="${employee.role}" disabled /></div>
        </div>
        <div class="two">
          <div class="form-row"><label>Department</label><input name="department" value="${employee.department}" ${compact ? "" : "disabled"} /></div>
          <div class="form-row"><label>Designation</label><input name="designation" value="${employee.designation}" ${compact ? "" : "disabled"} /></div>
        </div>
        <div class="two">
          <div class="form-row"><label>Phone</label><input name="phone" value="${employee.phone}" /></div>
          <div class="form-row"><label>Email</label><input value="${employee.email}" disabled /></div>
        </div>
        <div class="form-row"><label>Address</label><textarea name="address">${employee.address}</textarea></div>
        <button class="primary" type="submit">Save Profile</button>
      </form>
    </section>
  `;
}

function attendanceView(user) {
  const rows = isHr(user) ? state.attendance : state.attendance.filter((row) => row.employeeId === user.employeeId);
  return `
    ${pageHeader("Attendance", "Daily and weekly attendance tracking with check-in and check-out.", isHr(user) ? "" : `<button class="primary" data-action="checkin">Check In</button><button data-action="checkout">Check Out</button>`)}
    <section class="grid content-grid">
      <div class="table-shell">
        <table>
          <thead><tr><th>Date</th><th>Employee</th><th>Check In</th><th>Check Out</th><th>Status</th></tr></thead>
          <tbody>
            ${rows.map((row) => `
              <tr>
                <td>${row.date}</td>
                <td>${employeeName(row.employeeId)}</td>
                <td>${row.checkIn}</td>
                <td>${row.checkOut}</td>
                <td><span class="pill ${row.status.toLowerCase()}">${row.status}</span></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
      <div class="panel">
        <div class="panel-head"><h2>Monthly Markers</h2><span class="pill">${currentMonthLabel()}</span></div>
        <div class="calendar">${calendarDays(user)}</div>
      </div>
    </section>
  `;
}

function calendarDays(user) {
  const employeeId = isHr(user) ? selectedEmployeeId : user.employeeId;
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const daysInMonth = new Date(year, now.getMonth() + 1, 0).getDate();
  const weekdayOffset = new Date(year, now.getMonth(), 1).getDay();
  const blanks = Array.from({ length: weekdayOffset }, () => `<div class="day blank"></div>`).join("");
  const days = Array.from({ length: daysInMonth }, (_, index) => {
    const day = String(index + 1).padStart(2, "0");
    const dateKey = `${year}-${month}-${day}`;
    const row = state.attendance.find((item) => item.employeeId === employeeId && item.date === dateKey);
    const className = row?.status === "Present" ? "present" : row?.status === "Leave" ? "leave" : row?.status === "Absent" ? "absent" : "";
    const isToday = dateKey === today() ? " today" : "";
    return `<div class="day ${className}${isToday}" title="${dateKey}">${index + 1}</div>`;
  }).join("");
  return blanks + days;
}

function leaveView(user) {
  const rows = isHr(user) ? state.leaves : state.leaves.filter((leave) => leave.employeeId === user.employeeId);
  return `
    ${pageHeader("Leave Management", "Apply for time off and process approvals.", isHr(user) ? "" : `<button class="primary" data-action="show-leave-form">Apply Leave</button>`)}
    <section class="grid content-grid">
      <div class="panel">
        <div class="panel-head"><h2>Leave Requests</h2><span class="pill">${rows.length} shown</span></div>
        <div class="list">
          ${rows.length ? rows.map((leave) => leaveCard(leave, user)).join("") : `<div class="empty">No leave requests yet.</div>`}
        </div>
      </div>
      <div class="panel">
        <div class="panel-head"><h2>Apply for Leave</h2></div>
        <form class="form" id="leaveForm">
          <div class="form-row"><label>Type</label><select name="type"><option>Paid</option><option>Sick</option><option>Unpaid</option></select></div>
          <div class="two">
            <div class="form-row"><label>Start Date</label><input name="start" type="date" required /></div>
            <div class="form-row"><label>End Date</label><input name="end" type="date" required /></div>
          </div>
          <div class="form-row"><label>Remarks</label><textarea name="remarks" required></textarea></div>
          <button class="primary" type="submit">Submit Request</button>
        </form>
      </div>
    </section>
  `;
}

function leaveCard(leave, user) {
  return `
    <article class="card">
      <div class="panel-head">
        <div><strong>${employeeName(leave.employeeId)}</strong><div class="muted">${leave.type} - ${leave.start} to ${leave.end}</div></div>
        <span class="pill ${leave.status.toLowerCase()}">${leave.status}</span>
      </div>
      <p class="muted">${leave.remarks}</p>
      ${isHr(user) && leave.status === "Pending" ? `
        <div class="actions">
          <button class="success" data-leave-decision="${leave.id}" data-status="Approved">Approve</button>
          <button class="danger" data-leave-decision="${leave.id}" data-status="Rejected">Reject</button>
        </div>
      ` : ""}
    </article>
  `;
}

function payrollView(user) {
  const rows = isHr(user) ? state.payroll : state.payroll.filter((pay) => pay.employeeId === user.employeeId && pay.status === "Published");
  return `
    ${pageHeader("Payroll", isHr(user) ? "View and update salary records." : "Read-only salary visibility for employees.")}
    <section class="grid content-grid">
      <div class="table-shell">
        <table>
          <thead><tr><th>Period</th><th>Employee</th><th>Gross</th><th>Deductions</th><th>Net</th><th>Status</th></tr></thead>
          <tbody>
            ${rows.map((pay) => `
              <tr>
                <td>${pay.period}</td>
                <td>${employeeName(pay.employeeId)}</td>
                <td>${money(pay.gross)}</td>
                <td>${money(pay.deductions)}</td>
                <td>${money(pay.net)}</td>
                <td><span class="pill">${pay.status}</span></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
      <div class="panel">
        <div class="panel-head"><h2>Salary Structure</h2></div>
        ${isHr(user) ? salaryEditor() : `<div class="notice">Payroll is read-only for employees. Contact HR for salary structure changes.</div>`}
      </div>
    </section>
  `;
}

function salaryEditor() {
  const employee = state.employees.find((item) => item.id === selectedEmployeeId) ?? state.employees[1];
  return `
    <form class="form" id="salaryForm">
      <div class="form-row">
        <label>Employee</label>
        <select name="employeeId">
          ${state.employees.filter((item) => item.role === "EMPLOYEE").map((item) => `<option value="${item.id}" ${item.id === employee.id ? "selected" : ""}>${item.name}</option>`).join("")}
        </select>
      </div>
      <div class="form-row"><label>Monthly Gross</label><input name="salary" type="number" value="${employee.salary}" min="0" /></div>
      <button class="primary" type="submit">Update Salary</button>
    </form>
  `;
}

function wireframeView() {
  return `
    ${pageHeader("Wireframe Reference", "The supplied concept image is included in the deployable site.")}
    <div class="wireframe-card">
      <img src="wireframe-reference.svg" alt="Original HRMS wireframe reference" />
    </div>
  `;
}

function bindEvents() {
  document.querySelectorAll("[data-auth-mode]").forEach((button) => {
    button.addEventListener("click", () => {
      authMode = button.dataset.authMode;
      render();
    });
  });

  document.querySelectorAll("[data-view]").forEach((button) => {
    button.addEventListener("click", () => {
      view = button.dataset.view;
      sidebarOpen = false;
      render();
    });
  });

  document.querySelectorAll("[data-toggle-password]").forEach((button) => {
    button.addEventListener("click", () => {
      const input = qs(`#${button.dataset.togglePassword}`);
      if (!input) return;
      const hidden = input.type === "password";
      input.type = hidden ? "text" : "password";
      button.textContent = hidden ? "Hide" : "Show";
    });
  });

  qs("#employeeSearch")?.addEventListener("input", (event) => {
    employeeSearch = event.currentTarget.value;
    render();
    const input = qs("#employeeSearch");
    if (input) {
      input.focus();
      input.setSelectionRange(input.value.length, input.value.length);
    }
  });

  document.querySelectorAll("[data-select-employee]").forEach((button) => {
    button.addEventListener("click", () => {
      selectedEmployeeId = button.dataset.selectEmployee;
      render();
    });
  });

  document.querySelectorAll("[data-leave-decision]").forEach((button) => {
    button.addEventListener("click", () => {
      const leave = state.leaves.find((item) => item.id === button.dataset.leaveDecision);
      if (leave) {
        leave.status = button.dataset.status;
        leave.note = `${button.dataset.status} by HR`;
        saveState();
        toast(`Leave request ${button.dataset.status.toLowerCase()}.`);
        render();
      }
    });
  });

  qs("[data-action='logout']")?.addEventListener("click", () => {
    state.currentUserId = null;
    sidebarOpen = false;
    saveState();
    render();
  });

  qs("[data-action='reset-demo']")?.addEventListener("click", () => {
    if (window.confirm("Reset all demo data to defaults? This clears local changes.")) {
      resetDemo();
    }
  });

  document.querySelectorAll("[data-action='toggle-sidebar']").forEach((button) => {
    button.addEventListener("click", () => {
      sidebarOpen = !sidebarOpen;
      render();
    });
  });

  qs("[data-action='checkin']")?.addEventListener("click", () => {
    const user = currentUser();
    const existing = state.attendance.find((row) => row.employeeId === user.employeeId && row.date === today());
    if (existing) {
      existing.checkIn = new Date().toTimeString().slice(0, 5);
      existing.status = "Present";
    } else {
      state.attendance.unshift({ id: crypto.randomUUID(), employeeId: user.employeeId, date: today(), checkIn: new Date().toTimeString().slice(0, 5), checkOut: "-", status: "Present" });
    }
    saveState();
    toast("Checked in for today.");
    render();
  });

  qs("[data-action='checkout']")?.addEventListener("click", () => {
    const user = currentUser();
    const row = state.attendance.find((item) => item.employeeId === user.employeeId && item.date === today());
    if (row) {
      row.checkOut = new Date().toTimeString().slice(0, 5);
      saveState();
      toast("Checked out for today.");
      render();
    } else {
      toast("Check in first before checking out.");
    }
  });

  qs("#signinForm")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.currentTarget));
    const user = state.users.find((item) => item.email === data.email && item.password === data.password);
    if (!user) {
      toast("Invalid email or password.");
      return;
    }
    state.currentUserId = user.id;
    view = "dashboard";
    saveState();
    render();
  });

  qs("#signupForm")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.currentTarget));
    const id = crypto.randomUUID();
    const employeeId = crypto.randomUUID();
    const role = data.role === "HR" ? "HR" : "EMPLOYEE";
    state.users.push({ id, email: data.email, password: data.password, role, employeeId });
    state.employees.push({
      id: employeeId,
      code: data.employeeCode,
      name: `${data.firstName} ${data.lastName}`,
      email: data.email,
      role,
      department: role === "HR" ? "Human Resources" : "Unassigned",
      designation: role === "HR" ? "HR Officer" : "Employee",
      phone: "",
      address: "",
      salary: 0,
      status: "Active"
    });
    state.currentUserId = id;
    saveState();
    render();
  });

  qs("#profileForm")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const data = Object.fromEntries(new FormData(form));
    const employee = state.employees.find((item) => item.id === form.dataset.profileId);
    if (employee) {
      employee.phone = data.phone ?? employee.phone;
      employee.address = data.address ?? employee.address;
      employee.department = data.department ?? employee.department;
      employee.designation = data.designation ?? employee.designation;
      saveState();
      toast("Profile saved.");
      render();
    }
  });

  qs("#leaveForm")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const user = currentUser();
    const data = Object.fromEntries(new FormData(event.currentTarget));
    if (!data.start || !data.end || data.end < data.start) {
      toast("Choose a valid leave date range.");
      return;
    }
    state.leaves.unshift({
      id: crypto.randomUUID(),
      employeeId: user.employeeId,
      type: data.type,
      start: data.start,
      end: data.end,
      remarks: data.remarks,
      status: "Pending",
      note: ""
    });
    saveState();
    toast("Leave request submitted.");
    render();
  });

  qs("#salaryForm")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.currentTarget));
    const employee = state.employees.find((item) => item.id === data.employeeId);
    if (employee) {
      employee.salary = Number(data.salary);
      selectedEmployeeId = employee.id;
      saveState();
      toast("Salary structure updated.");
      render();
    }
  });
}

render();
