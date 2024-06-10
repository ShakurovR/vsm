import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import { Theme, presetGpnDefault } from "@consta/uikit/Theme";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Theme preset={presetGpnDefault}>
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    </Theme>
  </React.StrictMode>
);
