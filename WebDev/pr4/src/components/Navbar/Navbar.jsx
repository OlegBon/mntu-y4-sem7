import React from "react";
import { NavLink } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">Robot Control</div>
      <ul className="navbar-nav">
        <li>
          <NavLink to="/">Моніторинг</NavLink>
        </li>
        <li>
          <NavLink to="/log">Журнал завдань</NavLink>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
