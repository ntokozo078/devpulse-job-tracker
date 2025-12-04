from app import create_app

# Create the application instance using the factory function
app = create_app()

if __name__ == '__main__':
    # 'debug=True' enables the debugger and auto-reloader.
    # This means if you change code, the server restarts automatically.
    print("Starting DevPulse Server...")
    app.run(debug=True)