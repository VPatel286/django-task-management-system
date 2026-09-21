function Register({
  username,
  setUsername,
  password,
  setPassword,
  handleRegister,
  registerError,
  isRegistering,
  setShowRegister,
}) {
  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Create Account</h1>

        <p className="login-subtitle">
          Create your Task API account
        </p>

        <form onSubmit={handleRegister}>
          <div className="login-field">
            <label>Username</label>

            <input
              type="text"
              placeholder="Choose a username"
              value={username}
              onChange={(event) =>
                setUsername(event.target.value)
              }
            />
          </div>

          <div className="login-field">
            <label>Password</label>

            <input
              type="password"
              placeholder="Choose a password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
            />
          </div>

          {registerError && (
            <p className="login-error">
              {registerError}
            </p>
          )}

          <button
            type="submit"
            className="login-button"
            disabled={isRegistering}
          >
            {isRegistering ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <button
          type="button"
          className="secondary-button"
          onClick={() => setShowRegister(false)}
        >
          Back to Login
        </button>
      </div>
    </div>
  );
}

export default Register;