from flask import Flask, render_template, request, redirect, session, jsonify
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
import yfinance as yf
import plotly
import plotly.graph_objects as go
import json


app = Flask(__name__)

# Session için secret key
app.secret_key = "finance-dashboard-secret-key"


# Database
db = SQL("sqlite:///finance.db")


# =========================================================
# ASSETS
# =========================================================

ASSETS = {

    "Emtialar": {

        "Altın (XAU/USD)": {
            "symbol": "GC=F",
            "emoji": "🥇"
        },

        "Gümüş (XAG/USD)": {
            "symbol": "SI=F",
            "emoji": "🥈"
        },

        "Ham Petrol (WTI)": {
            "symbol": "CL=F",
            "emoji": "🛢️"
        },

        "Doğal Gaz": {
            "symbol": "NG=F",
            "emoji": "🔥"
        },
    },


    "Dövizler": {

        "Dolar (USD/TRY)": {
            "symbol": "USDTRY=X",
            "emoji": "💵"
        },

        "Euro (EUR/TRY)": {
            "symbol": "EURTRY=X",
            "emoji": "💶"
        },

        "Sterlin (GBP/TRY)": {
            "symbol": "GBPTRY=X",
            "emoji": "💷"
        },

        "Euro (EUR/USD)": {
            "symbol": "EURUSD=X",
            "emoji": "🇪🇺"
        },

        "Sterlin (GBP/USD)": {
            "symbol": "GBPUSD=X",
            "emoji": "🇬🇧"
        },

        "İsv. Frangı (CHF)": {
            "symbol": "USDCHF=X",
            "emoji": "🇨🇭"
        },

        "Japon Yeni (JPY)": {
            "symbol": "USDJPY=X",
            "emoji": "🇯🇵"
        },
    },


    "Kripto": {

        "Bitcoin (BTC)": {
            "symbol": "BTC-USD",
            "emoji": "₿"
        },

        "Ethereum (ETH)": {
            "symbol": "ETH-USD",
            "emoji": "Ξ"
        },

        "Solana (SOL)": {
            "symbol": "SOL-USD",
            "emoji": "◎"
        },

        "BNB": {
            "symbol": "BNB-USD",
            "emoji": "🟡"
        },
    },


    "Endeksler": {

        "S&P 500": {
            "symbol": "^GSPC",
            "emoji": "📈"
        },

        "NASDAQ": {
            "symbol": "^IXIC",
            "emoji": "💻"
        },

        "BIST 100": {
            "symbol": "XU100.IS",
            "emoji": "🇹🇷"
        },

        "DAX": {
            "symbol": "^GDAXI",
            "emoji": "🇩🇪"
        },

        "FTSE 100": {
            "symbol": "^FTSE",
            "emoji": "🇬🇧"
        },
    }
}


# =========================================================
# PERIODS
# =========================================================

PERIODS = {

    "1 Hafta": "5d",

    "1 Ay": "1mo",

    "3 Ay": "3mo",

    "6 Ay": "6mo",

    "1 Yıl": "1y",

    "5 Yıl": "5y"
}


# =========================================================
# MARKET WATCHLIST
# =========================================================

MARKET_WATCHLIST = {

    "Gold": {
        "symbol": "GC=F",
        "emoji": "🥇"
    },

    "Bitcoin": {
        "symbol": "BTC-USD",
        "emoji": "₿"
    },

    "USD / TRY": {
        "symbol": "USDTRY=X",
        "emoji": "💵"
    },

    "EUR / TRY": {
        "symbol": "EURTRY=X",
        "emoji": "💶"
    },

    "GBP / TRY": {
        "symbol": "GBPTRY=X",
        "emoji": "💷"
    },

    "BIST 100": {
        "symbol": "XU100.IS",
        "emoji": "🇹🇷"
    }

}

def get_market_data():

    market_data = []

    for name, info in MARKET_WATCHLIST.items():

        try:
            ticker = yf.Ticker(info["symbol"])
            hist = ticker.history(period="2d")

            if hist.empty:
                continue

            price = float(hist["Close"].iloc[-1])
            previous = float(hist["Close"].iloc[-2])

            change = ((price - previous) / previous) * 100

            market_data.append({
                "name": name,
                "emoji": info["emoji"],
                "price": price,
                "change_percent": change
            })

        except Exception:
            continue

    return market_data


# =========================================================
# CHART FUNCTION
# =========================================================

