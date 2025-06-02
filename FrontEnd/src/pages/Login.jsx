import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/loginPage.css';

const LoginPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault(); // prevent page refresh

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const result = await response.json();

      if (result.success) {
        console.log('Logged in as user_id:', result.user_id);
        // navigate to user_submit
        navigate('/user_submit', { state: { userId: result.user_id } });
      } else {
        setMessage(result.message || 'Login failed');
      }
    } catch (error) {
      setMessage('Server error. Please try again later.');
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-container">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            name="email"
            placeholder="Email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit">Login</button>
        </form>

        {message && <div className="login-error">{message}</div>}

        <div className="register-text">
          Don't have an account?{' '}
          <span className="register-link" onClick={() => navigate('/register')}>
            Register
          </span>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
