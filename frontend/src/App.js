import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import './App.css';
import Button from './components/Button';
import Nav from './components/Nav';
import Profile from './components/Profile';
import EditProfile from './components/EditProfile';
import Login from './components/Login'
import Home from './components/Home'
import CreateAcc from './components/CreateAcc'
import { NavLink, Switch, Route } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';

var herokuURL="https://wishlist-cst438.herokuapp.com/time"
var localHost="http://localhost:5000/time"

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch(localHost).then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <BrowserRouter>
      <div className="App"> 
        <Nav />
          <h1>      
            <Header title={"Wishlist App"}/>
          </h1>
        <Switch>
          <Route exact path="/" component={Home}></Route>
          <Route exact path="/login" component={Login}></Route>
          <Route exact path="/create_account" component={CreateAcc}></Route>
          <Route exact path="/profile" component={Profile}></Route>
          <Route exact path="/edit_profile" component={EditProfile}></Route>
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
