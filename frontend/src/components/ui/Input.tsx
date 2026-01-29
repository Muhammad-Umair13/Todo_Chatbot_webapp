import React, { InputHTMLAttributes, forwardRef } from "react";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftElement?: React.ReactNode;
  rightElement?: React.ReactNode;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      helperText,
      leftElement,
      rightElement,
      className = "",
      id,
      ...props
    },
    ref
  ) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, "-");

    return (
      <div className="w-full">
        {label && (
          <label
            htmlFor={inputId}
            className="block text-sm font-medium text-secondary-700 mb-1.5"
          >
            {label}
          </label>
        )}
        <div className="relative">
          {leftElement && (
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-secondary-400">
              {leftElement}
            </div>
          )}
          <input
            ref={ref}
            id={inputId}
            className={`
              block w-full rounded-lg border transition-colors duration-200
              ${leftElement ? "pl-10" : "pl-4"}
              ${rightElement ? "pr-10" : "pr-4"}
              py-2.5 text-secondary-900
              ${
                error
                  ? "border-red-300 focus:border-red-500 focus:ring-red-500"
                  : "border-secondary-300 focus:border-primary-500 focus:ring-primary-500"
              }
              placeholder:text-secondary-400
              focus:outline-none focus:ring-2 focus:ring-offset-0
              disabled:bg-secondary-50 disabled:text-secondary-500 disabled:cursor-not-allowed
              ${className}
            `}
            {...props}
          />
          {rightElement && (
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-secondary-400">
              {rightElement}
            </div>
          )}
        </div>
        {error && <p className="mt-1.5 text-sm text-red-600">{error}</p>}
        {helperText && !error && (
          <p className="mt-1.5 text-sm text-secondary-500">{helperText}</p>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";
