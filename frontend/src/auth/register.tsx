import { Button } from "@/components/ui/button";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { config } from "@/config";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import { useState } from "react";
import { useNavigate } from "react-router";

export const Register = () => {
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError("Passwords don't match!");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const response = await apiFetch(config.apiUrl + "/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "email": email,
          "password": password,
          "password_confirm": confirmPassword,
          "first_name": firstName,
          "last_name": lastName
        })
      })

      if (!response.ok) {
        const errorData = await response.json();

        let errorMessage = "Registration failed";
        if (errorData.detail) {
          if (typeof errorData.detail === 'string') {
            errorMessage = errorData.detail;
          } else if (Array.isArray(errorData.detail)) {
            errorMessage = errorData.detail.map((err: any) => {
              const field = err.loc?.[err.loc.length - 1] || 'field';
              const fieldName = field.replace(/_/g, ' ').replace(/\b\w/g, (l: string) => l.toUpperCase());
              return `${fieldName}: ${err.msg}`;
            }).join(', ');
          } else {
            errorMessage = errorData.detail.msg || JSON.stringify(errorData.detail);
          }
        }

        setError(errorMessage);
        return;
      }

      // Success
      const data = await response.json();
      const userData = {
        id: data.user.id,
        email: data.user.email,
        name: `${data.user.first_name} ${data.user.last_name}`
      };

      login(userData);

      setEmail("");
      setFirstName("");
      setLastName("");
      setPassword("");
      setConfirmPassword("");

      navigate("/dashboard")
    } catch (e: any) {
      setError(e.message || "Registration failed. Please try again.")
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="min-h-screen flex items-center justify-center bg-neutral-950 p-4">
        <Card className="w-full max-w-sm scale-125">
          <CardHeader>
            <CardTitle>Create an account</CardTitle>
            <CardDescription>
              Enter an email and password to create your account.
            </CardDescription>
            <CardAction>
              <Button variant="link" onClick={() => navigate("/login")}>Log In</Button>
            </CardAction>
          </CardHeader>

          {error && (
            <div className="mx-6 mb-4 bg-red-500/10 border border-red-500 text-red-500 p-3 rounded text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <CardContent>
              <div className="flex flex-col gap-6">
                <div className="grid gap-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="john.doe@example.com"
                    onChange={(e) => setEmail(e.target.value)}
                    value={email}
                    required
                  />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="firstName">First Name</Label>
                  <Input
                    id="firstName"
                    type="text"
                    placeholder="John"
                    onChange={(e) => setFirstName(e.target.value)}
                    value={firstName}
                    required
                  />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="lastName">Last Name</Label>
                  <Input
                    id="lastName"
                    type="text"
                    placeholder="Doe"
                    onChange={(e) => setLastName(e.target.value)}
                    value={lastName}
                    required
                  />
                </div>
                <div className="grid gap-2">
                  <div className="flex items-center">
                    <Label htmlFor="password">Password</Label>
                  </div>
                  <Input
                    id="password"
                    type="password"
                    placeholder="Enter password"
                    onChange={(e) => setPassword(e.target.value)}
                    value={password}
                    required
                  />
                </div>
                <div className="grid gap-2">
                  <div className="flex items-center">
                    <Label htmlFor="confirm-password">Confirm Password</Label>
                  </div>
                  <Input
                    id="confirm-password"
                    type="password"
                    placeholder="Enter password"
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    value={confirmPassword}
                    required
                  />
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex-col gap-2 mt-7">
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? "Registering..." : "Register"}
              </Button>
            </CardFooter>
          </form>
        </Card>
      </div >
    </div>
  );
};
