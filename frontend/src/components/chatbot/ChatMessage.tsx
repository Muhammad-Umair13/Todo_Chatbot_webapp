"use client";

import React from "react";
import { Message, MessageRole } from "@/lib/api";

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";
  const isAssistant = message.role === "assistant";
  const isTool = message.role === "tool";

  // Format timestamp
  const formatTime = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  // Don't render tool messages in the main chat (they're internal)
  if (isTool) {
    return null;
  }

  return (
    <div
      className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}
    >
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-blue-600 text-white rounded-br-md"
            : "bg-gray-100 text-gray-900 rounded-bl-md dark:bg-gray-700 dark:text-gray-100"
        }`}
      >
        {/* Role indicator for assistant */}
        {isAssistant && (
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-medium text-blue-600 dark:text-blue-400">
              AI Assistant
            </span>
          </div>
        )}

        {/* Message content */}
        <div className="whitespace-pre-wrap break-words text-sm">
          {message.content}
        </div>

        {/* Timestamp */}
        <div
          className={`text-xs mt-1 ${
            isUser ? "text-blue-200" : "text-gray-500 dark:text-gray-400"
          }`}
        >
          {formatTime(message.created_at)}
        </div>
      </div>
    </div>
  );
}

export default ChatMessage;
