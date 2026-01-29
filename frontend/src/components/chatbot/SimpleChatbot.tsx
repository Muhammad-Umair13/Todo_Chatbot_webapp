"use client";

import React, { useState, useRef, useEffect } from "react";
import { api, Message } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import { taskEvents } from "@/lib/task-events";

/**
 * Simple, attractive, and functional AI Chatbot component.
 *
 * Features:
 * - Clean minimal design
 * - Auto-scroll to latest message
 * - Loading indicator while AI responds
 * - Example prompts for quick start
 * - Responsive and accessible
 */
export function SimpleChatbot() {
  const { user, isLoading: authLoading } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  // Don't render chatbot if user is not logged in
  if (authLoading || !user) {
    return null;
  }

  const sendMessage = async (text: string) => {
    if (!text.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now(),
      conversation_id: conversationId || 0,
      role: "user",
      content: text.trim(),
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      let response;
      if (conversationId) {
        response = await api.sendMessage(conversationId, text.trim());
      } else {
        response = await api.quickChat(text.trim());
      }

      if (response.data) {
        setConversationId(response.data.conversation_id);
        // Get only user and assistant messages (filter out tool messages)
        const filteredMessages = response.data.messages.filter(
          (m) => m.role === "user" || m.role === "assistant"
        );
        setMessages(filteredMessages);

        // Check if any tool was called (task was modified) and notify dashboard
        const hasToolCalls = response.data.messages.some((m) => m.role === "tool");
        if (hasToolCalls) {
          taskEvents.emit();
        }
      } else if (response.error) {
        // Show error as assistant message
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            conversation_id: conversationId || 0,
            role: "assistant",
            content: `Sorry, something went wrong. Please try again.`,
            created_at: new Date().toISOString(),
          },
        ]);
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          conversation_id: conversationId || 0,
          role: "assistant",
          content: "Connection error. Please check your internet and try again.",
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(input);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setConversationId(null);
  };

  const examplePrompts = [
    "Add a task to buy groceries",
    "Show my tasks",
    "Mark task 1 as done",
  ];

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-5 right-5 z-50 w-14 h-14 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200 flex items-center justify-center text-white"
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen ? (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        )}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-5 z-50 w-96 max-w-[calc(100vw-40px)] bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden animate-in slide-in-from-bottom-5 duration-200">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div>
                <h3 className="text-white font-semibold text-sm">Task Assistant</h3>
                <p className="text-blue-100 text-xs">Ask me to manage your tasks</p>
              </div>
            </div>
            {messages.length > 0 && (
              <button
                onClick={clearChat}
                className="text-white/70 hover:text-white text-xs hover:bg-white/10 px-2 py-1 rounded transition-colors"
              >
                Clear
              </button>
            )}
          </div>

          {/* Messages */}
          <div className="h-80 overflow-y-auto p-4 space-y-3 bg-gray-50">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center px-4">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-3">
                  <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <p className="text-gray-600 text-sm mb-4">
                  Hi! I can help you manage tasks. Try:
                </p>
                <div className="space-y-2 w-full">
                  {examplePrompts.map((prompt) => (
                    <button
                      key={prompt}
                      onClick={() => sendMessage(prompt)}
                      className="w-full text-left text-sm px-3 py-2 bg-white rounded-lg border border-gray-200 text-gray-700 hover:border-blue-300 hover:bg-blue-50 transition-colors"
                    >
                      "{prompt}"
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <>
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`max-w-[80%] px-3 py-2 rounded-2xl text-sm ${
                        msg.role === "user"
                          ? "bg-blue-500 text-white rounded-br-sm"
                          : "bg-white text-gray-800 border border-gray-200 rounded-bl-sm shadow-sm"
                      }`}
                    >
                      <p className="whitespace-pre-wrap break-words">{msg.content}</p>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm">
                      <div className="flex gap-1">
                        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Input */}
          <form onSubmit={handleSubmit} className="p-3 bg-white border-t border-gray-100">
            <div className="flex gap-2">
              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type a message..."
                disabled={isLoading}
                className="flex-1 px-4 py-2 bg-gray-100 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={!input.trim() || isLoading}
                className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Animation styles */}
      <style jsx global>{`
        @keyframes slide-in-from-bottom-5 {
          from {
            transform: translateY(20px);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }
        .animate-in {
          animation: slide-in-from-bottom-5 0.2s ease-out;
        }
      `}</style>
    </>
  );
}

export default SimpleChatbot;
