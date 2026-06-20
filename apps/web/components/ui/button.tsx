import * as React from "react"; import { cn } from "@/lib/utils";
export function Button({className,...props}: React.ButtonHTMLAttributes<HTMLButtonElement>) { return <button className={cn("rounded-xl bg-cyan-400 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-50", className)} {...props}/> }
