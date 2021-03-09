import React, { useState, useEffect } from 'react';
import Header from './components/Header'
import Wishlists from './components/Wishlists'
import './App.css';

var herokuURL="https://wishlist-cst438.herokuapp.com/time"
var localHost="http://localhost:5000/time"

function App() {
  const [currentTime, setCurrentTime] = useState(0);
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
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="container">
      <Header />
      <Wishlists wishlists={wishlists} />
    </div>
  );
}

export default App;
