"use client";

import React, { useState } from "react";
import { ChatWindow } from "./ChatWindow";

export function ChatButton() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Floating Chat Button */}
      <button
        onClick={() => setIsOpen(true)}
        className={`fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-blue-600 text-white shadow-lg hover:bg-blue-700 hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center ${
          isOpen ? "scale-0 opacity-0" : "scale-100 opacity-100"
        }`}
        title="Open AI Chat"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          className="w-7 h-7"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z"
          />
        </svg>
      </button>

      {/* Chat Window Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-end justify-end p-6 pointer-events-none">
          {/* Backdrop */}
          <div
            className="absolute inset-0 bg-black/20 pointer-events-auto"
            onClick={() => setIsOpen(false)}
          />

          {/* Chat Window */}
          <div className="relative pointer-events-auto w-full max-w-2xl animate-slide-up">
            <ChatWindow onClose={() => setIsOpen(false)} />
          </div>
        </div>
      )}

      {/* Animation styles */}
      <style jsx global>{`
        @keyframes slide-up {
          from {
            transform: translateY(100%);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }
        .animate-slide-up {
          animation: slide-up 0.3s ease-out;
        }
      `}</style>
    </>
  );
}

export default ChatButton;
