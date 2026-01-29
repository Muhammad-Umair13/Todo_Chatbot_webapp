"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Header } from "@/components/layout/Header";
import { Container } from "@/components/layout/Container";
import { Card, CardHeader, CardBody, CardFooter } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Alert } from "@/components/ui/Alert";
import { useAuth } from "@/lib/auth-context";

interface LoginFormData {
  email: string;
  password: string;
}

interface FormErrors {
  email?: string;
  password?: string;
  general?: string;
}

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [formData, setFormData] = useState<LoginFormData>({
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.email) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Please enter a valid email address";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      await login(formData.email, formData.password);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Clear error when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  return (
    <div className="min-h-screen bg-secondary-50">
      <Header />

      <main className="py-12">
        <Container size="sm">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-secondary-900 mb-2">
              Welcome back
            </h1>
            <p className="text-secondary-600">
              Sign in to your account to continue
            </p>
          </div>

          {error && (
            <div className="mb-6">
              <Alert variant="error" onClose={() => setError(null)}>
                {error}
              </Alert>
            </div>
          )}

          <Card variant="bordered">
            <form onSubmit={handleSubmit}>
              <CardBody className="space-y-5">
                <Input
                  label="Email address"
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  error={errors.email}
                  placeholder="you@example.com"
                  autoComplete="email"
                  required
                />

                <Input
                  label="Password"
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  error={errors.password}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  required
                />

                <div className="flex items-center justify-between">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      className="w-4 h-4 rounded border-secondary-300 text-primary-600 focus:ring-primary-500"
                    />
                    <span className="text-sm text-secondary-600">Remember me</span>
                  </label>
                </div>
              </CardBody>

              <CardFooter className="flex flex-col gap-4">
                <Button
                  type="submit"
                  className="w-full"
                  size="lg"
                  isLoading={isLoading}
                >
                  Sign in
                </Button>

                <p className="text-center text-sm text-secondary-600">
                  {"Don't have an account? "}
                  <Link
                    href="/signup"
                    className="text-primary-600 hover:text-primary-700 font-medium"
                  >
                    Sign up
                  </Link>
                </p>
              </CardFooter>
            </form>
          </Card>
        </Container>
      </main>
    </div>
  );
}
