import React, { HTMLAttributes, forwardRef } from "react";

export interface ContainerProps extends HTMLAttributes<HTMLDivElement> {
  size?: "sm" | "md" | "lg" | "xl" | "full";
}

export const Container = forwardRef<HTMLDivElement, ContainerProps>(
  ({ children, size = "lg", className = "", ...props }, ref) => {
    const sizes = {
      sm: "max-w-2xl",
      md: "max-w-3xl",
      lg: "max-w-5xl",
      xl: "max-w-6xl",
      full: "max-w-full",
    };

    return (
      <div
        ref={ref}
        className={`mx-auto px-4 sm:px-6 lg:px-8 ${sizes[size]} ${className}`}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Container.displayName = "Container";
