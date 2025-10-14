import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cn } from "./utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
  variant?: "default" | "secondary" | "outline" | "ghost" | "destructive";
  size?: "sm" | "md" | "lg" | "icon";
}

const variantStyles: Record<NonNullable<ButtonProps["variant"]>, string> = {
  default: "bg-primary text-primary-foreground hover:bg-primary/90",
  secondary: "bg-slate-700 text-white hover:bg-slate-600",
  outline: "border border-slate-600 bg-transparent text-slate-100 hover:bg-slate-800/80",
  ghost: "hover:bg-slate-800/70 text-slate-100",
  destructive: "bg-red-600 text-white hover:bg-red-500",
};

const sizeStyles: Record<NonNullable<ButtonProps["size"]>, string> = {
  sm: "h-9 px-3 text-sm",
  md: "h-10 px-4 text-sm",
  lg: "h-11 px-6 text-base",
  icon: "h-10 w-10",
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "md", asChild, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        className={cn(
          "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-primary/60 disabled:pointer-events-none disabled:opacity-60",
          variantStyles[variant],
          sizeStyles[size],
          className,
        )}
        ref={ref}
        {...props}
      />
    );
  },
);
Button.displayName = "Button";