def build_chart(hist, name):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=hist.index,

            y=hist["Close"],

            mode="lines",

            name=name
        )
    )

    fig.update_layout(

        title=f"{name} Fiyat Grafiği",

        xaxis_title="Tarih",

        yaxis_title="Fiyat",

        template="plotly_dark",

        height=500
    )

    return fig


# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():

    market_data = get_market_data()

    if "user_id" in session:

        user = db.execute(
            "SELECT username FROM users WHERE id = ?",
            session["user_id"]
        )

        return render_template(
            "index.html",
            username=user[0]["username"],
            market_data=market_data
        )

    return render_template(
        "index.html",
        market_data=market_data
    )


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            error = "Username is required."

        elif not password:
            error = "Password is required."

        elif password != confirmation:
            error = "Passwords do not match."

        else:

            existing_user = db.execute(
                "SELECT * FROM users WHERE username = ?",
                username
            )

            if len(existing_user) > 0:

                error = "Username already exists."

            else:

                password_hash = generate_password_hash(password)

                db.execute(
                    "INSERT INTO users (username, hash) VALUES (?, ?)",
                    username,
                    password_hash
                )

                return redirect("/")

    return render_template(
        "register.html",
        error=error
    )


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")


        if not username:

            return "Username is required"


        if not password:

            return "Password is required"


        rows = db.execute(

            "SELECT * FROM users WHERE username = ?",

            username
        )


        if len(rows) != 1:

            return "Invalid username or password"


        if not check_password_hash(

            rows[0]["hash"],

            password

        ):

            return "Invalid username or password"


        session["user_id"] = rows[0]["id"]


        return redirect("/")


    return render_template("login.html")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect("/login")


    portfolio = db.execute(

        """
        SELECT * FROM portfolio
        WHERE user_id = ?
        """,

        session["user_id"]
    )


    total_invested = 0

    current_value = 0


    # -----------------------------------------
    # Portfolio hesaplamaları
    # -----------------------------------------

    for item in portfolio:

        invested = (

            item["amount"] *

            item["buy_price"]
        )


        total_invested += invested


        try:

            ticker = yf.Ticker(

                item["symbol"]
            )


            hist = ticker.history(

                period="1d"
            )


            if not hist.empty:

                price = float(

                    hist["Close"].iloc[-1]
                )


                item["current_price"] = price


                item["current_value"] = (

                    price *

                    item["amount"]
                )


                item["profit"] = (

                    item["current_value"]

                    - invested
                )


                if invested > 0:

                    item["profit_percent"] = (

                        item["profit"]

                        / invested

                    ) * 100

                else:

                    item["profit_percent"] = 0


                current_value += (

                    item["current_value"]
                )


            else:

                item["current_price"] = 0

                item["current_value"] = 0

                item["profit"] = 0

                item["profit_percent"] = 0


        except Exception:

            item["current_price"] = 0

            item["current_value"] = 0

            item["profit"] = 0

            item["profit_percent"] = 0


    # -----------------------------------------
    # Total Profit
    # -----------------------------------------

    total_profit = (

        current_value -

        total_invested
    )


    # -----------------------------------------
    # Total Return
    # -----------------------------------------

    if total_invested > 0:

        total_return = (

            total_profit /

            total_invested

        ) * 100

    else:

        total_return = 0


    # -----------------------------------------
    # Market Data
    # -----------------------------------------

    market_data = []


    for name, info in MARKET_WATCHLIST.items():

        try:

            ticker = yf.Ticker(

                info["symbol"]
            )


            hist = ticker.history(

                period="5d"
            )


            if not hist.empty:

                current_price = float(

                    hist["Close"].iloc[-1]
                )


                first_price = float(

                    hist["Close"].iloc[0]
                )


                if first_price != 0:

                    change_percent = (

                        (

                            current_price -

                            first_price

                        )

                        / first_price

                    ) * 100

                else:

                    change_percent = 0


                market_data.append({

                    "name": name,

                    "emoji": info["emoji"],

                    "price": current_price,

                    "change_percent": change_percent

                })


        except Exception:

            pass


    return render_template(

        "dashboard.html",

        portfolio=portfolio,

        assets=ASSETS,

        periods=PERIODS,

        total_invested=total_invested,

        current_value=current_value,

        total_profit=total_profit,

        total_return=total_return,

        return_percent=total_return,

        market_data=market_data
    )


# =========================================================
# ADD ASSET
# =========================================================

