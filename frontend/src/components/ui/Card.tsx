import React, { HTMLAttributes, forwardRef } from "react";

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "bordered" | "elevated";
  padding?: "none" | "sm" | "md" | "lg";
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    {
      children,
      variant = "default",
      padding = "md",
      className = "",
      ...props
    },
    ref
  ) => {
    const variants = {
      default: "bg-white shadow-sm border border-secondary-200",
      bordered: "bg-white border-2 border-secondary-200",
      elevated: "bg-white shadow-lg border-none",
    };

    const paddings = {
      none: "",
      sm: "p-4",
      md: "p-6",
      lg: "p-8",
    };

    return (
      <div
        ref={ref}
        className={`rounded-xl ${variants[variant]} ${paddings[padding]} ${className}`}
        {...props}
      >
        {children}
      </div>
    );
  }
);

export const CardHeader = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ children, className = "", ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={`border-b border-secondary-100 pb-4 mb-4 ${className}`}
        {...props}
      >
        {children}
      </div>
    );
  }
);

CardHeader.displayName = "CardHeader";

export const CardBody = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ children, className = "", ...props }, ref) => {
    return (
      <div ref={ref} className={className} {...props}>
        {children}
      </div>
    );
  }
);

CardBody.displayName = "CardBody";

export const CardFooter = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ children, className = "", ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={`border-t border-secondary-100 pt-4 mt-4 ${className}`}
        {...props}
      >
        {children}
      </div>
    );
  }
);

CardFooter.displayName = "CardFooter";
