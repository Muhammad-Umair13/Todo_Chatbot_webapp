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

interface SignupFormData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

interface FormErrors {
  name?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
  general?: string;
}

export default function SignupPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [formData, setFormData] = useState<SignupFormData>({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = "Name is required";
    } else if (formData.name.trim().length < 2) {
      newErrors.name = "Name must be at least 2 characters";
    }

    if (!formData.email) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Please enter a valid email address";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(formData.password)) {
      newErrors.password =
        "Password must contain at least one uppercase letter, one lowercase letter, and one number";
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
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
      await register(formData.email, formData.name, formData.password);
      router.push("/dashboard");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Registration failed. Please try again."
      );
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
              Create your account
            </h1>
            <p className="text-secondary-600">
              Start managing your tasks today
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
                  label="Full name"
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  error={errors.name}
                  placeholder="John Doe"
                  autoComplete="name"
                  required
                />

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
                  placeholder="At least 8 characters"
                  helperText="Must contain uppercase, lowercase, and number"
                  autoComplete="new-password"
                  required
                />

                <Input
                  label="Confirm password"
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  error={errors.confirmPassword}
                  placeholder="Confirm your password"
                  autoComplete="new-password"
                  required
                />

                <div className="flex items-start gap-2">
                  <input
                    type="checkbox"
                    id="terms"
                    className="mt-1 w-4 h-4 rounded border-secondary-300 text-primary-600 focus:ring-primary-500"
                    required
                  />
                  <label
                    htmlFor="terms"
                    className="text-sm text-secondary-600"
                  >
                    I agree to the{" "}
                    <Link
                      href="/terms"
                      className="text-primary-600 hover:text-primary-700 font-medium"
                    >
                      Terms of Service
                    </Link>{" "}
                    and{" "}
                    <Link
                      href="/privacy"
                      className="text-primary-600 hover:text-primary-700 font-medium"
                    >
                      Privacy Policy
                    </Link>
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
                  Create account
                </Button>

                <p className="text-center text-sm text-secondary-600">
                  {"Already have an account? "}
                  <Link
                    href="/login"
                    className="text-primary-600 hover:text-primary-700 font-medium"
                  >
                    Sign in
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
