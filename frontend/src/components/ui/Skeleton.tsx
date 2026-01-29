import React, { HTMLAttributes } from "react";

export interface SkeletonProps extends HTMLAttributes<HTMLDivElement> {
  variant?: "text" | "circular" | "rectangular";
  width?: string | number;
  height?: string | number;
}

export function Skeleton({
  variant = "text",
  width,
  height,
  className = "",
  ...props
}: SkeletonProps) {
  const variants = {
    text: "rounded h-4",
    circular: "rounded-full",
    rectangular: "rounded-lg",
  };

  const style: React.CSSProperties = {
    width: width || (variant === "text" ? "100%" : undefined),
    height:
      height ||
      (variant === "text"
        ? "1rem"
        : variant === "circular"
        ? width || "2.5rem"
        : undefined),
  };

  return (
    <div
      className={`animate-pulse bg-secondary-200 ${variants[variant]} ${className}`}
      style={style}
      {...props}
    />
  );
}

export function SkeletonCard() {
  return (
    <div className="bg-white rounded-xl border border-secondary-200 p-6 space-y-4">
      <div className="flex items-center justify-between">
        <Skeleton variant="text" width="60%" height="1.25rem" />
        <Skeleton variant="circular" width="1.5rem" height="1.5rem" />
      </div>
      <Skeleton variant="text" width="80%" />
      <Skeleton variant="text" width="40%" />
      <div className="flex gap-2 pt-2">
        <Skeleton variant="rectangular" width="5rem" height="2rem" />
        <Skeleton variant="rectangular" width="5rem" height="2rem" />
      </div>
    </div>
  );
}

export function SkeletonList({ count = 3 }: { count?: number }) {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }).map((_, i) => (
        <SkeletonCard key={i} />
      ))}
    </div>
  );
}
