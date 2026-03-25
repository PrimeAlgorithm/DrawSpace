import { Link } from "react-router";
import { ArrowRight, CheckCircle2, Layers3, PencilRuler, Sparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { FeatureCard } from "@/LandingPage/feature-card";
import "./App.css";

const features = [
  {
    icon: Layers3,
    title: "Boards that stay organized",
    description:
      "Move from quick sketches to structured planning without leaving the same workspace.",
  },
  {
    icon: PencilRuler,
    title: "Tools made for fast thinking",
    description:
      "Draw shapes, map flows, and turn rough ideas into something your team can build from.",
  },
  {
    icon: Sparkles,
    title: "Ready for collaboration",
    description:
      "Built to support shared whiteboards and real-time interaction as the product grows.",
  },
];

const steps = [
  "Create an account and start a board in seconds.",
  "Sketch systems, wireframes, or brainstorms with lightweight tools.",
  "Come back later and pick up where your ideas left off.",
];

function App() {
  return (
    <div className="min-h-screen overflow-hidden bg-[radial-gradient(circle_at_top,_rgba(56,189,248,0.12),_transparent_24%),linear-gradient(180deg,_#000000_0%,_#050505_38%,_#0a0a0a_100%)] text-slate-50">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col px-6 py-6 sm:px-8 lg:px-10">
        <header className="flex items-center justify-between rounded-full border border-white/10 bg-black/70 px-4 py-3 shadow-[0_20px_60px_rgba(0,0,0,0.55)] backdrop-blur md:px-6">
          <Link to="/" className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-white text-black shadow-lg shadow-white/10">
              <PencilRuler className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm font-medium uppercase tracking-[0.28em] text-white">
                DrawSpace
              </p>
              <p className="text-sm text-slate-400">Visual thinking for teams</p>
            </div>
          </Link>

          <div className="flex items-center gap-2">
            <Button
              asChild
              variant="ghost"
              className="hidden text-slate-200 hover:bg-white/10 hover:text-white sm:inline-flex"
            >
              <Link to="/login">Log in</Link>
            </Button>
            <Button
              asChild
              className="rounded-full bg-white px-5 text-black hover:bg-slate-200"
            >
              <Link to="/register">Get started</Link>
            </Button>
          </div>
        </header>

        <main className="flex flex-1 items-center py-12 lg:py-16">
          <div className="grid w-full items-center gap-12 lg:grid-cols-[1.05fr_0.95fr]">
            <section className="max-w-2xl">
              <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-black/60 px-4 py-2 text-sm font-medium text-slate-200 shadow-sm backdrop-blur">
                <span className="h-2 w-2 rounded-full bg-white" />
                Plan, sketch, and shape ideas in one place
              </div>

              <h1 className="mt-6 text-5xl font-semibold tracking-tight text-white sm:text-6xl">
                A simple whiteboard workspace that feels ready from day one.
              </h1>

              <p className="mt-6 max-w-xl text-lg leading-8 text-slate-300">
                DrawSpace gives you a clean place to brainstorm, map flows, and
                organize visual thinking without the clutter of a heavy design tool.
              </p>

              <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                <Button
                  asChild
                  size="lg"
                  className="rounded-full bg-white px-6 text-black hover:bg-slate-200"
                >
                  <Link to="/register">
                    Start free
                    <ArrowRight className="h-4 w-4" />
                  </Link>
                </Button>
                <Button
                  asChild
                  variant="outline"
                  size="lg"
                  className="rounded-full border-white/15 bg-black/70 px-6 text-slate-100 hover:bg-white/8"
                >
                  <Link to="/login">Open your workspace</Link>
                </Button>
              </div>
            </section>

            <section className="relative">
              <div className="absolute -left-10 top-10 h-32 w-32 rounded-full bg-white/8 blur-3xl" />
              <div className="absolute bottom-0 right-0 h-40 w-40 rounded-full bg-white/6 blur-3xl" />

              <Card className="relative overflow-hidden border-white/10 bg-black/70 py-0 shadow-[0_30px_80px_rgba(0,0,0,0.65)] backdrop-blur">
                <CardContent className="p-0">
                  <div className="border-b border-white/10 bg-black px-6 py-4 text-slate-100">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm uppercase tracking-[0.24em] text-slate-300">
                          Board Preview
                        </p>
                        <h2 className="mt-2 text-xl font-semibold">
                          Product planning workshop
                        </h2>
                      </div>
                      <div className="rounded-full border border-white/15 px-3 py-1 text-sm text-slate-300">
                        Active board
                      </div>
                    </div>
                  </div>

                  <div className="grid gap-6 p-6">
                    <div className="grid gap-4 sm:grid-cols-2">
                      {features.map((feature) => (
                        <FeatureCard key={feature.title} {...feature} />
                      ))}
                    </div>

                    <div className="rounded-3xl border border-white/10 bg-black/75 p-5">
                      <p className="text-sm font-semibold uppercase tracking-[0.22em] text-slate-400">
                        Getting started
                      </p>
                      <div className="mt-4 space-y-3">
                        {steps.map((step) => (
                          <div key={step} className="flex items-start gap-3">
                            <CheckCircle2 className="mt-0.5 h-5 w-5 text-white" />
                            <p className="text-sm leading-6 text-slate-300">{step}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
