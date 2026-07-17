import { SignIn } from "@clerk/nextjs";

export default function Page() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-radial from-slate-900 to-slate-950 p-4">
      <div className="w-full max-w-md space-y-6">
        <div className="flex flex-col items-center space-y-2 text-center">
          <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-teal-400 to-blue-500 bg-clip-text text-transparent">
            We Lift Portal
          </h1>
          <p className="text-sm text-slate-400">
            Sign in with passwordless magic link to manage gate codes.
          </p>
        </div>
        <div className="flex justify-center">
          <SignIn
            appearance={{
              variables: {
                colorPrimary: "#14b8a6",
              },
            }}
          />
        </div>
      </div>
    </div>
  );
}
