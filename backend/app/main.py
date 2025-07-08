import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    debug = os.getenv("FLASK_ENV", "production") != "production"
    port  = int(os.getenv("PORT", 5000))
    # 0.0.0.0 으로 바인딩하면 외부에서도 접근 가능
    app.run(host="0.0.0.0", port=port, debug=debug)