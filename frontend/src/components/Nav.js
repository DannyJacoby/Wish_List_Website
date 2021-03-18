import React from 'react';
import '../App.css';
import { Link } from 'react-router-dom';

function Nav() {

    const navStyle = {
        color: 'white'
    };

    return (
        <nav>
            <h1>Navigation</h1>
            <ul className="nav-links">
                <Link to="/" style={navStyle} >
                    <li>Home</li>
                </Link>
                <Link style={navStyle} to="/login">
                    <li>Login</li>
                </Link>
                <Link to="/create_account" style={navStyle} >
                    <li>Create Account</li>
                </Link>
                <Link to="/profile" style={navStyle} >
                    <li>Profile</li>
                </Link>
            </ul>
        </nav>
    );
}

export default Nav;