import React, { useState, useEffect } from 'react';
<<<<<<< HEAD
import Header from './components/Header'
import Wishlists from './components/Wishlists'
=======
import logo from './logo.svg';
>>>>>>> 6f9cf475f339f4c92c864244e0e46d21ee874e20
import './App.css';

var herokuURL="https://wishlist-cst438.herokuapp.com/time"
var localHost="http://localhost:5000/time"

function App() {
  const [currentTime, setCurrentTime] = useState(0);
<<<<<<< HEAD
  const [wishlists, setWishlists] = useState( [
    {
        id: 1,
        text: 'Wishlist 1',
        category: 'home',
        reminder: true,
    },
    {
        id: 2,
        text: 'Wishlist 2',
        category: 'expensive',
        reminder: true,
    },
    {
        id: 3,
        text: 'Gym Equipment',
        category: 'gym',
        reminder: false,
    }
])

  useEffect(() => {
    fetch(localHost).then(res => res.json()).then(data => {
=======

  useEffect(() => {
    fetch(herokuURL).then(res => res.json()).then(data => {
>>>>>>> 6f9cf475f339f4c92c864244e0e46d21ee874e20
      setCurrentTime(data.time);
    });
  }, []);

  return (
<<<<<<< HEAD
    <div className="container">
      <Header />
      <Wishlists wishlists={wishlists} />
=======
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>The current time is {currentTime}. </p>
      </header>
>>>>>>> 6f9cf475f339f4c92c864244e0e46d21ee874e20
    </div>
  );
}

export default App;