@app.route("/add_asset", methods=["POST"])
def add_asset():

    if "user_id" not in session:

        return redirect("/login")


    symbol = request.form.get("symbol")

    asset_name = request.form.get("asset_name")

    amount = request.form.get("amount")

    buy_price = request.form.get("buy_price")


    if not symbol or not asset_name or not amount or not buy_price:

        return "All fields are required"


    try:

        amount = float(amount)

        buy_price = float(buy_price)

    except ValueError:

        return "Amount and buy price must be numbers"


    db.execute(

        """
        INSERT INTO portfolio
        (user_id, symbol, asset_name, amount, buy_price)
        VALUES (?, ?, ?, ?, ?)
        """,

        session["user_id"],

        symbol,

        asset_name,

        amount,

        buy_price
    )


    return redirect("/dashboard")


# =========================================================
# MARKET ANALYSIS API
# =========================================================

@app.route("/api/analyze", methods=["POST"])
def analyze():

    if "user_id" not in session:

        return jsonify({

            "error": "Please log in first"

        }), 401


    try:

        body = request.get_json()


        symbol = body.get(

            "asset",

            ""
        )


        buy_price = float(

            body.get(

                "buy_price",

                0

            ) or 0
        )


        amount = float(

            body.get(

                "amount",

                0

            ) or 0
        )


        period_key = body.get(

            "period",

            "1 Ay"
        )


        period = PERIODS.get(

            period_key,

            "1mo"
        )


        # -----------------------------------------
        # Valid symbol
        # -----------------------------------------

        valid_symbols = []


        for category_assets in ASSETS.values():

            for asset_info in category_assets.values():

                valid_symbols.append(

                    asset_info["symbol"]
                )


        if symbol not in valid_symbols:

            return jsonify({

                "error": "Invalid asset"

            }), 400


        # -----------------------------------------
        # Yahoo Finance
        # -----------------------------------------

        ticker = yf.Ticker(symbol)


        hist = ticker.history(

            period=period
        )


        if hist.empty:

            return jsonify({

                "error": "No market data available"

            }), 400


        # -----------------------------------------
        # Prices
        # -----------------------------------------

        last_price = float(

            hist["Close"].iloc[-1]
        )


        first_price = float(

            hist["Close"].iloc[0]
        )


        high_price = float(

            hist["High"].max()
        )


        low_price = float(

            hist["Low"].min()
        )


        # -----------------------------------------
        # Change
        # -----------------------------------------

        price_change = (

            last_price -

            first_price
        )


        if first_price != 0:

            price_change_pct = (

                price_change /

                first_price

            ) * 100

        else:

            price_change_pct = 0


        # -----------------------------------------
        # Profit / Loss
        # -----------------------------------------

        profit = None

        profit_percent = None


        if buy_price > 0 and amount > 0:

            profit = (

                last_price -

                buy_price

            ) * amount


            profit_percent = (

                (

                    last_price -

                    buy_price

                )

                / buy_price

            ) * 100


        # -----------------------------------------
        # GRAPH
        # -----------------------------------------

        fig = go.Figure()


        fig.add_trace(

            go.Scatter(

                x=hist.index,

                y=hist["Close"],

                mode="lines",

                name="Price",

                line=dict(

                    color="#00d4ff",

                    width=3
                )
            )
        )


        if buy_price > 0:

            fig.add_hline(

                y=buy_price,

                line_dash="dash",

                line_color="#ffd700",

                annotation_text="Buy Price",

                annotation_position="right"
            )


        fig.update_layout(

            paper_bgcolor="#081832",

            plot_bgcolor="#091a38",

            font=dict(

                color="white"
            ),

            xaxis=dict(

                title="Date",

                gridcolor="#1c3155"
            ),

            yaxis=dict(

                title="Price",

                gridcolor="#1c3155"
            ),

            margin=dict(

                l=40,

                r=20,

                t=30,

                b=40
            ),

            height=500,

            hovermode="x unified"
        )


        graphJSON = json.dumps(

            fig,

            cls=plotly.utils.PlotlyJSONEncoder
        )


        return jsonify({

            "success": True,

            "last_price": last_price,

            "high_price": high_price,

            "low_price": low_price,

            "price_change": price_change,

            "price_change_pct": price_change_pct,

            "profit": profit,

            "profit_percent": profit_percent,

            "graphJSON": graphJSON

        })


    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================================
# DELETE ASSET
# =========================================================

