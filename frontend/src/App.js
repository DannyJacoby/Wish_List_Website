import React, { useState, useEffect } from 'react';
import Header from './components/Header'
import './App.css';
import Button from './components/Button';
import { NavLink, Switch, Route, Router } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';

// var herokuURL="https://wishlist-cst438.herokuapp.com/time"
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
      <h1>      
        <Header title={"Wishlist App"}/>
      </h1>
      <Navigation />
      <Main />
      <div className="btn">
        <Button text={"Create Account"}/>
      </div>

    </div>
    </BrowserRouter>
  );
}

const Navigation = () => (
  <nav>
    <ul>
      <li><NavLink to='/'>Home</NavLink></li>
      <li><NavLink to='/login'>Login</NavLink></li>
      <li><NavLink to='/createaccount'>CreateAccount</NavLink></li>
      <li><NavLink to='/profile'>Profile</NavLink></li>
    </ul>
  </nav>
);

const Home = () => (
  <div className='home'>
    <h1>Welcome to our wishlist app!</h1>
    <p> Create an account or login to get started.</p>
  </div>
);

const Login = () => (
  <div className='login'>
    <h1>Login Page</h1>
    <p>Ipsum dolor dolorem consectetur est velit fugiat. Dolorem provident corporis fuga saepe distinctio ipsam? Et quos harum excepturi dolorum molestias?</p>
    
  </div>
);

const CreateAcc = () => (
  <div className='createaccount'>
    <h1>Create an Account!</h1>
    <p>Enter your name, username, email, and password to get started.<strong>hello@example.com</strong></p>
  </div>
);

const Profile = () => (
  <div className='profile'>
    <h1>Profile Page</h1>
    <p> Create or view your wishlists here.</p>
  </div>
);

const Main = () => (
  <Switch>
    <Route path='/' component={Home}></Route>
    <Route path='/login' component={Login}></Route>
    <Route path='/createaccount' component={CreateAcc}></Route>
    <Route path='/profile' component={Profile}></Route>
  </Switch>
);

export default App;
