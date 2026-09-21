function Login({
  username,
  setUsername,
  password,
  setPassword,
  handleLogin,
  loginError,
  isLoggingIn,
  setShowRegister,
  registerSuccess,
}) {
    return (
        <div className="login-page">
            <div className="login-card">
                <h1>Task API</h1>
                <p className="login-subtitle">Sign in to your account</p>

                {registerSuccess && (
                    <p className="login-success">
                        {registerSuccess}
                    </p>
                )}

                <form onSubmit={handleLogin}>
                    <div className="login-field">
                        <label>Username</label>
                        <input
                            type="text"
                            placeholder="Enter your username"
                            value={username}
                            onChange={(event) => setUsername(event.target.value)}
                        />
                    </div>

                    <div className="login-field">
                        <label>Password</label>
                        <input
                            type="password"
                            placeholder="Enter your password"
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                        />
                    </div>

                    {loginError && (
                        <p className="login-error">
                            {loginError}
                        </p>
                    )}

                    <button
                        type="submit"
                        className="login-button"
                        disabled={isLoggingIn}
                    >
                        {isLoggingIn ? "Logging in..." : "Login"}
                    </button>

                    <button
                        type="button"
                        className="secondary-button"
                        onClick={() => setShowRegister(true)}
                    >
                        Create Account
                    </button>
                </form>
            </div>
        </div>
    );
}

export default Login;