@app.route("/delete_asset/<int:asset_id>", methods=["POST"])
def delete_asset(asset_id):

    if "user_id" not in session:

        return redirect("/login")


    db.execute(

        """
        DELETE FROM portfolio
        WHERE id = ? AND user_id = ?
        """,

        asset_id,

        session["user_id"]
    )


    return redirect("/dashboard")


# =========================================================
# EDIT ASSET
# =========================================================

@app.route(
    "/edit_asset/<int:asset_id>",
    methods=["GET", "POST"]
)
def edit_asset(asset_id):

    if "user_id" not in session:

        return redirect("/login")


    if request.method == "POST":

        asset_name = request.form.get(

            "asset_name"
        )

        amount = request.form.get(

            "amount"
        )

        buy_price = request.form.get(

            "buy_price"
        )


        if not asset_name or not amount or not buy_price:

            return "All fields are required"


        try:

            amount = float(amount)

            buy_price = float(buy_price)

        except ValueError:

            return "Amount and buy price must be numbers"


        db.execute(

            """
            UPDATE portfolio

            SET asset_name = ?,
                amount = ?,
                buy_price = ?

            WHERE id = ?
            AND user_id = ?
            """,

            asset_name,

            amount,

            buy_price,

            asset_id,

            session["user_id"]
        )


        return redirect("/dashboard")


    asset = db.execute(

        """
        SELECT * FROM portfolio

        WHERE id = ?

        AND user_id = ?
        """,

        asset_id,

        session["user_id"]
    )


    if len(asset) != 1:

        return "Asset not found"


    return render_template(

        "edit_asset.html",

        asset=asset[0]
    )


# =========================================================
# PORTFOLIO ALLOCATION API
# =========================================================

@app.route("/api/portfolio_allocation")
def portfolio_allocation():

    if "user_id" not in session:

        return jsonify({

            "error": "Please log in first"

        }), 401


    portfolio = db.execute(

        """
        SELECT asset_name,
               symbol,
               amount,
               buy_price

        FROM portfolio

        WHERE user_id = ?
        """,

        session["user_id"]
    )


    allocation = {}


    for item in portfolio:

        value = (

            item["amount"]

            * item["buy_price"]
        )


        name = item["asset_name"]


        if name in allocation:

            allocation[name] += value

        else:

            allocation[name] = value


    return jsonify({

        "success": True,

        "labels": list(
            allocation.keys()
        ),

        "values": list(
            allocation.values()
        )

    })


# =========================================================
# PORTFOLIO PERFORMANCE API
# =========================================================

@app.route("/api/portfolio_performance")
def portfolio_performance():

    if "user_id" not in session:

        return jsonify({

            "error": "Please log in first"

        }), 401


    period = request.args.get(

        "period",

        "1mo"
    )


    # Kullanıcının portföyünü al
    portfolio = db.execute(

        """
        SELECT symbol, amount

        FROM portfolio

        WHERE user_id = ?
        """,

        session["user_id"]
    )


    if not portfolio:

        return jsonify({

            "error": "Your portfolio is empty"

        }), 400


    total_series = None


    try:

        for item in portfolio:

            ticker = yf.Ticker(

                item["symbol"]
            )


            hist = ticker.history(

                period=period
            )


            if hist.empty:

                continue


            prices = (

                hist["Close"]

                * item["amount"]
            )


            if total_series is None:

                total_series = prices

            else:

                total_series = total_series.add(

                    prices,

                    fill_value=0
                )


        if (
            total_series is None
            or total_series.empty
        ):

            return jsonify({

                "error":
                "No market data available"

            }), 400


        # -----------------------------------------
        # Portfolio Performance Graph
        # -----------------------------------------

        fig = go.Figure()


        fig.add_trace(

            go.Scatter(

                x=total_series.index,

                y=total_series.values,

                mode="lines",

                name="Portfolio Value",

                line=dict(

                    color="#00f5a0",

                    width=3
                ),

                fill="tozeroy"
            )
        )


        fig.update_layout(

            paper_bgcolor="#081832",

            plot_bgcolor="#091a38",

            font=dict(

                color="white"
            ),

            xaxis=dict(

                title="Date",

                gridcolor="#1c3155"
            ),

            yaxis=dict(

                title="Portfolio Value",

                gridcolor="#1c3155"
            ),

            margin=dict(

                l=50,

                r=20,

                t=30,

                b=40
            ),

            height=500,

            hovermode="x unified"
        )


        graphJSON = json.dumps(

            fig,

            cls=plotly.utils.PlotlyJSONEncoder
        )


        return jsonify({

            "success": True,

            "graphJSON": graphJSON

        })


    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)
