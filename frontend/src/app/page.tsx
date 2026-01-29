"use client";

import React from "react";
import Link from "next/link";
import { Header } from "@/components/layout/Header";
import { Container } from "@/components/layout/Container";
import { Card, CardBody } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export default function HomePage() {
  const features = [
    {
      title: "Simple Task Management",
      description: "Create, update, and delete tasks with ease. Keep track of everything you need to do.",
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
      ),
    },
    {
      title: "Secure Authentication",
      description: "Your data is protected with JWT-based authentication. Log in securely from any device.",
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
      ),
    },
    {
      title: "Responsive Design",
      description: "Access your tasks from any device. Our app works seamlessly on desktop, tablet, and mobile.",
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
      ),
    },
  ];

  return (
    <div className="min-h-screen bg-secondary-50">
      <Header />

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 to-white" />
        <Container className="relative py-20 sm:py-32">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-secondary-900 mb-6 animate-fade-in">
              Organize your life with{" "}
              <span className="text-primary-600">Todo App</span>
            </h1>
            <p className="text-xl text-secondary-600 mb-8 animate-slide-in">
              A simple, secure, and responsive todo application to help you stay
              organized and productive.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center animate-slide-in">
              <Link href="/signup">
                <Button
                  size="lg"
                  rightIcon={
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  }
                >
                  Get Started Free
                </Button>
              </Link>
              <Link href="/login">
                <Button variant="outline" size="lg">
                  Sign In
                </Button>
              </Link>
            </div>
          </div>
        </Container>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <Container>
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">
              Everything you need to stay organized
            </h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Built with modern technologies to provide a fast, secure, and
              delightful experience.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} variant="bordered" className="hover:shadow-md transition-shadow">
                <CardBody className="p-6">
                  <div className="w-12 h-12 bg-primary-100 text-primary-600 rounded-lg flex items-center justify-center mb-4">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-secondary-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-secondary-600">{feature.description}</p>
                </CardBody>
              </Card>
            ))}
          </div>
        </Container>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-600">
        <Container>
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white mb-4">
              Ready to get organized?
            </h2>
            <p className="text-lg text-primary-100 mb-8 max-w-2xl mx-auto">
              Join thousands of users who trust Todo App to manage their daily
              tasks and stay productive.
            </p>
            <Link href="/signup">
              <Button
                variant="secondary"
                size="lg"
                className="bg-white text-primary-600 hover:bg-primary-50"
                rightIcon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                }
              >
                Start Free Today
              </Button>
            </Link>
          </div>
        </Container>
      </section>

      {/* Footer */}
      <footer className="bg-secondary-900 text-secondary-400 py-12">
        <Container>
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <svg
                className="w-6 h-6 text-primary-400"
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
              <span className="font-semibold text-white">Todo App</span>
            </div>
            <p className="text-sm">
              Built with Next.js 16+, React 19+, and TypeScript
            </p>
          </div>
        </Container>
      </footer>
    </div>
  );
}
