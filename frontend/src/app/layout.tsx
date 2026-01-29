import type { Metadata, Viewport } from "next";
import "./globals.css";
import { AuthProvider } from "@/lib/auth-context";
import { SimpleChatbot } from "@/components/chatbot";

export const metadata: Metadata = {
  title: "Phase III Todo App - AI Chatbot",
  description: "Full-Stack Multi-User Web Todo Application with AI Chatbot",
};

export const viewport: Viewport = {
  themeColor: "#2563eb",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased bg-secondary-50 text-secondary-900">
        <AuthProvider>
          {children}
          {/* Phase III: Simple AI Chatbot */}
          <SimpleChatbot />
        </AuthProvider>
      </body>
    </html>
  );
}
