"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "../ui/Button";
import { useAuth } from "@/lib/auth-context";

export function Header() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <header className="bg-white border-b border-secondary-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link
              href="/"
              className="text-xl font-bold text-primary-600 flex items-center gap-2"
            >
              <svg
                className="w-8 h-8"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
                />
              </svg>
              <span>Todo App</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            {user ? (
              <>
                <Link
                  href="/dashboard"
                  className="text-secondary-600 hover:text-secondary-900 font-medium transition-colors"
                >
                  Dashboard
                </Link>
                <div className="flex items-center gap-4 ml-4">
                  <span className="text-sm text-secondary-600">
                    {user.name || user.email}
                  </span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleLogout}
                  >
                    Logout
                  </Button>
                </div>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="text-secondary-600 hover:text-secondary-900 font-medium transition-colors"
                >
                  Login
                </Link>
                <Link href="/signup">
                  <Button size="sm">Sign Up</Button>
                </Link>
              </>
            )}
          </nav>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2 rounded-lg text-secondary-600 hover:bg-secondary-100 transition-colors"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label="Toggle menu"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {isMobileMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-secondary-100 animate-slide-in">
            <nav className="flex flex-col gap-4">
              {user ? (
                <>
                  <Link
                    href="/dashboard"
                    className="text-secondary-600 hover:text-secondary-900 font-medium px-2 py-2"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    Dashboard
                  </Link>
                  <div className="flex items-center justify-between px-2 py-2">
                    <span className="text-sm text-secondary-600">
                      {user.name || user.email}
                    </span>
                    <Button variant="outline" size="sm" onClick={handleLogout}>
                      Logout
                    </Button>
                  </div>
                </>
              ) : (
                <>
                  <Link
                    href="/login"
                    className="text-secondary-600 hover:text-secondary-900 font-medium px-2 py-2"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    Login
                  </Link>
                  <Link href="/signup" onClick={() => setIsMobileMenuOpen(false)}>
                    <Button className="w-full">Sign Up</Button>
                  </Link>
                </>
              )}
            </nav>
          </div>
        )}
      </div>
    </header>
  );
}
