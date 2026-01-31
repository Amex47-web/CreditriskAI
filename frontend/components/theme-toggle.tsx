"use client"

import * as React from "react"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import { motion } from "framer-motion"

export function ThemeToggle() {
    const { theme, setTheme } = useTheme()
    const [mounted, setMounted] = React.useState(false)

    React.useEffect(() => {
        setMounted(true)
    }, [])

    if (!mounted) {
        return <div className="w-16 h-8 rounded-full bg-gray-200 dark:bg-gray-800" />
    }

    const isDark = theme === "dark"

    return (
        <motion.div
            className={`
                relative flex h-8 w-16 cursor-pointer items-center rounded-full p-1 transition-colors duration-300
                ${isDark ? "bg-slate-800 ring-1 ring-slate-700" : "bg-sky-100 ring-1 ring-sky-200"}
            `}
            onClick={() => setTheme(isDark ? "light" : "dark")}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            aria-label="Toggle Theme"
        >
            <motion.div
                className={`
                    flex h-6 w-6 items-center justify-center rounded-full shadow-sm transition-colors duration-300
                    ${isDark ? "bg-slate-950 text-indigo-400" : "bg-white text-amber-500"}
                `}
                layout
                transition={{ type: "spring", stiffness: 700, damping: 30 }}
                style={{
                    marginLeft: isDark ? "auto" : "0",
                }}
            >
                <div className="relative flex items-center justify-center">
                    {isDark ? (
                        <Moon size={14} className="fill-current" />
                    ) : (
                        <Sun size={14} className="fill-current" />
                    )}
                </div>
            </motion.div>
        </motion.div>
    )
}
