"use client"

import type React from "react"
import { createContext, useState, useEffect } from "react"

interface User {
  id: string
  name: string
  email: string
}

interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

export const AuthContext = createContext<AuthContextType>({
  user: null,
  isLoading: false,
  login: async () => {},
  logout: () => {},
})

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check for stored user credentials
    // In a real app, you would check AsyncStorage or SecureStore
    const checkUserSession = async () => {
      try {
        // Simulate checking stored credentials
        setTimeout(() => {
          setIsLoading(false)
        }, 1000)
      } catch (error) {
        setIsLoading(false)
      }
    }

    checkUserSession()
  }, [])

  const login = async (email: string, password: string) => {
    // In a real app, you would validate with your API
    return new Promise<void>((resolve, reject) => {
      setTimeout(() => {
        // Simulate successful login
        if (email && password) {
          const userData: User = {
            id: "1",
            name: "John Doe",
            email: email,
          }
          setUser(userData)
          resolve()
        } else {
          reject(new Error("Invalid credentials"))
        }
      }, 1000)
    })
  }

  const logout = () => {
    // Clear user data
    setUser(null)
  }

  return <AuthContext.Provider value={{ user, isLoading, login, logout }}>{children}</AuthContext.Provider>
}
