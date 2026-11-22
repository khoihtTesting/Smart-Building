const subscriptionKey = window.APP_CONFIG?.SUBSCRIPTION_KEY || "";
const statusEl = document.getElementById("status");
const outputEl = document.getElementById("output");
const checkBtn = document.getElementById("checkBtn");

statusEl.textContent = subscriptionKey
  ? "Đã cấu hình subscriptionKey qua biến."
  : "Chưa có giá trị subscriptionKey (hãy cấu hình qua biến trên môi trường/cloud).";

checkBtn.addEventListener("click", () => {
  outputEl.textContent = JSON.stringify(
    {
      app: "soil-moisture-web",
      hasSubscriptionKey: Boolean(subscriptionKey),
      keyPreview: subscriptionKey ? `${subscriptionKey.slice(0, 4)}***` : null
    },
    null,
    2
  );
});