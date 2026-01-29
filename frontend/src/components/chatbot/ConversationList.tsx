"use client";

import React from "react";
import { Conversation } from "@/lib/api";

interface ConversationListProps {
  conversations: Conversation[];
  currentConversationId?: number;
  onSelect: (conversation: Conversation) => void;
  onNew: () => void;
  onDelete: (id: number) => void;
}

export function ConversationList({
  conversations,
  currentConversationId,
  onSelect,
  onNew,
  onDelete,
}: ConversationListProps) {
  // Format date for display
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return "Today";
    } else if (date.toDateString() === yesterday.toDateString()) {
      return "Yesterday";
    } else {
      return date.toLocaleDateString([], { month: "short", day: "numeric" });
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <button
          onClick={onNew}
          className="w-full flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-700 transition-colors"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="w-5 h-5"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 4.5v15m7.5-7.5h-15"
            />
          </svg>
          New Chat
        </button>
      </div>

      {/* Conversation list */}
      <div className="flex-1 overflow-y-auto">
        {conversations.length === 0 ? (
          <div className="p-4 text-center text-sm text-gray-500 dark:text-gray-400">
            No conversations yet.
            <br />
            Start a new chat!
          </div>
        ) : (
          <div className="p-2 space-y-1">
            {conversations.map((conv) => (
              <div
                key={conv.id}
                className={`group relative rounded-lg p-3 cursor-pointer transition-colors ${
                  currentConversationId === conv.id
                    ? "bg-blue-100 dark:bg-blue-900/30"
                    : "hover:bg-gray-100 dark:hover:bg-gray-800"
                }`}
                onClick={() => onSelect(conv)}
              >
                {/* Title */}
                <div className="font-medium text-sm text-gray-900 dark:text-gray-100 truncate pr-8">
                  {conv.title || "New Conversation"}
                </div>

                {/* Meta info */}
                <div className="flex items-center gap-2 mt-1 text-xs text-gray-500 dark:text-gray-400">
                  <span>{formatDate(conv.created_at)}</span>
                  <span>•</span>
                  <span>{conv.message_count} messages</span>
                </div>

                {/* Delete button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete(conv.id);
                  }}
                  className="absolute top-3 right-2 p-1 rounded opacity-0 group-hover:opacity-100 hover:bg-red-100 dark:hover:bg-red-900/30 text-gray-400 hover:text-red-600 transition-all"
                  title="Delete conversation"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth={1.5}
                    stroke="currentColor"
                    className="w-4 h-4"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
                    />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ConversationList;
