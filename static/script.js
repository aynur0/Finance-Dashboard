document.addEventListener("DOMContentLoaded", function () {

    const analyzeButton = document.getElementById("analyzeButton");

    analyzeButton.addEventListener("click", async function () {

        const asset = document.getElementById("asset").value;
        const buyPrice = document.getElementById("buyPrice").value;
        const amount = document.getElementById("amount").value;
        const period = document.getElementById("period").value;

        try {

            const response = await fetch("/api/analyze", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    asset: asset,
                    buy_price: buyPrice,
                    amount: amount,
                    period: period
                })
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.error);
                return;
            }

            // Güncel fiyat
            document.getElementById("lastPrice").textContent =
                "Current Price: $" + data.last_price.toFixed(2);

            // Fiyat değişimi
            document.getElementById("priceChange").textContent =
                "Price Change: " +
                data.price_change.toFixed(2) +
                " (" +
                data.price_change_pct.toFixed(2) +
                "%)";

            // Kâr / Zarar
            if (data.profit !== null) {

                document.getElementById("profit").textContent =
                    "Profit / Loss: $" +
                    data.profit.toFixed(2);

                document.getElementById("profitPercent").textContent =
                    "Profit / Loss %: " +
                    data.profit_percent.toFixed(2) +
                    "%";

            } else {

                document.getElementById("profit").textContent =
                    "Profit / Loss: Enter buy price and amount.";

                document.getElementById("profitPercent").textContent = "";

            }

        } catch (error) {

            console.error(error);

            alert("An error occurred while getting market data.");

        }

    });

});
