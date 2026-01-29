"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import { api, Conversation, Message } from "@/lib/api";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { ConversationList } from "./ConversationList";
import { taskEvents } from "@/lib/task-events";

interface ChatWindowProps {
  onClose?: () => void;
  isFullPage?: boolean;
}

export function ChatWindow({ onClose, isFullPage = false }: ChatWindowProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showSidebar, setShowSidebar] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fetch conversations on mount
  const fetchConversations = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await api.getConversations();
      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setConversations(response.data.conversations);
      }
    } catch (err) {
      setError("Failed to load conversations");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchConversations();
  }, [fetchConversations]);

  // Fetch messages when conversation changes
  const fetchMessages = useCallback(async (conversationId: number) => {
    setIsLoading(true);
    try {
      const response = await api.getMessages(conversationId);
      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setMessages(response.data);
      }
    } catch (err) {
      setError("Failed to load messages");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (currentConversation) {
      fetchMessages(currentConversation.id);
    } else {
      setMessages([]);
    }
  }, [currentConversation, fetchMessages]);

  // Handle selecting a conversation
  const handleSelectConversation = (conversation: Conversation) => {
    setCurrentConversation(conversation);
    setError(null);
  };

  // Handle creating a new conversation
  const handleNewConversation = async () => {
    setCurrentConversation(null);
    setMessages([]);
    setError(null);
  };

  // Handle deleting a conversation
  const handleDeleteConversation = async (id: number) => {
    try {
      const response = await api.deleteConversation(id);
      if (!response.error) {
        setConversations((prev) => prev.filter((c) => c.id !== id));
        if (currentConversation?.id === id) {
          setCurrentConversation(null);
          setMessages([]);
        }
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError("Failed to delete conversation");
    }
  };

  // Handle sending a message
  const handleSendMessage = async (content: string) => {
    setIsSending(true);
    setError(null);

    // Add optimistic user message
    const tempUserMessage: Message = {
      id: Date.now(),
      conversation_id: currentConversation?.id || 0,
      role: "user",
      content,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMessage]);

    try {
      let response;

      if (currentConversation) {
        // Send to existing conversation
        response = await api.sendMessage(currentConversation.id, content);
      } else {
        // Quick chat - creates new conversation
        response = await api.quickChat(content);
      }

      if (response.error) {
        setError(response.error);
        // Remove optimistic message on error
        setMessages((prev) => prev.filter((m) => m.id !== tempUserMessage.id));
      } else if (response.data) {
        // Update with real messages from server
        setMessages(response.data.messages);

        // Check if any tool was called (task was modified) and notify dashboard
        const hasToolCalls = response.data.messages.some((m) => m.role === "tool");
        if (hasToolCalls) {
          taskEvents.emit();
        }

        // If this was a quick chat, update conversation
        if (!currentConversation) {
          const newConv: Conversation = {
            id: response.data.conversation_id,
            user_id: "",
            title: content.slice(0, 50) + (content.length > 50 ? "..." : ""),
            created_at: new Date().toISOString(),
            message_count: response.data.messages.length,
          };
          setCurrentConversation(newConv);
          setConversations((prev) => [newConv, ...prev]);
        } else {
          // Update conversation in list
          setConversations((prev) =>
            prev.map((c) =>
              c.id === currentConversation.id
                ? { ...c, message_count: response.data!.messages.length }
                : c
            )
          );
        }
      }
    } catch (err) {
      setError("Failed to send message. Please try again.");
      setMessages((prev) => prev.filter((m) => m.id !== tempUserMessage.id));
    } finally {
      setIsSending(false);
    }
  };

  // Filter out tool messages for display
  const displayMessages = messages.filter((m) => m.role !== "tool");

  return (
    <div
      className={`flex ${
        isFullPage ? "h-screen" : "h-[600px] rounded-xl shadow-2xl"
      } bg-white dark:bg-gray-800 overflow-hidden`}
    >
      {/* Sidebar - Conversation List */}
      {showSidebar && (
        <div className="w-72 flex-shrink-0">
          <ConversationList
            conversations={conversations}
            currentConversationId={currentConversation?.id}
            onSelect={handleSelectConversation}
            onNew={handleNewConversation}
            onDelete={handleDeleteConversation}
          />
        </div>
      )}

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
          <div className="flex items-center gap-3">
            {/* Toggle sidebar button */}
            <button
              onClick={() => setShowSidebar(!showSidebar)}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              title={showSidebar ? "Hide sidebar" : "Show sidebar"}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-5 h-5 text-gray-600 dark:text-gray-300"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
                />
              </svg>
            </button>

            {/* Title */}
            <div>
              <h2 className="font-semibold text-gray-900 dark:text-white">
                {currentConversation?.title || "AI Task Assistant"}
              </h2>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Manage your tasks with natural language
              </p>
            </div>
          </div>

          {/* Close button (for modal/popup mode) */}
          {onClose && (
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-5 h-5 text-gray-600 dark:text-gray-300"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          )}
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          {/* Error Alert */}
          {error && (
            <div className="mb-4 p-3 bg-red-100 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-300 text-sm">
              {error}
              <button
                onClick={() => setError(null)}
                className="ml-2 underline hover:no-underline"
              >
                Dismiss
              </button>
            </div>
          )}

          {/* Loading state */}
          {isLoading && messages.length === 0 && (
            <div className="flex items-center justify-center h-full text-gray-500 dark:text-gray-400">
              <svg
                className="animate-spin h-8 w-8 mr-2"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Loading...
            </div>
          )}

          {/* Empty state */}
          {!isLoading && messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center px-4">
              <div className="w-16 h-16 mb-4 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-8 h-8 text-blue-600 dark:text-blue-400"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                Start a conversation
              </h3>
              <p className="text-gray-500 dark:text-gray-400 text-sm max-w-sm mb-4">
                I can help you manage your tasks. Try saying:
              </p>
              <div className="flex flex-wrap gap-2 justify-center">
                {[
                  "Add a task to buy milk",
                  "Show my pending tasks",
                  "Mark task 1 as complete",
                ].map((example) => (
                  <button
                    key={example}
                    onClick={() => handleSendMessage(example)}
                    className="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          {displayMessages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}

          {/* Typing indicator */}
          {isSending && (
            <div className="flex justify-start mb-4">
              <div className="bg-gray-100 dark:bg-gray-700 rounded-2xl rounded-bl-md px-4 py-3">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <ChatInput onSend={handleSendMessage} disabled={isSending} />
      </div>
    </div>
  );
}

export default ChatWindow;
