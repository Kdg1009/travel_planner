import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../css/loginPage.css';

const RegisterPage = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({email, password}),
            });

            const result = await response.json();

            if (result.success) {
                console.log("register success!");
                navigate('/login');
            } else {
                setMessage(result.message || 'Registeration failed');
            }
        } catch (error) {
            setMessage('Server error. Please try again later.');
        }
    };

    return (
        <div className="login-wrapper">
            <div className="login-container">
                <h2>Register</h2>
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
                  <button type="submit">Submit</button>
                </form>

                {message && <div className="login-error">{message}</div>}
            </div>
        </div>
    );
};

export default RegisterPage;